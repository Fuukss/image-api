from django.contrib import admin
from image.models import ImagePost, ExpiringImagePost

admin.site.register(ImagePost)
admin.site.register(ExpiringImagePost)
