from finance.models import Payment, FeeStructure
from finance.balances import BalanceService

from .models import PasswordResetAudit


class StudentPortalService:
    """
    Handles student dashboard data.
    """


    @staticmethod
    def get_student_dashboard(member):


        payments = (
            Payment.objects
            .filter(
                member=member
            )
            .select_related(
                "fee_structure",
                "receipt",
            )
            .order_by(
                "-payment_date"
            )
        )


        latest_payment = (
            payments.first()
        )


        total_paid = sum(
            payment.amount_paid
            for payment in payments
        )


        fee_structure = (
            FeeStructure.objects
            .filter(
                department=member.department,
                level=member.level,
                semester__is_active=True,
            )
            .first()
        )


        if fee_structure:


            total_fee = (
                BalanceService.total_fee(
                    fee_structure
                )
            )


            outstanding = (
                total_fee - total_paid
            )


            if total_paid == 0:

                status = "UNPAID"

            elif outstanding > 0:

                status = "PARTIAL"

            else:

                status = "PAID"



        else:

            total_fee = 0

            outstanding = 0

            status = "NO FEE"



        return {

            "total_fee":
                total_fee,


            "total_paid":
                total_paid,


            "outstanding":
                outstanding,


            "status":
                status,


            "payments":
                payments,


            "latest_payment":
                latest_payment,

        }


class AuditService:


    @staticmethod
    def log(
        *,
        user,
        action,
        description="",
        request=None,
    ):

        ip_address = None


        if request:

            ip_address = (
                request.META.get(
                    "REMOTE_ADDR"
                )
            )


        PasswordResetAudit.objects.create(

            user=user,

            action=action,

            description=description,

            ip_address=ip_address,

        )        
        