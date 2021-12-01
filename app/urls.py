"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.authentication import SessionAuthentication

from app import settings
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAdminUser

urlpatterns = [
    path('admin/', admin.site.urls),

    # REST FRAMEWORK URLS
    path('api/image/', include('api.urls', 'image_api')),
    path('api/docs', include_docs_urls(
        title='API documentation', permission_classes=[IsAdminUser],
        authentication_classes=[SessionAuthentication]
    )),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
