from django.views.generic import ListView
from django.db.models import Q
from core.mixins import AdminRequiredMixin
from members.models import Member, Department


class MemberListView(AdminRequiredMixin, ListView):
    model = Member
    template_name = "members/member_list.html"
    context_object_name = "members"
    paginate_by = 10

    def get_queryset(self):

        queryset = Member.objects.select_related(
            "department"
        )

        search = self.request.GET.get("search")
        department = self.request.GET.get("department")
        level = self.request.GET.get("level")
        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(

                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(student_id__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)

            )

        if department:

            queryset = queryset.filter(
                department_id=department
            )

        if level:

            queryset = queryset.filter(
                level=level
            )

        if status == "active":

            queryset = queryset.filter(
                active=True
            )

        elif status == "inactive":

            queryset = queryset.filter(
                active=False
            )

        return queryset.order_by(
            "last_name",
            "first_name"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["departments"] = Department.objects.all()
        context["levels"] = Member.LEVELS

        context["total_members"] = Member.objects.count()

        context["active_members"] = Member.objects.filter(
            active=True
        ).count()

        context["inactive_members"] = Member.objects.filter(
            active=False
        ).count()

        context["department_count"] = Department.objects.count()

        return context