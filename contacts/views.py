from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import ContactForm


class ContactView(TemplateView):
    template_name = "contacts/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent.")
            return redirect("contact")
        messages.error(request, "Please correct the errors below.")
        return self.get(request, *args, **kwargs)