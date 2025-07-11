from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_extensions.db.fields import AutoSlugField
from slugify import slugify

from mosreklamov import settings


class Category(models.Model):
    """
    Модель категории для статей блога.
    Содержит название и уникальный slug для URL.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]
    def get_absolute_url(self):
        """
        Возвращает URL страницы категории по её slug.
        """
        return reverse('category', kwargs={'cat_slug': self.slug})


class Article(models.Model):
    """
    Модель статьи блога с заголовком, содержимым, статусом публикации и связями с категориями и тегами.
    """
    STATUS_CHOICES = [('published', 'Опубликовано'), ('unpublished', 'Неопубликовано')]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.CharField(max_length=300, blank=True, verbose_name='Заголовок для СЕО')
    content = models.TextField(verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.CharField(choices=STATUS_CHOICES, default='published', verbose_name='Публикация')
    # Автозаполнение слага db_index=True,
    # pip install django-extensions python-slugify
    # INSTALLED_APPS = ['django_extensions']
    slug = AutoSlugField(
        max_length=100,
        unique=True,
        verbose_name='URL',
        populate_from = 'title',       # Источник для slug
        slugify_function = slugify,   # Функция транслитерации
        overwrite=True,               # Обновлять slug при изменении title
    )
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='articles', verbose_name='Категории')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    photo = models.ImageField(upload_to="articles_image", default=None, blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # добавляем автора статьи
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["time_create"]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        """
        Возвращает URL страницы статьи по её slug.
        """
        return reverse('article', kwargs={'art_slug': self.slug})

class TagPost(models.Model):
    """
    Модель тега для статей.
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["id"]
    def get_absolute_url(self):
        """
        Возвращает URL страницы статьи по её slug.
        """
        return reverse('tag', kwargs={'tag_slug': self.slug})

# класс для переопределения модели пользователя
class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями:
    фотография и дата рождения.
    """
    photo = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Фотография')
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    # Далее код для отображения аватарки в админке
    def avatar_preview(self):
        if self.photo:
            html = f'<img src="{self.photo.url}" width="100" height="100" style="object-fit: cover; border-radius: 6px;" />'
            return mark_safe(html)  # Говорим Django: не экранируй, это безопасно(mark_safe)
        return "(Нет изображения)"
    avatar_preview.short_description = "Превью аватара"