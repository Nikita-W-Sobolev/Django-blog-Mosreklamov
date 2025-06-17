from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Article(models.Model):
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

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["time_create"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'art_slug': self.slug})

class TagPost(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})