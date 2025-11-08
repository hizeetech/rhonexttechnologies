from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import StaffProfile, Task, ToDoItem, Report, ReportAck, Notification, StaffReport, StaffMessage
from django.utils import timezone


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_active", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("user__username", "user__email")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "status", "priority", "deadline", "created_at")
    list_filter = ("status", "priority")
    search_fields = ("title", "assigned_to__username")


@admin.action(description="Approve selected to-do items")
def approve_todos(modeladmin, request, queryset):
    for todo in queryset:
        todo.status = "APPROVED"
        todo.approved_by = request.user
        todo.approval_comment = todo.approval_comment or "Approved"
        todo.completed_at = todo.completed_at or timezone.now()
        todo.save()
        Notification.objects.create(
            recipient=todo.created_by,
            message=f"Your to-do '{todo.title}' was approved.",
        )


@admin.action(description="Reject selected to-do items")
def reject_todos(modeladmin, request, queryset):
    for todo in queryset:
        todo.status = "NEEDS_REVIEW"
        todo.approved_by = request.user
        if not todo.approval_comment:
            todo.approval_comment = "Please revise and resubmit."
        todo.save()
        Notification.objects.create(
            recipient=todo.created_by,
            message=f"Your to-do '{todo.title}' needs review.",
        )


@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "status", "due_date", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "created_by__username")
    actions = [approve_todos, reject_todos]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_type", "created_at")
    list_filter = ("report_type",)
    search_fields = ("title",)
    filter_horizontal = ("recipients",)


@admin.register(ReportAck)
class ReportAckAdmin(admin.ModelAdmin):
    list_display = ("report", "user", "acknowledged", "acknowledged_at")
    list_filter = ("acknowledged",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "message", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("recipient__username", "message")


@admin.action(description="Approve selected staff reports")
def approve_staff_reports(modeladmin, request, queryset):
    for sr in queryset:
        sr.status = "APPROVED"
        sr.save()
        Notification.objects.create(
            recipient=sr.submitted_by,
            message=f"Your {sr.get_role_display()} report '{sr.title}' was approved.",
        )


@admin.action(description="Request revisions on selected staff reports")
def request_revision_staff_reports(modeladmin, request, queryset):
    for sr in queryset:
        sr.status = "NEEDS_REVIEW"
        sr.save()
        Notification.objects.create(
            recipient=sr.submitted_by,
            message=f"Your {sr.get_role_display()} report '{sr.title}' needs review.",
        )


@admin.register(StaffReport)
class StaffReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_type", "role", "submitted_by", "status", "created_at")
    list_filter = ("role", "status", "report_type")
    search_fields = ("title", "submitted_by__username")
    actions = [approve_staff_reports, request_revision_staff_reports]


@admin.register(StaffMessage)
class StaffMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "report", "created_at", "short_content")
    search_fields = ("sender__username", "content")
    filter_horizontal = ("recipients",)

    def short_content(self, obj):
        return (obj.content[:60] + ("..." if len(obj.content) > 60 else ""))
    short_content.short_description = "Message"