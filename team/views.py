from django.views.generic import ListView
from .models import TeamMember


class TeamListView(ListView):
    model = TeamMember
    template_name = "team/list.html"
    context_object_name = "team"
    queryset = TeamMember.objects.all().order_by("order", "name")