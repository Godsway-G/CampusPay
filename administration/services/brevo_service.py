import sib_api_v3_sdk

from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from administration.models import EmailConfiguration



class BrevoEmailService:
    """
    Handles email sending using Brevo API.

    CampusPay central email delivery service.
    Uses Brevo Transactional Email API.
    """



    @staticmethod
    def get_configuration():
        """
        Returns active email configuration.
        """

        return (
            EmailConfiguration.objects
            .filter(is_active=True)
            .first()
        )



    @staticmethod
    def validate_recipient(email):
        """
        Checks if recipient email is valid.
        """

        try:

            validate_email(email)

            return True

        except ValidationError:

            print(
                "Invalid recipient email"
            )

            return False



    @staticmethod
    def send_email(
        subject,
        message,
        recipient,
        html_content=None,
    ):
        """
        Sends transactional email using Brevo API.
        """



        # =========================================
        # 1. Validate recipient
        # =========================================

        if not recipient:

            print(
                "Recipient email missing"
            )

            return False



        if not BrevoEmailService.validate_recipient(
            recipient
        ):

            return False




        # =========================================
        # 2. Get Email Configuration
        # =========================================

        config = (
            BrevoEmailService
            .get_configuration()
        )



        if not config:

            print(
                "Email configuration not found"
            )

            return False




        # =========================================
        # 3. Get API Key
        # =========================================

        api_key = (
            config.brevo_api_key
            or
            settings.BREVO_API_KEY
        )



        if not api_key:

            print(
                "Brevo API key missing"
            )

            return False




        # =========================================
        # 4. Configure Brevo API
        # =========================================

        configuration = (
            sib_api_v3_sdk.Configuration()
        )


        configuration.api_key[
            "api-key"
        ] = api_key



        api_instance = (
            sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(
                    configuration
                )
            )
        )




        # =========================================
        # 5. Sender Configuration
        # =========================================

        sender_email = (
            config.default_sender_email
            or
            settings.DEFAULT_FROM_EMAIL
        )



        sender = {

            "name":
                getattr(
                    config,
                    "sender_name",
                    "CampusPay"
                ),

            "email":
                sender_email,

        }




        # =========================================
        # 6. Recipient
        # =========================================

        to = [

            {
                "email": recipient
            }

        ]




        # =========================================
        # 7. HTML fallback
        # =========================================

        if not html_content:

            html_content = f"""
            <html>
                <body>

                    <p>
                    {message}
                    </p>

                </body>
            </html>
            """




        # =========================================
        # 8. Create Email
        # =========================================

        email = (
            sib_api_v3_sdk.SendSmtpEmail(

                sender=sender,

                to=to,

                subject=subject,

                text_content=message,

                html_content=html_content,

            )
        )




        # =========================================
        # 9. Send Email
        # =========================================

        try:


            response = (
                api_instance
                .send_transac_email(
                    email
                )
            )


            print(
                "Brevo Email Sent:",
                response
            )


            return True



        except sib_api_v3_sdk.ApiException as e:


            print(
                "Brevo API Error:"
            )

            print(
                e
            )


            return False



        except Exception as e:


            print(
                "Unexpected Email Error:"
            )

            print(
                e
            )


            return False