# Generated by Django 4.0.3 on 2022-03-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
