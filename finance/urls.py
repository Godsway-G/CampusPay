from django.urls import path

from .views import (
    FinanceDashboardView,
    PaymentListView,
    PaymentDetailView,
    RecordPaymentView,
    ReceiptDetailView,
    AcademicYearListView,
    AcademicYearCreateView,
    AcademicYearUpdateView,
    AcademicYearDeleteView, 
    SemesterListView,
    SemesterCreateView,
    SemesterUpdateView,
    SemesterDeleteView,
    FeeStructureListView,
    FeeStructureCreateView,
    FeeStructureUpdateView,
    FeeStructureDeleteView,
    MemberPaymentHistoryView,
    ReceiptPDFView,
    ReceiptListView,
    StudentReceiptPDFView,
)
from .views import PaymentBalanceAPIView

app_name = "finance"

urlpatterns = [
    # Dashboard
    path("", FinanceDashboardView.as_view(), name="dashboard"),

    # Payments
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/new/", RecordPaymentView.as_view(), name="payment-create"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),

    # Receipts
    path(
       "receipts/",
        ReceiptListView.as_view(),
        name="receipt-list",
    ),

    path(
       "receipts/<int:pk>/",
        ReceiptDetailView.as_view(),
        name="receipt-detail",
    ),

    path(
       "receipts/<int:pk>/pdf/",
       ReceiptPDFView.as_view(),
       name="receipt-pdf",
    ),        

    # Academic Years
    path(
        "academic-years/",
        AcademicYearListView.as_view(),
        name="academic-year-list",
    ),
    path(
        "academic-years/new/",
        AcademicYearCreateView.as_view(),
        name="academic-year-create",
    ),
    path(
        "academic-years/<int:pk>/edit/",
        AcademicYearUpdateView.as_view(),
        name="academic-year-update",
    ),
    path(
        "academic-years/<int:pk>/delete/",
        AcademicYearDeleteView.as_view(),
        name="academic-year-delete",
    ),
            # Semesters
    path(
        "semesters/",
        SemesterListView.as_view(),
       name="semester-list",
    ),

    path(
        "semesters/new/",
        SemesterCreateView.as_view(),
        name="semester-create",
    ),

    path(
        "semesters/<int:pk>/edit/",
        SemesterUpdateView.as_view(),
        name="semester-update",
    ),

    path(
        "semesters/<int:pk>/delete/",
        SemesterDeleteView.as_view(),
        name="semester-delete",
    ),
    
    # Fee Structures

    path(
      "fee-structures/",
      FeeStructureListView.as_view(),
      name="fee-structure-list",
    ),

    path(
       "fee-structures/new/",
       FeeStructureCreateView.as_view(),
       name="fee-structure-create",
    ),

    path(
       "fee-structures/<int:pk>/edit/",
        FeeStructureUpdateView.as_view(),
        name="fee-structure-update",
    ),

    path(
       "fee-structures/<int:pk>/delete/",
        FeeStructureDeleteView.as_view(),
        name="fee-structure-delete",
    ),
    
    
    
    path(
        "payment-balance/",
        PaymentBalanceAPIView.as_view(),
        name="payment-balance",
        ),
    
    path(
        "member/<int:pk>/payments/",
        MemberPaymentHistoryView.as_view(),
        name="member-payment-history",
        ),
    
    
    path(
        "receipts/<int:pk>/student-pdf/",
        StudentReceiptPDFView.as_view(),
        name="student-receipt-pdf",
    ),

]