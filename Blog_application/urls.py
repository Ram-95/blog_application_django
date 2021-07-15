"""Blog_application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .settings import development, production

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),
    path('', include('users.urls')),
]

curr_env = os.environ.get('DJANGO_ENV')
if curr_env == 'PROD':
    urlpatterns += static(production.MEDIA_URL, document_root=production.MEDIA_ROOT)
elif curr_env == 'DEV':
    urlpatterns += static(development.MEDIA_URL, document_root=development.MEDIA_ROOT)
