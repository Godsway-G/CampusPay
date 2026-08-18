from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.views.generic import ListView
from .forms import StudentPasswordChangeForm
from members.models import Member
from django.views.generic import DetailView

from .services import StudentPortalService

from django.contrib.auth import update_session_auth_hash

from .forms import PasswordResetRequestForm
from .models import PasswordResetRequest
from django.views.generic import FormView

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .services import AuditService
from .models import AuditLog

from django.contrib.auth.mixins import LoginRequiredMixin


from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from members.services import MemberService


class StudentDashboardView(LoginRequiredMixin,TemplateView
):

    template_name = (
        "portal/dashboard.html"
    )


    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):


        # only students allowed

        if request.user.role != "STUDENT":

            messages.error(
                request,
                "This portal is only for students."
            )

            return redirect(
                "accounts:login"
            )


        try:

            member = request.user.member_profile


        except Member.DoesNotExist:

           messages.error(
           request,
           "No student profile linked."
        )

           return redirect(
           "accounts:login"
        )


        if request.user.must_change_password:


            messages.warning(
                request,
                "Please change your temporary password."
            )


            return redirect(
                "portal:change_password"
            )


        return super().dispatch(
            request,
            *args,
            **kwargs
        )



    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )


        member = (
            self.request.user.member_profile
        )


        dashboard = (
            StudentPortalService
            .get_student_dashboard(member)
        )


        context.update(
            dashboard
        )


        context["member"] = member


        return context





class StudentLoginView(LoginView):

    template_name = "portal/login.html"

    redirect_authenticated_user = False


    def form_valid(self, form):

        user = form.get_user()


        if user.role != "STUDENT":

            messages.error(
                self.request,
                "Access denied. This portal is for students only."
            )

            return redirect(
                "portal:login"
            )


        login(
            self.request,
            user
        )


        return redirect(
            self.get_success_url()
        )


    def get_success_url(self):

        return reverse_lazy(
            "portal:dashboard"
        )




class PasswordResetRequestView(FormView):

    template_name = "portal/request_reset.html"

    form_class = PasswordResetRequestForm


    def form_valid(self, form):

        student_id = form.cleaned_data["student_id"]

        try:

            member = Member.objects.get(

                student_id=student_id

            )

        except Member.DoesNotExist:

            messages.error(

                self.request,

                "Student was not found."

            )

            return self.form_invalid(form)


        PasswordResetRequest.objects.create(

            member=member,

            reason=form.cleaned_data["reason"],

)


        messages.success(

            self.request,

            "Your password reset request has been submitted."

        )


        return redirect(

            "portal:login"

        )





class StudentPasswordChangeView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView,
):

    template_name = "portal/change_password.html"


    def form_invalid(self, form):

        print(form.errors)

        return super().form_invalid(form)


    def form_valid(self, form):

        print("FORM VALID")

        response = super().form_valid(form)

        user = self.request.user

        user.must_change_password = False

        user.save(update_fields=["must_change_password"])

        update_session_auth_hash(
            self.request,
            user
        )

        return response


    def get_success_url(self):

        return reverse_lazy(
            "portal:dashboard"
        )
        
        
    form_class = StudentPasswordChangeForm 
    
    


class PasswordResetRequestListView(
    LoginRequiredMixin,
    ListView,
):

    model = PasswordResetRequest

    template_name = "portal/reset_request_list.html"

    context_object_name = "requests"

    ordering = ["-requested_at"]

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role not in [
            "ADMIN",
            "TREASURER",
        ]:
            messages.error(
                request,
                "Access denied."
            )

            return redirect(
                "portal:dashboard"
            )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )
    
from django.views.generic import DetailView


class PasswordResetRequestDetailView(
    LoginRequiredMixin,
    DetailView,
):
    model = PasswordResetRequest
    template_name = "portal/reset_request_detail.html"
    context_object_name = "request_item"

# ADD HERE
@login_required
def approve_reset_request(request, pk):

    reset_request = get_object_or_404(
        PasswordResetRequest,
        pk=pk
    )


    # Get student member
    member = reset_request.member


    # Get user account
    user = member.user


    # Generate new temporary password
    password = MemberService.reset_portal_password(
        member
    )


    reset_request.status = (
        PasswordResetRequest.APPROVED
    )


    reset_request.processed_at = (
        timezone.now()
    )


    reset_request.save()


    # Audit log
    AuditService.log(
        user=user,
        action="PASSWORD_RESET_APPROVED",
        description=(
            "Password reset request approved."
        ),
        request=request,
    )


    messages.success(
        request,
        "Password reset approved successfully."
    )


    return render(
        request,
        "portal/reset_password_success.html",
        {
            "member": member,
            "password": password,
        }
    )
          
          
          
    


@login_required
def reject_reset_request(request, pk):

    reset_request = get_object_or_404(
        PasswordResetRequest,
        pk=pk
    )

    # -------------------------------------------------
    # SAFETY CHECK
    # -------------------------------------------------

    if request.user.role not in [
        "ADMIN",
        "TREASURER",
    ]:
        messages.error(
            request,
            "You are not authorized to reject password reset requests."
        )

        return redirect(
            "portal:dashboard"
        )

    # -------------------------------------------------
    # ONLY PENDING REQUESTS CAN BE REJECTED
    # -------------------------------------------------

    if reset_request.status != PasswordResetRequest.PENDING:

        messages.warning(
            request,
            "This password reset request has already been processed."
        )

        return redirect(
            "portal:reset-request-list"
        )

    # -------------------------------------------------
    # UPDATE REQUEST
    # -------------------------------------------------

    reset_request.status = (
        PasswordResetRequest.REJECTED
    )

    reset_request.processed_at = (
        timezone.now()
    )

    reset_request.save(
        update_fields=[
            "status",
            "processed_at",
        ]
    )

    # -------------------------------------------------
    # AUDIT LOG
    # -------------------------------------------------

    AuditService.log(
        user=request.user,
        action="PASSWORD_RESET_REJECTED",
        description=(
            "Password reset request rejected."
        ),
        request=request,
    )

    # -------------------------------------------------
    # SUCCESS MESSAGE
    # -------------------------------------------------

    messages.warning(
        request,
        "Password reset request rejected successfully."
    )

    return redirect(
        "portal:reset-request-list"
    )


class AuditLogListView(
    LoginRequiredMixin,
    ListView
):

    model = AuditLog

    template_name = (
        "portal/audit_logs.html"
    )

    context_object_name = (
        "logs"
    )

