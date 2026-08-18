from django.db import models
from django.conf import settings

# =====================================================
# ASSOCIATION SETTINGS
# =====================================================

class AssociationSettings(models.Model):
    """
    Stores the main association information used
    throughout CampusPay Enterprise.

    Only one record should exist.
    """

    association_name = models.CharField(
        max_length=200,
        verbose_name="Association Name",
    )

    association_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Association Code",
    )

    institution_name = models.CharField(
        max_length=200,
        verbose_name="Institution Name",
    )

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
    )

    website = models.URLField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    region = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="Ghana",
    )

    postal_address = models.CharField(
        max_length=150,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    motto = models.CharField(
        max_length=255,
        blank=True,
    )

    office_hours = models.CharField(
        max_length=150,
        blank=True,
    )

    facebook = models.URLField(
        blank=True,
    )

    x = models.URLField(
        blank=True,
        verbose_name="X (Twitter)",
    )

    instagram = models.URLField(
        blank=True,
    )

    linkedin = models.URLField(
        blank=True,
    )

    established_date = models.DateField(
        null=True,
        blank=True,
    )
    
    
    logo = models.ImageField(
    upload_to="associations/logos/",
    blank=True,
    null=True,
    )
    
    
    show_logo_on_receipts = models.BooleanField(
    default=True,
    )
    
    short_name = models.CharField(
    max_length=50,
    blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "Association Settings"

        verbose_name_plural = "Association Settings"

        ordering = ["association_name"]

    def __str__(self):

        return self.association_name


# =====================================================
# BRANDING SETTINGS
# =====================================================

class BrandingSettings(models.Model):
    """
    Stores CampusPay branding configuration.

    Only one record should exist.
    """

    logo = models.ImageField(
        upload_to="branding/logo/",
        blank=True,
        null=True,
    )

    favicon = models.ImageField(
        upload_to="branding/favicon/",
        blank=True,
        null=True,
    )

    login_logo = models.ImageField(
        upload_to="branding/login/",
        blank=True,
        null=True,
    )

    receipt_logo = models.ImageField(
        upload_to="branding/receipt/",
        blank=True,
        null=True,
    )

    primary_color = models.CharField(
        max_length=20,
        default="#0d6efd",
    )

    secondary_color = models.CharField(
        max_length=20,
        default="#6c757d",
    )

    accent_color = models.CharField(
        max_length=20,
        default="#198754",
    )

    sidebar_color = models.CharField(
        max_length=20,
        default="#1f2937",
    )

    theme = models.CharField(
        max_length=20,
        choices=[
            ("light", "Light"),
            ("dark", "Dark"),
            ("system", "System"),
        ],
        default="light",
    )

    footer_text = models.CharField(
        max_length=255,
        blank=True,
    )

    copyright_text = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Branding Settings"
        verbose_name_plural = "Branding Settings"

    def __str__(self):
        return "CampusPay Branding"
    
    
    
# =====================================================
# ACADEMIC DEFAULT SETTINGS
# =====================================================


class AcademicDefaults(models.Model):
    """
    Controls default academic settings across CampusPay.
    """

    academic_year = models.ForeignKey(
        "finance.AcademicYear",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_settings",
    )


    semester = models.ForeignKey(
        "finance.Semester",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="default_settings",
    )


    auto_select_active = models.BooleanField(
        default=True,
        verbose_name="Automatically use active semester",
    )


    allow_payment_without_defaults = models.BooleanField(
        default=False,
        verbose_name="Allow payments without academic defaults",
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )



    class Meta:

        verbose_name = "Academic Defaults"

        verbose_name_plural = "Academic Defaults"



    def save(self, *args, **kwargs):

        """
        Ensure only one academic default configuration exists.
        """

        self.pk = 1

        super().save(*args, **kwargs)



    def __str__(self):

        return "Academic Defaults"
    
    
# =====================================================
# RECEIPT SETTINGS
# =====================================================

class ReceiptSettings(models.Model):
    """
    Controls receipt generation and appearance.
    """

    receipt_prefix = models.CharField(
        max_length=20,
        default="CP",
        help_text="Example: CP-00001"
    )


    starting_number = models.PositiveIntegerField(
        default=1
    )


    include_logo = models.BooleanField(
        default=True
    )


    include_signature = models.BooleanField(
        default=False
    )


    signature_name = models.CharField(
        max_length=100,
        blank=True
    )


    signature_position = models.CharField(
        max_length=100,
        blank=True
    )


    footer_message = models.TextField(
        blank=True,
        default="Thank you for your payment."
    )


    show_phone = models.BooleanField(
        default=True
    )


    show_email = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name = "Receipt Settings"

        verbose_name_plural = "Receipt Settings"



    def __str__(self):

        return "Receipt Configuration"  
    
    
# =====================================================
# PAYMENT SETTINGS
# =====================================================

class PaymentSettings(models.Model):
    """
    Controls global payment behaviour in CampusPay.
    """

    # ==============================
    # Payment Rules
    # ==============================

    allow_partial_payment = models.BooleanField(
        default=True
    )


    prevent_overpayment = models.BooleanField(
        default=True
    )


    require_reference = models.BooleanField(
        default=True
    )


    minimum_payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    # ==============================
    # Payment Methods
    # ==============================

    allow_cash = models.BooleanField(
        default=True
    )


    allow_mobile_money = models.BooleanField(
        default=True
    )


    allow_bank_transfer = models.BooleanField(
        default=True
    )


    allow_card_payment = models.BooleanField(
        default=False
    )


    # ==============================
    # Receipt Behaviour
    # ==============================

    auto_generate_receipt = models.BooleanField(
        default=True
    )


    require_payment_approval = models.BooleanField(
        default=False
    )


    # ==============================
    # Currency
    # ==============================

    currency = models.CharField(
        max_length=10,
        default="GHS"
    )


    currency_symbol = models.CharField(
        max_length=5,
        default="₵"
    )


    # ==============================
    # Payment Reference System
    # ==============================

    reference_prefix = models.CharField(
        max_length=20,
        default="CP"
    )


    auto_generate_reference = models.BooleanField(
        default=True
    )


    reference_length = models.PositiveIntegerField(
        default=6
    )


    prevent_duplicate_reference = models.BooleanField(
        default=True
    )


    # ==============================
    # Editing Rules
    # ==============================

    allow_edit_after_payment = models.BooleanField(
        default=False
    )


    # ==============================
    # Late Payment
    # ==============================

    allow_late_payment = models.BooleanField(
        default=True
    )


    enable_late_fee = models.BooleanField(
        default=False
    )


    grace_period_days = models.PositiveIntegerField(
        default=0
    )


    # ==============================
    # Student Portal Ready
    # ==============================

    allow_student_online_payment = models.BooleanField(
        default=True
    )


    allow_student_receipt_download = models.BooleanField(
        default=True
    )


    # ==============================
    # Audit
    # ==============================

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name = "Payment Settings"

        verbose_name_plural = "Payment Settings"



    def __str__(self):

        return "Payment Configuration"
    
    # ===============================================
# EMAIL CONFIGURATION
# ===============================================

class EmailConfiguration(models.Model):
    """
    Controls CampusPay email delivery configuration.
    Supports Brevo API and SMTP.
    """


    PROVIDER_CHOICES = [

        ("brevo", "Brevo API"),

        ("smtp", "SMTP"),

    ]


    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES,
        default="brevo",
        verbose_name="Email Provider"
    )


    # ==========================================
    # BREVO API CONFIGURATION
    # ==========================================

    brevo_api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Brevo API Key"
    )


    # ==========================================
    # SMTP CONFIGURATION
    # ==========================================


    email_host = models.CharField(
        max_length=255,
        default="smtp.gmail.com",
        blank=True
    )


    email_port = models.PositiveIntegerField(
        default=587,
        blank=True
    )


    email_username = models.EmailField(
        blank=True
    )


    email_password = models.CharField(
        max_length=255,
        blank=True
    )


    encryption = models.CharField(
        max_length=20,
        choices=[
            ("TLS", "TLS"),
            ("SSL", "SSL"),
            ("NONE", "None"),
        ],
        default="TLS",
        blank=True
    )


    # ==========================================
    # SENDER INFORMATION
    # ==========================================


    sender_name = models.CharField(
        max_length=100,
        default="CampusPay"
    )


    default_sender_email = models.EmailField(
        blank=True
    )


    is_active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name = "Email Configuration"

        verbose_name_plural = "Email Configuration"



    def __str__(self):

        return "CampusPay Email Configuration"
    
    
 # =====================================================
