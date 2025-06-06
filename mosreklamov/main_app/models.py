from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Article(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    categories = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='articles')

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["time_create"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'art_slug': self.slug})