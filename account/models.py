from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .validator import email_validator, username_validator


class MyAccountManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str = None) -> object:
        """
        Set basic information about account and check
        email and username values
        """
        email_validator(email)
        username_validator(username)

        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, username: str, password: str) -> object:
        """
        Create super user account and set special fields automatically on true.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """
    Abstract representation of user account data.
    """
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="data joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    account_tier = models.ForeignKey(
        'plan.Plan',
        on_delete=models.CASCADE,
        null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()
    object = MyAccountManager().all()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_account_tier(self):
        return self.account_tier


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    After adding the user, assign a token to him.
    """
    if created:
        Token.objects.create(user=instance)

