from django.db import models
from django.utils.text import slugify


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to="team/")
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True, db_index=True)
    skills = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ["order", "name"]

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug or "team-member"
        i = 2
        Model = self.__class__
        while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)