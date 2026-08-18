from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    UserLoginView,
    UserLogoutView,
    RegisterView,
    AccessView,
)

app_name = "accounts"

urlpatterns = [

    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
       "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),


    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # -------------------------
    # Password Reset
    # -------------------------

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/emails/password_reset_email.html",
            subject_template_name="accounts/emails/password_reset_subject.txt",
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    
     


    path(
        "access/",
        AccessView.as_view(),
        name="access"
    ),  

]