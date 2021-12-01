from django.urls import path
from api.views import (
    api_create_image_view,
    ApiImageListView,
)

app_name = 'api'

urlpatterns = [
    path('create', api_create_image_view, name='create'),
    path('list', ApiImageListView.as_view(), name='list'),
]