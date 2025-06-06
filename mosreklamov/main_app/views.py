from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Category, Article


def index(request):
    categories_list = Category.objects.all()
    data = {
        'title': 'Изготовление наружной рекламы в Москве.',
        'categories': categories_list,
        'cat_selected': 0,  # Ничего не выбрано
        'data': [{'title': 'ГЛАВНАЯ', 'url_name': 'home'},
                 {'title': 'НАШИ РАБОТЫ', 'url_name': 'nashi-raboti'},
                 {'title': 'НАШИ ЦЕНЫ', 'url_name': 'nashi-ceny'},
                 {'title': 'О КОМПАНИИ', 'url_name': 'o-companiy'},
                 {'title': 'КОНТАКТЫ', 'url_name': 'contacts'}],
    }
    return render(request, "main_app/index.html", context=data)

def show_category(request, cat_slug):
    categories_list = Category.objects.all()
    category = get_object_or_404(Category, slug=cat_slug)
    articles = category.articles.filter(is_published=True)
    data = {
        'title': f"Рубрика: {category.name}",
        'articles': articles,
        'cat_selected': category.pk,
        'categories': categories_list,
        'data': [{'title': 'ГЛАВНАЯ', 'url_name': 'home'},
                 {'title': 'НАШИ РАБОТЫ', 'url_name': 'nashi-raboti'},
                 {'title': 'НАШИ ЦЕНЫ', 'url_name': 'nashi-ceny'},
                 {'title': 'О КОМПАНИИ', 'url_name': 'o-companiy'},
                 {'title': 'КОНТАКТЫ', 'url_name': 'contacts'}],
    }
    return render(request, "main_app/index.html", context=data)

def show_article(request, art_slug):
    categories_list = Category.objects.all()
    article = get_object_or_404(Article, slug=art_slug, is_published=True)
    category = article.categories
    data = {
        'title': f"Статья: {article.title}",
        'cat_selected': article.categories.pk,
        'article': article,
        'category': category,
        'categories': categories_list,
        'data': [{'title': 'ГЛАВНАЯ', 'url_name': 'home'},
                 {'title': 'НАШИ РАБОТЫ', 'url_name': 'nashi-raboti'},
                 {'title': 'НАШИ ЦЕНЫ', 'url_name': 'nashi-ceny'},
                 {'title': 'О КОМПАНИИ', 'url_name': 'o-companiy'},
                 {'title': 'КОНТАКТЫ', 'url_name': 'contacts'}],
    }
    return render(request, "main_app/index.html", context=data)

def nashi_raboti(request):
    return HttpResponse('<h1>Наши работы</h1>')

def nashi_ceny(request):
    return HttpResponse('<h1>Наши цены</h1>')

def o_companiy(request):
    return HttpResponse('<h1>О компании</h1>')

def contacts(request):
    return HttpResponse('<h1>Контакты</h1>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1><u>Страница не найдена</u></h1>')