from django.contrib import messages
from core.mixins import AdminRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from administration.models import ReceiptSettings
from .balances import BalanceService
from .forms import (
    AcademicYearForm,
    FeeStructureForm,
    PaymentForm,
    SemesterForm,
)
from .models import (
    AcademicYear,
    FeeStructure,
    Payment,
    Receipt,
    Semester,
)
from .services import PaymentService
from members.models import Member
from administration.services.academic_defaults import AcademicConfigurationService
from django.core.cache import cache
from .pdf import generate_receipt_pdf
from django.shortcuts import get_object_or_404 

# =====================================================
# Dashboard
# =====================================================

class FinanceDashboardView(AdminRequiredMixin, TemplateView):
    """
    Finance dashboard showing summary statistics.
    """

    template_name = "finance/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        payments = Payment.objects.select_related("member", "fee_structure")

        # Basic Stats
        total_payments = payments.count()
        total_amount = payments.aggregate(total=Sum("amount_paid"))["total"] or 0
        receipt_count = Receipt.objects.count()
        
        active_semester = (
            AcademicConfigurationService
            .get_active_semester()
)
        recent_payments = payments.order_by("-payment_date")[:5]

        # Collection & Method Stats
        today_collection = payments.filter(payment_date__date=today).aggregate(
            total=Sum("amount_paid")
        )["total"] or 0

        cash_payments = payments.filter(payment_method="Cash").count()
        momo_payments = payments.filter(payment_method="MoMo").count()
        bank_payments = payments.filter(payment_method="Bank").count()

        context.update({
            "page_title": "Finance Dashboard",
            "total_payments": total_payments,
            "total_amount": total_amount,
            "receipt_count": receipt_count,
            "active_semester": active_semester,
            "recent_payments": recent_payments,
            "today_collection": today_collection,
            "cash_payments": cash_payments,
            "momo_payments": momo_payments,
            "bank_payments": bank_payments,
        })
        
        return context


# =====================================================
# Academic Year CRUD
# =====================================================

class AcademicYearListView(AdminRequiredMixin, ListView):
    model = AcademicYear
    template_name = "finance/academic_year_list.html"
    context_object_name = "object_list"
    paginate_by = 10

    def get_queryset(self):
        queryset = AcademicYear.objects.select_related("association").order_by("-name")
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Academic Years"
        context["page_subtitle"] = "Manage academic years for the association."
        context["create_url"] = reverse_lazy("finance:academic-year-create")
        return context


