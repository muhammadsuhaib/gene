# Generated by Django 2.1.3 on 2019-02-01 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ophthalmology', '0025_auto_20190131_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientcandidategenemutationinfo',
            name='candidate_gene',
        ),
        migrations.RemoveField(
            model_name='patientcandidategenemutationinfo',
            name='patient_id',
        ),
        migrations.DeleteModel(
            name='PatientCandidateGeneMutationInfo',
        ),
    ]
