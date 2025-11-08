from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model as auth_get_user_model
from .models import ToDoItem, StaffReport


class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ["title", "description", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class BaseStaffReportForm(forms.ModelForm):
    # In-app messaging field (not stored on StaffReport; saved separately)
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        label="In-App message",
        help_text="Optional: send a message to selected recipients."
    )

    class Meta:
        model = StaffReport
        fields = ["title", "report_type", "recipients", "date_created", "content", "attachment"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "report_type": forms.Select(attrs={"class": "form-control"}),
            "recipients": forms.SelectMultiple(attrs={"class": "form-control"}),
            "date_created": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "content": forms.Textarea(attrs={"class": "form-control richtext", "rows": 6}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit recipients to active users (could be refined to active staff only)
        User = get_user_model()
        # Only show active users who are active staff (have StaffProfile and is_active=True)
        self.fields["recipients"].queryset = (
            User.objects.filter(is_active=True, staffprofile__is_active=True)
            .order_by("username")
        )


class CEOReportForm(BaseStaffReportForm):
    class Meta(BaseStaffReportForm.Meta):
        fields = BaseStaffReportForm.Meta.fields + ["strategic_focus"]
        widgets = {
            **BaseStaffReportForm.Meta.widgets,
            "strategic_focus": forms.TextInput(attrs={"class": "form-control", "placeholder": "Strategic focus"}),
        }


class COOReportForm(BaseStaffReportForm):
    class Meta(BaseStaffReportForm.Meta):
        fields = BaseStaffReportForm.Meta.fields + ["operations_area"]
        widgets = {
            **BaseStaffReportForm.Meta.widgets,
            "operations_area": forms.TextInput(attrs={"class": "form-control", "placeholder": "Operations area"}),
        }


class CFOReportForm(BaseStaffReportForm):
    class Meta(BaseStaffReportForm.Meta):
        fields = BaseStaffReportForm.Meta.fields + ["amount", "finance_category", "reference_code"]
        widgets = {
            **BaseStaffReportForm.Meta.widgets,
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "finance_category": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category"}),
            "reference_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Reference"}),
        }


class CMOReportForm(BaseStaffReportForm):
    class Meta(BaseStaffReportForm.Meta):
        fields = BaseStaffReportForm.Meta.fields + ["campaign_name", "channel"]
        widgets = {
            **BaseStaffReportForm.Meta.widgets,
            "campaign_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Campaign name"}),
            "channel": forms.TextInput(attrs={"class": "form-control", "placeholder": "Channel"}),
        }


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = auth_get_user_model()
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "your@email.com"}),
        }
        help_texts = {
            "email": "Used for password reset and receiving staff emails.",
        }