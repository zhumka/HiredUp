# Generated by Django 5.1.1 on 2024-11-01 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_jobseekerprofile_profession_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resume',
            name='job_seeker_profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='users.jobseekerprofile'),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='resume',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.resume'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='experience',
            field=models.TextField(blank=True, null=True, verbose_name='Опыт работы (в годах)'),
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('employer', 'Employer'), ('job_seeker', 'Job Seeker'), ('moderator', 'Moderator')], max_length=20, verbose_name='Тип пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_type', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]