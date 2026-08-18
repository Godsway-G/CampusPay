def user_sidebar(request):

    sidebar = None


    if request.user.is_authenticated:


        if request.user.role == "STUDENT":

            sidebar = "components/student_sidebar.html"


        elif request.user.role in [
            "ADMIN",
            "TREASURER",
        ]:

            sidebar = "components/admin_sidebar.html"


    return {
        "user_sidebar": sidebar
        
    }
    
    
    
from django.urls import resolve


def user_sidebar(request):
    """
    Determines the active sidebar section.
    """

    active_section = ""

    if request.path:
        try:
            match = resolve(request.path)

            namespace = match.namespace
            url_name = match.url_name

            if namespace == "dashboard":
                active_section = "dashboard"

            elif namespace == "members":
                active_section = "members"

            elif namespace == "finance":

                if url_name.startswith("receipt"):
                    active_section = "receipts"
                else:
                    active_section = "finance"

            elif namespace == "reports":
                active_section = "reports"

            elif namespace == "portal":
                active_section = "portal"

        except Exception:
            pass

    return {
        "active_section": active_section,
    }    