from django.db.models import Max
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.conf import settings

from members.models import Member

import secrets
import string



User = get_user_model()



class MemberService:


    @staticmethod
    def generate_membership_id():

        last_id = (
            Member.objects.aggregate(
                Max("id")
            )["id__max"] or 0
        )

        return f"CP-{last_id + 1:04d}"



    @staticmethod
    def generate_password():

        alphabet = (
            string.ascii_uppercase
            +
            string.digits
        )


        return "CP-" + "".join(
            secrets.choice(alphabet)
            for _ in range(6)
        )



    @staticmethod
    def create_portal_account(member):

        if member.user:

            return member.user, None



        password = (
            MemberService.generate_password()
        )


        user = User.objects.create_user(

            username=member.email,

            email=member.email,

            first_name=member.first_name,

            last_name=member.last_name,

            password=password,

            role=User.MEMBER,

        )
        user.must_change_password = True
        user.save() 

        member.user = user

        member.save()



        MemberService.send_portal_credentials(
            member,
            password,
        )


        return user, password




    @staticmethod
    def reset_portal_password(member):

        if not member.user:

            return None



        password = (
            MemberService.generate_password()
        )


        user = member.user


        user.set_password(password)

        user.must_change_password = True

        user.save()


        MemberService.send_portal_credentials(
            member,
            password,
        )


        return password





    @staticmethod
    def send_portal_credentials(member, password):

        subject = (
            "CampusPay Student Portal Account"
        )


        message = f"""

Hello {member.first_name},


Your CampusPay Student Portal account details:



Email:

{member.email}



Temporary Password:

{password}



Login:

http://127.0.0.1:8000/portal/login/



Please change your password after your first login.



CampusPay Enterprise

"""


        send_mail(

            subject,

            message,

            settings.DEFAULT_FROM_EMAIL,

            [member.email],

            fail_silently=False,

        )