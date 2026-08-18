from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, RegisterForm
from .models import User
from django.views.generic import TemplateView


class UserLoginView(LoginView):

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = False


    def form_valid(self, form):

        user = form.get_user()


        # Students cannot enter admin dashboard
        if user.role == "STUDENT":

           logout(self.request)

           return redirect("portal:login")


        remember_me = form.cleaned_data.get(
            "remember_me"
        )


        if remember_me:
            self.request.session.set_expiry(
                1209600
            )
        else:
            self.request.session.set_expiry(0)


        login(
            self.request,
            user
        )


        messages.success(
            self.request,
            f"Welcome back, {user.first_name or user.username}."
        )


        return redirect(
            self.get_success_url()
        )


    def get_success_url(self):

        user = self.request.user


        if user.role in [
            "ADMIN",
            "TREASURER"
        ]:

            return reverse_lazy(
                "dashboard:home"
            )


        if user.role == "STUDENT":

            if user.must_change_password:

                return reverse_lazy("portal:change_password")


            return reverse_lazy("portal:dashboard")


        return reverse_lazy(
            "accounts:login"
        )



class UserLogoutView(LogoutView):


    next_page = "/"



    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        messages.success(
            request,
            "You have successfully logged out."
        )

        return super().dispatch(
            request,
            *args,
            **kwargs
        )



class RegisterView(CreateView):

    form_class = RegisterForm

    template_name = (
        "accounts/register.html"
    )

    success_url = reverse_lazy(
        "accounts:login"
    )


    def form_valid(
        self,
        form
    ):

        messages.success(
            self.request,
            "Account created successfully. Please sign in."
        )

        return super().form_valid(form)





class AccessView(TemplateView):

    template_name = "accounts/access.html"    
    