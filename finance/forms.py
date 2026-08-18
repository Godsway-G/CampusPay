from django import forms

from .models import (
    AcademicYear,
    Semester,
    FeeStructure,
    Payment,
)


class BaseStyledModelForm(forms.ModelForm):
    """
    Base form that applies Bootstrap styling
    to all form fields automatically.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            css_class = "form-control"

            if isinstance(
                field.widget,
                (
                    forms.CheckboxInput,
                    forms.RadioSelect,
                ),
            ):
                css_class = "form-check-input"

            field.widget.attrs.setdefault(
                "class",
                css_class,
            )


class AcademicYearForm(BaseStyledModelForm):

    class Meta:
        model = AcademicYear

        fields = [
            "association",
            "name",
            "is_current",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Example: 2025/2026",
                }
            ),
        }


class SemesterForm(BaseStyledModelForm):

    class Meta:
        model = Semester
        fields = [
            "academic_year",
            "semester",
            "payment_deadline",
            "is_active",
        ]

        widgets = {
            "academic_year": forms.Select(
                attrs={"class": "form-select"}
            ),
            "semester": forms.Select(
                attrs={"class": "form-select"}
            ),
            "payment_deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
        
        
class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure

        fields = [
            "semester",
            "department",
            "level",
            "amount",
        ]

        widgets = {
            "semester": forms.Select(
                attrs={"class": "form-select"}
            ),
            "department": forms.Select(
                attrs={"class": "form-select"}
            ),
            "level": forms.Select(
                attrs={"class": "form-select"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                }
            ),
        }
        
        
        


class PaymentForm(BaseStyledModelForm):

    class Meta:
        model = Payment
        fields = [
            "member",
            "fee_structure",
            "amount_paid",
            "payment_method",
            "transaction_reference",
            "remarks",
        ]


    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)


        self.fields["fee_structure"].queryset = (
            FeeStructure.objects
            .select_related(
                "semester",
                "semester__academic_year",
                "department",
            )
            .filter(
                semester__is_active=True
            )
        )
        widgets = {

            "member":
                forms.Select(
                    attrs={
                        "class":
                        "form-select"
                    }
                ),


            "fee_structure":
                forms.Select(
                    attrs={
                        "class":
                        "form-select"
                    }
                ),


            "amount_paid":
                forms.NumberInput(
                    attrs={
                        "class":
                        "form-control",
                        "step":
                        "0.01",
                    }
                ),


            "payment_method":
                forms.Select(
                    attrs={
                        "class":
                        "form-select"
                    }
                ),


            "transaction_reference":
                forms.TextInput(
                    attrs={
                        "class":
                        "form-control"
                    }
                ),


            "remarks":
                forms.Textarea(
                    attrs={
                        "class":
                        "form-control",
                        "rows":
                        3,
                    }
                ),
        }