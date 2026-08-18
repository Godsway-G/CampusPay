from django.urls import path

from .views import (
    ReportDashboardView,
    FinanceReportView,
    MemberReportView,
    MemberDirectoryReportView,
    DepartmentSummaryReportView,
    LevelSummaryReportView,
    MemberStatusReportView,
    OutstandingReportView,
)
from .views import OutstandingReportPDFView
from .views import OutstandingReportExcelView

app_name = "reports"

urlpatterns = [

    path(
        "",
        ReportDashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "finance/",
        FinanceReportView.as_view(),
        name="finance-report",
    ),

    path(
        "members/",
        MemberReportView.as_view(),
        name="member-report",
    ),
    
    path(
    "members/directory/",
    MemberDirectoryReportView.as_view(),
    name="member-directory",
    ),

    path(
       "members/departments/",
       DepartmentSummaryReportView.as_view(),
       name="department-summary",
    ),

    path(
        "members/levels/",
        LevelSummaryReportView.as_view(),
        name="level-summary",
    ),

    path(
        "members/status/",
        MemberStatusReportView.as_view(),
        name="member-status",
    ),
    
    
    path(
        "outstanding/",
        OutstandingReportView.as_view(),
        name="outstanding-report",
    ),
    
    path(
        "outstanding/pdf/",
        OutstandingReportPDFView.as_view(),
        name="outstanding-pdf",
        ),   
    path(
        "outstanding/excel/",
        OutstandingReportExcelView.as_view(),
        name="outstanding-excel",
    ),
]