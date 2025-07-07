from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, \
    HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView
from mosreklamov import settings
from .forms import AddPostForm, CustomCreationForm, LoginUserForm, \
    ProfileEditForm, UserPasswordChangeForm
from .models import Category, Article, TagPost

main_menu = [{'title': 'ГЛАВНАЯ', 'url_name': 'home'},
             {'title': 'НАШИ РАБОТЫ', 'url_name': 'nashi-raboti'},
             {'title': 'ДОБАВИТЬ СТАТЬЮ', 'url_name': 'dobavit_staty'},
             {'title': 'КОНТАКТЫ', 'url_name': 'contacts'}]

tags = TagPost.objects.all().prefetch_related('tags')
categories_list = Category.objects.all().prefetch_related('articles')

def index(request):
    """
    Главная страница сайта.
    """
    data = {
        # 'categories': categories_list,
        'cat_selected': 0,  # Ничего не выбрано
        # 'data': main_menu,
        # 'tags': tags,
        'show_home_text': True,
    }
    return render(request, "main_app/index.html", context=data)


def show_category(request, cat_slug):
    """
    Отображение статей выбранной категории с пагинацией.
    """
    category = get_object_or_404(Category, slug=cat_slug)
    articles = category.articles.filter(is_published='published').select_related('author').prefetch_related('tags')
    # добавляем пагинацию
    paginator = Paginator(articles, 3)  # выводим articles(статьи) по 3 штуки за раз
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы
    data = {
        'title': f"Рубрика: {category.name}",
        'page_obj': page_obj,  # Передаём объект страницы вместо всех статей (теперь статьи - это page_obj)
        'articles': articles,
        'cat_selected': category.pk,
        # 'categories': categories_list,
        # 'data': main_menu,
        # 'tags': tags,
    }
    return render(request, "main_app/index.html", context=data)

def show_article(request, art_slug):
    """
    Отображение отдельной статьи.
    """
    article = get_object_or_404(Article.objects.select_related('categories'), slug=art_slug, is_published='published')
    category = article.categories
    data = {
        'title': f"Статья: {article.title}",
        'cat_selected': article.categories.pk,
        'article': article,
        'category': category,
        # 'categories': categories_list,
        # 'data': main_menu,
        # 'tags': tags,
    }
    return render(request, "main_app/index.html", context=data)

def show_tag_postlist(request, tag_slug):
    """
    Отображение статей, связанных с определенным тегом, с пагинацией.
    """
    my_tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = my_tag.tags.filter(is_published='published').select_related('categories').prefetch_related('tags')
    # добавляем пагинацию
    paginator = Paginator(posts, 5)  # выводим posts(статьи) по 5 штук за раз
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы
    data = {
        'title': f"Тег: {my_tag.name}",
        # 'data': main_menu,
        # 'categories': categories_list,
        'cat_selected': None,
        'posts': posts,
        # 'tags': tags,
        'page_obj': page_obj, # Передаём объект страницы вместо всех статей (теперь статьи - это page_obj)
    }
    return render(request, "main_app/index.html", context=data)


def nashi_raboti(request):
    """
    Заглушка для страницы 'Наши работы'.
    """
    return HttpResponse('<h1>Наши работы</h1>')


# функция для работы с добавлением новой статьи
def dobavit_staty(request):
    """
    Добавление новой статьи. Обрабатывает GET и POST запросы.
    """
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    data = {
        'title': 'Добавление новой статьи',
        # 'data': main_menu,
        # 'categories': categories_list,
        'cat_selected': None,
        'add_edit_article': True,
        # 'tags': tags,
        'form': form,
    }
    return render(request, "main_app/index.html", context=data)


# функция для работы с редактированием статьи
@login_required
@permission_required('main_app.change_article', raise_exception=True)
def edit_article(request, article_id):
    """
    Редактирование статьи с проверкой:
    1. Только авторизованные пользователи
    2. Только с правами change_article
    3. Только автор или суперпользователь
    """
    current_article = get_object_or_404(Article, id=article_id)  # получаем текущую статью
    if not (request.user == current_article.author or request.user.is_superuser):  # Проверка, что пользователь - автор статьи или админ
        raise PermissionDenied
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=current_article)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm(instance=current_article)  # форма с данными для редактирования
    data = {
        'title': 'Изменение статьи',
        # 'data': main_menu,
        # 'categories': categories_list,

        'cat_selected': None,
        'add_edit_article': True,
        # 'tags': tags,
        'form': form,
    }
    return render(request, "main_app/index.html", context=data)


