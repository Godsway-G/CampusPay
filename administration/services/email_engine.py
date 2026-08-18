from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template import Template, Context
import logging

from administration.models import EmailTemplate
from administration.services.brevo_service import (
    BrevoEmailService,
)


logger = logging.getLogger(__name__)


class EmailService:
    """
    Central email engine for CampusPay.

    Responsible for:

    - Finding email templates
    - Validating template status
    - Rendering template content
    - Validating recipients
    - Sending through Brevo
    - Handling delivery failures safely
    """

    # =====================================================
    # TEMPLATE
    # =====================================================

    @staticmethod
    def get_template(template_slug):
        """
        Retrieve an active email template.
        """

        return (
            EmailTemplate.objects
            .filter(
                slug=template_slug,
                is_active=True,
            )
            .first()
        )

    # =====================================================
    # RECIPIENT VALIDATION
    # =====================================================

    @staticmethod
    def validate_recipient(recipient):
        """
        Validate recipient email address.
        """

        if not recipient:
            raise ValidationError(
                "Recipient email address is required."
            )

        try:
            validate_email(recipient)

        except ValidationError:
            raise ValidationError(
                "Please provide a valid recipient email address."
            )

    # =====================================================
    # TEMPLATE RENDERING
    # =====================================================

    @staticmethod
    def render_content(content, context=None):
        """
        Render email content using Django's template engine.

        Example:

            Content:
                Hello {{ name }}

            Context:
                {
                    "name": "Godsway Xenyo"
                }

            Result:
                Hello Godsway Xenyo
        """

        if not content:
            return ""

        context = context or {}

        try:
            template = Template(content)

            return template.render(
                Context(context)
            )

        except Exception as exc:

            logger.exception(
                "Failed to render email template content."
            )

            print(
                f"Email template rendering failed: {exc}"
            )

            # Return the original content rather than
            # completely destroying the email.
            return content

    # =====================================================
    # SEND TEMPLATE
    # =====================================================

    @staticmethod
    def send_template(
        template_slug,
        recipient,
        context=None,
    ):
        """
        Send an email using a CampusPay email template.

        Parameters:

            template_slug:
                Unique slug of the EmailTemplate.

            recipient:
                Destination email address.

            context:
                Dictionary containing template variables.

        Returns:

            True
                Email sent successfully.

            False
                Email could not be sent.
        """

        context = context or {}

        # -------------------------------------------------
        # Validate recipient
        # -------------------------------------------------

        try:

            EmailService.validate_recipient(
                recipient
            )

        except ValidationError as exc:

            logger.warning(
                "Invalid email recipient: %s",
                recipient,
            )

            print(
                f"Email validation failed: {exc}"
            )

            return False

        # -------------------------------------------------
        # Retrieve template
        # -------------------------------------------------

        template = (
            EmailTemplate.objects
            .filter(
                slug=template_slug
            )
            .first()
        )

        # -------------------------------------------------
        # Template does not exist
        # -------------------------------------------------

        if not template:

            logger.warning(
                "Email template not found: %s",
                template_slug,
            )

            print(
                "Email template not found."
            )

            return False

        # -------------------------------------------------
        # Template inactive
        # -------------------------------------------------

        if not template.is_active:

            logger.warning(
                "Attempted to send inactive "
                "email template: %s",
                template_slug,
            )

            print(
                "Email template is inactive "
                "and cannot be sent."
            )

            return False

        # -------------------------------------------------
        # Render subject
        # -------------------------------------------------

        subject = (
            EmailService.render_content(
                template.subject,
                context,
            )
        )

        # -------------------------------------------------
        # Render plain text body
        # -------------------------------------------------

        message = (
            EmailService.render_content(
                template.body,
                context,
            )
        )

        # -------------------------------------------------
        # Render HTML content
        # -------------------------------------------------

        html_content = (
            EmailService.render_content(
                template.html_content,
                context,
            )
        )

        # -------------------------------------------------
        # Ensure HTML content exists
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Send through Brevo
        # -------------------------------------------------

        try:

            result = (
                BrevoEmailService.send_email(
                    subject=subject,
                    message=message,
                    recipient=recipient,
                    html_content=html_content,
                )
            )

            # -------------------------------------------------
            # Successful delivery
            # -------------------------------------------------

            if result:

                logger.info(
                    "Email sent successfully. "
                    "Template=%s Recipient=%s",
                    template_slug,
                    recipient,
                )

                return True

            # -------------------------------------------------
            # Delivery failed
            # -------------------------------------------------

            logger.error(
                "Email delivery failed. "
                "Template=%s Recipient=%s",
                template_slug,
                recipient,
            )

            return False

        # -------------------------------------------------
        # Unexpected email engine error
        # -------------------------------------------------

        except Exception as exc:

            logger.exception(
                "Unexpected email engine error. "
                "Template=%s Recipient=%s",
                template_slug,
                recipient,
            )

            print(
                f"Email sending failed: {exc}"
            )

            return False