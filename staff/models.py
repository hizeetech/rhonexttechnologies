from django.conf import settings
from django.db import models
from django.utils import timezone


class StaffProfile(models.Model):
    ROLE_CHOICES = [
        ("CEO_MD", "CEO/Managing Director"),
        ("COO", "COO (Admin/Operations)"),
        ("CFO", "CFO (Finance)"),
        ("CMO", "Chief Marketing Officer"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("REJECTED", "Rejected"),
    ]
    PRIORITY_CHOICES = [("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_tasks")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="PENDING")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} → {self.assigned_to}" 


class ToDoItem(models.Model):
    TODO_STATUS = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("AWAITING_APPROVAL", "Awaiting Approval"),
        ("APPROVED", "Approved"),
        ("NEEDS_REVIEW", "Needs Review"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todos")
    status = models.CharField(max_length=18, choices=TODO_STATUS, default="PENDING")
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="approved_todos")
    approval_comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.created_by})"


class Report(models.Model):
    REPORT_TYPE = [("WEEKLY", "Weekly"), ("MONTHLY", "Monthly"), ("SPECIAL", "Special")]
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="reports/", blank=True)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="reports", blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"


class ReportAck(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="acks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("report", "user")

    def __str__(self):
        return f"Ack {self.user} → {self.report}: {self.acknowledged}"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.recipient}: {self.message}"


class StaffReport(models.Model):
    ROLE_CHOICES = [
        ("CEO_MD", "CEO/Managing Director"),
        ("COO", "COO (Admin/Operations)"),
        ("CFO", "CFO (Finance)"),
        ("CMO", "Chief Marketing Officer"),
    ]

    REPORT_TYPE = [("WEEKLY", "Weekly"), ("MONTHLY", "Monthly"), ("SPECIAL", "Special")]

    STATUS_CHOICES = [
        ("SUBMITTED", "Submitted"),
        ("APPROVED", "Approved"),
        ("NEEDS_REVIEW", "Needs Review"),
    ]

    title = models.CharField(max_length=200)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to="staff_reports/", blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_reports")
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default="SUBMITTED")
    created_at = models.DateTimeField(default=timezone.now)
    # New fields
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE, default="WEEKLY")
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="staff_reports_received", blank=True)
    date_created = models.DateField(null=True, blank=True)

    # Role-specific supplemental fields
    # COO
    operations_area = models.CharField(max_length=120, blank=True)
    # CFO
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    finance_category = models.CharField(max_length=120, blank=True)
    reference_code = models.CharField(max_length=120, blank=True)
    # CMO
    campaign_name = models.CharField(max_length=160, blank=True)
    channel = models.CharField(max_length=120, blank=True)
    # CEO
    strategic_focus = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return f"{self.get_role_display()} Report: {self.title} by {self.submitted_by}"


class StaffMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_messages_sent")
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="staff_messages_received", blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    report = models.ForeignKey(StaffReport, null=True, blank=True, on_delete=models.SET_NULL, related_name="messages")

    def __str__(self):
        preview = (self.content[:30] + ("..." if len(self.content) > 30 else ""))
        return f"Msg by {self.sender}: {preview}"