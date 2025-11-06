from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_sitesettings_projects_carousel_interval'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='hero2_title',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero2_subtitle',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero2_media_image',
            field=models.ImageField(upload_to='hero/', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero2_media_video',
            field=models.FileField(upload_to='hero/', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='cta_headline_line1',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='cta_headline_line2',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='cta_headline_line3',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='cta_button_text',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='cta_button_url',
            field=models.URLField(blank=True),
        ),
        migrations.CreateModel(
            name='AudienceSegment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('icon', models.ImageField(upload_to='branding/', blank=True, null=True)),
                ('icon_class', models.CharField(max_length=100, blank=True, help_text='Optional Font Awesome class, e.g., fa-users')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
    ]