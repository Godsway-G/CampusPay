from django import forms

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
    EmailConfiguration,
    EmailTemplate,

)


class AssociationSettingsForm(forms.ModelForm):
    """
    Form for managing association information.
    """

    class Meta:
        
        def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)

           for field in self.fields.values():
               field.help_text = ""
               
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields.values():
                field.help_text = ""       

        model = AssociationSettings

        fields = [
    "association_name",
    "association_code",
    "short_name",
    "institution_name",
    "logo",
    "email",
    "phone_number",
    "website",
    "address",
    "city",
    "region",
    "country",
    "postal_address",
    "description",
    "established_date",
    "motto",
    "office_hours",
    "facebook",
    "x",
    "instagram",
    "linkedin",
    "show_logo_on_receipts",
    "is_active",
]

        widgets = {

            "association_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter association name",
                }
            ),

            "association_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: CSAA",
                }
            ),

            "institution_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Institution name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email address",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Physical address",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "region": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "postal_address": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

            "established_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
             "motto": forms.TextInput(
    attrs={
        "class": "form-control",
        "placeholder": "Association motto",
    }
),

"office_hours": forms.TextInput(
    attrs={
        "class": "form-control",
        "placeholder": "Mon - Fri, 8:00 AM - 5:00 PM",
    }
),

"facebook": forms.URLInput(
    attrs={
        "class": "form-control",
        "placeholder": "https://facebook.com/...",
    }
),

"x": forms.URLInput(
    attrs={
        "class": "form-control",
        "placeholder": "https://x.com/...",
    }
),

"instagram": forms.URLInput(
    attrs={
        "class": "form-control",
        "placeholder": "https://instagram.com/...",
    }
),

"linkedin": forms.URLInput(
    attrs={
        "class": "form-control",
        "placeholder": "https://linkedin.com/company/...",
    }
),


    "short_name": forms.TextInput(
    attrs={
        "class": "form-control",
        "placeholder": "Example: CSSA",
    }
),
    
    
    
    "logo": forms.ClearableFileInput(
    attrs={
        "class": "form-control",
    }
),
    
    
    "show_logo_on_receipts": forms.CheckboxInput(
    attrs={
        "class": "form-check-input",
    }
),



        }
        
        


class BrandingSettingsForm(forms.ModelForm):
    """
    Form for managing CampusPay branding settings.
    """

    class Meta:

        model = BrandingSettings

        fields = [
            "logo",
            "login_logo",
            "receipt_logo",
            "favicon",
            "primary_color",
            "secondary_color",
            "accent_color",
            "sidebar_color",
            "theme",
            "footer_text",
            "copyright_text",
        ]

        widgets = {

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "login_logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "receipt_logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "favicon": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "primary_color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "color",
                }
            ),

            "secondary_color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "color",
                }
            ),

            "accent_color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "color",
                }
            ),

            "sidebar_color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "color",
                }
            ),

            "theme": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "footer_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter footer text",
                }
            ),

            "copyright_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "© 2026 CampusPay. All rights reserved.",
                }
            ),

        }
        
        
    
    
# =====================================================
# ACADEMIC DEFAULTS FORM
# =====================================================


class AcademicDefaultsForm(forms.ModelForm):
    """
    Controls default academic configuration.
    """

    class Meta:

        model = AcademicDefaults


        fields = [
            "academic_year",
            "semester",
            "auto_select_active",
            "allow_payment_without_defaults",
        ]



        widgets = {


            "academic_year": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),



            "semester": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),



            "auto_select_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "allow_payment_without_defaults": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }        
        


# =====================================================
# RECEIPT SETTINGS FORM
# =====================================================

class ReceiptSettingsForm(forms.ModelForm):

    class Meta:

        model = ReceiptSettings

        fields = [
            "receipt_prefix",
            "starting_number",
            "include_logo",
            "include_signature",
            "signature_name",
            "signature_position",
            "footer_message",
            "show_phone",
            "show_email",
        ]


        widgets = {

            "receipt_prefix": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),


            "starting_number": forms.NumberInput(
                attrs={
                    "class":"form-control"
                }
            ),


            "signature_name": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),


            "signature_position": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),


            "footer_message": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":4
                }
            ),

        }        
        


