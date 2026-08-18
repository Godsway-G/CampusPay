from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class StudentPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            "old_password": "Enter your temporary password",
            "new_password1": "Enter your new password",
            "new_password2": "Confirm your new password",
        }

        for name, field in self.fields.items():

            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": placeholders.get(name, ""),
            })
            
            


from django import forms


class PasswordResetRequestForm(forms.Form):

    student_id = forms.CharField(

        label="Student ID",

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "0325080106",

                "autocomplete": "off",

            }

        )

    )


    reason = forms.CharField(

        label="Reason",

        widget=forms.Textarea(

            attrs={

                "class": "form-control",

                "rows": 4,

                "placeholder": (
                    "Briefly explain why you need your password reset."
                ),

            }

        )

    )