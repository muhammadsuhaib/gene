# Generated by Django 2.1.4 on 2018-12-27 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ophthalmology', '0015_patientgeneralinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientgeneralinfoophthalmologyocularcompli',
            name='other',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patientgeneralinfoophthalmologysystabnormality',
            name='other',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
