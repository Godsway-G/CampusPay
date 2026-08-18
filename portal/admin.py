from django.contrib import admin

from .models import PasswordResetRequest


@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "status",
        "requested_at",
        "processed_at",
    )

    list_filter = (
        "status",
        "requested_at",
    )

    search_fields = (
        "member__student_id",
        "member__email",
        "member__first_name",
        "member__last_name",
    )