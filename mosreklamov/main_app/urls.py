from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, re_path, register_converter, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('nashi_raboti/', views.nashi_raboti, name='nashi-raboti'),
    path('dobavit_staty/', views.dobavit_staty, name='dobavit_staty'),
    path('article/edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('article/delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('article/<slug:art_slug>/', views.show_article, name='article'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/', PasswordResetView.as_view(
        template_name="main_app/password_reset_form.html",
        success_url=reverse_lazy("password_reset_done"),
        email_template_name="main_app/password_reset_email.html"),
        name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name="main_app/password_reset_done.html"),
        name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="main_app/password_reset_confirm.html",
        success_url=reverse_lazy("password_reset_complete")),
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name="main_app/password_reset_complete.html"),
        name='password_reset_complete'),
]
