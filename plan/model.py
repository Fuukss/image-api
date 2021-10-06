from django.db import models


class Plan(models.Model):
    plan_name = models.CharField(verbose_name="plan name", max_length=60, unique=True)
    thumbnail_width = models.IntegerField(verbose_name="width")
    thumbnail_height = models.IntegerField(verbose_name="height")
    original_file = models.BooleanField(verbose_name="original file", default=False)
    expires_link = models.BooleanField(verbose_name="expires link", default=False)

    USERNAME_FIELD = 'plan_name'
    REQUIRED_FIELDS = ["plan_name", ]

    def __str__(self):
        return self.plan_name
