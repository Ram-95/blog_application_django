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
from ckeditor_uploader import views as ckeditor_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),
    path('', include('users.urls')),
    path('api/v1/', include('blogs_api.urls')),
    #path('ckeditor/', include('ckeditor_uploader.urls')),

    path('ckeditor/upload/', login_required(ckeditor_views.upload),
         name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)),
         name='ckeditor_browse'),
]

curr_env = os.environ.get('DJANGO_ENV')
if curr_env == 'PROD':
    urlpatterns += static(production.MEDIA_URL,
                          document_root=production.MEDIA_ROOT)

elif curr_env == 'DEV':
    print(f'\n You are in Development.\n\n')
    urlpatterns += static(development.MEDIA_URL,
                          document_root=development.MEDIA_ROOT)
    urlpatterns += static(development.STATIC_URL,
                          document_root=development.STATIC_ROOT)
