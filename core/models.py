from django.db import models


class Association(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )

    short_name = models.CharField(
        max_length=20,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="associations/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name