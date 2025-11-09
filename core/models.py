from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField()
    # Optional media for hero visual
    hero_media_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    hero_media_video = models.FileField(upload_to="hero/", blank=True, null=True)
    # Secondary hero content
    hero2_title = models.CharField(max_length=255, blank=True)
    hero2_subtitle = models.TextField(blank=True)
    hero2_media_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    hero2_media_video = models.FileField(upload_to="hero/", blank=True, null=True)
    # Process graphic (roadmap/screenshot)
    process_graphic = models.ImageField(upload_to="branding/", blank=True, null=True)
    # CTA section content
    cta_headline_line1 = models.CharField(max_length=255, blank=True)
    cta_headline_line2 = models.CharField(max_length=255, blank=True)
    cta_headline_line3 = models.CharField(max_length=255, blank=True)
    cta_button_text = models.CharField(max_length=100, blank=True)
    cta_button_url = models.URLField(blank=True)
    # Carousel settings
    projects_carousel_interval = models.PositiveIntegerField(default=5, help_text="Seconds between slides for Featured Projects")
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    footer_text = models.TextField(blank=True)

    def __str__(self):
        return self.site_name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    client_photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    def __str__(self):
        return f"{self.client_name} - {self.company}" if self.company else self.client_name


class ClientLogo(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="clients/")
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class AudienceSegment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to="branding/", blank=True, null=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text="Optional Font Awesome class, e.g., fa-users")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class FeaturedService(models.Model):
    """Homepage-only Featured Service cards, managed separately from Services."""
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    image = models.ImageField(upload_to="services/icons/", blank=True, null=True)
    link_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Featured Service (Homepage)"
        verbose_name_plural = "Featured Services (Homepage)"

    def __str__(self):
        return self.title