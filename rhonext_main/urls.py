"""
URL configuration for rhonext_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('services/', include('services.urls')),
    path('projects/', include('projects.urls')),
    path('blog/', include('blog.urls')),
    path('team/', include('team.urls')),
    path('contact/', include('contacts.urls')),
    path('staff/', include('staff.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Use Django's handler404 to render friendly 404 without breaking APPEND_SLASH redirects
handler404 = 'core.views.custom_404'

# Friendly 404 for unknown URLs even in DEBUG, excluding known prefixes
# Use non-capturing groups to prevent passing regex groups to the view
urlpatterns += [
    re_path(r'^(?!(?:admin|services|projects|blog|team|contact|staff|static|media)(?:/|$)).*$', custom_404),
]
