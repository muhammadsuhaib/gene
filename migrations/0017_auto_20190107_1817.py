# Generated by Django 2.1.4 on 2019-01-07 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ophthalmology', '0016_auto_20181227_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientgeneralinfo',
            name='admin_sub_disease_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patientgeneralinfo',
            name='sub_disease',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ophthalmology.SubDiseaseDt'),
        ),
    ]