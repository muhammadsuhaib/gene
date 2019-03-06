from django.db import models
from django.contrib.auth.models import User


class AffectedDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'affected_dt'
        verbose_name_plural = 'AffectedDt'


class AgeAtOnsetClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'age_at_onset_classification_dt'
        verbose_name_plural = 'AgeAtOnsetClassificationDt'


class AgeAtOnsetOfOcularSymptomDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'age_at_onset_of_ocular_symptom_dt'
        verbose_name_plural = 'AgeAtOnsetOfOcularSymptomDt'


class AgeAtTheInitialDiagnosisClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'age_at_the_initial_diagnosis_classification_dt'
        verbose_name_plural = 'AgeAtTheInitialDiagnosisClassificationDt'


class AgeAtTheInitialDiagnosisDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'age_at_the_initial_diagnosis_dt'
        verbose_name_plural = 'AgeAtTheInitialDiagnosisDt'


class AgeCategoryDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'age_category_dt'
        verbose_name_plural = 'AgeCategoryDt'


class AgeForSurgeryDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'age_for_surgery_dt'
        verbose_name_plural = 'AgeForSurgeryDt'


class AiDiagnosisForAgeRelatedMacularDegenerationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_diagnosis_for_age_related_macular_degeneration_dt'
        verbose_name_plural = 'AiDiagnosisForAgeRelatedMacularDegenerationDt'


class AiDiagnosisForCornealDiseasesDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_diagnosis_for_corneal_diseases_dt'
        verbose_name_plural = 'AiDiagnosisForCornealDiseasesDt'


class AiDiagnosisForDiabeticRetinopathyDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_diagnosis_for_diabetic_retinopathy_dt'
        verbose_name_plural = 'AiDiagnosisForDiabeticRetinopathyDt'


class AiDiagnosisForGlaucomaDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_diagnosis_for_glaucoma_dt'
        verbose_name_plural = 'AiDiagnosisForGlaucomaDt'


class AiDiagnosisForInheritedRetinalDiseasesDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_diagnosis_for_inherited_retinal_diseases_dt'
        verbose_name_plural = 'AiDiagnosisForInheritedRetinalDiseasesDt'


class AlleleFrequencyDatabaseDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'allele_frequency_database_dt'
        verbose_name_plural = 'AlleleFrequencyDatabaseDt'


class AxialLengthClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'axial_length_classification_dt'
        verbose_name_plural = 'AxialLengthClassificationDt'


class AxialLengthDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'axial_length_dt'
        verbose_name_plural = 'AxialLengthDt'


class BilateralDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'bilateral_dt'
        verbose_name_plural = 'BilateralDt'


class ConsanguineousDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'consanguineous_dt'
        verbose_name_plural = 'ConsanguineousDt'


class CountryOfOriginDt(models.Model):
	name = models.CharField(max_length=255)
	
	class Meta:
		db_table = 'country_of_origin_dt'
		verbose_name_plural = 'CountryOfOriginDt'
		
	def __str__(self):
		return self.name
	


class ElectrophysiologicalFindingsDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'electrophysiological_findings_dt'
        verbose_name_plural = 'ElectrophysiologicalFindingsDt'


class EthnicityDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ethnicity_dt'
        verbose_name_plural = 'EthnicityDt'


class FamilyHistoryDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'family_history_dt'
        verbose_name_plural = 'FamilyHistoryDt'


class FluctuationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'fluctuation_dt'
        verbose_name_plural = 'FluctuationDt'


class FullFieldElectrophysiologicalGroupingDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'full_field_electrophysiological_grouping_dt'
        verbose_name_plural = 'FullFieldElectrophysiologicalGroupingDt'


class HcOnMedicationOrNotInsulinDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'hc_on_medication_or_not_insulin_dt'
        verbose_name_plural = 'HcOnMedicationOrNotInsulinDt'


class HcOnMedicationOrNotStatinDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'hc_on_medication_or_not_statin_dt'
        verbose_name_plural = 'HcOnMedicationOrNotStatinDt'


class InheritanceDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'inheritance_dt'
        verbose_name_plural = 'InheritanceDt'


class IntraocularPressureClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'intraocular_pressure_classification_dt'
        verbose_name_plural = 'IntraocularPressureClassificationDt'


class IntraocularPressureDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'intraocular_pressure_dt'
        verbose_name_plural = 'IntraocularPressureDt'


class LensDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'lens_dt'
        verbose_name_plural = 'LensDt'


class MultifocalElectrophysiologicalGroupingDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'multifocal_electrophysiological_grouping_dt'
        verbose_name_plural = 'MultifocalElectrophysiologicalGroupingDt'


class NumberOfAffectedMembersInTheSamePedigreeDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'number_of_affected_members_in_the_same_pedigree_dt'
        verbose_name_plural = 'NumberOfAffectedMembersInTheSamePedigreeDt'


class NumberOfSurgeryDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'number_of_surgery_dt'
        verbose_name_plural = 'NumberOfSurgeryDt'


class OcularComplicationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_complication_dt'
        verbose_name_plural = 'OcularComplicationDt'


class OcularMedicationInternalDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_medication_internal_dt'
        verbose_name_plural = 'OcularMedicationInternalDt'


class OcularMedicationTopicalDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_medication_topical_dt'
        verbose_name_plural = 'OcularMedicationTopicalDt'


class OcularSurgeriesCataractDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_surgeries_cataract_dt'
        verbose_name_plural = 'OcularSurgeriesCataractDt'


class OcularSurgeriesCorneaDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_surgeries_cornea_dt'
        verbose_name_plural = 'OcularSurgeriesCorneaDt'


class OcularSurgeriesGlaucomaDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_surgeries_glaucoma_dt'
        verbose_name_plural = 'OcularSurgeriesGlaucomaDt'


class OcularSurgeriesLasersDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_surgeries_lasers_dt'
        verbose_name_plural = 'OcularSurgeriesLasersDt'


class OcularSurgeriesRetinaDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_surgeries_retina_dt'
        verbose_name_plural = 'OcularSurgeriesRetinaDt'


class OcularSurgeriesVitreousInfectionDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_surgeries_vitreous_infection_dt'
        verbose_name_plural = 'OcularSurgeriesVitreousInfectionDt'


class OcularSymptomDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ocular_symptom_dt'
        verbose_name_plural = 'OcularSymptomDt'


class OnMedicationOrNotDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'on_medication_or_not_dt'
        verbose_name_plural = 'OnMedicationOrNotDt'


class OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmic_medication_subtenon_or_subconjunctival_injection_dt'
        verbose_name_plural = 'OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt'


class OphthalmologyAgeRelatedMacularDegenerationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_age_related_macular_degeneration_dt'
        verbose_name_plural = 'OphthalmologyAgeRelatedMacularDegenerationDt'


class OphthalmologyCataractDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_cataract_dt'
        verbose_name_plural = 'OphthalmologyCataractDt'


class OphthalmologyCornealDiseasesDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_corneal_diseases_dt'
        verbose_name_plural = 'OphthalmologyCornealDiseasesDt'


class OphthalmologyDiableticRetinopathyDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_diabletic_retinopathy_dt'
        verbose_name_plural = 'OphthalmologyDiableticRetinopathyDt'


class OphthalmologyGlaucomaDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_glaucoma_dt'
        verbose_name_plural = 'OphthalmologyGlaucomaDt'


class OphthalmologyMyopiaDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_myopia_dt'
        verbose_name_plural = 'OphthalmologyMyopiaDt'


class OphthalmologyNormalDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_normal_dt'
        verbose_name_plural = 'OphthalmologyNormalDt'


class OphthalmologyOthersDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_others_dt'
        verbose_name_plural = 'OphthalmologyOthersDt'


class OphthalmologyRetinalArteryVeinOcculusionDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_retinal_artery_vein_occulusion_dt'
        verbose_name_plural = 'OphthalmologyRetinalArteryVeinOcculusionDt'


class OphthalmologyUveitisDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ophthalmology_uveitis_dt'
        verbose_name_plural = 'OphthalmologyUveitisDt'


class OriginPrefectureInJapanDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'origin_prefecture_in_japan_dt'
        verbose_name_plural = 'OriginPrefectureInJapanDt'


class PresentUnpresentDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'present_unpresent_dt'
        verbose_name_plural = 'PresentUnpresentDt'


class ProgressionDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'progression_dt'
        verbose_name_plural = 'ProgressionDt'


class RefractiveErrorSphericalEquivalentClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'refractive_error_spherical_equivalent_classification_dt'
        verbose_name_plural = 'RefractiveErrorSphericalEquivalentClassificationDt'


class RefractiveErrorSphericalEquivalentDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'refractive_error_spherical_equivalent_dt'
        verbose_name_plural = 'RefractiveErrorSphericalEquivalentDt'


class RelationshipToProbandDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'relationship_to_proband_dt'
        verbose_name_plural = 'RelationshipToProbandDt'


class SexDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sex_dt'
        verbose_name_plural = 'SexDt'


class StaticPerimetryMeanSensitivityClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'static_perimetry_mean_sensitivity_classification_dt'
        verbose_name_plural = 'StaticPerimetryMeanSensitivityClassificationDt'


class StaticPerimetryMeanSensitivityDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'static_perimetry_mean_sensitivity_dt'
        verbose_name_plural = 'StaticPerimetryMeanSensitivityDt'


class SyndromicDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'syndromic_dt'
        verbose_name_plural = 'SyndromicDt'


class SystemicAbnormalityDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'systemic_abnormality_dt'
        verbose_name_plural = 'SystemicAbnormalityDt'


class TypicalDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'typical_dt'
        verbose_name_plural = 'TypicalDt'


class VisualAcuityClassificationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'visual_acuity_classification_dt'
        verbose_name_plural = 'VisualAcuityClassificationDt'


class VisualAcuityDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'visual_acuity_dt'
        verbose_name_plural = 'VisualAcuityDt'
		
class DiseaseCausCandGeneDt(models.Model):
	disease = models.ForeignKey('DiseaseDt',models.SET_NULL,blank=True,null=True)
	name = models.CharField(max_length=255)
	
	class Meta:
		db_table = 'disease_caus_cand_gene_dt'
		verbose_name_plural = 'DiseaseCausCandGeneDt'


class InstituteDt(models.Model):
	institute_id = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	class Meta:
		db_table = 'institute_dt'
		verbose_name_plural = 'InstituteDt'
		
	def __str__(self):
		return self.name
	

