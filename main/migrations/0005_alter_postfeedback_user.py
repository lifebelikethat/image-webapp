# Generated by Django 4.2.11 on 2024-04-24 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfeedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='feedback', to=settings.AUTH_USER_MODEL),
        ),
    ]
