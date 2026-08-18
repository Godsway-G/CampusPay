from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    UpdateView,
    View,
    ListView,
    CreateView,
    DetailView,
)
from administration.services.email_engine import EmailService
from core.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
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

from .forms import (
    AssociationSettingsForm,
    BrandingSettingsForm,
    AcademicDefaultsForm,
    ReceiptSettingsForm,
    PaymentSettingsForm,
    EmailConfigurationForm,
    UserManagementSettingsForm,
    SystemRoleForm,
    NotificationSettingsForm,
    SecuritySettingsForm,
    BackupRestoreSettingsForm,
    AuditLogFilterForm,
    GeneralConfigurationForm,
    EmailTemplateForm,
    EmailTemplateTestForm,
)
import logging

logger = logging.getLogger(__name__)

from administration.services.academic_defaults import (
    AcademicConfigurationService,
)

from administration.services.email_service import (
    EmailConfigurationService,
)

from django.template import Template, Context
from django.utils import timezone


# =====================================================
# ADMINISTRATION DASHBOARD
# =====================================================

class AdministrationDashboardView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "administration/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["active_section"] = "settings"
        context["page_title"] = "Administration Settings"

        # -------------------------------------------------
        # Configuration Status
        # -------------------------------------------------

        context["association_configured"] = (
            AssociationSettings.objects.exists()
        )

        context["branding_configured"] = (
            BrandingSettings.objects.exists()
        )

        context["academic_defaults_configured"] = (
            AcademicDefaults.objects.exists()
        )

        context["payment_settings_configured"] = (
            PaymentSettings.objects.exists()
        )

        context["receipt_settings_configured"] = (
            ReceiptSettings.objects.exists()
        )

        context["email_configuration_configured"] = (
            EmailConfiguration.objects.exists()
        )
        
        context["email_templates_configured"] = (
            EmailTemplate.objects.exists()
        )

        context["user_management_configured"] = (
            UserManagementSettings.objects.exists()
        )

        context["roles_permissions_configured"] = (
            SystemRole.objects.exists()
        )

        context["notification_settings_configured"] = (
            NotificationSettings.objects.exists()
        )

        context["security_settings_configured"] = (
            SecuritySettings.objects.exists()
        )

        context["backup_restore_configured"] = (
            BackupRestoreSettings.objects.exists()
        )

        context["general_configuration_configured"] = (
            GeneralConfiguration.objects.exists()
        )

        return context


# =====================================================
# ASSOCIATION INFORMATION SETTINGS
# =====================================================

class AssociationSettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = AssociationSettings
    form_class = AssociationSettingsForm
    template_name = "administration/association/form.html"

    success_url = reverse_lazy(
        "administration:association"
    )

    def get_object(self):

        obj = (
            AssociationSettings.objects
            .first()
        )

        if obj is None:

            obj = AssociationSettings.objects.create(
                association_name="",
                association_code="TEMP",
                institution_name="",
                email="admin@example.com",
                phone_number="",
            )

        return obj

    def form_valid(self, form):

        messages.success(
            self.request,
            "Association information updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# BRANDING SETTINGS
# =====================================================

class BrandingSettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    """
    Manage CampusPay branding configuration.
    """

    model = BrandingSettings
    form_class = BrandingSettingsForm
    template_name = "administration/branding/form.html"

    success_url = reverse_lazy(
        "administration:branding"
    )

    def get_object(self):

        obj, created = (
            BrandingSettings.objects
            .get_or_create(id=1)
        )

        return obj

    def form_valid(self, form):

        messages.success(
            self.request,
            "CampusPay branding settings updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# ACADEMIC DEFAULT SETTINGS
# =====================================================

class AcademicDefaultsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = AcademicDefaults
    form_class = AcademicDefaultsForm

    template_name = (
        "administration/academic_defaults/form.html"
    )

    success_url = reverse_lazy(
        "administration:academic-defaults"
    )

    def get_object(self):

        obj, created = (
            AcademicDefaults.objects
            .get_or_create(id=1)
        )

        return obj

    def form_valid(self, form):

        messages.success(
            self.request,
            "Academic defaults updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# RECEIPT SETTINGS
# =====================================================

class ReceiptSettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = ReceiptSettings
    form_class = ReceiptSettingsForm

    template_name = (
        "administration/receipt_settings/form.html"
    )

    success_url = reverse_lazy(
        "administration:dashboard"
    )

    def get_object(self):

        settings, created = (
            ReceiptSettings.objects
            .get_or_create(pk=1)
        )

        return settings

    def form_valid(self, form):

        messages.success(
            self.request,
            "Receipt settings updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# PAYMENT SETTINGS
# =====================================================

class PaymentSettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = PaymentSettings
    form_class = PaymentSettingsForm

    template_name = (
        "administration/payment_settings/form.html"
    )

    success_url = reverse_lazy(
        "administration:dashboard"
    )

    def get_object(self):

        settings, created = (
            PaymentSettings.objects
            .get_or_create(pk=1)
        )

        return settings

    def form_valid(self, form):

        messages.success(
            self.request,
            "Payment settings updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# EMAIL CONFIGURATION SETTINGS
# =====================================================

class EmailConfigurationView(
    LoginRequiredMixin,
    UpdateView,
):
    model = EmailConfiguration
    form_class = EmailConfigurationForm

    template_name = (
        "administration/email_configuration/form.html"
    )

    success_url = reverse_lazy(
        "administration:dashboard"
    )

    def get_object(self):

        email_config, created = (
            EmailConfiguration.objects
            .get_or_create(pk=1)
        )

        return email_config

    def form_valid(self, form):

        messages.success(
            self.request,
            "Email configuration updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# EMAIL TEMPLATE MANAGEMENT
# =====================================================


class EmailTemplateListView(
    LoginRequiredMixin,
    ListView,
):

    model = EmailTemplate

    template_name = (
        "administration/email_templates/list.html"
    )

    context_object_name = "templates"

    ordering = [
        "name"
    ]


class EmailTemplateCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = EmailTemplate

    form_class = EmailTemplateForm

    template_name = (
        "administration/email_templates/form.html"
    )

    success_url = reverse_lazy(
        "administration:email-template-list"
    )


    def form_valid(self, form):

        messages.success(
            self.request,
            "Email template created successfully."
        )

        return super().form_valid(form)


class EmailTemplateUpdateView(
    LoginRequiredMixin,
    UpdateView,
):

    model = EmailTemplate

    form_class = EmailTemplateForm

    template_name = (
        "administration/email_templates/form.html"
    )

    success_url = reverse_lazy(
        "administration:email-template-list"
    )


    def form_valid(self, form):

        messages.success(
            self.request,
            "Email template updated successfully."
        )

        return super().form_valid(form)


class EmailTemplatePreviewView(
    LoginRequiredMixin,
    DetailView,
):

    model = EmailTemplate

    template_name = (
        "administration/email_templates/preview.html"
    )

    context_object_name = "template"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        template = self.object

        # -------------------------------------------------
        # PREVIEW DATA
        # -------------------------------------------------

        preview_context = {

            "name": "Godsway Xenyo",

            "amount": "150.00",

            "reference": "CP-000123",

            "date": timezone.now().strftime(
                "%B %d, %Y"
            ),

            "recipient": "Preview Recipient",

            "system_name": "CampusPay",

        }

        # -------------------------------------------------
        # RENDER SUBJECT
        # -------------------------------------------------

        if template.subject:

            try:

                subject_template = Template(
                    template.subject
                )

                preview_subject = (
                    subject_template.render(
                        Context(preview_context)
                    )
                )

            except Exception:

                preview_subject = template.subject

        else:

            preview_subject = "(No subject configured)"

        # -------------------------------------------------
        # RENDER HTML
        # -------------------------------------------------

        if template.html_content:

            try:

                html_template = Template(
                    template.html_content
                )

                preview_html = (
                    html_template.render(
                        Context(preview_context)
                    )
                )

            except Exception:

                preview_html = template.html_content

        else:

            preview_html = ""

        # -------------------------------------------------
        # RENDER PLAIN TEXT
        # -------------------------------------------------

        if template.body:

            try:

                body_template = Template(
                    template.body
                )

                preview_body = (
                    body_template.render(
                        Context(preview_context)
                    )
                )

            except Exception:

                preview_body = template.body

        else:

            preview_body = ""

        # -------------------------------------------------
        # FINAL CONTEXT
        # -------------------------------------------------

        context["preview_recipient"] = (
            "Preview Recipient"
        )

        context["preview_subject"] = (
            preview_subject
        )

        context["preview_html"] = (
            preview_html
        )

        context["preview_body"] = (
            preview_body
        )

        return context

# =====================================================
# SEND TEST EMAIL
# =====================================================


class EmailTemplateTestView(
    LoginRequiredMixin,
    View,
):

    template_name = (
        "administration/email_templates/test.html"
    )


    def get_template(self, pk):

        return EmailTemplate.objects.filter(
            pk=pk
        ).first()


    def get(self, request, pk):

        template = self.get_template(pk)

        if not template:

            messages.error(
                request,
                "The selected email template could not be found."
            )

            return redirect(
                "administration:email-template-list"
            )


        form = EmailTemplateTestForm(
            initial={
                "recipient": request.user.email
            }
        )


        return render(
            request,
            self.template_name,
            {
                "template": template,
                "form": form,
            }
        )


    def post(self, request, pk):

        template = self.get_template(pk)

        if not template:

            messages.error(
                request,
                "The selected email template could not be found."
            )

            return redirect(
                "administration:email-template-list"
            )


        # -------------------------------------------------
        # SAFETY CHECK — INACTIVE TEMPLATE
        # -------------------------------------------------

        if not template.is_active:

            messages.error(
                request,
                "This email template is inactive and cannot be sent."
            )

            return redirect(
                "administration:email-template-list"
            )


        form = EmailTemplateTestForm(
            request.POST
        )


        if not form.is_valid():

            return render(
                request,
                self.template_name,
                {
                    "template": template,
                    "form": form,
                }
            )


        recipient = form.cleaned_data["recipient"]


        # -------------------------------------------------
        # TEST CONTEXT
        # -------------------------------------------------

        context = {

            # Simulated student
            "name": "Godsway Xenyo",

            #Recipient receiving the test email
            "recipient": recipient,
            

            "system_name": "CampusPay",
            # Simulated payment information
            "amount": "GHS 150.00",

            "reference": "CP-TEST-000123",
            
            "date": timezone.now().strftime("%B %d, %Y"),

        }


        # -------------------------------------------------
        # SEND
        # -------------------------------------------------

        try:

            result = EmailService.send_template(
                template_slug=template.slug,
                recipient=recipient,
                context=context,
            )

        except Exception:

            logger.exception(
                "Unexpected error while sending test email."
            )

            result = False


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if result:

            messages.success(
                request,
                f"Test email sent successfully to {recipient}."
            )

        else:

            messages.error(
                request,
                "The test email could not be sent. "
                "Check the email configuration and Brevo settings."
            )


        return redirect(
            "administration:email-template-list"
        )


# =====================================================
# ACTIVATE EMAIL TEMPLATE
# =====================================================


class EmailTemplateActivateView(
    LoginRequiredMixin,
    View,
):

    def post(self, request, pk):

        template = EmailTemplate.objects.filter(
            pk=pk
        ).first()


        if not template:

            messages.error(
                request,
                "The email template could not be found."
            )

            return redirect(
                "administration:email-template-list"
            )


        if template.is_active:

            messages.info(
                request,
                "This email template is already active."
            )

            return redirect(
                "administration:email-template-list"
            )


        template.is_active = True

        template.save(
            update_fields=[
                "is_active"
            ]
        )


        messages.success(
            request,
            f'"{template.name}" has been activated.'
        )


        return redirect(
            "administration:email-template-list"
        )


# =====================================================
# DEACTIVATE EMAIL TEMPLATE
# =====================================================


class EmailTemplateDeactivateView(
    LoginRequiredMixin,
    View,
):

    def post(self, request, pk):

        template = EmailTemplate.objects.filter(
            pk=pk
        ).first()


        if not template:

            messages.error(
                request,
                "The email template could not be found."
            )

            return redirect(
                "administration:email-template-list"
            )


        if not template.is_active:

            messages.info(
                request,
                "This email template is already inactive."
            )

            return redirect(
                "administration:email-template-list"
            )


        template.is_active = False

        template.save(
            update_fields=[
                "is_active"
            ]
        )


        messages.success(
            request,
            f'"{template.name}" has been deactivated.'
        )


        return redirect(
            "administration:email-template-list"
        )


# =====================================================
# USER MANAGEMENT SETTINGS
# =====================================================

class UserManagementSettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = UserManagementSettings

    form_class = UserManagementSettingsForm

    template_name = (
        "administration/user_management/form.html"
    )

    success_url = reverse_lazy(
        "administration:dashboard"
    )

    def get_object(self):

        settings, created = (
            UserManagementSettings.objects
            .get_or_create(pk=1)
        )

        return settings

    def form_valid(self, form):

        messages.success(
            self.request,
            "User management settings updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# ROLES & PERMISSIONS SETTINGS
# =====================================================

class SystemRoleView(
    LoginRequiredMixin,
    UpdateView,
):
    model = SystemRole

    form_class = SystemRoleForm

    template_name = (
        "administration/roles_permissions/form.html"
    )

    success_url = reverse_lazy(
        "administration:roles-permissions"
    )

    def get_object(self):

        role, created = (
            SystemRole.objects.get_or_create(
                pk=1,
                defaults={
                    "role_name": "super_admin",
                    "can_manage_users": True,
                    "can_manage_finance": True,
                    "can_manage_members": True,
                    "can_manage_reports": True,
                    "can_access_settings": True,
                },
            )
        )

        return role

    def form_valid(self, form):

        messages.success(
            self.request,
            "Roles and permissions updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# NOTIFICATION SETTINGS
# =====================================================

class NotificationSettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = NotificationSettings

    form_class = NotificationSettingsForm

    template_name = (
        "administration/notifications/form.html"
    )

    success_url = reverse_lazy(
        "administration:notifications"
    )

    def get_object(self):

        settings, created = (
            NotificationSettings.objects
            .get_or_create(pk=1)
        )

        return settings

    def form_valid(self, form):

        messages.success(
            self.request,
            "Notification settings updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# SECURITY SETTINGS
# =====================================================

class SecuritySettingsView(
    LoginRequiredMixin,
    UpdateView,
):
    model = SecuritySettings

    form_class = SecuritySettingsForm

    template_name = (
        "administration/security/form.html"
    )

    success_url = reverse_lazy(
        "administration:dashboard"
    )

    def get_object(self):

        security, created = (
            SecuritySettings.objects
            .get_or_create(pk=1)
        )

        return security

    def form_valid(self, form):

        messages.success(
            self.request,
            "Security settings updated successfully.",
        )

        return super().form_valid(form)


# =====================================================
# BACKUP & RESTORE SETTINGS
# =====================================================

class BackupRestoreSettingsView(
    LoginRequiredMixin,
    View,
):
    template_name = (
        "administration/backup_restore/form.html"
    )

    def get(self, request):

        settings = (
            BackupRestoreSettings.objects
            .first()
        )

        if not settings:

            settings = (
                BackupRestoreSettings.objects
                .create()
            )

        form = BackupRestoreSettingsForm(
            instance=settings
        )

        return render(
            request,
            self.template_name,
            {
                "form": form
            },
        )

    def post(self, request):

        settings = (
            BackupRestoreSettings.objects
            .first()
        )

        if not settings:

            settings = (
                BackupRestoreSettings.objects
                .create()
            )

        form = BackupRestoreSettingsForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Backup settings updated successfully.",
            )

            return redirect(
                "administration:backup-restore"
            )

        return render(
            request,
            self.template_name,
            {
                "form": form
            },
        )


# =====================================================
# AUDIT LOGS
# =====================================================

class AuditLogListView(
    LoginRequiredMixin,
    View,
):
    template_name = (
        "administration/audit_logs/list.html"
    )

    def get(self, request):

        logs = (
            AuditLog.objects
            .select_related("user")
            .order_by("-created_at")
        )

        form = AuditLogFilterForm(
            request.GET or None
        )

        if form.is_valid():

            action = form.cleaned_data.get(
                "action"
            )

            start_date = form.cleaned_data.get(
                "start_date"
            )

            end_date = form.cleaned_data.get(
                "end_date"
            )

            if action:

                logs = logs.filter(
                    action=action
                )

            if start_date:

                logs = logs.filter(
                    created_at__date__gte=start_date
                )

            if end_date:

                logs = logs.filter(
                    created_at__date__lte=end_date
                )

        context = {
            "logs": logs,
            "filter_form": form,
        }

        return render(
            request,
            self.template_name,
            context,
        )


# =====================================================
# GENERAL CONFIGURATION
# =====================================================

class GeneralConfigurationView(
    LoginRequiredMixin,
    View,
):
    template_name = (
        "administration/general_configuration/form.html"
    )

    def get(self, request):

        settings = (
            GeneralConfiguration.objects
            .first()
        )

        if not settings:

            settings = (
                GeneralConfiguration.objects
                .create()
            )

        form = GeneralConfigurationForm(
            instance=settings
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request):

        settings = (
            GeneralConfiguration.objects
            .first()
        )

        if not settings:

            settings = (
                GeneralConfiguration.objects
                .create()
            )

        form = GeneralConfigurationForm(
            request.POST,
            instance=settings,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "General configuration updated successfully.",
            )

            return redirect(
                "administration:general-configuration"
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )


# =====================================================
# TEST EMAIL
# =====================================================

@login_required
def test_email(request):

    user_email = request.user.email

    if not user_email:

        messages.error(
            request,
            "Your account has no email address.",
        )

        return redirect(
            "administration:email-configuration"
        )

    result = (
        EmailConfigurationService
        .send_test_email(user_email)
    )

    if result:

        messages.success(
            request,
            f"Test email sent successfully to {user_email}",
        )

    else:

        messages.error(
            request,
            "Email sending failed. Check email configuration.",
        )

    return redirect(
        "administration:email-configuration"
    )