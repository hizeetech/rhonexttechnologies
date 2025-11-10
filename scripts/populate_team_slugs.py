import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rhonext_main.settings")
django.setup()

from team.models import TeamMember

updated = 0
for m in TeamMember.objects.all():
    if not m.slug:
        m.save()
        updated += 1

print(f"Populated slugs for {updated} team members.")