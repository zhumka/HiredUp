# Generated by Django 5.1.1 on 2024-12-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_employerprofile_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='users/static/users/img/defaultUserAvatar.svg', null=True, upload_to='users/static/users/img', verbose_name='Аватар'),
        ),
    ]
