from django.db import models
from django.db.models import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .validators import check_size_value


class ThumbnailPlan(models.Model):
    """
    Model representation for thumbnail plan.
    """
    thumbnail_id = models.AutoField(primary_key=True)
    thumbnail_width = models.IntegerField(verbose_name="width", default=0, validators=[check_size_value])
    thumbnail_height = models.IntegerField(verbose_name="height", default=0, validators=[check_size_value])

    def __str__(self):
        return str(str(self.thumbnail_width) + 'x' + str(self.thumbnail_height))

    class Meta:
        ordering = ['thumbnail_id']


class Plan(models.Model):
    """
    Model representation for account plan.
    """
    plan_name = models.CharField(verbose_name="plan name", max_length=60, unique=True)
    thumbnail_name = models.ManyToManyField(ThumbnailPlan)
    original_file = models.BooleanField(verbose_name="original file", default=False)
    expires_link = models.BooleanField(verbose_name="expires link", default=False)

    USERNAME_FIELD = 'plan_name'
    REQUIRED_FIELDS = ["plan_name", ]

    def __str__(self):
        return self.plan_name

    class Meta:
        ordering = ['plan_name']

    def save(self, *args, **kwargs):
        self.plan_name = self.plan_name.capitalize()
        return super(Plan, self).save(*args, **kwargs)

    def get_thumbnail_plan(self):
        return [str(thumbnail) for thumbnail in self.thumbnail_name.all()]

    def get_original_file(self):
        return self.original_file

    def get_expires_link(self):
        return self.expires_link


# TODO: Add update signal - after initialization data!
@receiver([pre_delete], sender=Plan)
def default_plan_handler(sender, instance, **kwargs):
    """
    Signal for unable deleted basics plans.
    """
    if instance.plan_name in ["Basic", "Premium", "Enterprise"]:
        raise ProtectedError('The General user plan can not be deleted', instance)
    # if not instance._state.adding:
    #     raise ProtectedError('The General thumbnail plan can not be changed', instance)


@receiver([pre_delete], sender=ThumbnailPlan)
def default_thumbnail_plan_handler(sender, instance, **kwargs):
    """
    Signal for unable deleted basics thumbnail plans.
    """
    if instance.thumbnail_width == "200" and instance.thumbnail_height == "200" or \
            instance.thumbnail_width == "400" and instance.thumbnail_height == "400":
        raise ProtectedError('The General thumbnail plan can not be deleted', instance)
    # if not instance._state.adding:
    #     raise ProtectedError('The General thumbnail plan can not be changed', instance)
