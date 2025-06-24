from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from main_app.models import Article, Category, User

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'is_published', 'categories')  # поля, отображаемые в админ панели
    list_display_links = ('title',)  # делает данное поле кликабельным для перехода в статью
    ordering = ['id']  # указываем сортировку статей (только для админ панели)
    list_editable = ('is_published', )  # Позволяет менять значение не открывая статью. Появится раскрывающееся меню
    list_per_page = 10  # сколько статей отображается на главной странице
    # prepopulated_fields = {'slug': ('title',)}  # в админке поле слаг будет заполняться автоматически (не сочетается с readonly_fields)
    readonly_fields = ('slug',)  # показываем slug, но не даем редактировать
    filter_horizontal = ['tags']  # Преобразует виджет в развёрнутую форму. Можно filter_vertical.
    search_fields = ['title__startswith', 'categories__name']  # добавляет поиск по первым буквам заголовка(добавили lookups) и имени категории
    list_filter = ['categories__name', 'is_published']  # добавляет фильтрацию по категории и статусу

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # поля, отображаемые в админ панели
    list_display_links = ('name',)  # делает данное поле кликабельным для перехода в статью

# Регистрируем User
# admin.site.register(User, UserAdmin)
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name', 'photo', 'email', 'date_joined')