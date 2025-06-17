from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import AddPostForm
from .models import Category, Article, TagPost

main_menu = [{'title': 'ГЛАВНАЯ', 'url_name': 'home'},
             {'title': 'НАШИ РАБОТЫ', 'url_name': 'nashi-raboti'},
             {'title': 'ДОБАВИТЬ СТАТЬЮ', 'url_name': 'dobavit_staty'},
             {'title': 'КОНТАКТЫ', 'url_name': 'contacts'}]

tags = TagPost.objects.all()
categories_list = Category.objects.all()

def index(request):
    data = {
        'categories': categories_list,
        'cat_selected': 0,  # Ничего не выбрано
        'data': main_menu,
        'tags': tags,
        'show_home_text': True,
    }
    return render(request, "main_app/index.html", context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    articles = category.articles.filter(is_published='published')
    # добавляем пагинацию
    paginator = Paginator(articles, 3)  # выводим articles(статьи) по 3 штуки за раз
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы
    data = {
        'title': f"Рубрика: {category.name}",
        'page_obj': page_obj,  # Передаём объект страницы вместо всех статей (теперь статьи - это page_obj)
        'articles': articles,
        'cat_selected': category.pk,
        'categories': categories_list,
        'data': main_menu,
        'tags': tags,
    }
    return render(request, "main_app/index.html", context=data)

def show_article(request, art_slug):
    article = get_object_or_404(Article, slug=art_slug, is_published='published')
    category = article.categories
    data = {
        'title': f"Статья: {article.title}",
        'cat_selected': article.categories.pk,
        'article': article,
        'category': category,
        'categories': categories_list,
        'data': main_menu,
        'tags': tags,
    }
    return render(request, "main_app/index.html", context=data)

def show_tag_postlist(request, tag_slug):
    my_tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = my_tag.tags.filter(is_published='published')
    # добавляем пагинацию
    paginator = Paginator(posts, 5)  # выводим posts(статьи) по 5 штук за раз
    page_number = request.GET.get('page')  # Получаем номер страницы из GET-параметра
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы
    data = {
        'title': f"Тег: {my_tag.name}",
        'data': main_menu,
        'categories': categories_list,
        'cat_selected': None,
        'posts': posts,
        'tags': tags,
        'page_obj': page_obj, # Передаём объект страницы вместо всех статей (теперь статьи - это page_obj)
    }
    return render(request, "main_app/index.html", context=data)


def nashi_raboti(request):
    return HttpResponse('<h1>Наши работы</h1>')


# функция для работы с добавлением новой статьи
def dobavit_staty(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    data = {
        'title': 'Добавление новой статьи',
        'data': main_menu,
        'categories': categories_list,
        'cat_selected': None,
        'add_edit_article': True,
        'tags': tags,
        'form': form,
    }
    return render(request, "main_app/index.html", context=data)


# функция для работы с редактированием статьи
def edit_article(request, article_id):
    current_article = get_object_or_404(Article, id=article_id)  # получаем текущую статью
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=current_article)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm(instance=current_article)  # форма с данными для редактирования
    data = {
        'title': 'Изменение статьи',
        'data': main_menu,
        'categories': categories_list,
        'cat_selected': None,
        'add_edit_article': True,
        'tags': tags,
        'form': form,
    }
    return render(request, "main_app/index.html", context=data)


# Функция для работы с удалением м статьи
@require_POST  # Разрешает только POST запросы
def delete_article(request, article_id):
    current_article = get_object_or_404(Article, id=article_id)
    current_article.delete()
    messages.success(request, "Статья успешно удалена")
    return redirect('home')


def contacts(request):
    return HttpResponse('<h1>Контакты</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1><u>Страница не найдена</u></h1>')