# =====================================================
# PAYMENT SETTINGS FORM
# =====================================================

class PaymentSettingsForm(forms.ModelForm):
    """
    Form for managing CampusPay payment configuration.
    """

    class Meta:

        model = PaymentSettings

        fields = [

            # Payment Rules
            "allow_partial_payment",
            "prevent_overpayment",
            "require_reference",
            "minimum_payment_amount",

            # Payment Methods
            "allow_cash",
            "allow_mobile_money",
            "allow_bank_transfer",
            "allow_card_payment",

            # Receipt Behaviour
            "auto_generate_receipt",
            "require_payment_approval",

            # Currency
            "currency",
            "currency_symbol",

            # Reference System
            "reference_prefix",
            "auto_generate_reference",
            "reference_length",
            "prevent_duplicate_reference",

            # Editing Rules
            "allow_edit_after_payment",

            # Late Payment
            "allow_late_payment",
            "enable_late_fee",
            "grace_period_days",

            # Student Portal
            "allow_student_online_payment",
            "allow_student_receipt_download",
        ]


        widgets = {


            # =========================
            # Payment Rules
            # =========================

            "allow_partial_payment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "prevent_overpayment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "require_reference": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "minimum_payment_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),



            # =========================
            # Payment Methods
            # =========================

            "allow_cash": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "allow_mobile_money": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "allow_bank_transfer": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "allow_card_payment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            # =========================
            # Receipt
            # =========================

            "auto_generate_receipt": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "require_payment_approval": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            # =========================
            # Currency
            # =========================

            "currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "GHS",
                }
            ),


            "currency_symbol": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "₵",
                }
            ),



            # =========================
            # Reference System
            # =========================

            "reference_prefix": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CP",
                }
            ),


            "auto_generate_reference": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "reference_length": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),


            "prevent_duplicate_reference": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            # =========================
            # Editing
            # =========================

            "allow_edit_after_payment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            # =========================
            # Late Payment
            # =========================

            "allow_late_payment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "enable_late_fee": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "grace_period_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),



            # =========================
            # Student Portal
            # =========================

            "allow_student_online_payment": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "allow_student_receipt_download": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }
        




class EmailConfigurationForm(forms.ModelForm):
    """
    Form for managing CampusPay email server configuration.
    """

    class Meta:

        model = EmailConfiguration

        fields = [
            "email_host",
            "email_port",
            "email_username",
            "email_password",
            "encryption",
            "default_sender_email",
            "is_active",
        ]


        widgets = {


            "email_host": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "smtp.gmail.com",
                }
            ),


            "email_port": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "587",
                }
            ),


            "email_password": forms.PasswordInput(
                attrs={
                  "class": "form-control",
                  "placeholder": "Leave blank to keep current password"
                }
            ),


            "email_password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email password",
                }
            ),


            "encryption": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),


            "default_sender_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "noreply@campuspay.com",
                }
            ),


            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


        }
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)

       if self.instance and self.instance.pk:
        self.fields["email_password"].required = False
        
    
    def clean_email_password(self):

       password = self.cleaned_data.get(
        "email_password"
    )

       if not password and self.instance.pk:
           return self.instance.email_password

       return password
        


# =====================================================
# EMAIL TEMPLATE FORM
# =====================================================


class EmailTemplateForm(forms.ModelForm):
    """
    Form for managing CampusPay email templates.
    """

    class Meta:

        model = EmailTemplate

        fields = [
            "name",
            "slug",
            "description",
            "template_type",
            "subject",
            "body",
            "html_content",
            "is_active",
        ]


        widgets = {


            "name": forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Template name"
                }
            ),



            "slug": forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"payment_confirmation"
                }
            ),



            "description": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":3,
                }
            ),



            "template_type": forms.Select(
                attrs={
                    "class":"form-select",
                }
            ),



            "subject": forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Email subject"
                }
            ),



            "body": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":8,
                    "placeholder":
                    "Plain text email content"
                }
            ),



            "html_content": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows":12,
                    "placeholder":
                    "HTML email content"
                }
            ),



            "is_active": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input"
                }
            ),

        }
        
        
# =====================================================
# EMAIL TEMPLATE TEST FORM
# =====================================================

