from django import forms

from .models import Member


class MemberForm(forms.ModelForm):

    class Meta:

        model = Member

        fields = [
            "student_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "level",
            "department",
            "photo",
            "active",
        ]

        widgets = {

            "student_id": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "first_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "last_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "gender": forms.Select(
                attrs={"class": "form-select"}
            ),

            "level": forms.Select(
                attrs={"class": "form-select"}
            ),

            "department": forms.Select(
                attrs={"class": "form-select"}
            ),

            "photo": forms.FileInput(
                attrs={"class": "form-control"}
            ),

            "active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

        }