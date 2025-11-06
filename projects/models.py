from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    full_description = models.TextField()
    technologies = models.CharField(max_length=255)
    image = models.ImageField(upload_to="projects/main/")
    gallery = models.ManyToManyField(
        'ProjectImage',
        blank=True,
        related_name='used_in_projects',
        related_query_name='used_in_projects',
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "-created_at"]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")

    def __str__(self):
        return f"Image for {self.project.title}"

# Optional M2M gallery if needed; some teams prefer explicit FK usage only.
# To match prompt explicitly, you can add on Project a gallery ManyToMany to ProjectImage via a separate migration.