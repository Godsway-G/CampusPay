from django.db import models


class TimeStampedModel(models.Model):
    """
    Base model that provides timestamps.
    """

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
        
import uuid 

class UUIDModel(models.Model):
    """
    Abstract model with UUID primary identifier.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    class Meta:
        abstract = True