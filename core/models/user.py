import pytz

from core import constants
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    TIMEZONES = [(c, c) for c in pytz.common_timezones]

    username = None
    
    first_name = models.CharField(
        _('first name'), max_length=150
    )
    last_name = models.CharField(
        _('last name'), max_length=150
    )

    email = models.EmailField(
        _('email address'), unique=True,
    )
    email_validated = models.BooleanField(
        _('email validated'), default=False, editable=False
    )
    phone_number = models.CharField(
        _("phone number"), max_length=15, blank=True, null=True
    )
    phone_validated = models.BooleanField(
        _('phone validated'), default=False, editable=False
    )
    language = models.SlugField(
        _('language'), default=settings.LANGUAGE_CODE,
        choices=settings.LANGUAGES
    )
    timezone = models.CharField(
        _('timezone'), max_length=100, default=settings.TIME_ZONE,
        choices=TIMEZONES
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        return super().clean()
        
