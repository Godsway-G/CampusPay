from django.contrib import admin

from .models import (
    AcademicYear,
    Semester,
    FeeStructure,
    Payment,
    Receipt,
)



from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # This enables the autocomplete to find users based on these fields
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "association",
        "is_current",
        "created_at",
    )

    list_filter = (
        "is_current",
        "association",
    )

    search_fields = (
        "name",
        "association__name",
    )

    ordering = ("-name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Academic Year Information", {
            "fields": (
                "association",
                "name",
                "is_current",
            )
        }),
        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = (
        "academic_year",
        "semester",
        "payment_deadline",
        "is_active",
    )

    list_filter = (
        "semester",
        "is_active",
        "academic_year",
    )

    search_fields = (
        "academic_year__name",
    )

    ordering = (
        "-academic_year",
        "semester",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "payment_deadline"

    fieldsets = (
        ("Semester Information", {
            "fields": (
                "academic_year",
                "semester",
                "payment_deadline",
                "is_active",
            )
        }),
        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = (
        "semester",
        "department",
        "level",
        "amount",
    )

    list_filter = (
        "semester",
        "department",
        "level",
    )

    search_fields = (
        "department__name",
        "semester__academic_year__name",
    )

    ordering = (
        "semester",
        "department",
        "level",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Fee Structure", {
            "fields": (
                "semester",
                "department",
                "level",
                "amount",
            )
        }),
        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "member",
        "amount_paid",
        "payment_method",
        "payment_date",
        "recorded_by",
    )

    list_filter = (
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "payment_id",
        "member__student_id",
        "member__first_name",
        "member__last_name",
        "transaction_reference",
    )

    ordering = (
        "-payment_date",
    )

    date_hierarchy = "payment_date"

    readonly_fields = (
        "payment_id",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "member",
        "fee_structure",
        "recorded_by",
    )

    fieldsets = (
        ("Payment Information", {
            "fields": (
                "payment_id",
                "member",
                "fee_structure",
                "amount_paid",
                "payment_method",
                "transaction_reference",
                "payment_date",
                "recorded_by",
                "remarks",
            )
        }),
        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "payment",
        "generated_at",
        "printed",
    )

    list_filter = (
        "printed",
        "generated_at",
    )

    search_fields = (
        "receipt_number",
        "payment__payment_id",
        "payment__member__student_id",
    )

    ordering = (
        "-generated_at",
    )

    readonly_fields = (
        "receipt_number",
        "generated_at",
    )

    date_hierarchy = "generated_at"

    autocomplete_fields = (
        "payment",
    )

    fieldsets = (
        ("Receipt Information", {
            "fields": (
                "receipt_number",
                "payment",
                "printed",
            )
        }),
        ("System Information", {
            "classes": ("collapse",),
            "fields": (
                "generated_at",
            )
        }),
    )