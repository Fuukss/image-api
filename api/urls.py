from django.urls import path

from api.views import (
    api_detail_image_view,
    api_create_image_view,
)

app_name = 'api'

urlpatterns = [
    path('<slug>/', api_detail_image_view, name='details'),
    path('create', api_create_image_view, name='create'),
]