from django.views.generic import ListView, DetailView
from .models import TeamMember


class TeamListView(ListView):
    model = TeamMember
    template_name = "team/list.html"
    context_object_name = "team"
    queryset = TeamMember.objects.all().order_by("order", "name")


class TeamDetailView(DetailView):
    model = TeamMember
    template_name = "team/detail.html"
    context_object_name = "member"
    slug_field = "slug"
    slug_url_kwarg = "slug"