import random
import string

from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = 'image/{author_id}/{filename}'.format(
        author_id=str(instance.author.id),
        filename=filename
    )
    return file_path

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class ImagePost(models.Model):
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.slug


@receiver(post_delete, sender=ImagePost)
def submission_delete(sender, instance, *args, **kwargs):
    instance.image.delete(False)


def pre_save_image_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + rand_slug())


pre_save.connect(pre_save_image_receiver, sender=ImagePost)
