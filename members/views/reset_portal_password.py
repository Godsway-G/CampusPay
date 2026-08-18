from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from members.models import Member
from members.services import MemberService



def reset_portal_password(request, pk):

    member = get_object_or_404(
        Member,
        pk=pk
    )


    password = MemberService.reset_portal_password(
        member
    )


    messages.success(
        request,
        
        f"New portal password generated: {password}"
    )


    return redirect(
        "members:list"
    )