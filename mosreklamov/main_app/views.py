from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

def index(request):
    data = {
        'title': 'Mosreklamov',
    }
    return render(request, "main_app/index.html", context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1><u>Страница не найдена</u></h1>')