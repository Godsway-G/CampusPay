from django.urls import path

from .views import (
    MemberListView,
    MemberCreateView,
    MemberDetailView,
    MemberUpdateView,
    MemberDeleteView,
)

from .views.portal_account import (
    create_portal_account,
    reset_portal_password,
)


app_name = "members"


urlpatterns = [

    path(
        "",
        MemberListView.as_view(),
        name="list",
    ),


    path(
        "create/",
        MemberCreateView.as_view(),
        name="create",
    ),


    path(
        "<int:pk>/",
        MemberDetailView.as_view(),
        name="detail",
    ),


    path(
        "<int:pk>/edit/",
        MemberUpdateView.as_view(),
        name="edit",
    ),


    path(
        "<int:pk>/delete/",
        MemberDeleteView.as_view(),
        name="delete",
    ),


    # Portal account creation

    path(
        "<int:pk>/portal-account/",
        create_portal_account,
        name="portal_account",
    ),


    # Password reset

    path(
        "<int:pk>/reset-password/",
        reset_portal_password,
        name="reset_password",
    ),

]