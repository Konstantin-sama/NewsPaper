# Generated by Django 4.2.5 on 2024-03-05 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idpk', models.IntegerField()),
                ('idpkid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                             to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
