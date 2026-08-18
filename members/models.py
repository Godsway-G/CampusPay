from django.db import models
from django.conf import settings


class Department(models.Model):
    """
    University Departments
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class Member(models.Model):
    """
    Association Member
    """

    LEVELS = [
        ("100", "Level 100"),
        ("200", "Level 200"),
        ("300", "Level 300"),
        ("400", "Level 400"),
    ]

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    # Link each member to one login account
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="member_profile",
        null=True,
        blank=True,
    )

    student_id = models.CharField(
        max_length=30,
        unique=True
    )

    first_name = models.CharField(
        max_length=80
    )

    last_name = models.CharField(
        max_length=80
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER
    )

    level = models.CharField(
        max_length=10,
        choices=LEVELS
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )

    photo = models.ImageField(
        upload_to="members/",
        blank=True,
        null=True
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Member"
        verbose_name_plural = "Members"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"