# Generated by Django 5.1.1 on 2024-11-03 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_jobseekerprofile_profession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='company_logo',
            field=models.ImageField(default='Изображение отсутствует', upload_to='users/static/users/img'),
        ),
    ]
