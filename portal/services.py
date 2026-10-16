from finance.models import Payment, FeeStructure
from finance.balances import BalanceService

from .models import PasswordResetAudit


class StudentPortalService:
    """
    Handles student portal dashboard data.

    The portal does not perform its own financial calculations.
    It reuses the existing Finance and Balance services.
    """

    @staticmethod
    def get_student_dashboard(member):

        # --------------------------------------------------
        # CURRENT FEE STRUCTURE
        # --------------------------------------------------

        fee_structure = (
            FeeStructure.objects
            .select_related(
                "semester",
                "semester__academic_year",
                "department",
            )
            .filter(
                department=member.department,
                level=member.level,
                semester__is_active=True,
                semester__academic_year__is_current=True,
            )
            .first()
        )

        # --------------------------------------------------
        # NO CURRENT FEE
        # --------------------------------------------------

        if not fee_structure:

            return {
                "current_academic_year": None,
                "current_semester": None,
                "fee_structure": None,
                "total_fee": 0,
                "total_paid": 0,
                "outstanding": 0,
                "status": "NO FEE",
                "payments": Payment.objects.none(),
                "latest_payment": None,
            }

        # --------------------------------------------------
        # CURRENT ACADEMIC PERIOD
        # --------------------------------------------------

        semester = fee_structure.semester
        academic_year = semester.academic_year

        # --------------------------------------------------
        # CURRENT PAYMENTS
        # --------------------------------------------------

        payments = (
            Payment.objects
            .filter(
                member=member,
                fee_structure=fee_structure,
            )
            .select_related(
                "fee_structure",
                "fee_structure__semester",
                "fee_structure__semester__academic_year",
                "receipt",
            )
            .order_by(
                "-payment_date"
            )
        )

        latest_payment = payments.first()

        # --------------------------------------------------
        # FINANCIAL CALCULATIONS
        # --------------------------------------------------

        total_fee = (
            BalanceService.total_fee(
                fee_structure
            )
        )

        total_paid = (
            BalanceService.total_paid(
                member,
                fee_structure,
            )
        )

        outstanding = (
            BalanceService.outstanding_balance(
                member,
                fee_structure,
            )
        )

        status = (
            BalanceService.payment_status(
                member,
                fee_structure,
            )
        )

        # --------------------------------------------------
        # RETURN DASHBOARD DATA
        # --------------------------------------------------

        return {
            "current_academic_year": academic_year,
            "current_semester": semester,
            "fee_structure": fee_structure,
            "total_fee": total_fee,
            "total_paid": total_paid,
            "outstanding": outstanding,
            "status": status,
            "payments": payments,
            "latest_payment": latest_payment,
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
            ip_address = request.META.get(
                "REMOTE_ADDR"
            )

        PasswordResetAudit.objects.create(
            user=user,
            action=action,
            description=description,
            ip_address=ip_address,
        )