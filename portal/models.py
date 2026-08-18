from django.db import models

from members.models import Member
from django.conf import settings

class PasswordResetRequest(models.Model):

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

    STATUS = [

        (PENDING, "Pending"),

        (APPROVED, "Approved"),

       (REJECTED, "Rejected"),

    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
    )

    # NEW FIELD
    reason = models.TextField(
        max_length=500,
    )

    requested_at = models.DateTimeField(
        auto_now_add=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default=PENDING,
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.member.student_id} - {self.status}"
    
    
    
class PasswordResetAudit(models.Model):

    ACTIONS = [

        ("REQUEST", "Reset Requested"),

        ("APPROVED", "Reset Approved"),

        ("REJECTED", "Reset Rejected"),

    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    action = models.CharField(
        max_length=20,
        choices=ACTIONS
    )


    description = models.TextField(
        blank=True
    )


    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return f"{self.user} - {self.action}" 
    
    
    
class AuditLog(models.Model):

    ACTION_CHOICES = [

        (
            "PASSWORD_RESET_APPROVED",
            "Password Reset Approved"
        ),

        (
            "PASSWORD_RESET_REJECTED",
            "Password Reset Rejected"
        ),

        (
            "PASSWORD_RESET_REQUESTED",
            "Password Reset Requested"
        ),

    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )


    action = models.CharField(
        max_length=100,
        choices=ACTION_CHOICES
    )


    description = models.TextField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return f"{self.action} - {self.created_at}"       
        
               