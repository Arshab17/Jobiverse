# Generated by Django 4.1.7 on 2023-07-01 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_account.employee'),
        ),
        migrations.AddField(
            model_name='notification',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.job_vacancy'),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='applicants',
            field=models.ManyToManyField(related_name='job_applied', to='employee_account.employee'),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
        migrations.AddField(
            model_name='job_application',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
        migrations.AddField(
            model_name='job_application',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee_account.employee'),
        ),
        migrations.AddField(
            model_name='job_application',
            name='job_vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.job_vacancy'),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
