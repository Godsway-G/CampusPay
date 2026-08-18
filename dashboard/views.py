from django.views.generic import TemplateView


from core.mixins import AdminRequiredMixin


from .services import DashboardService



class DashboardView(AdminRequiredMixin, TemplateView):


    template_name = "dashboard/dashboard.html"



    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)



        user = self.request.user



        display_name = (

            user.first_name.strip()

            if user.first_name

            else user.username

        )



        statistics = (
            DashboardService
            .get_dashboard_statistics()
        )



        context.update({


            "page_title":
                "Dashboard",



            "greeting":
                DashboardService.get_greeting(),



            "user_name":
                display_name,



            "user_role":
                user.role,



            **statistics,

        })



        return context