from decimal import Decimal

from django.db.models import Sum, Q

from members.models import (
    Member,
)

from finance.models import (
    Payment,
    FeeStructure,
    Semester,
)


class ReportService:


    @staticmethod
    def generate():

        data = ReportService.outstanding_report()


        return {

            "report": data["report"],

            "total_expected":
                data["total_expected"],

            "total_paid":
                data["total_paid"],

            "total_outstanding":
                data["total_outstanding"],

        }
    
    @staticmethod
    def outstanding_report(
        search=None,
        department=None,
        level=None,
        status=None,
    ):

        report = []

        total_expected = Decimal("0.00")
        total_paid = Decimal("0.00")
        total_outstanding = Decimal("0.00")

        #
        # Active Semester
        #

        active_semester = Semester.objects.filter(
            is_active=True
        ).first()

        if active_semester is None:

            return {
                "report": [],
                "total_expected": Decimal("0.00"),
                "total_paid": Decimal("0.00"),
                "total_outstanding": Decimal("0.00"),
                "active_semester": None,
            }

        #
        # Members
        #

        members = Member.objects.select_related(
            "department"
        )

        #
        # Search
        #

        if search:

            members = members.filter(

                Q(student_id__icontains=search)

                |

                Q(first_name__icontains=search)

                |

                Q(last_name__icontains=search)

                |

                Q(email__icontains=search)

            )

        #
        # Department Filter
        #

        if department:

            members = members.filter(
                department_id=department
            )

        #
        # Level Filter
        #

        if level:

            members = members.filter(
                level=level
            )

        #
        # Build Report
        #

        for member in members:

            fee_structure = FeeStructure.objects.filter(

                semester=active_semester,

                level=member.level,

            ).first()

            #
            # Expected Fee
            #

            expected = (

                fee_structure.amount

                if fee_structure

                else Decimal("0.00")

            )

            #
            # Amount Paid
            #

            if fee_structure:

                paid = (

                    Payment.objects.filter(

                        member=member,

                        fee_structure=fee_structure,

                    ).aggregate(

                        total=Sum("amount_paid")

                    )["total"]

                    or Decimal("0.00")

                )

            else:

                paid = Decimal("0.00")

            #
            # Balance
            #

            balance = expected - paid

            if balance < Decimal("0.00"):

                balance = Decimal("0.00")

            #
            # Status
            #

            if balance == Decimal("0.00"):

                payment_status = "Paid"

            elif paid > Decimal("0.00"):

                payment_status = "Partial"

            else:

                payment_status = "Outstanding"

            #
            # Status Filter
            #

            if status:

                if payment_status != status:

                    continue

            #
            # Totals
            #

            total_expected += expected

            total_paid += paid

            total_outstanding += balance

            #
            # Row
            #

            report.append({

                "member": member,

                "semester": active_semester,

                "expected": expected,

                "paid": paid,

                "balance": balance,

                "status": payment_status,

            })

        return {

            "report": report,

            "total_expected": total_expected,

            "total_paid": total_paid,

            "total_outstanding": total_outstanding,

            "active_semester": active_semester,

        }