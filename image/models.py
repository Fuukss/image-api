from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from image.validators import image_size, validate_file_extension


# Create a file save path based on the user name and file name
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

    def __str__(self):
        return str(self.image).lower()


@receiver(post_delete, sender=ImagePost)
def submission_delete(sender, instance, *args, **kwargs):
    instance.image.delete(False)


def pre_save_image_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + str(instance.image))


pre_save.connect(pre_save_image_receiver, sender=ImagePost)
