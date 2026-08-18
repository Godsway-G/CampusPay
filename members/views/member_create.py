from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from members.models import Member
from members.forms import MemberForm


class MemberCreateView(
    LoginRequiredMixin,
    CreateView,
):

    model = Member

    form_class = MemberForm

    template_name = "members/member_form.html"

    success_url = reverse_lazy(
        "members:list"
    )