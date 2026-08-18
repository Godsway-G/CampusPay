from administration.models import EmailTemplate
from administration.services.brevo_service import BrevoEmailService


class EmailTemplateService:
    """
    Handles CampusPay reusable email templates.
    """


    @staticmethod
    def get_template(slug):

        return (
            EmailTemplate.objects
            .filter(
                slug=slug,
                is_active=True
            )
            .first()
        )



    @staticmethod
    def render_content(content, context):

        if not content:
            return ""


        for key, value in context.items():

            placeholder = "{{" + key + "}}"

            content = content.replace(
                placeholder,
                str(value)
            )


        return content



    @staticmethod
    def send_template_email(
        template_slug,
        recipient,
        context={}
    ):

        template = (
            EmailTemplateService
            .get_template(template_slug)
        )


        if not template:
            print(
                "Email template not found"
            )

            return False



        subject = (
            EmailTemplateService
            .render_content(
                template.subject,
                context
            )
        )


        body = (
            EmailTemplateService
            .render_content(
                template.body,
                context
            )
        )


        html = (
            EmailTemplateService
            .render_content(
                template.html_content,
                context
            )
        )



        return (
            BrevoEmailService
            .send_email(
               subject=subject,
               message=body,
               recipient=recipient,
               html_content=html
    )
)