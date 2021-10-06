import random
import string
from cv2 import imread, cv2
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from image.validators import image_size, validate_file_extension


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


def upload_location(instance, filename, **kwargs):
    file_path = 'image/{author_name}/{filename}'.format(
        author_name=str(instance.author.username),
        filename=str(filename)
    )
    return file_path


class ImagePost(models.Model):
    image = models.ImageField(upload_to=upload_location, null=False, blank=False,
                              validators=[image_size, validate_file_extension])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    image_thumbnail_200 = ImageSpecField(source='image',
                                         processors=[ResizeToFill(200, 200)],
                                         format='JPEG',
                                         options={'quality': 60})

    image_thumbnail_400 = ImageSpecField(source='image',
                                         processors=[ResizeToFill(400, 400)],
                                         format='JPEG',
                                         options={'quality': 60})

    def __str__(self):
        return str(self.image)


@receiver(post_delete, sender=ImagePost)
def submission_delete(sender, instance, *args, **kwargs):
    instance.image.delete(False)


def pre_save_image_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + str(instance.image))


pre_save.connect(pre_save_image_receiver, sender=ImagePost)