class EmailTemplateTestForm(forms.Form):
    """
    Form used to send a test email from an active
    CampusPay email template.
    """

    recipient = forms.EmailField(
        label="Recipient Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@email.com",
            }
        ),
    )        



        

# =====================================================
# USER MANAGEMENT SETTINGS FORM
# =====================================================


class UserManagementSettingsForm(forms.ModelForm):
    """
    Form for managing user management preferences.
    """


    class Meta:

        model = UserManagementSettings


        fields = [
            "allow_registration",
            "require_email_verification",
            "max_login_attempts",
            "session_timeout",
            "allow_profile_update",
        ]


        widgets = {


            "allow_registration": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "require_email_verification": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "max_login_attempts": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),


            "session_timeout": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 5,
                }
            ),


            "allow_profile_update": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }        
        
        
# =====================================================
# SYSTEM ROLES & PERMISSIONS FORM
# =====================================================

class SystemRoleForm(forms.ModelForm):

    """
    Form for managing CampusPay administrator roles
    and access permissions.
    """


    class Meta:

        model = SystemRole


        fields = [

            "role_name",

            "can_manage_users",

            "can_manage_finance",

            "can_manage_members",

            "can_manage_reports",

            "can_access_settings",

            "is_active",

        ]



        widgets = {


            "role_name": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),



            "can_manage_users": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "can_manage_finance": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "can_manage_members": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "can_manage_reports": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "can_access_settings": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }           
        
     
     


# =====================================================
# NOTIFICATION SETTINGS FORM
# =====================================================


class NotificationSettingsForm(forms.ModelForm):

    """
    Form for managing CampusPay notification preferences.
    """


    class Meta:

        model = NotificationSettings


        fields = [

            "payment_notifications",

            "receipt_notifications",

            "email_notifications",

            "system_alerts",

            "announcement_notifications",

            "is_active",

        ]


        widgets = {


            "payment_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "receipt_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "email_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "system_alerts": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "announcement_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),


            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }  
        
        
        
# =====================================================
# SECURITY SETTINGS FORM
# =====================================================


class SecuritySettingsForm(forms.ModelForm):

    """
    Form for managing CampusPay security policies.
    """


    class Meta:

        model = SecuritySettings


        fields = [

            "minimum_password_length",

            "require_uppercase",

            "require_numbers",

            "require_special_characters",

            "enable_login_attempt_limit",

            "max_login_attempts",

            "session_timeout_minutes",

            "enable_two_factor",

            "is_active",

        ]



        widgets = {


            "minimum_password_length": forms.NumberInput(
                attrs={
                    "class":"form-control",
                }
            ),


            "max_login_attempts": forms.NumberInput(
                attrs={
                    "class":"form-control",
                }
            ),


            "session_timeout_minutes": forms.NumberInput(
                attrs={
                    "class":"form-control",
                }
            ),


            "require_uppercase": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                }
            ),


            "require_numbers": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                }
            ),


            "require_special_characters": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                }
            ),


            "enable_login_attempt_limit": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                }
            ),


            "enable_two_factor": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                }
            ),


            "is_active": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                }
            ),

        }
        
        
# =====================================================
# BACKUP & RESTORE SETTINGS FORM
# =====================================================


class BackupRestoreSettingsForm(forms.ModelForm):

    """
    Form for managing CampusPay backup configuration.
    """


    class Meta:

        model = BackupRestoreSettings


        fields = [

            "automatic_backup",

            "backup_frequency",

            "storage_location",

            "backup_status",

            "is_active",

        ]



        widgets = {


            "automatic_backup": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),



            "backup_frequency": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),



            "storage_location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Local Server",
                }
            ),



            "backup_status": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Active",
                }
            ),



            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        } 
 
        
        

# =====================================================
# AUDIT LOG FILTER FORM
# =====================================================

class AuditLogFilterForm(forms.Form):

    action = forms.ChoiceField(
        choices=[("", "All Actions")] + AuditLog.ACTION_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
    )
    
    
    
    
    
class GeneralConfigurationForm(forms.ModelForm):

    class Meta:

        model = GeneralConfiguration

        fields = "__all__"

        widgets = {

            "maintenance_message": forms.Textarea(
                attrs={"rows":4}
            ),

        }    