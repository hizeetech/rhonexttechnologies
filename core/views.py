from django.views.generic import TemplateView
from services.models import Service
from projects.models import Project
from .models import SiteSettings, Testimonial, ClientLogo, AudienceSegment


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = SiteSettings.objects.first()
        context["settings"] = settings
        context["featured_services"] = Service.objects.filter(is_featured=True)
        # Show all featured projects ordered by explicit order then newest
        context["featured_projects"] = Project.objects.filter(is_featured=True).order_by("order", "-created_at")
        context["testimonials"] = Testimonial.objects.all()[:10]
        context["client_logos"] = ClientLogo.objects.all()[:12]
        context["audiences"] = AudienceSegment.objects.filter(is_active=True).order_by("order", "name")
        return context


class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = SiteSettings.objects.first()
        return context