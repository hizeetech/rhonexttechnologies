from django.contrib import admin
from .models import SiteSettings, Testimonial, ClientLogo, AudienceSegment, FeaturedService


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "contact_phone")
    fieldsets = (
        (None, {"fields": ("site_name", "logo", "footer_text")}),
        ("Hero", {"fields": ("hero_title", "hero_subtitle", "hero_media_image", "hero_media_video")}),
        ("Secondary Hero", {"fields": ("hero2_title", "hero2_subtitle", "hero2_media_image", "hero2_media_video")}),
        ("Process Graphic", {"fields": ("process_graphic",)}),
        ("CTA", {"fields": ("cta_headline_line1", "cta_headline_line2", "cta_headline_line3", "cta_button_text", "cta_button_url")}),
        ("Carousel", {"fields": ("projects_carousel_interval",)}),
        ("Contact", {"fields": ("contact_email", "contact_phone", "address")}),
        ("Social", {"fields": ("linkedin", "twitter", "facebook")}),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "company", "position")


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "url")
    list_editable = ("order",)
    search_fields = ("name",)


# Admin branding
admin.site.site_header = "RHONEXT Admin"
admin.site.site_title = "RHONEXT Admin"
admin.site.index_title = "Content Management"
@admin.register(AudienceSegment)
class AudienceSegmentAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "description")


@admin.register(FeaturedService)
class FeaturedServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "short_description")
    fields = ("title", "short_description", "image", "link_url", "order", "is_active")