# EMAIL TEMPLATES
# =====================================================


class EmailTemplate(models.Model):
    """
    Stores reusable CampusPay email templates.
    """


    TEMPLATE_TYPES = [

        ("payment_confirmation", "Payment Confirmation"),

        ("receipt_notification", "Receipt Notification"),

        ("password_reset", "Password Reset"),

        ("account_creation", "Account Creation"),

        ("system_alert", "System Alert"),

        ("announcement", "Announcement"),

    ]


    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Template Name",
    )


    slug = models.SlugField(
        max_length=150,
        unique=True,
        help_text="Unique identifier used by the system",
    )


    description = models.TextField(
        blank=True,
        help_text="Explain when this template is used",
    )


    template_type = models.CharField(
        max_length=50,
        choices=TEMPLATE_TYPES,
        default="system_alert",
    )


    subject = models.CharField(
        max_length=255,
    )


    body = models.TextField(
        blank=True,
        help_text="Plain text email content",
    )


    html_content = models.TextField(
        blank=True,
        help_text="HTML email content",
    )


    is_active = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:

        verbose_name = "Email Template"

        verbose_name_plural = "Email Templates"

        ordering = [
            "name"
        ]


    def __str__(self):

        return f"{self.name} ({self.template_type})"
    
    
    
    
    
