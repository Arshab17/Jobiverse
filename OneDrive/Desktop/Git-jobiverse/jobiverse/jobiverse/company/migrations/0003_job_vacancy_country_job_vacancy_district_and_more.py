# Generated by Django 4.1.7 on 2023-07-14 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job_vacancy',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='district',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='experience_from',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='experience_to',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='salary_from',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='salary_to',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='job_vacancy',
            name='vacancy',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(blank=True, max_length=10, null=True)),
                ('job_vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.job_vacancy')),
            ],
        ),
    ]
