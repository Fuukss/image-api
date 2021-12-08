import os
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from image.validators import image_size, validate_file_extension
from sorl.thumbnail import delete
from sorl.thumbnail import get_thumbnail
from django.utils import timezone


def share_link(request, image):
    """
    Function to share an image link (absolute url)
    request: request, image: model.<image>
    """
    image_url = str(request.build_absolute_uri(image.url))
    if "?" in image_url:
        image_url = image_url[:image_url.rfind("?")]
    return image_url


def upload_location(instance, filename, **kwargs):
    """
    Create a file save path based on the user name and file name
    """
    file_path = 'image/{author_name}/{filename}'.format(
        author_name=str(instance.author.username),
        filename=str(filename)
    )
    return file_path


def upload_location_for_expires_images(instance, filename, **kwargs):
    """
    Create a file save path based on the user name and file name
    """
    filename = filename.split('/')[-1]
    file_path = 'expires/{author_name}/{filename}'.format(
        author_name=str(instance.author.username),
        filename=str(filename)
    )
    return file_path


def drop_empty_folders(directory):
    """Verify that every empty folder removed in local storage."""

    for dir_path, dir_names, file_names in os.walk(directory, topdown=False):
        if not dir_names and not file_names:
            os.rmdir(dir_path)


class ExpiringImagePost(models.Model):
    create_image_time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location_for_expires_images, null=False, blank=False)
    author = models.CharField(max_length=55)
    time = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return str(self.image).lower()

    def return_image(self):
        return self.image

    def get_delete_time(self):
        return self.create_image_time + timedelta(seconds=int(self.time))

    def delete_image(self):
        self.delete()


class ImagePost(models.Model):
    """
    Class representation for image.
    """
    image = models.ImageField(upload_to=upload_location, null=False, blank=False,
                              validators=[image_size, validate_file_extension])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.image).lower()

    def get_a_thumbnail(self, request, size):
        if self.image:
            thumbnail = get_thumbnail(self.image, size, quality=90)
            return share_link(request, thumbnail)
        return None

    def delete_thumbnail(self):
        if self.image:
            delete(self.image)
        return None

    def get_original_image(self, request):
        if self.image:
            return share_link(request, self.image)
        return None

    def get_original_expires_image(self, request, time_out_url):
        if self.image:
            expires_image = ExpiringImagePost(image=self.image.file, author=self.author, time=time_out_url)
            expires_image.save()
            return share_link(request, expires_image.return_image())


@receiver(post_delete, sender=ImagePost)
def submission_delete(sender, instance, *args, **kwargs):
    """
    Signal for delete all thumbnails created based on deleted image.
    """
    try:
        image = ImagePost
        image.delete_thumbnail(instance)
    finally:
        drop_empty_folders("media/expires")
        drop_empty_folders("media/CACHE")
        drop_empty_folders("media/image")
