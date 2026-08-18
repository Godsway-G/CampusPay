from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q
from django.utils import timezone

from core.mixins import LoginRequiredMixin

from finance.models import (
    Payment,
    Receipt,
)

from members.models import (
    Member,
    Department,
)
from reports.services import ReportService

from django.http import HttpResponse
from django.conf import settings
import os
from .pdf import generate_outstanding_report_pdf
from .excel import generate_outstanding_report_excel

# =====================================================
# REPORT DASHBOARD
# =====================================================

class ReportDashboardView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = (
        "reports/dashboard.html"
    )


    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )


        context["active_section"] = (
            "reports"
        )


        report = (
            ReportService.generate()
        )


        records = report["report"]



        context["paid_count"] = sum(
           1
           for item in records
           if item["status"] == "Paid"
        )


        context["partial_count"] = sum(
           1
           for item in records
           if item["status"] == "Partial"
        )


        context["outstanding_count"] = sum(
            1
            for item in records
            if item["status"] == "Outstanding"
        )



        departments = {}

        for item in records:

            dept = str(
    item["member"].department
)


        departments[dept] = (
            departments.get(
                dept,
                0
            )
            +
            float(
                item["paid"]
            )
        )


        context["department_names"] = list(
            departments.keys()
        )


        context["department_totals"] = list(
            departments.values()
        )


        return context

# =====================================================
# FINANCE REPORT
# =====================================================

class FinanceReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/finance_report.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        payments = Payment.objects.select_related(
            "member",
            "fee_structure",
        )

        context["payment_count"] = payments.count()

        context["total_revenue"] = (

            payments.aggregate(

                total=Sum("amount_paid")

            )["total"]

            or 0

        )

        today = timezone.now().date()

        context["today_collection"] = (

            payments.filter(

                payment_date=today

            ).aggregate(

                total=Sum("amount_paid")

            )["total"]

            or 0

        )

        context["receipt_count"] = Receipt.objects.count()

        context["recent_payments"] = (

            payments.order_by(

                "-payment_date"

            )[:10]

        )

        context["active_section"] = "reports"

        return context


# =====================================================
# MEMBER REPORT
# =====================================================

class MemberReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/member_report.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["active_section"] = "reports"

        return context


# =====================================================
# MEMBER DIRECTORY
# =====================================================

class MemberDirectoryReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/member_directory.html"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        members = (

            Member.objects

            .select_related(
                "department"
            )

            .order_by(
                "last_name",
                "first_name",
            )

        )


        context["members"] = members

        context["total_members"] = members.count()

        context["active_section"] = "reports"


        return context


# =====================================================
# DEPARTMENT SUMMARY
# =====================================================

class DepartmentSummaryReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/department_summary.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["departments"] = (

            Department.objects

            .annotate(

                total_members=Count("member")

            )

            .order_by("name")

        )

        context["active_section"] = "reports"

        return context


# =====================================================
# LEVEL SUMMARY
# =====================================================

class LevelSummaryReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/level_summary.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["levels"] = (

            Member.objects

            .values("level")

            .annotate(

                total=Count("id")

            )

            .order_by("level")

        )

        context["active_section"] = "reports"

        return context


# =====================================================
# MEMBER STATUS
# =====================================================

class MemberStatusReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/member_status.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["active"] = (

            Member.objects.filter(

                active=True

            )

        )

        context["inactive"] = (

            Member.objects.filter(

                active=False

            )

        )

        context["active_section"] = "reports"

        return context


# =====================================================
# OUTSTANDING FEES REPORT
# =====================================================

class OutstandingReportView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "reports/outstanding_report.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        search = self.request.GET.get("search")
        department = self.request.GET.get("department")
        level = self.request.GET.get("level")
        status = self.request.GET.get("status")

        report_data = ReportService.outstanding_report(
            search=search,
            department=department,
            level=level,
            status=status,
        )

        context.update(report_data)

        context["departments"] = Department.objects.all()
        context["levels"] = Member.LEVELS
        context["active_section"] = "reports"

        # -----------------------------
        # Chart Data
        # -----------------------------

        report = report_data["report"]

        context["paid_count"] = sum(
            1 for item in report if item["status"] == "Paid"
        )

        context["partial_count"] = sum(
            1 for item in report if item["status"] == "Partial"
        )

        context["outstanding_count"] = sum(
            1 for item in report if item["status"] == "Outstanding"
        )

        departments = {}

        for item in report:

            dept = str(item["member"].department)

            departments[dept] = (
                departments.get(dept, 0)
                + float(item["paid"])
            )

        context["department_names"] = list(departments.keys())
        context["department_totals"] = list(departments.values())

        return context
    
    
    
class OutstandingReportPDFView(
    LoginRequiredMixin,
    TemplateView
):

    def get(self, request):

        data = (
            ReportService.outstanding_report(

                search=request.GET.get("search"),
                department=request.GET.get("department"),
                level=request.GET.get("level"),
                status=request.GET.get("status"),
            )
        )


        filename = "outstanding_report.pdf"


        filepath = os.path.join(
            settings.BASE_DIR,
            filename
        )


        generate_outstanding_report_pdf(
            data,
            filepath
        )


        with open(filepath, "rb") as pdf:

            response = HttpResponse(
                pdf.read(),
                content_type="application/pdf"
            )


            response[
                "Content-Disposition"
            ] = (
                "attachment; "
                "filename=outstanding_report.pdf"
            )


            return response
        
        
        
class OutstandingReportExcelView(
    LoginRequiredMixin,
    TemplateView
):

    def get(
        self,
        request
    ):


        data = (
            ReportService.outstanding_report(


                search=request.GET.get(
                    "search"
                ),

                department=request.GET.get(
                    "department"
                ),

                level=request.GET.get(
                    "level"
                ),

                status=request.GET.get(
                    "status"
                ),

            )
        )


        filename = (
            "outstanding_report.xlsx"
        )


        filepath = os.path.join(
            settings.BASE_DIR,
            filename
        )


        generate_outstanding_report_excel(
            data,
            filepath
        )


        with open(
            filepath,
            "rb"
        ) as excel:


            response = HttpResponse(

                excel.read(),

                content_type=(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            )


            response[
                "Content-Disposition"
            ] = (
                "attachment;"
                " filename=outstanding_report.xlsx"
            )


            return response        