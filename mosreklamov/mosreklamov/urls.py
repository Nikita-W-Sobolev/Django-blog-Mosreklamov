"""
URL configuration for mosreklamov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main_app import views
from main_app.views import page_not_found
from mosreklamov import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
] + debug_toolbar_urls()

# Это строчки для связывания маршрута с рабочим каталогом для отладочного сервера
# Иначе изображение не будет выводиться
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = "Панель администрирования сайта Mosreklamov"
admin.site.index_title = "Статьи о наружной рекламе"