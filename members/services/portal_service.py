"""

    Returns:
        _type_: _description_
    """
from django.core.mail import send_mail
from django.conf import settings

from finance.models import Payment


class StudentPortalService:
    """
    Handles student portal operations.
    """


    @staticmethod
    def get_student_dashboard(member):

        payments = Payment.objects.filter(
            member=member
        )

        total_paid = sum(
            payment.amount
            for payment in payments
        )

        return {
            "payments": payments,
            "total_paid": total_paid,
            "payment_count": payments.count(),
        }



    @staticmethod
    def send_portal_credentials(user, password):

        subject = "Welcome to CampusPay Enterprise"

        message = f"""
Hello {user.first_name},

Your CampusPay Student Portal Account has been created.

--------------------------------

Email:
{user.email}

Temporary Password:
{password}

--------------------------------

Login here:

http://127.0.0.1:8000/portal/login/

For security reasons, please change your password after your first login.

Thank you.

CampusPay Enterprise Team
"""


        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        """
        """