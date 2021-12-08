from celery import shared_task, task
from image.models import ExpiringImagePost
from django.utils import timezone


@task
def delete_expired_images():
    for image in ExpiringImagePost.objects.all():
        if timezone.now() >= image.get_delete_time():
            image.delete_image()
