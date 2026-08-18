from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView

from members.models import Member


class MemberDeleteView(
    LoginRequiredMixin,
    DeleteView,
):

    model = Member

    template_name = (
        "members/member_confirm_delete.html"
    )

    success_url = reverse_lazy(
        "members:list"
    )