class DiseaseDt(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	
	class Meta:
		db_table = 'disease_dt'
		verbose_name_plural = 'DiseaseDt'
		
	def __str__(self):
		return self.name

class SubDiseaseDt(models.Model):
	disease = models.ForeignKey('DiseaseDt', models.PROTECT)
	name = models.CharField(max_length=255)
		
	class Meta:
		db_table = 'sub_disease_dt'
		verbose_name_plural = 'SubDiseaseDt'
	

class AdminDiseaseDt(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	
	class Meta:
		db_table = 'admin_disease_dt'
		verbose_name_plural = 'AdminDiseaseDt'
		
	def __str__(self):
		return self.name

class AdminSubDiseaseDt(models.Model):
	disease = models.ForeignKey('AdminDiseaseDt', models.PROTECT)
	name = models.CharField(max_length=255)
		
	class Meta:
		db_table = 'admin_sub_disease_dt'
		verbose_name_plural = 'AdminSubDiseaseDt'
		
	def __str__(self):
		return self.name


class GeneDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'gene_dt'
        verbose_name_plural = 'GeneDt'


class MutationDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'mutation_dt'
        verbose_name_plural = 'MutationDt'


class DnaExtractionInProcessDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'dna_extraction_in_process_dt'
        verbose_name_plural = 'DnaExtractionInProcessDt'


class SequencingDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sequencing_dt'
        verbose_name_plural = 'SequencingDt'


class AnalysisDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'analysis_dt'
        verbose_name_plural = 'AnalysisDt'


class ChromosomeDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'chromosome_dt'
        verbose_name_plural = 'ChromosomeDt'
		
		
class CausCandDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'caus_cand_dt'
        verbose_name_plural = 'CausCandDt'
		
class TypeOldNewDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'type_old_new_dt'
        verbose_name_plural = 'TypeOldNewDt'


class ExonDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'exon_dt'
        verbose_name_plural = 'ExonDt'


class SequencingStatusDt(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sequencing_status_dt'
        verbose_name_plural = 'SequencingStatusDt'








class PatientGeneralInfo(models.Model):
	user = models.ForeignKey(User,models.SET_NULL,blank=True,null=True)
	institute = models.ForeignKey('InstituteDt',models.SET_NULL,blank=True,null=True)
	patient_id = models.CharField(max_length=255)
	pedigree_chart = models.FileField()
	relationship_to_proband = models.ForeignKey('RelationshipToProbandDt',models.SET_NULL,blank=True,null=True)
	relationship_to_proband_other = models.CharField(max_length=255, blank=True, null=True)
	sample_id = models.CharField(max_length=255)
	admin_sub_disease_id = models.CharField(max_length=255, blank=True, null=True)
	birth_year_month = models.CharField(max_length=255, blank=True, null=True)
	sex = models.ForeignKey('SexDt',models.SET_NULL,blank=True,null=True)
	sex_other = models.CharField(max_length=255, blank=True, null=True)
	registration_date = models.DateTimeField(models.SET_NULL,blank=True,null=True)
	dna_sample_collection_date = models.DateTimeField(models.SET_NULL,blank=True,null=True)
	disease = models.ForeignKey('DiseaseDt',models.SET_NULL,blank=True,null=True)
	sub_disease = models.ForeignKey('SubDiseaseDt',models.SET_NULL,blank=True,null=True)
	disease_other = models.CharField(max_length=255, blank=True, null=True)
	affected = models.ForeignKey('AffectedDt', models.SET_NULL,blank=True,null=True)
	affected_other = models.CharField(max_length=255, blank=True, null=True)
	inheritance = models.ForeignKey('InheritanceDt', models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created')
	inheritance_other = models.CharField(max_length=255, blank=True, null=True)
	syndromic = models.ForeignKey('SyndromicDt',models.SET_NULL,blank=True,null=True)
	syndromic_other = models.CharField(max_length=255, blank=True, null=True)
	bilateral = models.ForeignKey('BilateralDt', models.SET_NULL,blank=True,null=True)
	bilateral_other = models.CharField(max_length=255, blank=True, null=True)
	ocular_symptom_1 = models.ForeignKey('OcularSymptomDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created')
	ocular_symptom_1_other = models.CharField(max_length=255, blank=True, null=True)
	ocular_symptom_2 = models.ForeignKey('OcularSymptomDt',  models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created33')
	ocular_symptom_2_other = models.CharField(max_length=255, blank=True, null=True)
	ocular_symptom_3 = models.ForeignKey('OcularSymptomDt',  models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created11')
	ocular_symptom_3_other = models.CharField(max_length=255, blank=True, null=True)
	progression = models.ForeignKey('ProgressionDt',models.SET_NULL,blank=True,null=True)
	progression_other = models.CharField(max_length=255, blank=True, null=True)
	flactuation = models.ForeignKey('FluctuationDt',models.SET_NULL,blank=True,null=True)
	flactuation_other = models.CharField(max_length=255, blank=True, null=True)
	family_history = models.ForeignKey('FamilyHistoryDt',models.SET_NULL,blank=True,null=True)
	family_history_other = models.CharField(max_length=255, blank=True, null=True)
	consanguineous = models.ForeignKey('ConsanguineousDt', models.SET_NULL,blank=True,null=True)
	consanguineous_other = models.CharField(max_length=255, blank=True, null=True)
	number_of_affected_members_in_the_same_pedigree = models.ForeignKey('NumberOfAffectedMembersInTheSamePedigreeDt', models.SET_NULL,blank=True,null=True)
	number_of_affected_members_in_the_same_pedigree_other = models.CharField(max_length=255, blank=True, null=True)
	ethnicity = models.ForeignKey('EthnicityDt', models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created1')
	ethnicity_other = models.CharField(max_length=255, blank=True, null=True)
	country_of_origine = models.ForeignKey('CountryOfOriginDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created2')
	country_of_origine_other = models.CharField(max_length=255, blank=True, null=True)
	origin_prefecture_in_japan = models.ForeignKey('OriginPrefectureInJapanDt',models.SET_NULL,blank=True,null=True)
	origin_prefecture_in_japan_other = models.CharField(max_length=255, blank=True, null=True)
	ethnic_of_father = models.ForeignKey('EthnicityDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created3')
	ethnic_of_father_other = models.CharField(max_length=255, blank=True, null=True)
	original_country_of_father = models.ForeignKey('CountryOfOriginDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created5')
	original_country_of_father_other = models.CharField(max_length=255, blank=True, null=True)
	origin_of_father_in_japan = models.ForeignKey('OriginPrefectureInJapanDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created')
	origin_of_father_in_japan_other = models.CharField(max_length=255, blank=True, null=True)
	ethnic_of_mother = models.ForeignKey('EthnicityDt', models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created6')
	ethnic_of_mother_other = models.CharField(max_length=255, blank=True, null=True)
	original_country_of_mother = models.ForeignKey('CountryOfOriginDt', models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created6')
	original_country_of_mother_other = models.CharField(max_length=255, blank=True, null=True)
	origin_of_mother_in_japan = models.ForeignKey('OriginPrefectureInJapanDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created9')
	origin_of_mother_in_japan_other = models.CharField(max_length=255, blank=True, null=True)
	#registration = models.CharField(max_length=255, blank=True, null=True)
	gene_type = models.ForeignKey('GeneDt',models.SET_NULL,blank=True,null=True)
	gene_type_other = models.CharField(max_length=255, blank=True, null=True)
	inheritance_type = models.ForeignKey('InheritanceDt',models.SET_NULL,blank=True,null=True,related_name='%(class)s_requests_created3')
	inheritance_type_other = models.CharField(max_length=255, blank=True, null=True)
	mutation_type = models.ForeignKey('MutationDt',models.SET_NULL,blank=True,null=True)
	mutation_type_other = models.CharField(max_length=255, blank=True, null=True)
	gene_inheritance_mutation_comments = models.CharField(max_length=255, blank=True, null=True)
	overall_comments = models.CharField(max_length=255, blank=True, null=True)
	dna_extraction_process = models.ForeignKey('DnaExtractionInProcessDt',models.SET_NULL,blank=True,null=True,  related_name="+")
	dna_extraction_process_other = models.CharField(max_length=255, blank=True, null=True)
	sequencing = models.ForeignKey('SequencingDt',models.SET_NULL,blank=True,null=True,  related_name="+")
	sequencing_other = models.CharField(max_length=255, blank=True, null=True)
	analysis = models.ForeignKey('AnalysisDt',models.SET_NULL,blank=True,null=True,  related_name="+")
	analysis_other = models.CharField(max_length=255, blank=True, null=True)
	registration_id =  models.CharField(max_length=255, blank=True, null=True)
	is_draft =  models.BooleanField(default=0)
	
	class Meta:
		db_table = 'patient_general_info'
		verbose_name_plural = 'PatientGeneralInfo'


class PatientGeneralInfoFamily(models.Model):
    patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    family_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'patient_general_info_family'
        verbose_name_plural = 'PatientGeneralInfoFamily'


class PatientGeneralInfoMultiVisit(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	key = models.CharField(max_length=255)
	value = models.CharField(max_length=255, blank=True, null=True)
	field_name = models.CharField(max_length=255, blank=True, null=True)
	field_direction = models.CharField(max_length=50, blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	other = models.CharField(max_length=255, blank=True, null=True)
	model_name = models.CharField(max_length=255, blank=True, null=True)
	
    # patient_id = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    # date = models.DateTimeField()
    # logmar_visual_acuity_right = models.ForeignKey('VisualAcuityDt',  models.PROTECT,  related_name="+")
    # logmar_visual_acuity_classification_right = models.ForeignKey('VisualAcuityClassificationDt',  models.PROTECT,  related_name="+")
    # logmar_visual_acuity_left = models.ForeignKey('VisualAcuityDt',  models.PROTECT,  related_name="+")
    # logmar_visual_acuity_classification_left = models.ForeignKey('VisualAcuityClassificationDt',  models.PROTECT,  related_name="+")
    # date = models.DateTimeField()
    # blood_pressure_systolic_mmhg = models.CharField(max_length=255, blank=True, null=True)
    # blood_pressure_diastolic_mmhg = models.CharField(max_length=255, blank=True, null=True)
    # hypertension_classification = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # hypertension_medication = models.ForeignKey('OnMedicationOrNotDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # blood_total_cholesterol_level_mgdl = models.CharField(max_length=255, blank=True, null=True)
    # blood_ldl_cholesterol_level_mgdl = models.CharField(max_length=255, blank=True, null=True)
    # hypercholestremia_classification = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # hypercholestremia_medication = models.ForeignKey('HcOnMedicationOrNotStatinDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # fasting_blood_glucose_mgdl = models.CharField(max_length=255, blank=True, null=True)
    # hba1c_percentage = models.CharField(max_length=255, blank=True, null=True)
    # diabetes_mellitus = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # diabetes_mellitus_medication = models.ForeignKey('HcOnMedicationOrNotInsulinDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # clinical_course_of_systemic_disorder_or_no_systemic_disorder = models.CharField(max_length=255, blank=True, null=True)
    # typical = models.ForeignKey('TypicalDt',  models.PROTECT,  related_name="+", blank=True, null=True)
	
	class Meta:
		db_table = 'patient_general_info_multi_visit'
		verbose_name_plural = 'PatientGeneralInfoMultiVisit'


class PatientGeneralInfoMultiVisitOphthalmologyImages(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	key = models.CharField(max_length=255)
	value = models.CharField(max_length=255, blank=True, null=True)
	field_name = models.CharField(max_length=255, blank=True, null=True)
	field_direction = models.CharField(max_length=50, blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	
    # patient_id = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    # date = models.DateTimeField()
    # corn_phot_right = models.FileField()
    # corn_phot_left = models.FileField()
    # corn_phot_on_fluor_right = models.FileField()
    # corn_phot_on_fluor_left = models.FileField()
    # corn_topography_right = models.FileField()
    # corn_topography_left = models.FileField()
    # corn_endotherial_photy_right = models.FileField()
    # corn_endotherial_photy_left = models.FileField()
    # opt_cohe_tomo_of_anterior_segment_right = models.FileField()
    # opt_cohe_tomo_of_anterior_segment_left = models.FileField()
    # ax_length_right = models.FileField()
    # ax_length_left = models.FileField()
    # lens_phot_right = models.FileField()
    # lens_phot_left = models.FileField()
    # fund_phot_wide_field_right = models.FileField()
    # fund_phot_wide_field_left = models.FileField()
    # fund_autoflu_right = models.FileField()
    # fund_autoflu_left = models.FileField()
    # fund_autoflu_wide_field_right = models.FileField()
    # fund_autoflu_wide_field_left = models.FileField()
    # infra_imaging_right = models.FileField()
    # infra_imaging_left = models.FileField()
    # infra_imaging_wide_field_right = models.FileField()
    # infra_imaging_wide_field_left = models.FileField()
    # fluor_angi_right = models.FileField()
    # fluor_angi_left = models.FileField()
    # fluor_angi_wide_field_right = models.FileField()
    # fluor_angi_wide_field_left = models.FileField()
    # indo_green_angi_right = models.FileField()
    # indo_green_angi_left = models.FileField()
    # indo_green_angi_wide_field_right = models.FileField()
    # indo_green_angi_wide_field_left = models.FileField()
    # opt_cohe_tomo_disc_right = models.FileField()
    # opt_cohe_tomo_disc_left = models.FileField()
    # opt_cohe_tomo_macula_line_right = models.FileField()
    # opt_cohe_tomo_macula_line_left = models.FileField()
    # opt_cohe_tomo_macula_3d_right = models.FileField()
    # opt_cohe_tomo_macula_3d_left = models.FileField()
    # opt_cohe_tomo_macula_en_face_right = models.FileField()
    # opt_cohe_tomo_macula_en_face_left = models.FileField()
    # opt_cohe_tomo_angi_right = models.FileField()
    # opt_cohe_tomo_angi_left = models.FileField()
    # adap_optic_imaging_right = models.FileField()
    # adap_optic_imaging_left = models.FileField()
    # full_field_elect_right = models.FileField()
    # full_field_elect_left = models.FileField()
    # mult_elect_right = models.FileField()
    # mult_elect_left = models.FileField()
    # focal_macu_elect_right = models.FileField()
    # focal_macu_elect_left = models.FileField()
    # patt_elect_right = models.FileField()
    # patt_elect_left = models.FileField()
    # patt_visual_evoked_potential_right = models.FileField()
    # patt_visual_evoked_potential_left = models.FileField()
    # flash_visual_evoked_potential_right = models.FileField()
    # flash_visual_evoked_potential_left = models.FileField()
    # pupilometry_right = models.FileField()
    # pupilometry_left = models.FileField()
    # dark_adaptmetry_right = models.FileField()
    # dark_adaptmetry_left = models.FileField()
    # kine_visual_field_test_right = models.FileField()
    # kine_visual_field_test_left = models.FileField()
    # static_visual_field_test_right = models.FileField()
    # static_visual_field_test_left = models.FileField()
    # microperimetry_right = models.FileField()
    # microperimetry_left = models.FileField()
    # color_vision_test_right = models.FileField()
    # color_vision_test_left = models.FileField()
    # image_others = models.FileField()
    # image_comments = models.FileField()
	
	class Meta:
		db_table = 'patient_general_info_multi_visit_ophthalmology_images'
		verbose_name_plural = 'PatientGeneralInfoMultiVisitOphthalmologyImages'


class PatientGeneralInfoMultiVisitOphthalmology(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	key = models.CharField(max_length=255)
	value = models.CharField(max_length=255, blank=True, null=True)
	field_name = models.CharField(max_length=255, blank=True, null=True)
	field_direction = models.CharField(max_length=50, blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	other = models.CharField(max_length=255, blank=True, null=True)
	model_name = models.CharField(max_length=255, blank=True, null=True)
	
	
    # patient_id = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    # date = models.DateTimeField()
    # intra_ocul_pres_right = models.ForeignKey('IntraocularPressureDt',  models.PROTECT,  related_name="+")
    # intra_ocul_pres_clas_right = models.ForeignKey('IntraocularPressureClassificationDt',  models.PROTECT,  related_name="+")
    # intra_ocul_pres_left = models.ForeignKey('IntraocularPressureDt',  models.PROTECT,  related_name="+")
    # intra_ocul_pres_clas_left = models.ForeignKey('IntraocularPressureClassificationDt',  models.PROTECT,  related_name="+")
    # refr_error_sphe_equi_right = models.ForeignKey('RefractiveErrorSphericalEquivalentDt',  models.PROTECT,  related_name="+")
    # refr_error_sphe_equi_clas_right = models.ForeignKey('RefractiveErrorSphericalEquivalentClassificationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # refr_error_sphe_equi_left = models.ForeignKey('RefractiveErrorSphericalEquivalentDt',  models.PROTECT,  related_name="+")
    # refr_error_sphe_equi_clas_left = models.ForeignKey('RefractiveErrorSphericalEquivalentClassificationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # corn_thic_right = models.CharField(max_length=255)
    # corn_thic_left = models.CharField(max_length=255)
    # lens_right = models.ForeignKey('LensDt',  models.PROTECT,  related_name="+")
    # lens_left = models.ForeignKey('LensDt',  models.PROTECT,  related_name="+")
    # axia_leng_right = models.ForeignKey('AxialLengthDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # axia_leng_clas_right = models.ForeignKey('AxialLengthClassificationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # axia_leng_left = models.ForeignKey('AxialLengthDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # axia_leng_clas_left = models.ForeignKey('AxialLengthClassificationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # macu_thic_right = models.CharField(max_length=255, blank=True, null=True)
    # macu_edema_right = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # macu_schisis_right = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # epir_memb_right = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # sub_sensreti_fuild_right = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # sub_reti_epith_memb_fuild_right = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # macu_thic_left = models.CharField(max_length=255, blank=True, null=True)
    # macu_edema_left = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # macu_schisis_left = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # epir_memb_left = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # sub_sensreti_fuild_left = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # sub_reti_epith_memb_fuild_left = models.ForeignKey('PresentUnpresentDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # foveal_thic_right = models.CharField(max_length=255, blank=True, null=True)
    # foveal_thic_left = models.CharField(max_length=255, blank=True, null=True)
    # choro_thic_right = models.CharField(max_length=255, blank=True, null=True)
    # choro_thic_left = models.CharField(max_length=255, blank=True, null=True)
    # stat_peri_mean_sens_hfa24_2_right = models.ForeignKey('StaticPerimetryMeanSensitivityDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # stat_peri_mean_sens_clas_right = models.ForeignKey('StaticPerimetryMeanSensitivityClassificationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # stat_peri_mean_sens_hfa24_2_left = models.ForeignKey('StaticPerimetryMeanSensitivityDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # stat_peri_mean_sens_clas_left = models.ForeignKey('StaticPerimetryMeanSensitivityClassificationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # electro_right = models.ForeignKey('ElectrophysiologicalFindingsDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # full_field_electphysiol_clas_right = models.ForeignKey('FullFieldElectrophysiologicalGroupingDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # multi_electphysiol_clas_right = models.ForeignKey('MultifocalElectrophysiologicalGroupingDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # electroneg_config_of_dark_apa = models.CharField(max_length=255, blank=True, null=True)
    # electro_left = models.ForeignKey('ElectrophysiologicalFindingsDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # full_field_electphysiol_clas_left = models.ForeignKey('FullFieldElectrophysiologicalGroupingDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # multi_electphysiol_clas_left = models.ForeignKey('MultifocalElectrophysiologicalGroupingDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_diagnosis_for_others_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accuracy_for_others_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diagnosis_for_others_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accuracy_for_others_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_comments = models.CharField(max_length=255, blank=True, null=True)
	
	class Meta:
		db_table = 'patient_general_info_multi_visit_ophthalmology'
		verbose_name_plural = 'PatientGeneralInfoMultiVisitOphthalmology'


class PatientGeneralInfoOphthalmologySystAbnormality(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	name = models.ForeignKey('SystemicAbnormalityDt',  models.PROTECT,  related_name="+", blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	other = models.CharField(max_length=255, blank=True, null=True)
	
	class Meta:
		db_table = 'patient_general_info_ophthalmology_syst_abnormality'
		verbose_name_plural = 'PatientGeneralInfoOphthalmologySystAbnormality'


class PatientGeneralInfoOphthalmologyOcularCompli(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	name = models.ForeignKey('OcularSymptomDt',  models.PROTECT,  related_name="+", blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	other = models.CharField(max_length=255, blank=True, null=True)
	
	class Meta:
		db_table = 'patient_general_info_ophthalmology_ocular_compli'
		verbose_name_plural = 'PatientGeneralInfoOphthalmologyOcularCompli'


class PatientGeneralInfoOphthalmology(models.Model):
    patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    ocul_surgeries_catrct_right = models.ForeignKey('OcularSurgeriesCataractDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    ocul_surgeries_catrct_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_catrct_surgery_perf_right = models.ForeignKey('AgeForSurgeryDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    age_catrct_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_catrct_surgery_perf_right = models.ForeignKey('NumberOfSurgeryDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    no_catrct_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_catrct_left = models.ForeignKey('OcularSurgeriesCataractDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    ocul_surgeries_catrct_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_catrct_surgery_perf_left = models.ForeignKey('AgeForSurgeryDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    age_catrct_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_catrct_surgery_perf_left = models.ForeignKey('NumberOfSurgeryDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    no_catrct_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_at_onset_of_ocul_symp = models.ForeignKey('AgeAtOnsetOfOcularSymptomDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    age_at_onset_of_ocul_symp_other = models.CharField(max_length=255, blank=True, null=True)
    onset_of_diease_clas = models.ForeignKey('AgeAtOnsetClassificationDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    onset_of_diease_clas_other = models.CharField(max_length=255, blank=True, null=True)
    age_at_the_init_diag = models.ForeignKey('AgeAtTheInitialDiagnosisDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    age_at_the_init_diag_other = models.CharField(max_length=255, blank=True, null=True)
    age_at_the_init_diag_clas = models.ForeignKey('AgeAtTheInitialDiagnosisClassificationDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    age_at_the_init_diag_clas_other = models.CharField(max_length=255, blank=True, null=True)
    gene_middle_results = models.FileField()
    vcf_whole_exome_sequencing = models.FileField()
    vcf_whole_genome_sequencing = models.FileField()
    gene_comments = models.CharField(max_length=255, blank=True, null=True)
    

    class Meta:
        db_table = 'patient_general_info_ophthalmology'
        verbose_name_plural = 'PatientGeneralInfoOphthalmology'


class PatientOtherMultiVisitImages(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	key = models.CharField(max_length=255)
	value = models.CharField(max_length=255, blank=True, null=True)
	field_name = models.CharField(max_length=255, blank=True, null=True)
	field_direction = models.CharField(max_length=50, blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	
	
    # patient_id = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    # fund_phot_right = models.FileField()
    # fund_phot_left = models.FileField()
    # corn_phot_ai_diag_corn_dise_right = models.FileField()
    # corn_phot_ai_diag_corn_dise_left = models.FileField()
    # corn_phot_on_fluo_ai_diag_corn_dise_right = models.FileField()
    # corn_phot_on_fluo_ai_diag_corn_dise_left = models.FileField()
    # fund_phot_ai_diag_glau_right = models.FileField()
    # fund_phot_ai_diag_glau_left = models.FileField()
    # opti_cohe_tomo_disc_ai_diag_glau_right = models.FileField()
    # opti_cohe_tomo_disc_ai_diag_glau_left = models.FileField()
    # stat_visual_field_ai_diag_glau_right = models.FileField()
    # stat_visual_field_ai_diag_glau_left = models.FileField()
    # fund_phot_ai_diag_diab_retino_right = models.FileField()
    # fund_phot_ai_diag_diab_retino_left = models.FileField()
    # fluo_angio_ai_diag_diaet_retino_right = models.FileField()
    # fluo_angio_ai_diag_diaet_retino_left = models.FileField()
    # opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right = models.FileField()
    # opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left = models.FileField()
    # fund_phot_ai_diag_age_rela_macu_dege_right = models.FileField()
    # fund_phot_ai_diag_age_rela_macu_dege_left = models.FileField()
    # fluo_angio_ai_diag_age_rela_macu_dege_right = models.FileField()
    # fluo_angio_ai_diag_age_rela_macu_dege_left = models.FileField()
    # indocy_green_angio_ai_diag_age_rela_macu_dege_right = models.FileField()
    # indocy_green_angio_ai_diag_age_rela_macu_dege_left = models.FileField()
    # opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right = models.FileField()
    # opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left = models.FileField()
    # fund_phot_ai_diag_inher_reti_dise_right = models.FileField()
    # fund_phot_ai_diag_inher_reti_dise_left = models.FileField()
    # fund_autofluo_wide_field_ai_diag_inher_reti_dise_right = models.FileField()
    # fund_autofluo_wide_field_ai_diag_inher_reti_dise_left = models.FileField()
    # opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right = models.FileField()
    # opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left = models.FileField()
    # opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right = models.FileField()
    # opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left = models.FileField()
    # full_field_elect_ai_diag_inher_reti_dise_right = models.FileField()
    # full_field_elect_ai_diag_inher_reti_dise_left = models.FileField()
    # multifocal_elect_ai_diag_inher_reti_dise_right = models.FileField()
    # multifocal_elect_ai_diag_inher_reti_dise_left = models.FileField()
    # vcf_files_ai_diag_inher_reti_dise_right = models.FileField()
    # vcf_files_ai_diag_inher_reti_dise_left = models.FileField()
    # others_ai_diag_right = models.FileField()
    # others_ai_diag_left = models.FileField()
    # comments = models.FileField()

	class Meta:
		db_table = 'patient_other_multi_visit_images'
		verbose_name_plural = 'PatientOtherMultiVisitImages'


#class PatientCandidateGeneMutationInfo(models.Model):
    #patient_id = models.ForeignKey('PatientGeneralInfo', models.PROTECT)
    #type_old_new = models.CharField(max_length=1, blank=True, null=True)
    #candidate_gene = models.ForeignKey('GeneDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    #candidate_mutation = models.CharField(max_length=255, blank=True, null=True)

    #class Meta:
        #db_table = 'patient_candidate_gene_mutation_info'
        #verbose_name_plural = 'PatientCandidateGeneMutationInfo'


class PatientCausativeGeneInfo(models.Model):
    patient = models.ForeignKey('PatientGeneralInfo', models.PROTECT)
    type_old_new = models.ForeignKey('TypeOldNewDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    type_old_new_other = models.CharField(max_length=255, blank=True, null=True)
    caus_cand = models.ForeignKey('CausCandDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    caus_cand_other = models.CharField(max_length=255, blank=True, null=True)
    caus_cand_gene = models.ForeignKey('GeneDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    disease_caus_cand_gene = models.ForeignKey('DiseaseCausCandGeneDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    caus_cand_gene_other = models.CharField(max_length=255, blank=True, null=True)
    disease_caus_cand_gene_other = models.CharField(max_length=255, blank=True, null=True)
    chromosome = models.ForeignKey('ChromosomeDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    chromosome_other = models.CharField(max_length=255, blank=True, null=True)
    chromosome_comment = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    transcript = models.CharField(max_length=255, blank=True, null=True)
    exon = models.ForeignKey('ExonDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    exon_other = models.CharField(max_length=255, blank=True, null=True)
    exon_comment = models.CharField(max_length=255, blank=True, null=True)
    caus_cand_mutation_nucleotide_amino_acid = models.CharField(max_length=255, blank=True, null=True)
    caus_cand_mutation_nucleotide_amino_acid_comment =  models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'patient_causative_gene_info'
        verbose_name_plural = 'PatientCausativeGeneInfo'


class PatientCausativeGeneInfoEthnicity(models.Model):
    patient_causative_gene_info = models.ForeignKey(PatientCausativeGeneInfo, models.PROTECT)
    freq_ethnicity = models.ForeignKey('AlleleFrequencyDatabaseDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    freq_ethnicity_per = models.CharField(max_length=255, blank=True, null=True)
    freq_ethnicity_other = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'patient_causative_gene_info_ethnicity'
        verbose_name_plural = 'PatientCausativeGeneInfoEthnicity'


class PatientCausativeGeneInfoLocalPopulation(models.Model):
    patient_causative_gene_info = models.ForeignKey(PatientCausativeGeneInfo, models.PROTECT)
    freq_local_population = models.ForeignKey('AlleleFrequencyDatabaseDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    freq_local_population_per = models.CharField(max_length=255, blank=True, null=True)
    freq_local_population_other = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'patient_causative_gene_info_local_population'
        verbose_name_plural = 'PatientCausativeGeneInfoLocalPopulation'


class PatientGeneralInfoMultiVisitOphthalmologyAi(models.Model):
	patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
	key = models.CharField(max_length=255)
	value = models.CharField(max_length=255, blank=True, null=True)
	field_name = models.CharField(max_length=255, blank=True, null=True)
	field_direction = models.CharField(max_length=50, blank=True, null=True)
	date = models.CharField(max_length=50, blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)
	other = models.CharField(max_length=255, blank=True, null=True)
	model_name = models.CharField(max_length=255, blank=True, null=True)
	
    # patient_id = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    # ai_diag_corn_dise_corn_phot_right = models.ForeignKey('AiDiagnosisForCornealDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_corn_diag_corn_phot_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_corn_dise_corn_phot_left = models.ForeignKey('AiDiagnosisForCornealDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_corn_diag_corn_phot_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_corn_dise_corn_phot_on_fluo_right = models.ForeignKey('AiDiagnosisForCornealDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_corn_diag_corn_phot_on_fluo_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_corn_dise_corn_phot_on_fluo_left = models.ForeignKey('AiDiagnosisForCornealDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_corn_diag_corn_phot_on_fluo_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_glau_fundus_phot_right = models.ForeignKey('AiDiagnosisForGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_glau_fundus_phot_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_glau_fundus_phot_left = models.ForeignKey('AiDiagnosisForGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_glau_fundus_phot_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_glau_opti_cohe_tomo_disc_right = models.ForeignKey('AiDiagnosisForGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_glau_opti_cohe_tomo_disc_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_glau_opti_cohe_tomo_disc_left = models.ForeignKey('AiDiagnosisForGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_glau_opti_cohe_tomo_disc_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_glau_static_perimetry_right = models.ForeignKey('AiDiagnosisForGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_glau_static_perimetry_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_glau_static_visual_field_left = models.ForeignKey('AiDiagnosisForGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_glau_static_visual_field_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_diab_retino_fundus_phot_right = models.ForeignKey('AiDiagnosisForDiabeticRetinopathyDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_diab_retino_fundus_phot_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_diab_retino_fundus_phot_left = models.ForeignKey('AiDiagnosisForDiabeticRetinopathyDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_diab_retino_fundus_phot_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_diab_retino_fluo_angio_right = models.ForeignKey('AiDiagnosisForDiabeticRetinopathyDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_diab_retino_fluo_angio_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diagnsis_diab_retino_fluo_angio_left = models.ForeignKey('AiDiagnosisForDiabeticRetinopathyDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_diab_retino_fluo_angio_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right = models.ForeignKey('AiDiagnosisForDiabeticRetinopathyDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left = models.ForeignKey('AiDiagnosisForDiabeticRetinopathyDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_fundus_phot_right = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_fundus_phot_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_fundus_phot_left = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_fundus_phot_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_fluo_angio_right = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_fluo_angio_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_fluo_angio_left = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_fluo_angio_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_indocy_green_angio_right = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_indocy_green_angio_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_indocy_green_angio_left = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_indocy_green_angio_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left = models.ForeignKey('AiDiagnosisForAgeRelatedMacularDegenerationDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_fundus_phot_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_fundus_phot_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_fundus_phot_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_fundus_phot_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_full_field_electroret_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_full_field_electroret_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_full_field_electroret_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_full_field_electroret_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_multifocal_electroret_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_multifocal_electroret_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_multifocal_electroret_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_multifocal_electroret_left_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_vcf_files_right = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_vcf_files_right_per = models.CharField(max_length=255, blank=True, null=True)
    # ai_diag_inheri_retin_dise_vcf_files_left = models.ForeignKey('AiDiagnosisForInheritedRetinalDiseasesDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    # ai_accu_inheri_retin_dise_vcf_files_left_per = models.CharField(max_length=255, blank=True, null=True)
	class Meta:
		db_table = 'patient_general_info_multi_visit_ophthalmology_ai'
		verbose_name_plural = 'PatientGeneralInfoMultiVisitOphthalmologyAi'


class PatientOtherCommonInfo(models.Model):
    patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    direct_sequencing_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    direct_sequencing_1_other = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    direct_sequencing_2_other = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_3 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    direct_sequencing_3_other = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_4 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    direct_sequencing_4_other = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_5 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    direct_sequencing_5_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_1_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_2_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_analysis_2_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_3 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_3_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_3 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_analysis_3_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_4 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_4_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_4 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_analysis_4_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_5 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_5_other = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_5 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_enrichment_ngs_panel_analysis_5_other = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_exome_sequencing_1_other = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_exome_sequencing_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_exome_sequencing_2_other = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_analysis_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_exome_sequencing_analysis_2_other = models.CharField(max_length=255, blank=True, null=True)
    exome_sequencing_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    exome_sequencing_1_other = models.CharField(max_length=255, blank=True, null=True)
    exome_sequencing_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    exome_sequencing_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    whole_exome_sequencing_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    whole_exome_sequencing_1_other = models.CharField(max_length=255, blank=True, null=True)
    whole_exome_sequencing_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    whole_exome_sequencing_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    sequencing_other_collaborators_1_other = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    sequencing_other_collaborators_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    sequencing_other_collaborators_2_other = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_analysis_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    sequencing_other_collaborators_analysis_2_other = models.CharField(max_length=255, blank=True, null=True)
    beadarray_platform_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    beadarray_platform_1_other = models.CharField(max_length=255, blank=True, null=True)
    beadarray_platform_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    beadarray_platform_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    other_sequencing = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    other_sequencing_other = models.CharField(max_length=255, blank=True, null=True)
    mitochondria_ngs_whole_gene_sequence_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    mitochondria_ngs_whole_gene_sequence_1_other = models.CharField(max_length=255, blank=True, null=True)
    mitochondria_ngs_whole_gene_sequence_analysis_1 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    mitochondria_ngs_whole_gene_sequence_analysis_1_other = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_sequence_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_mitochondrial_sequence_2_other = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_sequence_analysis_2 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_mitochondrial_sequence_analysis_2_other = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_hot_spot_panel_sequence_3 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_mitochondrial_hot_spot_panel_sequence_3_other = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_hot_spot_panel_sequence_analysis_3 = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other = models.CharField(max_length=255, blank=True, null=True)
    other_analysis = models.ForeignKey('SequencingStatusDt',models.SET_NULL,blank=True,null=True,  related_name="+")
    other_analysis_other = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_1_comments = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_2_comments = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_3_comments = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_4_comments = models.CharField(max_length=255, blank=True, null=True)
    direct_sequencing_5_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_1_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_2_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_2_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_3_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_3_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_4_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_4_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_5_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_enrichment_ngs_panel_analysis_5_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_1_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_2_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_exome_sequencing_analysis_2_comments = models.CharField(max_length=255, blank=True, null=True)
    exome_sequencing_1_comments = models.CharField(max_length=255, blank=True, null=True)
    exome_sequencing_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    whole_exome_sequencing_1_comments = models.CharField(max_length=255, blank=True, null=True)
    whole_exome_sequencing_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_1_comments = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_2_comments = models.CharField(max_length=255, blank=True, null=True)
    sequencing_other_collaborators_analysis_2_comments = models.CharField(max_length=255, blank=True, null=True)
    beadarray_platform_1_comments = models.CharField(max_length=255, blank=True, null=True)
    beadarray_platform_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    other_sequencing_comments = models.CharField(max_length=255, blank=True, null=True)
    mitochondria_ngs_whole_gene_sequence_1_comments = models.CharField(max_length=255, blank=True, null=True)
    mitochondria_ngs_whole_gene_sequence_analysis_1_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_sequence_2_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_sequence_analysis_2_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_hot_spot_panel_sequence_3_comments = models.CharField(max_length=255, blank=True, null=True)
    targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments = models.CharField(max_length=255, blank=True, null=True)
    other_analysis_comments = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = 'patient_other_common_info'
        verbose_name_plural = 'PatientOtherCommonInfo'


class PatientOtherUncommonInfoOphthalmology(models.Model):
    patient = models.ForeignKey(PatientGeneralInfo, models.PROTECT)
    ocul_surgeries_cornea_right = models.ForeignKey('OcularSurgeriesCorneaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_cornea_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_corneal_surgery_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_corneal_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_corneal_surgery_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_corneal_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_cornea_left = models.ForeignKey('OcularSurgeriesCorneaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_cornea_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_corneal_surgery_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_corneal_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_corneal_surgery_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_corneal_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_glaucoma_right = models.ForeignKey('OcularSurgeriesGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_glaucoma_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_glaucoma_surgery_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_glaucoma_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_glaucomal_surgery_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_glaucomal_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_glaucoma_left = models.ForeignKey('OcularSurgeriesGlaucomaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_glaucoma_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_glaucoma_surgery_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_glaucoma_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_glaucomal_surgery_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_glaucomal_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_retina_right = models.ForeignKey('OcularSurgeriesRetinaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_retina_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_vitreoretina_surgery_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_vitreoretina_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_vitreoretinal_surgery_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_vitreoretinal_surgery_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_retina_left = models.ForeignKey('OcularSurgeriesRetinaDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_retina_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_vitreoretina_surgery_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_vitreoretina_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_vitreoretinal_surgery_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_vitreoretinal_surgery_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_lasers_right = models.ForeignKey('OcularSurgeriesLasersDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_lasers_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_ocul_surgeries_lasers_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_ocul_surgeries_lasers_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_ofocul_surgeries_lasers_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_ofocul_surgeries_lasers_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_surgeries_lasers_left = models.ForeignKey('OcularSurgeriesLasersDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_surgeries_lasers_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_ocul_surgeries_lasers_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_ocul_surgeries_lasers_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_ofocul_surgeries_lasers_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_ofocul_surgeries_lasers_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    opht_medi_subtenon_subconj_injec_right = models.ForeignKey('OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    opht_medi_subtenon_subconj_injec_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_opht_medi_subtenon_subconj_injec_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_opht_medi_subtenon_subconj_injec_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_opht_medi_subtenon_subconj_injec_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_opht_medi_subtenon_subconj_injec_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    opht_medi_subtenon_subconj_injec_left = models.ForeignKey('OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    opht_medi_subtenon_subconj_injec_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_opht_medi_subtenon_subconj_injec_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_opht_medi_subtenon_subconj_injec_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_opht_medi_subtenon_subconj_injec_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_opht_medi_subtenon_subconj_injec_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_medi_internal_right = models.ForeignKey('OcularMedicationInternalDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_medi_internal_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_ocul_medi_internal_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_ocul_medi_internal_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_ocul_medi_internal_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_ocul_medi_internal_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_medi_internal_left = models.ForeignKey('OcularMedicationInternalDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_medi_internal_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_ocul_medi_internal_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_ocul_medi_internal_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_ocul_medi_internal_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_ocul_medi_internal_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_medi_topical_right = models.ForeignKey('OcularMedicationTopicalDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_medi_topical_right_other = models.CharField(max_length=255, blank=True, null=True)
    age_ocul_medi_topical_perf_right = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_ocul_medi_topical_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    no_ocul_medi_topical_perf_right = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_ocul_medi_topical_perf_right_other = models.CharField(max_length=255, blank=True, null=True)
    ocul_medi_topical_left = models.ForeignKey('OcularMedicationTopicalDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    ocul_medi_topical_left_other = models.CharField(max_length=255, blank=True, null=True)
    age_ocul_medi_topical_perf_left = models.ForeignKey('AgeForSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    age_ocul_medi_topical_perf_left_other = models.CharField(max_length=255, blank=True, null=True)
    no_ocul_medi_topical_perf_left = models.ForeignKey('NumberOfSurgeryDt',  models.PROTECT,  related_name="+", blank=True, null=True)
    no_ocul_medi_topical_perf_left_other = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'patient_other_uncommon_info_ophthalmology'
        verbose_name_plural = 'PatientOtherUncommonInfoOphthalmology'