# =====================================================
# USER MANAGEMENT SETTINGS
# =====================================================


class UserManagementSettings(models.Model):
    """
    Controls user management preferences.
    """

    allow_registration = models.BooleanField(
        default=False,
        verbose_name="Allow User Registration"
    )


    require_email_verification = models.BooleanField(
        default=True,
        verbose_name="Require Email Verification"
    )


    max_login_attempts = models.PositiveIntegerField(
        default=5,
        verbose_name="Maximum Login Attempts"
    )


    session_timeout = models.PositiveIntegerField(
        default=30,
        verbose_name="Session Timeout (minutes)"
    )


    allow_profile_update = models.BooleanField(
        default=True,
        verbose_name="Allow Profile Updates"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        verbose_name = "User Management Settings"

        verbose_name_plural = "User Management Settings"


    def __str__(self):

        return "User Management Configuration"  
              
              
              

# =====================================================
# SYSTEM ROLES & PERMISSIONS
# =====================================================


class SystemRole(models.Model):
    """
    Defines roles and permissions for CampusPay
    administrators and staff users.
    """

    ROLE_CHOICES = [

        ("super_admin", "Super Administrator"),

        ("admin", "Administrator"),

        ("finance", "Finance Officer"),

        ("staff", "Staff Member"),

    ]


    role_name = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        unique=True,
    )


    can_manage_users = models.BooleanField(
        default=False,
    )


    can_manage_finance = models.BooleanField(
        default=False,
    )


    can_manage_members = models.BooleanField(
        default=False,
    )


    can_manage_reports = models.BooleanField(
        default=False,
    )


    can_access_settings = models.BooleanField(
        default=False,
    )


    is_active = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:

        verbose_name = "System Role"

        verbose_name_plural = "System Roles"

        ordering = [
            "role_name"
        ]


    def __str__(self):

        return self.get_role_name_display()
    
    
    
# =====================================================
# NOTIFICATION SETTINGS
# =====================================================


class NotificationSettings(models.Model):
    """
    Controls CampusPay system notification preferences.
    """


    payment_notifications = models.BooleanField(
        default=True,
    )


    receipt_notifications = models.BooleanField(
        default=True,
    )


    email_notifications = models.BooleanField(
        default=True,
    )


    system_alerts = models.BooleanField(
        default=True,
    )


    announcement_notifications = models.BooleanField(
        default=False,
    )


    is_active = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )



    class Meta:

        verbose_name = "Notification Setting"

        verbose_name_plural = "Notification Settings"



    def __str__(self):

        return "CampusPay Notification Settings"   
    
    
    
