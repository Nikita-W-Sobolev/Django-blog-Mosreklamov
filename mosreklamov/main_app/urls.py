from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('nashi_raboti/', views.nashi_raboti, name='nashi-raboti'),
    path('dobavit_staty/', views.dobavit_staty, name='dobavit_staty'),
    path('o_companiy/', views.o_companiy, name='o-companiy'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('article/<slug:art_slug>/', views.show_article, name='article'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
]
