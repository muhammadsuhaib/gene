# Generated by Django 2.1.3 on 2018-12-22 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ophthalmology', '0013_auto_20181220_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDiseaseDt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'AdminDiseaseDt',
                'db_table': 'admin_disease_dt',
            },
        ),
        migrations.CreateModel(
            name='AdminSubDiseaseDt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ophthalmology.AdminDiseaseDt')),
            ],
            options={
                'verbose_name_plural': 'AdminSubDiseaseDt',
                'db_table': 'admin_sub_disease_dt',
            },
        ),
        migrations.RemoveField(
            model_name='patientcausativegeneinfolocalpopulation',
            name='freq_ethnicity_other',
        ),
        migrations.RemoveField(
            model_name='patientcausativegeneinfolocalpopulation',
            name='freq_ethnicity_per',
        ),
        migrations.AddField(
            model_name='patientcausativegeneinfolocalpopulation',
            name='freq_local_population_other',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patientcausativegeneinfolocalpopulation',
            name='freq_local_population_per',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='affecteddt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ageatonsetclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ageatonsetofocularsymptomdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ageattheinitialdiagnosisclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ageattheinitialdiagnosisdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='agecategorydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ageforsurgerydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='aidiagnosisforagerelatedmaculardegenerationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='aidiagnosisforcornealdiseasesdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='aidiagnosisfordiabeticretinopathydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='aidiagnosisforglaucomadt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='aidiagnosisforinheritedretinaldiseasesdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='allelefrequencydatabasedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='analysisdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='axiallengthclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='axiallengthdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bilateraldt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='causcanddt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='chromosomedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='consanguineousdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='countryoforigindt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='diseasedt',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='dnaextractioninprocessdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='electrophysiologicalfindingsdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ethnicitydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='exondt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='familyhistorydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='fluctuationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='fullfieldelectrophysiologicalgroupingdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='genedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='hconmedicationornotinsulindt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='hconmedicationornotstatindt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='inheritancedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='institutedt',
            name='institute_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='institutedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='intraocularpressureclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='intraocularpressuredt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='lensdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='multifocalelectrophysiologicalgroupingdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='mutationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='numberofaffectedmembersinthesamepedigreedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='numberofsurgerydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularcomplicationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularmedicationinternaldt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularmedicationtopicaldt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsurgeriescataractdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsurgeriescorneadt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsurgeriesglaucomadt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsurgerieslasersdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsurgeriesretinadt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsurgeriesvitreousinfectiondt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ocularsymptomdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='onmedicationornotdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmicmedicationsubtenonorsubconjunctivalinjectiondt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologyagerelatedmaculardegenerationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologycataractdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologycornealdiseasesdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologydiableticretinopathydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologyglaucomadt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologymyopiadt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologynormaldt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologyothersdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologyretinalarteryveinocculusiondt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ophthalmologyuveitisdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='originprefectureinjapandt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patientcandidategenemutationinfo',
            name='candidate_mutation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfo',
            name='caus_cand_mutation_nucleotide_amino_acid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfo',
            name='caus_cand_mutation_nucleotide_amino_acid_comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfo',
            name='chromosome_comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfo',
            name='exon_comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfo',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfo',
            name='transcript',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfoethnicity',
            name='freq_ethnicity_other',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientcausativegeneinfoethnicity',
            name='freq_ethnicity_per',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfo',
            name='gene_inheritance_mutation_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfo',
            name='overall_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfo',
            name='patient_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfo',
            name='registration',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfo',
            name='sample_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfofamily',
            name='family_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patientgeneralinfoophthalmology',
            name='gene_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='beadarray_platform_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='beadarray_platform_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='direct_sequencing_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='direct_sequencing_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='direct_sequencing_3_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='direct_sequencing_4_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='direct_sequencing_5_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='exome_sequencing_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='exome_sequencing_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='mitochondria_ngs_whole_gene_sequence_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='mitochondria_ngs_whole_gene_sequence_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='other_analysis_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='other_sequencing_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='sequencing_other_collaborators_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='sequencing_other_collaborators_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='sequencing_other_collaborators_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='sequencing_other_collaborators_analysis_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_3_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_4_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_5_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_analysis_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_analysis_3_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_analysis_4_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_enrichment_ngs_panel_analysis_5_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_exome_sequencing_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_exome_sequencing_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_exome_sequencing_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_exome_sequencing_analysis_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_mitochondrial_hot_spot_panel_sequence_3_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_mitochondrial_sequence_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='targt_mitochondrial_sequence_analysis_2_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='whole_exome_sequencing_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientothercommoninfo',
            name='whole_exome_sequencing_analysis_1_comments',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='presentunpresentdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='progressiondt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='refractiveerrorsphericalequivalentclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='refractiveerrorsphericalequivalentdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='relationshiptoprobanddt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sequencingdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sequencingstatusdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sexdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='staticperimetrymeansensitivityclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='staticperimetrymeansensitivitydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='subdiseasedt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='syndromicdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='systemicabnormalitydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='typeoldnewdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='typicaldt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='visualacuityclassificationdt',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='visualacuitydt',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
