# Generated by Django 5.1.5 on 2025-02-04 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0008_remove_course_general_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralCoursePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
