from django.contrib import admin

from .models import (
    AssociationSettings,
    BrandingSettings,
    AcademicDefaults,
    ReceiptSettings,
    PaymentSettings,
    EmailConfiguration,
    UserManagementSettings,
    SystemRole,
    NotificationSettings,
    SecuritySettings,
    BackupRestoreSettings,
    AuditLog,
    GeneralConfiguration,
    EmailTemplate,
)

@admin.register(AssociationSettings)
class AssociationSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "association_name",
        "association_code",
        "institution_name",
        "email",
        "phone_number",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "country",
    )

    search_fields = (
        "association_name",
        "association_code",
        "institution_name",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Association Information",
            {
                "fields": (
                    "association_name",
                    "association_code",
                    "institution_name",
                    "description",
                )
            },
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "email",
                    "phone_number",
                    "website",
                    "address",
                    "postal_address",
                    "city",
                    "region",
                    "country",
                )
            },
        ),

        (
            "System",
            {
                "fields": (
                    "established_date",
                    "is_active",
                    "created_at",
                    "updated_at",
                )
            },
        ),

    )
    
    
    def has_add_permission(self, request):
       """
       Allow only one Association Settings record.
       """
       return not AssociationSettings.objects.exists()
   
   
@admin.register(BrandingSettings)
class BrandingSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "primary_color",
        "secondary_color",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not BrandingSettings.objects.exists() 
    
    
    
    
# =====================================================
# ACADEMIC DEFAULTS
# =====================================================

@admin.register(AcademicDefaults)
class AcademicDefaultsAdmin(admin.ModelAdmin):

    list_display = (
        "academic_year",
        "semester",
        "auto_select_active",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not AcademicDefaults.objects.exists()



# =====================================================
# RECEIPT SETTINGS
# =====================================================

@admin.register(ReceiptSettings)
class ReceiptSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_prefix",
        "starting_number",
        "include_logo",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not ReceiptSettings.objects.exists()



# =====================================================
# PAYMENT SETTINGS
# =====================================================

@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "currency",
        "allow_partial_payment",
        "prevent_overpayment",
        "auto_generate_receipt",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not PaymentSettings.objects.exists()



# =====================================================
# EMAIL CONFIGURATION
# =====================================================

@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(admin.ModelAdmin):

    list_display = [
        "provider",
        "sender_name",
        "default_sender_email",
        "is_active",
        "updated_at",
    ]


    list_filter = [
        "provider",
        "is_active",
    ]


    search_fields = [
        "sender_name",
        "default_sender_email",
    ]


    readonly_fields = [
        "created_at",
        "updated_at",
    ]


    fieldsets = (

        (
            "Email Provider",
            {
                "fields": (
                    "provider",
                    "brevo_api_key",
                )
            }
        ),


        (
            "Sender Information",
            {
                "fields": (
                    "sender_name",
                    "default_sender_email",
                )
            }
        ),


        (
            "SMTP Configuration (Backup)",
            {
                "fields": (
                    "email_host",
                    "email_port",
                    "email_username",
                    "email_password",
                    "encryption",
                )
            }
        ),


        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            }
        ),


        (
            "Audit",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )


# =====================================================
# USER MANAGEMENT SETTINGS
# =====================================================

@admin.register(UserManagementSettings)
class UserManagementSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "allow_registration",
        "require_email_verification",
        "max_login_attempts",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not UserManagementSettings.objects.exists()



# =====================================================
# SYSTEM ROLES
# =====================================================

@admin.register(SystemRole)
class SystemRoleAdmin(admin.ModelAdmin):

    list_display = (
        "role_name",
        "can_manage_users",
        "can_manage_finance",
        "can_manage_members",
        "is_active",
    )

    list_filter = (
        "role_name",
        "is_active",
    )

    search_fields = (
        "role_name",
    )



# =====================================================
# NOTIFICATION SETTINGS
# =====================================================

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "payment_notifications",
        "receipt_notifications",
        "email_notifications",
        "system_alerts",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not NotificationSettings.objects.exists()



# =====================================================
# SECURITY SETTINGS
# =====================================================

@admin.register(SecuritySettings)
class SecuritySettingsAdmin(admin.ModelAdmin):

    list_display = (
        "minimum_password_length",
        "enable_login_attempt_limit",
        "enable_two_factor",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not SecuritySettings.objects.exists()



# =====================================================
# BACKUP & RESTORE SETTINGS
# =====================================================

@admin.register(BackupRestoreSettings)
class BackupRestoreSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "automatic_backup",
        "backup_frequency",
        "storage_location",
        "backup_status",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not BackupRestoreSettings.objects.exists()



# =====================================================
# AUDIT LOGS
# =====================================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "action",
        "user",
        "model_name",
        "created_at",
    )

    list_filter = (
        "action",
        "created_at",
    )

    search_fields = (
        "description",
        "model_name",
        "object_id",
    )

    readonly_fields = (
        "created_at",
    )



# =====================================================
# GENERAL CONFIGURATION
# =====================================================

@admin.register(GeneralConfiguration)
class GeneralConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        "system_name",
        "system_version",
        "timezone",
        "maintenance_mode",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return not GeneralConfiguration.objects.exists()
    
    
    
    
# =====================================================
# EMAIL TEMPLATE ADMIN
# =====================================================


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing CampusPay email templates.
    """


    list_display = [
        "name",
        "template_type",
        "is_active",
        "created_at",
        "updated_at",
    ]


    list_filter = [
        "template_type",
        "is_active",
        "created_at",
    ]


    search_fields = [
        "name",
        "slug",
        "subject",
        "description",
    ]


    readonly_fields = [
        "created_at",
        "updated_at",
    ]


    ordering = [
        "name"
    ]


    fieldsets = (

        (
            "Template Information",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "template_type",
                    "is_active",
                )
            }
        ),


        (
            "Email Content",
            {
                "fields": (
                    "subject",
                    "body",
                    "html_content",
                )
            }
        ),


        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )          
   