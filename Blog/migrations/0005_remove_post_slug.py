# Generated by Django 4.1.6 on 2023-02-09 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]