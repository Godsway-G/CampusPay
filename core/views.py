from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)

from .mixins import (
    CampusLoginRequiredMixin,
    SuccessMessageMixin
)

from django.shortcuts import render

def home(request):
    return render(request, "home.html")



class BaseListView(
    CampusLoginRequiredMixin,
    ListView
):
    paginate_by = 20


class BaseCreateView(
    CampusLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    pass


class BaseUpdateView(
    CampusLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    pass


class BaseDeleteView(
    CampusLoginRequiredMixin,
    DeleteView
):
    pass


class BaseDetailView(
    CampusLoginRequiredMixin,
    DetailView
):
    pass