# Функция для работы с удалением статьи
@require_POST  # Разрешает только POST запросы
@login_required  # Гарантирует, что только авторизованные пользователи получат доступ
@permission_required('main_app.delete_article', raise_exception=True)  # проверяет конкретные права, raise_exception=True - возвращает 403 вместо перенаправления на логин
def delete_article(request, article_id):
    """
    Удаление статьи с проверкой:
    1. Только POST-запросы
    2. Только авторизованные пользователи
    3. Только с правами delete_article
    4. Только автор или суперпользователь
    """
    current_article = get_object_or_404(Article, id=article_id)
    if not (request.user == current_article.author or request.user.is_superuser):  # Дополнительная проверка, что пользователь - автор статьи или админ
        raise PermissionDenied
    current_article.delete()
    messages.success(request, "Статья успешно удалена")
    return redirect('home')


def contacts(request):
    """
    Заглушка для страницы контактов.
    """
    return HttpResponse('<h1>Контакты</h1>')


def page_not_found(request, exception):
    """
    Кастомная страница 404 ошибки.
    """
    return HttpResponseNotFound('<h1><u>Страница не найдена</u></h1>')


# функция для регистрации нового пользователя
def register(request):
    """
    Регистрация нового пользователя.
    """
    if request.method == "POST":
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomCreationForm()
    data = {
        'title': 'Регистрация',
        # 'data': main_menu,
        # 'categories': categories_list,
        # 'tags': tags,
        'form': form,
    }
    return render(request, 'main_app/register.html', context=data)


def profile_view(request):
    """
    Просмотр и редактирование профиля пользователя.
    Защищено от изменений для социальных аккаунтов.
    """
    if hasattr(request.user, 'social_auth') and request.user.social_auth.exists():
        raise PermissionDenied("Редактирование профиля недоступно для социальных аккаунтов")
    user = request.user
    default_image = settings.DEFAULT_USER_IMAGE
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # if 'photo' in request.FILES:
            #     # Удаляем старое фото, если оно было
            #     if user.photo:
            #         user.photo.delete(save=False)
            #     user.photo = request.FILES['photo']
            form.save()
            messages.success(request, "Профиль успешно обновлен")
            return redirect('home')
        else:
            messages.error(request, "Ошибка при обновлении профиля")
    else:
        form = ProfileEditForm(instance=user)  # Заполняем форму текущими данными пользователя
    context = {
        'title': 'Профиль пользователя',
        'default_image': default_image,
        'user': user,
        # 'data': main_menu,
        # 'categories': categories_list,
        # 'tags': tags,
        'form': form,
    }
    return render(request, 'main_app/profile.html', context)


# для отображения формы входа
class LoginUser(LoginView):
    """
    Класс-представление для входа пользователя.
    Поддерживает опцию "Запомнить меня".
    """
    form_class = LoginUserForm  # класс формы для аутентификации или используем стандартную AuthenticationForm
    template_name = 'main_app/login.html'  # маршрут до шаблона
    # дополнительные переменные, передаваемые в шаблон
    extra_context = {
        'title': 'Авторизация',
        # 'data': main_menu,
        # 'categories': categories_list,
        # 'tags': tags,
    }
    def form_valid(self, form):  # вызывается, когда форма прошла валидацию успешно
        remember = form.cleaned_data.get('remember_me')
        if not remember:
            self.request.session.set_expiry(0)  # Сессия будет жить только до закрытия браузера.
        else:
            self.request.session.set_expiry(1209600)  # Сессия будет активна 2 недели, даже если браузер закрывать.
        return super().form_valid(form)
    def get_success_url(self):  # Метод для определения URL, по которому перейдём после удачной авторизации
        return reverse_lazy('home')


def logout_user(request):
    """
    Функция выхода пользователя из системы.
    """
    logout(request)
    return HttpResponseRedirect(reverse('login'))


class UserPasswordChange(PasswordChangeView):
    """
    Класс-представление для изменения пароля пользователя.
    """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "main_app/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-представление для удаления текущего пользователя.
    """
    model = get_user_model()
    template_name = 'main_app/account_confirm_delete.html'
    success_url = reverse_lazy('home')  # куда перенаправить после удаления
    def get_object(self, queryset=None):
        """
        Возвращает объект текущего аутентифицированного пользователя.
        """
        return self.request.user