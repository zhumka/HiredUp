# Generated by Django 5.1.1 on 2024-10-03 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='category',
        ),
        migrations.RemoveField(
            model_name='job',
            name='employer',
        ),
        migrations.DeleteModel(
            name='JobCategory',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
    ]
