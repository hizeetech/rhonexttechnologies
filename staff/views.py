from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from urllib.parse import urlparse
from django.utils import timezone

from .forms import ToDoItemForm, CEOReportForm, COOReportForm, CFOReportForm, CMOReportForm, UserEmailForm
from .models import Notification, Report, ReportAck, Task, ToDoItem, StaffProfile, StaffReport, StaffMessage


def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("staff:login")
        try:
            profile = StaffProfile.objects.get(user=request.user)
        except StaffProfile.DoesNotExist:
            messages.warning(request, "Your account is not linked to an active staff profile.")
            return redirect("staff:no_access")
        if not profile.is_active:
            messages.warning(request, "Your staff profile is inactive. Please contact an administrator.")
            return redirect("staff:no_access")
        return view_func(request, *args, **kwargs)
    return _wrapped


class StaffLoginView(LoginView):
    template_name = "staff/login.html"
    redirect_authenticated_user = True


class StaffLogoutView(LogoutView):
    next_page = reverse_lazy("staff:login")


@staff_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by("-created_at")
    todos = ToDoItem.objects.filter(created_by=request.user).order_by("-created_at")
    reports = Report.objects.filter(recipients=request.user).order_by("-created_at")
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by("-created_at")[:10]
    try:
        role = StaffProfile.objects.get(user=request.user).get_role_display()
    except StaffProfile.DoesNotExist:
        role = "Staff"
    return render(
        request,
        "staff/dashboard.html",
        {
            "tasks": tasks,
            "todos": todos,
            "reports": reports,
            "notifications": notifications,
            "role": role,
            "has_email": bool(getattr(request.user, "email", "")),
        },
    )


@staff_required
def todos_add(request):
    if request.method == "POST":
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.created_by = request.user
            todo.save()
            Notification.objects.create(
                recipient=request.user,
                message=f"To-do '{todo.title}' created.",
            )
            return redirect("staff:dashboard")
    else:
        form = ToDoItemForm()
    return render(request, "staff/todo_form.html", {"form": form})


@staff_required
def todos_mark_complete(request, pk):
    todo = get_object_or_404(ToDoItem, pk=pk, created_by=request.user)
    todo.status = "AWAITING_APPROVAL"
    todo.completed_at = timezone.now()
    todo.save()
    Notification.objects.create(
        recipient=request.user,
        message=f"To-do '{todo.title}' submitted for approval.",
    )
    return redirect("staff:dashboard")


@staff_required
def tasks_list(request):
    tasks = Task.objects.filter(assigned_to=request.user).order_by("-created_at")
    return render(request, "staff/tasks_list.html", {"tasks": tasks})


@staff_required
def task_ack_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    task.status = "COMPLETED"
    task.save()
    Notification.objects.create(
        recipient=request.user,
        message=f"Task '{task.title}' marked completed.",
    )
    from django.contrib.auth import get_user_model
    for admin in get_user_model().objects.filter(is_superuser=True):
        Notification.objects.create(
            recipient=admin,
            message=f"{request.user.username} acknowledged completion of task '{task.title}'.",
        )
    return redirect("staff:dashboard")


@staff_required
def reports_list(request):
    reports = Report.objects.filter(recipients=request.user).order_by("-created_at")
    return render(request, "staff/reports_list.html", {"reports": reports})


@staff_required
def reports_submit(request):
    try:
        profile = StaffProfile.objects.get(user=request.user)
        role_code = profile.role
        role_label = profile.get_role_display()
    except StaffProfile.DoesNotExist:
        role_code = "COO"
        role_label = "COO"

    form_class = {
        "CEO_MD": CEOReportForm,
        "COO": COOReportForm,
        "CFO": CFOReportForm,
        "CMO": CMOReportForm,
    }.get(role_code, COOReportForm)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            sr = form.save(commit=False)
            sr.submitted_by = request.user
            sr.role = role_code
            sr.status = "SUBMITTED"
            # If user provided date_created, keep it; else None (admin sees created_at)
            sr.save()
            # Save recipients selection
            recipients = form.cleaned_data.get("recipients")
            if recipients is not None:
                sr.recipients.set(recipients)
            Notification.objects.create(
                recipient=request.user,
                message=f"{sr.get_role_display()} report '{sr.title}' submitted.",
                link=reverse("staff:staff_report_detail", args=[sr.pk]),
            )
            from django.contrib.auth import get_user_model
            for admin in get_user_model().objects.filter(is_superuser=True):
                Notification.objects.create(
                    recipient=admin,
                    message=f"New {sr.get_role_display()} report submitted by {request.user.username}: '{sr.title}'.",
                    link=reverse("staff:staff_report_detail", args=[sr.pk]),
                )
            # Notify recipients they have received the report
            if recipients:
                for r in recipients:
                    Notification.objects.create(
                        recipient=r,
                        message=f"You were shared the {sr.get_role_display()} report '{sr.title}'.",
                        link=reverse("staff:staff_report_detail", args=[sr.pk]),
                    )
            # Create in-app message if provided
            msg_text = form.cleaned_data.get("message")
            if msg_text:
                msg = StaffMessage.objects.create(sender=request.user, content=msg_text, report=sr)
                if recipients:
                    msg.recipients.set(recipients)
                # Notify recipients of the message
                if recipients:
                    for r in recipients:
                        Notification.objects.create(
                            recipient=r,
                            message=f"New message regarding report '{sr.title}'.",
                            link=reverse("staff:staff_message_detail", args=[msg.pk]),
                        )
            return redirect("staff:dashboard")
    else:
        form = form_class()
    return render(request, "staff/report_form.html", {"form": form, "role_code": role_code, "role_label": role_label})


