from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from administration.models import ReceiptSettings
from .utils import generate_reference


class AcademicYear(models.Model):
    """
    Represents an academic year.
    Example: 2025/2026
    """

    association = models.ForeignKey(
        "core.Association",
        on_delete=models.CASCADE,
        related_name="academic_years",
    )

    name = models.CharField(
    max_length=20,
    )
    

    is_current = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
      ordering = ["-name"]

      verbose_name = "Academic Year"

      verbose_name_plural = "Academic Years"

      constraints = [
        models.UniqueConstraint(
            fields=["association", "name"],
            name="unique_academic_year_per_association",
        )
        ]

    def __str__(self):
        return self.name


class Semester(models.Model):
    """
    Represents a semester within an academic year.
    """

    FIRST = "FIRST"
    SECOND = "SECOND"

    SEMESTER_CHOICES = [
        (FIRST, "First Semester"),
        (SECOND, "Second Semester"),
    ]

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name="semesters",
    )

    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES,
    )

    payment_deadline = models.DateField()

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
        ordering = ["academic_year", "semester"]
        constraints = [ 
           models.UniqueConstraint(
        fields=["academic_year", "semester"],
        name="unique_semester_per_academic_year",
        )
        ]
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def __str__(self):
        return f"{self.academic_year} - {self.get_semester_display()}"


class FeeStructure(models.Model):
    """
    Defines the amount a member should pay.
    """

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="fee_structures",
    )

    department = models.ForeignKey(
        "members.Department",
        on_delete=models.CASCADE,
        related_name="fee_structures",
    )

    LEVEL_CHOICES = [
        ("100", "Level 100"),
        ("200", "Level 200"),
        ("300", "Level 300"),
        ("400", "Level 400"),
    ]

    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "semester",
            "department",
            "level",
        ]
        constraints = [
           models.UniqueConstraint(
              fields=[
                 "semester",
                 "department",
                 "level",
                ],
              name="unique_fee_structure",
            )
        ]
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structures"

    def __str__(self):
        return (
            f"{self.department} | "
            f"{self.level} | "
            f"GH₵{self.amount}"
        )


class Payment(models.Model):
    """
    Records every payment made by a member.
    """

    CASH = "Cash"
    MOMO = "MoMo"
    BANK = "Bank"
    CARD = "Card"

    PAYMENT_METHODS = [
        (CASH, "Cash"),
        (MOMO, "Mobile Money"),
        (BANK, "Bank Transfer"),
        (CARD, "Card"),
    ]

    payment_id = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.PROTECT,
        related_name="payments",
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    payment_date = models.DateTimeField(
        default= timezone.now,
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recorded_payments",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-payment_date"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def clean(self):
       super().clean()

       if self.amount_paid is None:
          raise ValidationError({
            "amount_paid": "Please enter the payment amount."
        })

       if self.amount_paid <= Decimal("0.00"):
           raise ValidationError({
            "amount_paid": "Amount paid must be greater than zero."
        })

       if not self.fee_structure_id:
           raise ValidationError({
            "fee_structure": "Please select a fee structure."
        })

       if not self.fee_structure.semester.is_active:
           raise ValidationError(
            "Payments cannot be recorded for an inactive semester."
        )
     

    def save(self, *args, **kwargs):

    # Run model validation first
       self.full_clean()

       if not self.payment_id:
          self.payment_id = generate_reference(
            Payment,
            "payment_id",
            "PAY",
        )

       super().save(*args, **kwargs)

class Receipt(models.Model):
    """
    Receipt generated after a successful payment.
    """

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name="receipt",
    )

    generated_at = models.DateTimeField(
        auto_now_add=True,
    )

    printed = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ["-generated_at"]
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    def save(self, *args, **kwargs):

        if not self.receipt_number:

            settings = ReceiptSettings.objects.first()

            prefix = "RCP"

            if settings:
               prefix = settings.receipt_prefix

            self.receipt_number = generate_reference(
               Receipt,
               "receipt_number",
               prefix,
            )

        super().save(*args, **kwargs)