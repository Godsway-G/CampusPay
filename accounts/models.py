from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = "ADMIN"
    TREASURER = "TREASURER"
    MEMBER = "MEMBER"
    STUDENT = "STUDENT"
    
    
    ROLE_CHOICES = [
    (ADMIN, "Administrator"),
    (TREASURER, "Treasurer"),
    (MEMBER, "Member"),
    (STUDENT, "Student"),
]

    role = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default=MEMBER,
)
    
    # Force student to change temporary password
    must_change_password = models.BooleanField(
        default=True,
    )
    

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
 
     
     
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
 
 
 
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.username
