# Generated by Django 4.1.4 on 2023-03-07 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance_app', '0003_alter_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='attendance_app.employee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='picture',
            field=models.ImageField(upload_to='static/pictures'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
    ]
