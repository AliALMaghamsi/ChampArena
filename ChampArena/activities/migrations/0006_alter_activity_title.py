# Generated by Django 5.1.4 on 2024-12-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_activity_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]