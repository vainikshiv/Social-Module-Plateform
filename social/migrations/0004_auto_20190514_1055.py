# Generated by Django 2.1.7 on 2019-05-14 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
