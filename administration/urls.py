from django.urls import path


from .views import (

    # Dashboard
    AdministrationDashboardView,


    # Settings
    AssociationSettingsView,
    BrandingSettingsView,
    AcademicDefaultsView,
    ReceiptSettingsView,
    PaymentSettingsView,
    EmailConfigurationView,
    UserManagementSettingsView,
    SystemRoleView,
    NotificationSettingsView,
    SecuritySettingsView,
    BackupRestoreSettingsView,
    AuditLogListView,
    GeneralConfigurationView,


    # Email
    test_email,


    # Email Templates
     EmailTemplateListView,
    EmailTemplateCreateView,
    EmailTemplateUpdateView,
    EmailTemplatePreviewView,
    EmailTemplateTestView,
    EmailTemplateActivateView,
    EmailTemplateDeactivateView,

)


app_name = "administration"



urlpatterns = [

    # =========================================
    # Administration Dashboard
    # =========================================

    path(
        "",
        AdministrationDashboardView.as_view(),
        name="dashboard",
    ),



    # =========================================
    # Association Settings
    # =========================================

    path(
        "association/",
        AssociationSettingsView.as_view(),
        name="association",
    ),



    # =========================================
    # Branding Settings
    # =========================================

    path(
        "branding/",
        BrandingSettingsView.as_view(),
        name="branding",
    ),



    # =========================================
    # Academic Defaults
    # =========================================

    path(
        "academic-defaults/",
        AcademicDefaultsView.as_view(),
        name="academic-defaults",
    ),



    # =========================================
    # Receipt Settings
    # =========================================

    path(
        "receipt-settings/",
        ReceiptSettingsView.as_view(),
        name="receipt-settings",
    ),



    # =========================================
    # Payment Settings
    # =========================================

    path(
        "payment-settings/",
        PaymentSettingsView.as_view(),
        name="payment-settings",
    ),



    # =========================================
    # Email Configuration
    # =========================================

    path(
        "email-configuration/",
        EmailConfigurationView.as_view(),
        name="email-configuration",
    ),



    path(
        "test-email/",
        test_email,
        name="test-email",
    ),




    # =========================================
    # User Management
    # =========================================

    path(
        "user-management/",
        UserManagementSettingsView.as_view(),
        name="user-management",
    ),




    # =========================================
    # Roles & Permissions
    # =========================================

    path(
        "roles-permissions/",
        SystemRoleView.as_view(),
        name="roles-permissions",
    ),




    # =========================================
    # Notifications
    # =========================================

    path(
        "notifications/",
        NotificationSettingsView.as_view(),
        name="notifications",
    ),




    # =========================================
    # Security
    # =========================================

    path(
        "security/",
        SecuritySettingsView.as_view(),
        name="security",
    ),




    # =========================================
    # Backup
    # =========================================

    path(
        "backup-restore/",
        BackupRestoreSettingsView.as_view(),
        name="backup-restore",
    ),




    # =========================================
    # Audit Logs
    # =========================================

    path(
        "audit-logs/",
        AuditLogListView.as_view(),
        name="audit-logs",
    ),




    # =========================================
    # General Configuration
    # =========================================

    path(
        "general-configuration/",
        GeneralConfigurationView.as_view(),
        name="general-configuration",
    ),





    # =========================================
    # Email Template Management
    # =========================================


    path(
        "email-templates/",
        EmailTemplateListView.as_view(),
        name="email-template-list",
    ),



    path(
        "email-templates/create/",
        EmailTemplateCreateView.as_view(),
        name="email-template-create",
    ),



    path(
        "email-templates/<int:pk>/edit/",
        EmailTemplateUpdateView.as_view(),
        name="email-template-edit",
    ),



    path(
        "email-templates/<int:pk>/preview/",
        EmailTemplatePreviewView.as_view(),
        name="email-template-preview",
    ),
    
    path(
        "email-templates/<int:pk>/test/",
        EmailTemplateTestView.as_view(),
        name="email-template-test",
    ),
    
    path(
        "email-templates/<int:pk>/activate/",
        EmailTemplateActivateView.as_view(),
        name="email-template-activate",
    ),
    
    path(
        "email-templates/<int:pk>/deactivate/",
        EmailTemplateDeactivateView.as_view(),
        name="email-template-deactivate",
    ),


]