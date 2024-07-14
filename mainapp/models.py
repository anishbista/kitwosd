from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.common import CommonModel


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        return super().save(*args, **kwargs)


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to="site-settings")
    logo_alt = models.CharField(max_length=255, null=True, blank=True)

    phone = models.CharField(
        default="",
        max_length=255,
        null=False,
        blank=False,
    )

    company_email = models.EmailField(
        null=False,
        blank=False,
    )

    facebook = models.URLField(null=True, blank=True, max_length=255)
    linkedin = models.URLField(null=True, blank=True, max_length=255)
    instagram = models.URLField(null=True, blank=True, max_length=255)

    address = models.CharField(
        max_length=500,
        default="",
        null=False,
        blank=False,
    )

    location_iframe = models.TextField(
        default="",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class HomeBanner(models.Model):

    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=350)

    background_image = models.ImageField(
        null=False, blank=False, upload_to="banner-image/"
    )
    bg_image_alt = models.CharField(null=True, blank=True, max_length=255)
    image = models.ImageField(null=False, blank=False, upload_to="banner-image/")
    alt = models.CharField(null=True, blank=True, max_length=255)

    publish = models.BooleanField(default=True)
