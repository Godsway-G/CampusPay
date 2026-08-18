from django.contrib import admin
from .models import Department, Member


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        "student_id",
        "full_name",
        "department",
        "level",
        "active",
        "portal_account",
    )

    list_filter = (
        "department",
        "level",
        "active",
    )

    search_fields = (
        "student_id",
        "first_name",
        "last_name",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def portal_account(self, obj):

        return obj.user is not None

    portal_account.boolean = True
    portal_account.short_description = "Portal"