from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class BootstrapFormMixin:

    """
    Automatically applies Bootstrap classes
    to every form field.
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            css = field.widget.attrs.get("class", "")

            field.widget.attrs["class"] = (

                css +

                " form-control"

            ).strip()



class LoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(
        label="Username",
 
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
            "id": "password"
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input"
        })
    )


class RegisterForm(BootstrapFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

    username = forms.CharField(
        
    )

    first_name = forms.CharField(
        
    )

    last_name = forms.CharField(
       
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )

    phone = forms.CharField(
        
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = "MEMBER"

        if commit:
            user.save()

        return user