# Generated by Django 2.1.3 on 2019-01-31 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ophthalmology', '0022_auto_20190129_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseCausCandGeneDt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'DiseaseCausCandGeneDt',
                'db_table': 'disease_caus_cand_gene_dt',
            },
        ),
        migrations.AddField(
            model_name='patientcausativegeneinfo',
            name='disease_caus_cand_gene_other',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patientcausativegeneinfo',
            name='disease_caus_cand_gene',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='ophthalmology.DiseaseCausCandGeneDt'),
        ),
    ]
