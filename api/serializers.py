import os
import sys
import tempfile
from sys import getsizeof
from cv2 import imread, cv2

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers

from image.models import ImagePost


class ImageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = ImagePost
        fields = ['image', 'slug', 'username']

    def get_username_from_author(self, image_post):
        username = image_post.author.username
        return username

    def validate_image_url(self, image_post):
        image = image_post.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url


IMAGE_SIZE_MAX_BYTES = 20000000


class ImagePostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['image', 'slug', 'author']

    def save(self):

        try:
            image = self.validated_data['image']
            slug = self.validated_data['slug']

            image_post = ImagePost(
                author=self.validated_data['author'],
                slug=slug,
                image=image,
            )

            url = os.path.join(tempfile.gettempdir(), str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

            img = cv2.imread(url)
            dimensions = img.shape  # gives: (height, width, ?)

            aspect_ratio = dimensions[1] / dimensions[0]  # divide w / h
            if aspect_ratio < 1:
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
            image_post.save()
            return image_post
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a slug and an image."})
