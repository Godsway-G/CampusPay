from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
)

from django.contrib import messages

from members.models import Member
from members.services import MemberService



def create_portal_account(request, pk):

    member = get_object_or_404(Member, pk=pk)

    user, password = MemberService.create_portal_account(member)

    if password is None:
        messages.warning(
            request,
            "This member already has a portal account. Use 'Reset Password' if a new temporary password is required."
        )
        return redirect("members:list")

    context = {
        "member": member,
        "email": member.email,
        "password": password,
    }

    messages.success(
        request,
        "Portal account created successfully."
    )

    return render(
        request,
        "members/portal_success.html",
        context,
    )



def reset_portal_password(request, pk):

    member = get_object_or_404(
        Member,
        pk=pk
    )


    password = MemberService.reset_portal_password(
        member
    )


    if password:

        messages.success(
            request,
            "Portal password reset successfully. New password sent to student."
        )


    else:

        messages.error(
            request,
            "This member has no portal account."
        )


    return redirect(
        "members:list"
    )