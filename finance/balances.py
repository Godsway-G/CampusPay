from decimal import Decimal

from django.db.models import Sum

from .models import Payment


class BalanceService:
    """
    Handles payment balance calculations.
    """

    @staticmethod
    def total_fee(fee_structure):
        """
        Returns the total amount required.
        """

        return fee_structure.amount


    @staticmethod
    def total_paid(member, fee_structure):
        """
        Calculates all payments made
        by a member for a fee.
        """

        amount = (
            Payment.objects.filter(
                member=member,
                fee_structure=fee_structure,
            )
            .aggregate(
                total=Sum("amount_paid")
            )
            ["total"]
        )

        return amount or Decimal("0.00")


    @classmethod
    def outstanding_balance(
        cls,
        member,
        fee_structure,
    ):
        """
        Calculates remaining amount.
        """

        balance = (
            cls.total_fee(fee_structure)
            -
            cls.total_paid(
                member,
                fee_structure,
            )
        )

        return max(
            balance,
            Decimal("0.00")
        )


    @classmethod
    def payment_status(
        cls,
        member,
        fee_structure,
    ):
        """
        Returns payment state.
        """

        outstanding = cls.outstanding_balance(
            member,
            fee_structure,
        )

        if outstanding == 0:

            return "PAID"

        elif cls.total_paid(
            member,
            fee_structure,
        ) > 0:

            return "PARTIAL"

        return "UNPAID"