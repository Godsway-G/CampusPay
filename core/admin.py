from django.contrib import admin
from .models import Association


@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "email",
        "phone",
        "is_active",
    )

    search_fields = (
        "name",
        "short_name",
    )

    list_filter = (
        "is_active",
    )