from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from image.validators import image_size, validate_file_extension
from sorl.thumbnail import delete, ImageField
from sorl.thumbnail import get_thumbnail
import os, sys


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


def drop_empty_folders(directory):
    """Verify that every empty folder removed in local storage."""

    for dir_path, dir_names, file_names in os.walk(directory, topdown=False):
        if not dir_names and not file_names:
            os.rmdir(dir_path)


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

    def get_expires_link(self, request, expiration_seconds=60):
        if self.image:
            original_image = self.image
            last_modified_time = os.path.getmtime(original_image)
            if last_modified_time >= expiration_seconds:
                # delete the file
                os.remove(original_image)
                return share_link(request, original_image)
            return None


@receiver(post_delete, sender=ImagePost)
def submission_delete(sender, instance, *args, **kwargs):
    """
    Signal for delete all thumbnails created based on deleted image.
    """
    try:
        image = ImagePost
        image.delete_thumbnail(instance)
    finally:
        drop_empty_folders("media_cdn/CACHE/")
