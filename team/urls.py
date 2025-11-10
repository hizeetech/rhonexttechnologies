from django.urls import path
from .views import TeamListView, TeamDetailView


urlpatterns = [
    path("", TeamListView.as_view(), name="team_list"),
    path("<slug:slug>/", TeamDetailView.as_view(), name="team_detail"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team_detail_pk"),
]