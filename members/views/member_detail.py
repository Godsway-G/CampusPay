from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from members.models import Member


class MemberDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = Member

    template_name = "members/member_detail.html"

    context_object_name = "member"