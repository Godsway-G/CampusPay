from decimal import Decimal

from django.core.cache import cache
from django.db.models import Sum
from django.utils import timezone

from finance.models import (
    Payment,
    Receipt,
    FeeStructure,
)

from members.models import Member



class DashboardService:
    """
    Handles dashboard statistics and calculations.
    """



    @staticmethod
    def get_greeting():

        hour = timezone.localtime().hour


        if hour < 12:
            return "Good Morning"


        elif hour < 17:
            return "Good Afternoon"


        return "Good Evening"





    @staticmethod
    def get_total_members():

        return Member.objects.count()





    @staticmethod
    def get_total_payments():

        return (
            Payment.objects.aggregate(
                total=Sum("amount_paid")
            )["total"]
            or Decimal("0.00")
        )





    @staticmethod
    def get_total_receipts():

        return Receipt.objects.count()





    @staticmethod
    def get_outstanding_balance():
        """
        Calculates real outstanding balance.

        Logic:

        Member
            ↓
        Matching FeeStructure
            ↓
        Minus Payments

        Returns total unpaid balance.
        """

        active_members = (
            Member.objects
            .select_related(
                "department"
            )
        )


        total_outstanding = Decimal("0.00")



        for member in active_members:


            fee_structure = (
                FeeStructure.objects
                .filter(
                    department=member.department,
                    level=member.level,
                    semester__is_active=True,
                )
                .first()
            )


            if not fee_structure:
                continue



            amount_paid = (
                Payment.objects
                .filter(
                    member=member,
                    fee_structure=fee_structure,
                )
                .aggregate(
                    total=Sum("amount_paid")
                )
                ["total"]
                or Decimal("0.00")
            )



            balance = (
                fee_structure.amount
                -
                amount_paid
            )



            if balance > 0:

                total_outstanding += balance



        return total_outstanding





    @staticmethod
    def get_recent_activities():

        return (
            Payment.objects
            .select_related(
                "member",
                "recorded_by",
                "fee_structure",
            )
            .order_by(
                "-payment_date"
            )[:10]
        )





    @staticmethod
    def get_dashboard_statistics():

        cache_key = "dashboard_statistics"



        statistics = cache.get(
            cache_key
        )



        if statistics:

            return statistics




        statistics = {

            "total_members":
                DashboardService.get_total_members(),


            "total_payments":
                DashboardService.get_total_payments(),


            "total_receipts":
                DashboardService.get_total_receipts(),


            "outstanding_balance":
                DashboardService.get_outstanding_balance(),


            "recent_activities":
                DashboardService.get_recent_activities(),

        }




        cache.set(

            cache_key,

            statistics,

            timeout=300

        )



        return statistics