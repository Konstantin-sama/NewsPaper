# Generated by Django 4.2.5 on 2023-12-23 23:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='authorUser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authors',
                                       to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, max_length=64, related_name='categories',
                                         to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commentUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