# =====================================================
# SECURITY SETTINGS
# =====================================================


class SecuritySettings(models.Model):
    """
    Controls CampusPay system security preferences.
    """


    minimum_password_length = models.PositiveIntegerField(
        default=8,
    )


    require_uppercase = models.BooleanField(
        default=True,
    )


    require_numbers = models.BooleanField(
        default=True,
    )


    require_special_characters = models.BooleanField(
        default=True,
    )


    enable_login_attempt_limit = models.BooleanField(
        default=True,
    )


    max_login_attempts = models.PositiveIntegerField(
        default=5,
    )


    session_timeout_minutes = models.PositiveIntegerField(
        default=30,
    )


    enable_two_factor = models.BooleanField(
        default=False,
    )


    is_active = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )


    class Meta:

        verbose_name = "Security Setting"

        verbose_name_plural = "Security Settings"



    def __str__(self):

        return "CampusPay Security Settings"     
    
    
# =====================================================
# BACKUP & RESTORE SETTINGS
# =====================================================


class BackupRestoreSettings(models.Model):
    """
    Controls CampusPay backup and restore configuration.
    """


    BACKUP_FREQUENCY_CHOICES = [

        ("daily", "Daily"),

        ("weekly", "Weekly"),

        ("monthly", "Monthly"),

        ("manual", "Manual Only"),

    ]


    automatic_backup = models.BooleanField(
        default=False,
        verbose_name="Enable Automatic Backup",
    )


    backup_frequency = models.CharField(
        max_length=20,
        choices=BACKUP_FREQUENCY_CHOICES,
        default="manual",
    )


    storage_location = models.CharField(
        max_length=255,
        default="Local Server",
    )


    last_backup_date = models.DateTimeField(
        null=True,
        blank=True,
    )


    backup_status = models.CharField(
        max_length=50,
        default="Not Configured",
    )


    is_active = models.BooleanField(
        default=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    updated_at = models.DateTimeField(
        auto_now=True,
    )



    class Meta:

        verbose_name = "Backup & Restore Setting"

        verbose_name_plural = "Backup & Restore Settings"



    def __str__(self):

        return "CampusPay Backup Configuration"    
  
  
  
# =====================================================
# AUDIT LOGS
# =====================================================


class AuditLog(models.Model):
    """
    Stores important system activities
    inside CampusPay.
    """


    ACTION_CHOICES = [

        ("LOGIN", "User Login"),

        ("LOGOUT", "User Logout"),

        ("CREATE", "Create"),

        ("UPDATE", "Update"),

        ("DELETE", "Delete"),

        ("PAYMENT", "Payment Activity"),

        ("RECEIPT", "Receipt Activity"),

        ("SETTINGS", "Settings Change"),

    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )


    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
    )


    model_name = models.CharField(
        max_length=100,
        blank=True,
    )


    object_id = models.CharField(
        max_length=100,
        blank=True,
    )


    description = models.TextField()


    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        verbose_name = "Audit Log"

        verbose_name_plural = "Audit Logs"

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return f"{self.action} - {self.user}"
    
    
    
    
# =====================================================
# GENERAL CONFIGURATION
# =====================================================

class GeneralConfiguration(models.Model):
    """
    Stores global CampusPay system configuration.
    Only one record should exist.
    """

    system_name = models.CharField(
        max_length=150,
        default="CampusPay Enterprise",
    )

    system_version = models.CharField(
        max_length=20,
        default="1.0.0",
    )

    timezone = models.CharField(
        max_length=100,
        default="Africa/Accra",
    )

    language = models.CharField(
        max_length=50,
        default="English",
    )

    date_format = models.CharField(
        max_length=30,
        default="d M Y",
    )

    maintenance_mode = models.BooleanField(
        default=False,
    )

    maintenance_message = models.TextField(
        blank=True,
        default="CampusPay is currently under maintenance.",
    )

    allow_debug_information = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "General Configuration"

        verbose_name_plural = "General Configuration"

    def __str__(self):

        return "General Configuration"    