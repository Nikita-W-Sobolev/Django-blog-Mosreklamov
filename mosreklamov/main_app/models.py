from django.db import models
from django.urls import reverse


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
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True, verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    categories = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='articles')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')
    photo = models.ImageField(upload_to="articles_image", default=None, blank=True, null=True, verbose_name='Изображение статьи')

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