class AcademicYearCreateView(AdminRequiredMixin, CreateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "finance/academic_year_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Academic year created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("finance:academic-year-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "New Academic Year"
        context["cancel_url"] = reverse_lazy("finance:academic-year-list")
        return context


class AcademicYearUpdateView(AdminRequiredMixin, UpdateView):
    model = AcademicYear
    form_class = AcademicYearForm
    template_name = "finance/academic_year_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Academic year updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("finance:academic-year-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Academic Year"
        context["cancel_url"] = reverse_lazy("finance:academic-year-list")
        return context


class AcademicYearDeleteView(AdminRequiredMixin, DeleteView):
    model = AcademicYear
    template_name = "finance/academic_year_confirm_delete.html"
    success_url = reverse_lazy("finance:academic-year-list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Academic year deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("finance:academic-year-list")
        return context


# =====================================================
# Semester CRUD (Follows same structure...)
# =====================================================
# [Remaining classes continue here in standard PEP 8 format]


# =====================================================
# Semester CRUD
# =====================================================

class SemesterListView(AdminRequiredMixin, ListView):

    model = Semester

    template_name = "finance/semester_list.html"

    context_object_name = "object_list"

    paginate_by = 10

    def get_queryset(self):

        queryset = Semester.objects.select_related(
            "academic_year"
        )

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(
                academic_year__name__icontains=search
            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page_title"] = "Semesters"

        context["page_subtitle"] = (
            "Manage semesters."
        )

        context["create_url"] = reverse_lazy(
            "finance:semester-create"
        )

        return context


class SemesterCreateView(AdminRequiredMixin, CreateView):

    model = Semester

    form_class = SemesterForm

    template_name = "finance/semester_form.html"

    success_url = reverse_lazy(
        "finance:semester-list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Semester created successfully."
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page_title"] = "Create Semester"

        context["page_subtitle"] = (
            "Add a new semester."
        )

        context["cancel_url"] = reverse_lazy(
            "finance:semester-list"
        )

        return context


class SemesterUpdateView(AdminRequiredMixin, UpdateView):

    model = Semester

    form_class = SemesterForm

    template_name = "finance/semester_form.html"

    success_url = reverse_lazy(
        "finance:semester-list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Semester updated successfully."
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page_title"] = "Edit Semester"

        context["page_subtitle"] = (
            "Update semester information."
        )

        context["cancel_url"] = reverse_lazy(
            "finance:semester-list"
        )

        return context


class SemesterDeleteView(AdminRequiredMixin, DeleteView):

    model = Semester

    template_name = "finance/semester_confirm_delete.html"

    success_url = reverse_lazy(
        "finance:semester-list"
    )

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "Semester deleted successfully."
        )

        return super().delete(
            request,
            *args,
            **kwargs,
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["cancel_url"] = reverse_lazy(
            "finance:semester-list"
        )

        return context


# =====================================================
# Fee Structure CRUD
# =====================================================

class FeeStructureListView(AdminRequiredMixin, ListView):

    model = FeeStructure

    template_name = "finance/fee_structure_list.html"

    context_object_name = "object_list"

    paginate_by = 10

    def get_queryset(self):

        queryset = FeeStructure.objects.select_related(
            "semester",
            "semester__academic_year",
            "department",
        )

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(
                department__name__icontains=search
            )

        return queryset.order_by(
            "semester__academic_year__name",
            "semester__semester",
            "department__name",
            "level",
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["page_title"] = "Fee Structures"

        context["page_subtitle"] = (
            "Manage association fee structures."
        )

        context["create_url"] = reverse_lazy(
            "finance:fee-structure-create"
        )

        return context


class FeeStructureCreateView(AdminRequiredMixin, CreateView):

    model = FeeStructure

    form_class = FeeStructureForm

    template_name = "finance/fee_structure_form.html"

    success_url = reverse_lazy(
        "finance:fee-structure-list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Fee structure created successfully."
        )

        return super().form_valid(form)


class FeeStructureUpdateView(AdminRequiredMixin, UpdateView):

    model = FeeStructure

    form_class = FeeStructureForm

    template_name = "finance/fee_structure_form.html"

    success_url = reverse_lazy(
        "finance:fee-structure-list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "Fee structure updated successfully."
        )

        return super().form_valid(form)


class FeeStructureDeleteView(AdminRequiredMixin, DeleteView):

    model = FeeStructure

    template_name = "finance/fee_structure_confirm_delete.html"

    success_url = reverse_lazy(
        "finance:fee-structure-list"
    )

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "Fee structure deleted successfully."
        )

        return super().delete(
            request,
            *args,
            **kwargs,
        )


class PaymentDetailView(AdminRequiredMixin, DetailView):
    """
    Displays payment details.
    """

    model = Payment

    template_name = "finance/payment_detail.html"

    context_object_name = "payment"


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        payment = self.object


        context["balance"] = (
            BalanceService.outstanding_balance(
                payment.member,
                payment.fee_structure,
            )
        )


        context["receipt"] = (
            payment.receipt
            if hasattr(payment, "receipt")
            else None
        )


        return context


class PaymentListView(AdminRequiredMixin, ListView):
    """
    Displays all recorded payments.
    """

    model = Payment
    template_name = "finance/payment_list.html"
    context_object_name = "payments"
    paginate_by = 20

    def get_queryset(self):
        queryset = (
            Payment.objects.select_related(
                "member",
                "member__department",
                "fee_structure",
                "fee_structure__semester",
                "fee_structure__semester__academic_year",
                "recorded_by",
            
        ))

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                models.Q(payment_id__icontains=search)
                | models.Q(member__student_id__icontains=search)
                | models.Q(member__first_name__icontains=search)
                | models.Q(member__last_name__icontains=search)
                | models.Q(transaction_reference__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        payments = self.get_queryset()

        context["page_title"] = "Payments"

        context["total_payments"] = payments.count()

        context["total_amount"] = (
            payments.aggregate(
                total=Sum("amount_paid")
            )["total"]
            or 0
        )

        return context

class RecordPaymentView(AdminRequiredMixin, CreateView):
    """
    Records a new payment.
    """

    model = Payment

    form_class = PaymentForm

    template_name = "finance/payment_form.html"

    success_url = reverse_lazy("finance:payment-list")

    def form_valid(self, form):

       print("=" * 60)
       print("FORM IS VALID")
       print(form.cleaned_data)

       cleaned = form.cleaned_data

       try:

          print("Checking payment...")

          PaymentService.can_accept_payment(
            member=cleaned["member"],
            fee_structure=cleaned["fee_structure"],
            amount_paid=cleaned["amount_paid"],
           )

          print("Recording payment...")

          payment, receipt = PaymentService.record_payment(
            member=cleaned["member"],
            fee_structure=cleaned["fee_structure"],
            amount_paid=cleaned["amount_paid"],
            payment_method=cleaned["payment_method"],
            transaction_reference=cleaned["transaction_reference"],
            payment_date=timezone.now(),
            recorded_by=self.request.user,
            remarks=cleaned["remarks"],
        )

          print("SUCCESS")
          print(payment.pk)
          print(receipt.receipt_number)

          messages.success(
            self.request,
            f"Payment recorded successfully. Receipt: {receipt.receipt_number}",
        )

          return redirect(
            "finance:payment-detail",
            pk=payment.pk,
        )

       except Exception as exc:

        print("ERROR")
        print(exc)

        form.add_error(None, str(exc))
        

        return self.form_invalid(form)

class ReceiptListView(
    LoginRequiredMixin,
    ListView,
):

    model = Receipt

    template_name = "finance/receipt_list.html"

    context_object_name = "receipts"

    ordering = ["-generated_at"]

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["receipt_settings"] = (
            ReceiptSettings.objects.first()
        )

        return context



class ReceiptDetailView(
    LoginRequiredMixin,
    DetailView,
):
    model = Receipt
    template_name = "finance/receipt_detail.html"
    context_object_name = "receipt"

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            "payment",
            "payment__member",
            "payment__member__user",
            "payment__fee_structure",
            "payment__fee_structure__semester",
        )

        user = self.request.user

        # Staff can retain access to finance receipts.
        if user.is_staff:
            return queryset

        # Students can access only receipts linked to their account.
        return queryset.filter(
            payment__member__user=user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receipt_settings"] = (
            ReceiptSettings.objects.first()
        )
        return context

    
    
    
class PaymentBalanceAPIView(AdminRequiredMixin, View):
    """
    Returns payment balance information.
    """

    def get(self, request):

        member_id = request.GET.get(
            "member"
        )

        fee_id = request.GET.get(
            "fee"
        )


        if not member_id or not fee_id:

            return JsonResponse(
                {}
            )


        from members.models import Member
        from .models import FeeStructure


        member = Member.objects.get(
            id=member_id
        )


        fee_structure = FeeStructure.objects.get(
            id=fee_id
        )


        data = {

            "total_fee":
                str(
                    BalanceService.total_fee(
                        fee_structure
                    )
                ),


            "total_paid":
                str(
                    BalanceService.total_paid(
                        member,
                        fee_structure,
                    )
                ),


            "outstanding":
                str(
                    BalanceService.outstanding_balance(
                        member,
                        fee_structure,
                    )
                ),


            "status":
                BalanceService.payment_status(
                    member,
                    fee_structure,
                )

        }


   
   
   
        return JsonResponse(data)   
    
    
    
    
    
class MemberPaymentHistoryView(AdminRequiredMixin,DetailView
   )  :

    model = Member

    template_name = (
        "finance/member_payment_history.html"
    )

    context_object_name = "member"


    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        member = self.object


        payments = (
            Payment.objects
            .filter(
                member=member
            )
            .select_related(
                "fee_structure",
                "fee_structure__semester",
                "receipt",
            )
            .order_by(
                "-payment_date"
            )
        )


        context["payments"] = payments


        context["total_paid"] = (
            payments.aggregate(
                total=Sum(
                    "amount_paid"
                )
            )["total"]
            or 0
        )


        return context        



class ReceiptPDFView(AdminRequiredMixin, View):

    def get(self, request, pk):

        receipt = Receipt.objects.select_related(
            "payment",
            "payment__member",
            "payment__fee_structure",
            "payment__fee_structure__semester",
        ).get(pk=pk)

        return generate_receipt_pdf(
            receipt
        ) 
        

class StudentReceiptPDFView(LoginRequiredMixin, View):

    def get(self, request, pk):
        receipt = get_object_or_404(
            Receipt.objects.select_related(
                "payment",
                "payment__member",
                "payment__fee_structure",
                "payment__fee_structure__semester",
            ).filter(
                payment__member__user=request.user
            ),
            pk=pk,
        )

        return generate_receipt_pdf(receipt)
          
    