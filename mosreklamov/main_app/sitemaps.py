from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from main_app.models import Category, Article


# индексируем главный страницы
class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"
    def items(self):
        return ['home', 'contacts']
    def location(self, item):
        return reverse(item)  # Генерируем URL для статических страниц

class ArticleSitemap(Sitemap):
    changefreq = "weekly"  # Как часто обновляется страница
    priority = 0.9         # Приоритет (0.1–1.0)
    def items(self):
        return Article.objects.filter(is_published='published')
    def lastmod(self, obj):
        return obj.time_update  # Дата последнего изменения

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    def items(self):
        return Category.objects.all()