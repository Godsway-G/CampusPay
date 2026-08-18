from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from administration.models import EmailConfiguration



class EmailConfigurationService:
    """
    Central email service for CampusPay.
    Handles SMTP configuration and email delivery.
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
    def is_enabled():
        """
        Checks if email configuration exists.
        """

        return (
            EmailConfigurationService
            .get_configuration()
            is not None
        )



    @staticmethod
    def get_default_sender():

       config = (
          EmailConfigurationService
          .get_configuration()
    )


       if config and config.default_sender_email:

          return config.default_sender_email


       return settings.DEFAULT_FROM_EMAIL
   
   
   

    @staticmethod
    def get_connection():
        """
        Creates SMTP connection dynamically.
        """

        config = (
            EmailConfigurationService
            .get_configuration()
        )


        if not config:
            return None



        return get_connection(

            backend=
            "django.core.mail.backends.smtp.EmailBackend",

            host=config.email_host,

            port=config.email_port,

            username=config.email_username,

            password=config.email_password,

            use_tls=(
                config.encryption == "TLS"
            ),

            use_ssl=(
                config.encryption == "SSL"
            ),
            
            timeout=30,

        )



    @staticmethod
    def send_email(
        subject,
        message,
        recipient_list,
        html_message=None,
    ):
        """
        General email sender.
        """

        connection = (
            EmailConfigurationService
            .get_connection()
        )


        if not connection:
            return False



        message = EmailMessage(

            subject=subject,

            body=message,

            from_email=(
                EmailConfigurationService
                .get_default_sender()
            ),

            to=recipient_list,


            connection=connection,

        )



        if html_message:

           message.content_subtype = "html"
           message.body = html_message



        
        try:

           sent = message.send()

           return sent > 0


        except Exception as e:

            print(
                 f"Email sending failed: {e}" )

            return False

        



    @staticmethod
    def send_test_email(email):

      if not email:
        return False


      return EmailConfigurationService.send_email(

        subject="CampusPay Email Test",

        message=(
            "Congratulations.\n\n"
            "Your CampusPay email configuration "
            "is working successfully.\n\n"
            "CampusPay Enterprise"
        ),

        recipient_list=[
            email
        ],

    )