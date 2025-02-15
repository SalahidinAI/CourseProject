# Generated by Django 5.1.5 on 2025-02-02 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0003_alter_teacher_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images'),
        ),
        migrations.AlterField(
            model_name='coursereview',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_review', to='course_app.course'),
        ),
    ]
