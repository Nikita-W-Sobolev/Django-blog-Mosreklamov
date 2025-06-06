from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('nashi_raboti/', views.nashi_raboti, name='nashi-raboti'),
    path('nashi_ceny/', views.nashi_ceny, name='nashi-ceny'),
    path('o_companiy/', views.o_companiy, name='o-companiy'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/<slug:cat_slug>/', views.show_category, name='category')
]