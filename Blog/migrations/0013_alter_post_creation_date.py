# Generated by Django 4.1.6 on 2023-02-15 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0012_post_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
