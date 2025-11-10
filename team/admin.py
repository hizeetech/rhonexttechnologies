from django.contrib import admin
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "order", "slug")
    list_editable = ("order",)
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "position", "slug")