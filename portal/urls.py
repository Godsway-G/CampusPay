from django.urls import path

from .views import (
    StudentDashboardView,
    StudentLoginView,
    StudentPasswordChangeView,
    PasswordResetRequestView,
    PasswordResetRequestListView,
    PasswordResetRequestDetailView,
    approve_reset_request,
    reject_reset_request,
)
from .views import AuditLogListView

app_name = "portal"

urlpatterns = [

    path(
        "",
        StudentDashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "login/",
        StudentLoginView.as_view(),
        name="login",
    ),

    path(
        "change-password/",
        StudentPasswordChangeView.as_view(),
        name="change_password",
    ),
                path(

        "forgot-password/",

        PasswordResetRequestView.as_view(),

        name="forgot-password",
    ),
                
                
    path(
       "password-reset-requests/",
       PasswordResetRequestListView.as_view(),
       name="reset-request-list",
    ),

    path(
       "password-reset-requests/<int:pk>/",
       PasswordResetRequestDetailView.as_view(),
       name="reset-request-detail",
    ),
    
    
    path(
       "reset-requests/<int:pk>/approve/",
        approve_reset_request,
        name="approve-reset",
    ),

    path(
        "reset-requests/<int:pk>/reject/",
        reject_reset_request,
        name="reject-reset",
    ),
    
    
     path(
        "audit-logs/",
        AuditLogListView.as_view(),
        name="audit-logs",
    ),

]