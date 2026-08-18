from django.db import transaction
from django.core.cache import cache

from .models import Payment, Receipt
from .balances import BalanceService
from .utils import generate_reference

from administration.models import (
    PaymentSettings,
    ReceiptSettings,
)


class PaymentService:
    """
    Handles payment processing and validation.
    """


    @staticmethod
    def get_payment_settings():
        """
        Returns system payment settings.
        Creates default settings if none exist.
        """

        settings = PaymentSettings.objects.first()

        if settings is None:
            settings = PaymentSettings.objects.create()

        return settings



    @staticmethod
    def can_accept_payment(
        member,
        fee_structure,
        amount_paid,
    ):
        """
        Validates whether a payment can be accepted.
        """

        settings = PaymentService.get_payment_settings()


        # ----------------------------------
        # Validate amount
        # ----------------------------------

        if amount_paid <= 0:

            raise ValueError(
                "Payment amount must be greater than zero."
            )


        # ----------------------------------
        # Minimum payment rule
        # ----------------------------------

        if amount_paid < settings.minimum_payment_amount:

            raise ValueError(
                f"Minimum payment allowed is "
                f"{settings.currency_symbol}"
                f"{settings.minimum_payment_amount}"
            )


        # ----------------------------------
        # Active semester validation
        # ----------------------------------

        if not fee_structure.semester.is_active:

            raise ValueError(
                "Cannot pay for an inactive semester."
            )


        # ----------------------------------
        # Outstanding balance validation
        # ----------------------------------

        outstanding = (
            BalanceService.outstanding_balance(
                member,
                fee_structure,
            )
        )


        if (
            settings.prevent_overpayment
            and amount_paid > outstanding
        ):

            raise ValueError(
                f"Payment exceeds outstanding balance. "
                f"Remaining amount is "
                f"{settings.currency_symbol}"
                f"{outstanding}"
            )


        return True



    @staticmethod
    @transaction.atomic
    def record_payment(
        *,
        member,
        fee_structure,
        amount_paid,
        payment_method,
        transaction_reference,
        payment_date,
        recorded_by,
        remarks="",
    ):
        """
        Creates payment and generates receipt.
        """


        payment = Payment.objects.create(

            member=member,

            fee_structure=fee_structure,

            amount_paid=amount_paid,

            payment_method=payment_method,

            transaction_reference=transaction_reference,

            payment_date=payment_date,

            recorded_by=recorded_by,

            remarks=remarks,
        )


        receipt = Receipt.objects.create(
            payment=payment
        )


        # Clear dashboard cache
        cache.delete(
            "dashboard_statistics"
        )


        return payment, receipt



    @staticmethod
    def get_receipt_settings():
        """
        Returns receipt configuration.
        Creates default settings if missing.
        """

        settings = ReceiptSettings.objects.first()


        if settings is None:

            settings = ReceiptSettings.objects.create()


        return settings