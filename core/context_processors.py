from .models import SiteSettings
from django.conf import settings
from django.utils import timezone


def site_settings(request):
    """Inject SiteSettings globally so base templates can access the logo and metadata."""
    return {
        "settings": SiteSettings.objects.first(),
        "static_version": getattr(settings, "STATIC_VERSION", "v1"),
        "now": timezone.now(),
    }