@staff_required
def report_ack(request, pk):
    report = get_object_or_404(Report, pk=pk)
    ack, _ = ReportAck.objects.get_or_create(report=report, user=request.user)
    ack.acknowledged = True
    ack.acknowledged_at = timezone.now()
    ack.save()
    Notification.objects.create(
        recipient=request.user,
        message=f"Report '{report.title}' acknowledged.",
    )
    return redirect("staff:reports")


@staff_required
def notification_mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save()
    return redirect("staff:dashboard")


@staff_required
def notification_view(request, pk):
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    # Do not auto-mark read to allow explicit action; provide button in template.
    context = {"notification": notif}
    if notif.link:
        try:
            path = urlparse(notif.link).path
            # staff report detail
            import re
            m = re.match(r"^/staff/staff-reports/(\d+)/$", path)
            if m:
                report = get_object_or_404(StaffReport, pk=int(m.group(1)))
                # authorization: submitter, recipient, or superuser
                if report.submitted_by == request.user or report.recipients.filter(pk=request.user.pk).exists() or request.user.is_superuser:
                    context["report"] = report
            m2 = re.match(r"^/staff/messages/(\d+)/$", path)
            if m2:
                msg = get_object_or_404(StaffMessage, pk=int(m2.group(1)))
                if msg.sender == request.user or msg.recipients.filter(pk=request.user.pk).exists() or request.user.is_superuser:
                    context["staff_message"] = msg
        except Exception:
            pass
    # Fallback: infer from notification text when link is missing
    if "report" not in context and "staff_message" not in context:
        import re
        title_match = re.search(r"report '([^']+)'", notif.message or "")
        if title_match:
            title = title_match.group(1)
            sr = StaffReport.objects.filter(title=title).order_by("-created_at").first()
            if sr and (sr.submitted_by == request.user or sr.recipients.filter(pk=request.user.pk).exists() or request.user.is_superuser):
                context["report"] = sr
                # try to fetch a related message
                msg = (
                    StaffMessage.objects.filter(report=sr)
                    .filter(Q(sender=request.user) | Q(recipients__pk=request.user.pk))
                    .order_by("-created_at")
                    .first()
                )
                if msg:
                    context["staff_message"] = msg
    return render(request, "staff/notification_detail.html", context)


@staff_required
def staff_report_detail(request, pk):
    sr = get_object_or_404(StaffReport, pk=pk)
    if not (sr.submitted_by == request.user or sr.recipients.filter(pk=request.user.pk).exists() or request.user.is_superuser):
        return redirect("staff:dashboard")
    return render(request, "staff/staff_report_detail.html", {"report": sr})


@staff_required
def staff_message_detail(request, pk):
    msg = get_object_or_404(StaffMessage, pk=pk)
    if not (msg.sender == request.user or msg.recipients.filter(pk=request.user.pk).exists() or request.user.is_superuser):
        return redirect("staff:dashboard")
    return render(request, "staff/staff_message_detail.html", {"message": msg})

def no_access(request):
    try:
        profile = StaffProfile.objects.get(user=request.user)
        is_active = profile.is_active
    except StaffProfile.DoesNotExist:
        profile = None
        is_active = False
    context = {
        "profile": profile,
        "is_active": is_active,
    }
    return render(request, "staff/no_access.html", context)
@staff_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserEmailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                recipient=user,
                message="Profile updated: email saved.",
            )
            messages.success(request, "Email saved successfully.")
            return redirect("staff:profile")
    else:
        form = UserEmailForm(instance=user)
    return render(request, "staff/profile.html", {"form": form})

@staff_required
def email_test(request):
    user = request.user
    recipient = getattr(user, "email", "")
    context = {}
    if not recipient:
        context["error"] = "No email set on your profile. Please add your email."
    else:
        from django.core.mail import send_mail
        from django.conf import settings
        try:
            send_mail(
                subject="RHONEXT Test Email",
                message="This is a quick test email from RHONEXT staff portal.",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None),
                recipient_list=[recipient],
                fail_silently=False,
            )
            context["success"] = f"Sent test email to {recipient}."
        except Exception as e:
            context["error"] = f"Failed to send email: {e}"
    return render(request, "staff/email_test_result.html", context)