from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    StaffLoginView,
    StaffLogoutView,
    dashboard,
    profile,
    tasks_list,
    task_ack_complete,
    reports_list,
    reports_submit,
    report_ack,
    todos_add,
    todos_mark_complete,
    notification_mark_read,
    notification_view,
    staff_report_detail,
    staff_message_detail,
    email_test,
)

app_name = "staff"

urlpatterns = [
    path("login/", StaffLoginView.as_view(), name="login"),
    path("logout/", StaffLogoutView.as_view(), name="logout"),
    # Password reset
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="staff/password_reset_form.html", email_template_name="staff/password_reset_email.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="staff/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="staff/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="staff/password_reset_complete.html"), name="password_reset_complete"),
    path("dashboard/", dashboard, name="dashboard"),
    path("profile/", profile, name="profile"),
    path("email-test/", email_test, name="email_test"),
    path("tasks/", tasks_list, name="tasks"),
    path("tasks/<int:pk>/ack-complete/", task_ack_complete, name="task_ack_complete"),
    path("reports/", reports_list, name="reports"),
    path("reports/submit/", reports_submit, name="report_submit"),
    path("reports/<int:pk>/ack/", report_ack, name="report_ack"),
    path("todos/add/", todos_add, name="todos_add"),
    path("todos/<int:pk>/complete/", todos_mark_complete, name="todos_complete"),
    path("notifications/<int:pk>/read/", notification_mark_read, name="notification_read"),
    path("notifications/<int:pk>/view/", notification_view, name="notification_view"),
    path("staff-reports/<int:pk>/", staff_report_detail, name="staff_report_detail"),
    path("messages/<int:pk>/", staff_message_detail, name="staff_message_detail"),
]