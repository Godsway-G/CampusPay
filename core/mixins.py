from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.core.exceptions import PermissionDenied


class SuccessMessageMixin:
    """
    Adds a success message after form submission.
    """

    success_message = None

    def form_valid(self, form):

        response = super().form_valid(form)

        if self.success_message:

            messages.success(
                self.request,
                self.success_message
            )

        return response
    
    


from django.contrib.auth.mixins import LoginRequiredMixin


class CampusLoginRequiredMixin(LoginRequiredMixin):
    """
    Forces authentication before accessing protected pages.
    """

    login_url = "login"

    redirect_field_name = "next"

    raise_exception = False
    
    
    


class RoleRequiredMixin:

    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):

        if request.user.role not in self.allowed_roles:

            raise PermissionDenied

        return super().dispatch(
            request,
            *args,
            **kwargs
        )    
        
 
 

class AdminRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role not in ["ADMIN", "TREASURER"]:
            messages.error(request, "Access denied.")

            if request.user.role == "STUDENT":
                return redirect("portal:dashboard")

            return redirect("accounts:login")

        return super().dispatch(request, *args, **kwargs)
        