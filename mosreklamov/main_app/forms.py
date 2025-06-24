import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from main_app.models import Article, Category, User


class AddPostForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категория')
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class CustomCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'photo', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            translated_errors = []
            for msg in e.messages:
                if msg.startswith("This password is too short"):
                    translated_errors.append(
                        "Пароль слишком короткий. Минимум 8 символов.")
                elif msg.startswith("This password is too common"):
                    translated_errors.append(
                        "Введённый пароль слишком широко распространён.")
                elif msg.startswith("This password is entirely numeric"):
                    translated_errors.append(
                        "Пароль не должен состоять только из цифр.")
                else:
                    translated_errors.append(msg)
            raise ValidationError(translated_errors)
        return password
    # функция-валидатор проверки уникальности email адреса
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():  # если в текущей модели user существует запись с указанным email, то
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False, label='Запомнить меня')
    def clean_username(self):
        """
        Кастомная валидация поля username, позволяющая входить как по логину, так и по email.
        Метод вызывается автоматически при валидации формы.
        """
        username = self.cleaned_data.get('username')
        User = get_user_model()
        # Если введен email (содержит @)
        if '@' in username:
            try:
                # Ищем пользователя по email (регистронезависимо)
                user = User.objects.get(email__iexact=username)  # iexact означает case-insensitive поиск (неважно Test@test.com или TEST@TEST.COM)
                return user.username  # Возвращаем username для стандартной аутентификации
            except User.DoesNotExist:
                raise ValidationError("Пользователь с таким email не найден")
        # Если введен логин - оставляем как есть
        return username

# форма для редактирования данных пользователей
class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput())
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput())
    this_year = datetime.date.today().year
    birth_date = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))
    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'birth_date', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'photo': 'Фото профиля',
        }
        widgets = {
            'photo': forms.FileInput(attrs={'accept': 'image/*'})
        }

# класс для изменения профиля формы
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput())