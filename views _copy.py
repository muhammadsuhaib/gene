from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import urlencode # Python 3
import urllib
import random
from django.db.models import Q
import os
import datetime
from django.core.files.storage import FileSystemStorage
import re
from django.apps import apps

from ophthalmology.models import InstituteDt,RelationshipToProbandDt,SexDt,DiseaseDt,AffectedDt,InheritanceDt,SyndromicDt,BilateralDt,OcularSymptomDt,ProgressionDt,FluctuationDt,FamilyHistoryDt,ConsanguineousDt,NumberOfAffectedMembersInTheSamePedigreeDt,EthnicityDt,CountryOfOriginDt,OriginPrefectureInJapanDt,GeneDt,InheritanceDt,MutationDt,OcularSurgeriesCorneaDt,AgeForSurgeryDt,NumberOfSurgeryDt,OcularSurgeriesGlaucomaDt,OcularSurgeriesRetinaDt,OcularSurgeriesLasersDt,OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt,OcularMedicationInternalDt,OcularMedicationTopicalDt,PatientGeneralInfo,PatientOtherUncommonInfoOphthalmology,OcularSurgeriesCataractDt,PatientGeneralInfoOphthalmology,PatientGeneralInfoMultiVisitOphthalmologyImages,VisualAcuityDt,VisualAcuityClassificationDt,PresentUnpresentDt,OnMedicationOrNotDt,HcOnMedicationOrNotStatinDt,HcOnMedicationOrNotInsulinDt,TypicalDt,AgeAtOnsetOfOcularSymptomDt,AgeAtTheInitialDiagnosisDt,DnaExtractionInProcessDt,AnalysisDt,AgeAtOnsetClassificationDt,AgeAtTheInitialDiagnosisClassificationDt,SequencingDt,AiDiagnosisForCornealDiseasesDt,AiDiagnosisForGlaucomaDt,AiDiagnosisForDiabeticRetinopathyDt,AiDiagnosisForAgeRelatedMacularDegenerationDt,AiDiagnosisForInheritedRetinalDiseasesDt,SequencingStatusDt,IntraocularPressureDt,IntraocularPressureClassificationDt,RefractiveErrorSphericalEquivalentDt,RefractiveErrorSphericalEquivalentClassificationDt,LensDt,AxialLengthDt,AxialLengthClassificationDt,StaticPerimetryMeanSensitivityDt,StaticPerimetryMeanSensitivityClassificationDt,ElectrophysiologicalFindingsDt,FullFieldElectrophysiologicalGroupingDt,MultifocalElectrophysiologicalGroupingDt,ChromosomeDt,ExonDt,AlleleFrequencyDatabaseDt,PatientGeneralInfoMultiVisit,PatientGeneralInfoMultiVisitOphthalmology,PatientOtherMultiVisitImages,PatientGeneralInfoMultiVisitOphthalmologyAi,PatientOtherCommonInfo,PatientCausativeGeneInfo,PatientCausativeGeneInfoEthnicity,PatientCausativeGeneInfoLocalPopulation,PatientGeneralInfoFamily,SystemicAbnormalityDt,PatientGeneralInfoOphthalmologySystAbnormality,PatientGeneralInfoOphthalmologyOcularCompli,CausCandDt,TypeOldNewDt,AdminDiseaseDt,AdminSubDiseaseDt

from core.models import DoctorDisease

# Create your views here.

@login_required(login_url='/')
def index(request):
	#left menu bar query data
	userAssignedDiseases = DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id__in=userAssignedDiseases.disease).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data
	
	PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.select_related("institute","sex").all()
	if PatientGeneralInfoDetial:
		for PatientGeneralInfoDetial1 in PatientGeneralInfoDetial:
			family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial1.id).values("family_id").first();
			if family_detail:
				PatientGeneralInfoDetial1.family_id = family_detail["family_id"]
			else:
				PatientGeneralInfoDetial1.family_id = ''
				
	
	
	context		=	{
		"assignedDiseases":assignedDiseases,
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial
	}
	return render(request, 'ophthalmology/index.html',context)
	
@login_required(login_url='/')
def add_new_patient(request,selected_disease_id):
	#left menu bar query data
	userAssignedDiseases = DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id__in=userAssignedDiseases.disease).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data
	
	step_images_name_list_right	=	["corn_phot_right","corn_phot_on_fluor_right","corn_topography_right","corn_endotherial_photy_right","opt_cohe_tomo_of_anterior_segment_right","ax_length_right","lens_phot_right","fund_phot_wide_field_right","fund_autoflu_right","fund_autoflu_wide_field_right","infra_imaging_right","infra_imaging_wide_field_right","fluor_angi_right","fluor_angi_wide_field_right","indo_green_angi_right","indo_green_angi_wide_field_right","opt_cohe_tomo_disc_right","opt_cohe_tomo_macula_line_right","opt_cohe_tomo_macula_3d_right","opt_cohe_tomo_macula_en_face_right","opt_cohe_tomo_angi_right","adap_optic_imaging_right","full_field_elect_right","mult_elect_right","focal_macu_elect_right","patt_elect_right","patt_visual_evoked_potential_right","flash_visual_evoked_potential_right","pupilometry_right","dark_adaptmetry_right","kine_visual_field_test_right","static_visual_field_test_right","microperimetry_right","color_vision_test_right","image_others"]
		
	step_images_name_list_left	=	["corn_phot_left","corn_phot_on_fluor_left","corn_topography_left","corn_endotherial_photy_left","opt_cohe_tomo_of_anterior_segment_left","ax_length_left","lens_phot_left","fund_phot_wide_field_left","fund_autoflu_left","fund_autoflu_wide_field_left","infra_imaging_left","infra_imaging_wide_field_left","fluor_angi_left","fluor_angi_wide_field_left","indo_green_angi_left","indo_green_angi_wide_field_left","opt_cohe_tomo_disc_left","opt_cohe_tomo_macula_line_left","opt_cohe_tomo_macula_3d_left","opt_cohe_tomo_macula_en_face_left","opt_cohe_tomo_angi_left","adap_optic_imaging_left","full_field_elect_left","mult_elect_left","focal_macu_elect_left","patt_elect_left","patt_visual_evoked_potential_left","flash_visual_evoked_potential_left","pupilometry_left","dark_adaptmetry_left","kine_visual_field_test_left","static_visual_field_test_left","microperimetry_left","color_vision_test_left","image_comments"]
		
	step4_images_name_list_all	=	["corn_phot_left","corn_phot_right","corn_phot_on_fluor_left","corn_phot_on_fluor_right","corn_topography_left","corn_topography_right","corn_endotherial_photy_left","corn_endotherial_photy_right","opt_cohe_tomo_of_anterior_segment_left","opt_cohe_tomo_of_anterior_segment_right","ax_length_left","ax_length_right","lens_phot_left","lens_phot_right","fund_phot_wide_field_left","fund_phot_wide_field_right","fund_autoflu_left","fund_autoflu_right","fund_autoflu_wide_field_left","fund_autoflu_wide_field_right","infra_imaging_left","infra_imaging_right","infra_imaging_wide_field_left","infra_imaging_wide_field_right","fluor_angi_left","fluor_angi_right","fluor_angi_wide_field_left","fluor_angi_wide_field_right","indo_green_angi_left","indo_green_angi_right","indo_green_angi_wide_field_left","indo_green_angi_wide_field_right","opt_cohe_tomo_disc_left","opt_cohe_tomo_disc_right","opt_cohe_tomo_macula_line_left","opt_cohe_tomo_macula_line_right","opt_cohe_tomo_macula_3d_left","opt_cohe_tomo_macula_3d_right","opt_cohe_tomo_macula_en_face_left","opt_cohe_tomo_macula_en_face_right","opt_cohe_tomo_angi_left","opt_cohe_tomo_angi_right","adap_optic_imaging_left","adap_optic_imaging_right","full_field_elect_left","full_field_elect_right","mult_elect_left","mult_elect_right","focal_macu_elect_left","focal_macu_elect_right","patt_elect_left","patt_elect_right","patt_visual_evoked_potential_left","patt_visual_evoked_potential_right","flash_visual_evoked_potential_left","flash_visual_evoked_potential_right","pupilometry_left","pupilometry_right","dark_adaptmetry_left","dark_adaptmetry_right","kine_visual_field_test_left","kine_visual_field_test_right","static_visual_field_test_left","static_visual_field_test_right","microperimetry_left","microperimetry_right","color_vision_test_left","color_vision_test_right","image_comments","image_others"]
	
	step_other_multi_visit_images_right	=	["fund_phot_right","corn_phot_ai_diag_corn_dise_right","corn_phot_on_fluo_ai_diag_corn_dise_right","fund_phot_ai_diag_glau_right","opti_cohe_tomo_disc_ai_diag_glau_right","stat_visual_field_ai_diag_glau_right","fund_phot_ai_diag_diab_retino_right","fluo_angio_ai_diag_diaet_retino_right","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right","fund_phot_ai_diag_age_rela_macu_dege_right","fluo_angio_ai_diag_age_rela_macu_dege_right","indocy_green_angio_ai_diag_age_rela_macu_dege_right","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right","fund_phot_ai_diag_inher_reti_dise_right","fund_autofluo_wide_field_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right","full_field_elect_ai_diag_inher_reti_dise_right","multifocal_elect_ai_diag_inher_reti_dise_right","vcf_files_ai_diag_inher_reti_dise_right","others_ai_diag_right"]
	
	step_other_multi_visit_images_left	=	["fund_phot_left","corn_phot_ai_diag_corn_dise_left","corn_phot_on_fluo_ai_diag_corn_dise_left","fund_phot_ai_diag_glau_left","opti_cohe_tomo_disc_ai_diag_glau_left","stat_visual_field_ai_diag_glau_left","fund_phot_ai_diag_diab_retino_left","fluo_angio_ai_diag_diaet_retino_left","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left","fund_phot_ai_diag_age_rela_macu_dege_left","fluo_angio_ai_diag_age_rela_macu_dege_left","indocy_green_angio_ai_diag_age_rela_macu_dege_left","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left","fund_phot_ai_diag_inher_reti_dise_left","fund_autofluo_wide_field_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left","full_field_elect_ai_diag_inher_reti_dise_left","multifocal_elect_ai_diag_inher_reti_dise_left","vcf_files_ai_diag_inher_reti_dise_left","others_ai_diag_left"]
	
	
	step_other_multi_visit_images_all	=	["fund_phot_left","fund_phot_right","corn_phot_ai_diag_corn_dise_left","corn_phot_ai_diag_corn_dise_right","corn_phot_on_fluo_ai_diag_corn_dise_left","corn_phot_on_fluo_ai_diag_corn_dise_right","fund_phot_ai_diag_glau_left","fund_phot_ai_diag_glau_right","opti_cohe_tomo_disc_ai_diag_glau_left","opti_cohe_tomo_disc_ai_diag_glau_right","stat_visual_field_ai_diag_glau_left","stat_visual_field_ai_diag_glau_right","fund_phot_ai_diag_diab_retino_left","fund_phot_ai_diag_diab_retino_right","fluo_angio_ai_diag_diaet_retino_left","fluo_angio_ai_diag_diaet_retino_right","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right","fund_phot_ai_diag_age_rela_macu_dege_left","fund_phot_ai_diag_age_rela_macu_dege_right","fluo_angio_ai_diag_age_rela_macu_dege_left","fluo_angio_ai_diag_age_rela_macu_dege_right","indocy_green_angio_ai_diag_age_rela_macu_dege_left","indocy_green_angio_ai_diag_age_rela_macu_dege_right","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right","fund_phot_ai_diag_inher_reti_dise_left","fund_phot_ai_diag_inher_reti_dise_right","fund_autofluo_wide_field_ai_diag_inher_reti_dise_left","fund_autofluo_wide_field_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right","full_field_elect_ai_diag_inher_reti_dise_left","full_field_elect_ai_diag_inher_reti_dise_right","multifocal_elect_ai_diag_inher_reti_dise_left","multifocal_elect_ai_diag_inher_reti_dise_right","vcf_files_ai_diag_inher_reti_dise_left","vcf_files_ai_diag_inher_reti_dise_right","others_ai_diag_left","others_ai_diag_right"]
	
	##PatientGeneralInfoMultiVisitOphthalmology
	
	
	
	
	
	
	if request.method	==	"POST":
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'static/ophthalmology/'+str(currentMonth)+str(currentYear)+"/"
		if not os.path.exists(user_folder):
			os.mkdir(user_folder)
			
		pedigree_chart	=	""
		registration_id = ""
		if request.method == 'POST' and len(request.FILES) != 0:
			if request.FILES.get("pedigree_chart"):
				myfile = request.FILES.get("pedigree_chart")
				fs = FileSystemStorage()
				filename = myfile.name.split(".")[0].lower()
				extension = myfile.name.split(".")[-1].lower()
				newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
				fs.save(user_folder+newfilename, myfile)	
				pedigree_chart	=	str(currentMonth)+str(currentYear)+"/"+newfilename
	
		#return HttpResponse(request.POST["institute_id"])
		
		PatientInfo					=	PatientGeneralInfo()
		
		if request.POST["institute_id"] != "" and request.POST["registration_date"] != "":
			rend_string = random.randint(1000000, 9999999);
			registration_id	=	request.POST["institute_id"]+''+request.POST["registration_date"].replace("-","")+''+str(rend_string);
			##return HttpResponse(registration_id);
			PatientInfo.registration_id	=	registration_id
		
		if request.POST["institute_id"] != "":
			institute_id	=	InstituteDt.objects.filter(institute_id=request.POST["institute_id"]).values("id").first();	
			PatientInfo.institute_id = institute_id["id"];	
			
		if request.POST["patient_id"] != "":
			PatientInfo.patient_id	=	request.POST["patient_id"]
			
		if request.POST["relationship_to_proband"] != "":
			PatientInfo.relationship_to_proband_id	=	request.POST["relationship_to_proband"]
			
		if request.POST["relationship_to_proband_other"] != "":
			PatientInfo.relationship_to_proband_other	=	request.POST["relationship_to_proband_other"]
			
		if request.POST["birth_year_month"] != "":
			PatientInfo.birth_year_month	=	request.POST["birth_year_month"]
			
		if request.POST["sex"] != "":
			PatientInfo.sex_id	=	request.POST["sex"]
			
		if request.POST["sex_other"] != "":
			PatientInfo.sex_other	=	request.POST["sex_other"]
			
		if request.POST["registration_date"] != "":
			PatientInfo.registration_date	=	request.POST["registration_date"]
			
		if request.POST["dna_sample_collection_date"] != "":
			PatientInfo.dna_sample_collection_date	=	request.POST["dna_sample_collection_date"]
			
		if request.POST["disease"] != "":
			PatientInfo.disease_id	=	request.POST["disease"]
			
		if request.POST["disease_other"] != "":
			PatientInfo.disease_other	=	request.POST["disease_other"]
			
		if request.POST["affected"] != "":
			PatientInfo.affected_id	=	request.POST["affected"]
			
		if request.POST["affected_other"] != "":
			PatientInfo.affected_other	=	request.POST["affected_other"]
		
		#return HttpResponse(PatientInfo.affected_id)
			
		if request.POST["inheritance"] != "":
			PatientInfo.inheritance_id	=	request.POST["inheritance"]
			
		if request.POST["inheritance_other"] != "":
			PatientInfo.inheritance_other	=	request.POST["inheritance_other"]
			
		if request.POST["sample_id"] != "":
			PatientInfo.sample_id	=	request.POST["sample_id"]
			
		if request.POST["syndromic"] != "":
			PatientInfo.syndromic_id	=	request.POST["syndromic"]
			
		if request.POST["syndromic_other"] != "":
			PatientInfo.syndromic_other	=	request.POST["syndromic_other"]
			
		if request.POST["bilateral"] != "":
			PatientInfo.bilateral_id	=	request.POST["bilateral"]
			
		if request.POST["bilateral_other"] != "":
			PatientInfo.bilateral_other	=	request.POST["bilateral_other"]
			
		if request.POST["ocular_symptom_1"] != "":
			PatientInfo.ocular_symptom_1_id	=	request.POST["ocular_symptom_1"]
			
		if request.POST["ocular_symptom_1_other"] != "":
			PatientInfo.ocular_symptom_1_other	=	request.POST["ocular_symptom_1_other"]
			
		if request.POST["ocular_symptom_2"] != "":
			PatientInfo.ocular_symptom_2_id	=	request.POST["ocular_symptom_2"]
			
		if request.POST["ocular_symptom_2_other"] != "":
			PatientInfo.ocular_symptom_2_other	=	request.POST["ocular_symptom_2_other"]
			
		if request.POST["ocular_symptom_3"] != "":
			PatientInfo.ocular_symptom_3_id	=	request.POST["ocular_symptom_3"]
			
		if request.POST["ocular_symptom_3_other"] != "":
			PatientInfo.ocular_symptom_3_other	=	request.POST["ocular_symptom_3_other"]
			
		if request.POST["progression"] != "":
			PatientInfo.progression_id	=	request.POST["progression"]
			
		if request.POST["progression_other"] != "":
			PatientInfo.progression_other	=	request.POST["progression_other"]
			
		if request.POST["flactuation"] != "":
			PatientInfo.flactuation_id	=	request.POST["flactuation"]
			
		if request.POST["flactuation_other"] != "":
			PatientInfo.flactuation_other	=	request.POST["flactuation_other"]
			
		if request.POST["family_history"] != "":
			PatientInfo.family_history_id	=	request.POST["family_history"]
			
		if request.POST["family_history_other"] != "":
			PatientInfo.family_history_other	=	request.POST["family_history_other"]
			
		if request.POST["consanguineous"] != "":
			PatientInfo.consanguineous_id	=	request.POST["consanguineous"]
			
		if request.POST["consanguineous_other"] != "":
			PatientInfo.consanguineous_other	=	request.POST["consanguineous_other"]
			
		if request.POST["number_of_affected_members_in_the_same_pedigree"] != "":
			PatientInfo.number_of_affected_members_in_the_same_pedigree	=	request.POST["number_of_affected_members_in_the_same_pedigree"]
			
		if request.POST["number_of_affected_members_in_the_same_pedigree_other"] != "":
			PatientInfo.number_of_affected_members_in_the_same_pedigree_other	=	request.POST["number_of_affected_members_in_the_same_pedigree_other"]
			
		if request.POST["ethnicity"] != "":
			PatientInfo.ethnicity_id	=	request.POST["ethnicity"]
			
		if request.POST["ethnicity_other"] != "":
			PatientInfo.ethnicity_other	=	request.POST["ethnicity_other"]
			
		if request.POST["country_of_origine"] != "":
			PatientInfo.country_of_origine	=	request.POST["country_of_origine"]
			
		if request.POST["country_of_origine_other"] != "":
			PatientInfo.country_of_origine_other	=	request.POST["country_of_origine_other"]
			
		if request.POST["origin_prefecture_in_japan"] != "":
			PatientInfo.origin_prefecture_in_japan	=	request.POST["origin_prefecture_in_japan"]
			
		if request.POST["origin_prefecture_in_japan_other"] != "":
			PatientInfo.origin_prefecture_in_japan_other	=	request.POST["origin_prefecture_in_japan_other"]
			
		if request.POST["ethnic_of_father"] != "":
			PatientInfo.ethnic_of_father_id	=	request.POST["ethnic_of_father"]
			
		if request.POST["ethnic_of_father_other"] != "":
			PatientInfo.ethnic_of_father_other	=	request.POST["ethnic_of_father_other"]
			
		if request.POST["original_country_of_father"] != "":
			PatientInfo.original_country_of_father	=	request.POST["original_country_of_father"]
			
		if request.POST["original_country_of_father_other"] != "":
			PatientInfo.original_country_of_father_other	=	request.POST["original_country_of_father_other"]
			
		if request.POST["origin_of_father_in_japan"] != "":
			PatientInfo.origin_of_father_in_japan	=	request.POST["origin_of_father_in_japan"]
			
		if request.POST["origin_of_father_in_japan_other"] != "":
			PatientInfo.origin_of_father_in_japan_other	=	request.POST["origin_of_father_in_japan_other"]
		
		if request.POST["ethnic_of_mother"] != "":
			PatientInfo.ethnic_of_mother_id	=	request.POST["ethnic_of_mother"]
			
		if request.POST["ethnic_of_mother_other"] != "":
			PatientInfo.ethnic_of_mother_other	=	request.POST["ethnic_of_mother_other"]
			
		if request.POST["original_country_of_mother"] != "":
			PatientInfo.original_country_of_mother	=	request.POST["original_country_of_mother"]
			
		if request.POST["original_country_of_mother_other"] != "":
			PatientInfo.original_country_of_mother_other	=	request.POST["original_country_of_mother_other"]
			
		if request.POST["origin_of_mother_in_japan"] != "":
			PatientInfo.origin_of_mother_in_japan	=	request.POST["origin_of_mother_in_japan"]
			
		if request.POST["origin_of_mother_in_japan_other"] != "":
			PatientInfo.origin_of_mother_in_japan_other	=	request.POST["origin_of_mother_in_japan_other"]
			
		if request.POST["registration"] != "":
			PatientInfo.registration	=	request.POST["registration"]
			
		if request.POST["gene_type"] != "":
			PatientInfo.gene_type_id	=	request.POST["gene_type"]
			
		if request.POST["gene_type_other"] != "":
			PatientInfo.gene_type_other	=	request.POST["gene_type_other"]
			
		if request.POST["family_history"] != "":
			PatientInfo.family_history_id	=	request.POST["family_history"]
			
		if request.POST["family_history_other"] != "":
			PatientInfo.family_history_other	=	request.POST["family_history_other"]
			
		if request.POST["inheritance_type"] != "":
			PatientInfo.inheritance_type_id	=	request.POST["inheritance_type"]
			
		if request.POST["inheritance_type_other"] != "":
			PatientInfo.inheritance_type_other	=	request.POST["inheritance_type_other"]
			
		if request.POST["mutation_type"] != "":
			PatientInfo.mutation_type_id	=	request.POST["mutation_type"]
			
		if request.POST["mutation_type_other"] != "":
			PatientInfo.mutation_type_other	=	request.POST["mutation_type_other"]
			
		if request.POST["gene_inheritance_mutation_comments"] != "":
			PatientInfo.gene_inheritance_mutation_comments	=	request.POST["gene_inheritance_mutation_comments"]
			
		if request.POST["sequencing"] != "":
			PatientInfo.sequencing_id	=	request.POST["sequencing"]
			
		if request.POST["sequencing_other"] != "":
			PatientInfo.sequencing_other	=	request.POST["sequencing_other"]
			
		if request.POST["analysis"] != "":
			PatientInfo.analysis_id	=	request.POST["analysis"]
			
		if request.POST["analysis_other"] != "":
			PatientInfo.analysis_other	=	request.POST["analysis_other"]
			
		if request.POST["dna_extraction_process"] != "":
			PatientInfo.dna_extraction_process_id	=	request.POST["dna_extraction_process"]
			
		if request.POST["dna_extraction_process_other"] != "":
			PatientInfo.dna_extraction_process_other	=	request.POST["dna_extraction_process_other"]
			
			
		
			
		PatientInfo.pedigree_chart	=	pedigree_chart
		PatientInfo.is_draft	=	request.POST["is_draft"]
		#return HttpResponse(PatientInfo.registration_id)
		PatientInfo.save()
		lastPatientId		=	PatientInfo.id
		
		PatientGeneralInfoFamilyInfo   			= PatientGeneralInfoFamily()
		
		if request.POST["family_id"] != "":
			PatientGeneralInfoFamilyInfo.family_id	=	request.POST["family_id"]
		
		PatientGeneralInfoFamilyInfo.patient_id	=	lastPatientId	
		
		PatientGeneralInfoFamilyInfo.save()	
			
		
		
		
		PatientOtherUncommonInfoOphthalmologyInfo	=	PatientOtherUncommonInfoOphthalmology()
		if request.POST["ocul_surgeries_cornea_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_id	=	request.POST["ocul_surgeries_cornea_right"]
			
		if request.POST["ocul_surgeries_cornea_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other	=	request.POST["ocul_surgeries_cornea_right_other"]
			
		if request.POST["ocul_surgeries_cornea_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_id	=	request.POST["ocul_surgeries_cornea_left"]
			
		if request.POST["ocul_surgeries_cornea_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other	=	request.POST["ocul_surgeries_cornea_left_other"]
			
		if request.POST["age_corneal_surgery_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_id	=	request.POST["age_corneal_surgery_perf_right"]
			
		if request.POST["age_corneal_surgery_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other	=	request.POST["age_corneal_surgery_perf_right_other"]
			
		if request.POST["age_corneal_surgery_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_id	=	request.POST["age_corneal_surgery_perf_left"]	
			
		if request.POST["age_corneal_surgery_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other	=	request.POST["age_corneal_surgery_perf_left_other"]	
			
		if request.POST["no_corneal_surgery_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_id	=	request.POST["no_corneal_surgery_perf_right"]
			
		if request.POST["no_corneal_surgery_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other	=	request.POST["no_corneal_surgery_perf_right_other"]	
		
		if request.POST["no_corneal_surgery_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_id	=	request.POST["no_corneal_surgery_perf_left"]	
			
		if request.POST["no_corneal_surgery_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other	=	request.POST["no_corneal_surgery_perf_left_other"]	
			
		if request.POST["ocul_surgeries_glaucoma_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_id	=	request.POST["ocul_surgeries_glaucoma_right"]	
			
		if request.POST["ocul_surgeries_glaucoma_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other	=	request.POST["ocul_surgeries_glaucoma_right_other"]	

		if request.POST["ocul_surgeries_glaucoma_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_id	=	request.POST["ocul_surgeries_glaucoma_left"]
			
		if request.POST["ocul_surgeries_glaucoma_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other	=	request.POST["ocul_surgeries_glaucoma_left_other"]	
			
		if request.POST["age_glaucoma_surgery_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_id	=	request.POST["age_glaucoma_surgery_perf_right"]	
			
		if request.POST["age_glaucoma_surgery_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other	=	request.POST["age_glaucoma_surgery_perf_right_other"]	
		
		if request.POST["age_glaucoma_surgery_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_id	=	request.POST["age_glaucoma_surgery_perf_left"]	
			
		if request.POST["age_glaucoma_surgery_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other	=	request.POST["age_glaucoma_surgery_perf_left_other"]	
			
		if request.POST["no_glaucomal_surgery_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_id	=	request.POST["no_glaucomal_surgery_perf_right"]	
			
		if request.POST["no_glaucomal_surgery_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other	=	request.POST["no_glaucomal_surgery_perf_right_other"]	
			
		if request.POST["no_glaucomal_surgery_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_id	=	request.POST["no_glaucomal_surgery_perf_left"]
			
		if request.POST["no_glaucomal_surgery_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other	=	request.POST["no_glaucomal_surgery_perf_left_other"]	
			
		if request.POST["ocul_surgeries_retina_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_id	=	request.POST["ocul_surgeries_retina_right"]	
			
		if request.POST["ocul_surgeries_retina_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other	=	request.POST["ocul_surgeries_retina_right_other"]	
			
		if request.POST["ocul_surgeries_retina_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_id	=	request.POST["ocul_surgeries_retina_left"]	
			
		if request.POST["ocul_surgeries_retina_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other	=	request.POST["ocul_surgeries_retina_left_other"]	
			
		if request.POST["age_vitreoretina_surgery_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_id	=	request.POST["age_vitreoretina_surgery_perf_right"]
			
		if request.POST["age_vitreoretina_surgery_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other	=	request.POST["age_vitreoretina_surgery_perf_right_other"]
			
		if request.POST["age_vitreoretina_surgery_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_id	=	request.POST["age_vitreoretina_surgery_perf_left"]
			
		if request.POST["age_vitreoretina_surgery_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other	=	request.POST["age_vitreoretina_surgery_perf_left_other"]
			
		if request.POST["no_vitreoretinal_surgery_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_id	=	request.POST["no_vitreoretinal_surgery_perf_right"]
			
		if request.POST["no_vitreoretinal_surgery_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other	=	request.POST["no_vitreoretinal_surgery_perf_right_other"]
			
		if request.POST["no_vitreoretinal_surgery_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_id	=	request.POST["no_vitreoretinal_surgery_perf_left"]
			
		if request.POST["no_vitreoretinal_surgery_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other	=	request.POST["no_vitreoretinal_surgery_perf_left_other"]
			
		if request.POST["age_ocul_surgeries_lasers_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_id	=	request.POST["age_ocul_surgeries_lasers_perf_right"]
			
		if request.POST["age_ocul_surgeries_lasers_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other	=	request.POST["age_ocul_surgeries_lasers_perf_right_other"]
			
		if request.POST["age_ocul_surgeries_lasers_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_id	=	request.POST["age_ocul_surgeries_lasers_perf_left"]
			
		if request.POST["age_ocul_surgeries_lasers_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other	=	request.POST["age_ocul_surgeries_lasers_perf_left_other"]
			
		if request.POST["no_ofocul_surgeries_lasers_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_id	=	request.POST["no_ofocul_surgeries_lasers_perf_right"]
			
		if request.POST["no_ofocul_surgeries_lasers_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other	=	request.POST["no_ofocul_surgeries_lasers_perf_right_other"]
			
		if request.POST["no_ofocul_surgeries_lasers_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_id	=	request.POST["no_ofocul_surgeries_lasers_perf_left"]
			
		if request.POST["no_ofocul_surgeries_lasers_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other	=	request.POST["no_ofocul_surgeries_lasers_perf_left_other"]
			
		if request.POST["ocul_surgeries_lasers_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_id	=	request.POST["ocul_surgeries_lasers_right"]
			
		if request.POST["ocul_surgeries_lasers_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other	=	request.POST["ocul_surgeries_lasers_right_other"]
			
		if request.POST["ocul_surgeries_lasers_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_id	=	request.POST["ocul_surgeries_lasers_left"]
			
		if request.POST["ocul_surgeries_lasers_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other	=	request.POST["ocul_surgeries_lasers_left_other"]
			
		if request.POST["age_opht_medi_subtenon_subconj_injec_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_id	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_right"]
			
		if request.POST["age_opht_medi_subtenon_subconj_injec_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_right_other"]
			
		if request.POST["age_opht_medi_subtenon_subconj_injec_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_id	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_left"]
			
		if request.POST["age_opht_medi_subtenon_subconj_injec_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_left_other"]
			
		if request.POST["no_opht_medi_subtenon_subconj_injec_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_id	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_right"]
			
		if request.POST["no_opht_medi_subtenon_subconj_injec_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_right_other"]
			
		if request.POST["no_opht_medi_subtenon_subconj_injec_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_id	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_left"]
			
		if request.POST["no_opht_medi_subtenon_subconj_injec_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_left_other"]
			
		if request.POST["opht_medi_subtenon_subconj_injec_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_id	=	request.POST["opht_medi_subtenon_subconj_injec_right"]
			
		if request.POST["opht_medi_subtenon_subconj_injec_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other	=	request.POST["opht_medi_subtenon_subconj_injec_right_other"]
			
		if request.POST["opht_medi_subtenon_subconj_injec_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_id	=	request.POST["opht_medi_subtenon_subconj_injec_left"]
			
		if request.POST["opht_medi_subtenon_subconj_injec_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other	=	request.POST["opht_medi_subtenon_subconj_injec_left_other"]
			
		if request.POST["ocul_medi_internal_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_id	=	request.POST["ocul_medi_internal_right"]
			
		if request.POST["ocul_medi_internal_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other	=	request.POST["ocul_medi_internal_right_other"]
			
		if request.POST["ocul_medi_internal_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_id	=	request.POST["ocul_medi_internal_left"]
			
		if request.POST["ocul_medi_internal_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other	=	request.POST["ocul_medi_internal_left_other"]
			
		if request.POST["age_ocul_medi_internal_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_id	=	request.POST["age_ocul_medi_internal_perf_right"]
			
		if request.POST["age_ocul_medi_internal_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other	=	request.POST["age_ocul_medi_internal_perf_right_other"]
			
		if request.POST["age_ocul_medi_internal_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_id	=	request.POST["age_ocul_medi_internal_perf_left"]
			
		if request.POST["age_ocul_medi_internal_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other	=	request.POST["age_ocul_medi_internal_perf_left_other"]
			
		if request.POST["no_ocul_medi_internal_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_id	=	request.POST["no_ocul_medi_internal_perf_right"]
			
		if request.POST["no_ocul_medi_internal_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other	=	request.POST["no_ocul_medi_internal_perf_right_other"]
			
		if request.POST["no_ocul_medi_internal_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_id	=	request.POST["no_ocul_medi_internal_perf_left"]
			
		if request.POST["no_ocul_medi_internal_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other	=	request.POST["no_ocul_medi_internal_perf_left_other"]
			
		if request.POST["ocul_medi_topical_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_id	=	request.POST["ocul_medi_topical_right"]
			
		if request.POST["ocul_medi_topical_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other	=	request.POST["ocul_medi_topical_right_other"]
			
		if request.POST["ocul_medi_topical_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_id	=	request.POST["ocul_medi_topical_left"]
			
		if request.POST["ocul_medi_topical_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other	=	request.POST["ocul_medi_topical_left_other"]
			
		if request.POST["age_ocul_medi_topical_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_id	=	request.POST["age_ocul_medi_topical_perf_right"]
			
		if request.POST["age_ocul_medi_topical_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other	=	request.POST["age_ocul_medi_topical_perf_right_other"]
			
		if request.POST["age_ocul_medi_topical_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_id	=	request.POST["age_ocul_medi_topical_perf_left"]
			
		if request.POST["age_ocul_medi_topical_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other	=	request.POST["age_ocul_medi_topical_perf_left_other"]
			
		if request.POST["no_ocul_medi_topical_perf_right"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_id	=	request.POST["no_ocul_medi_topical_perf_right"]
			
		if request.POST["no_ocul_medi_topical_perf_right_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other	=	request.POST["no_ocul_medi_topical_perf_right_other"]
			
		if request.POST["no_ocul_medi_topical_perf_left"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_id	=	request.POST["no_ocul_medi_topical_perf_left"]
			
		if request.POST["no_ocul_medi_topical_perf_left_other"] != "":
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_other	=	request.POST["no_ocul_medi_topical_perf_left_other"]
				
		PatientOtherUncommonInfoOphthalmologyInfo.patient_id	=	lastPatientId
		PatientOtherUncommonInfoOphthalmologyInfo.save()
		
		
		##PatientGeneralInfoOphthalmology
		
		PatientGeneralInfoOphthalmologyInfo	=	PatientGeneralInfoOphthalmology()
		
		gene_middle_results			=	""
		vcf_whole_exome_sequencing	=	""
		vcf_whole_genome_sequencing	=	""
		
		
		
		##return HttpResponse( request.FILES['gene_middle_results'])
		if request.FILES.get("gene_middle_results"):
			myfile1 = request.FILES['gene_middle_results']
			fs = FileSystemStorage()
			filename = myfile1.name.split(".")[0].lower()
			extension = myfile1.name.split(".")[-1].lower()
			newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
			fs.save(user_folder+newfilename, myfile1)	
			gene_middle_results	=	str(currentMonth)+str(currentYear)+"/"+newfilename
			
		if request.FILES.get('vcf_whole_exome_sequencing'):	
			myfile2 = request.FILES['vcf_whole_exome_sequencing']
			fs = FileSystemStorage()
			filename = myfile2.name.split(".")[0].lower()
			extension = myfile2.name.split(".")[-1].lower()
			newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
			fs.save(user_folder+newfilename, myfile2)	
			vcf_whole_exome_sequencing	=	str(currentMonth)+str(currentYear)+"/"+newfilename
			
		if request.FILES.get('vcf_whole_genome_sequencing'):	
			myfile3 = request.FILES['vcf_whole_genome_sequencing']
			fs = FileSystemStorage()
			filename = myfile3.name.split(".")[0].lower()
			extension = myfile3.name.split(".")[-1].lower()
			newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
			fs.save(user_folder+newfilename, myfile3)	
			vcf_whole_genome_sequencing	=	str(currentMonth)+str(currentYear)+"/"+newfilename
				
				
			
		
		PatientGeneralInfoOphthalmologyInfo.gene_middle_results			=	gene_middle_results
		PatientGeneralInfoOphthalmologyInfo.vcf_whole_exome_sequencing	=	vcf_whole_exome_sequencing
		PatientGeneralInfoOphthalmologyInfo.vcf_whole_genome_sequencing	=	vcf_whole_genome_sequencing
		
		if request.POST["ocul_surgeries_catrct_left"] != "":
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_id	=	request.POST["ocul_surgeries_catrct_left"]
			
		if request.POST["ocul_surgeries_catrct_left_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other	=	request.POST["ocul_surgeries_catrct_left_other"]
			
		if request.POST["age_catrct_surgery_perf_left"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_id	=	request.POST["age_catrct_surgery_perf_left"]
			
		if request.POST["age_catrct_surgery_perf_left_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other	=	request.POST["age_catrct_surgery_perf_left_other"]
			
		if request.POST["no_catrct_surgery_perf_left"] != "":
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_id	=	request.POST["no_catrct_surgery_perf_left"]
			
		if request.POST["no_catrct_surgery_perf_left_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other	=	request.POST["no_catrct_surgery_perf_left_other"]
		
		if request.POST["age_at_onset_of_ocul_symp"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_id	=	request.POST["age_at_onset_of_ocul_symp"]
		
		if request.POST["age_at_onset_of_ocul_symp_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other	=	request.POST["age_at_onset_of_ocul_symp_other"]
			
		if request.POST["age_at_the_init_diag"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_id	=	request.POST["age_at_the_init_diag"]
			
		if request.POST["age_at_the_init_diag_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other	=	request.POST["age_at_the_init_diag_other"]
			
		if request.POST["age_at_the_init_diag_clas"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_id	=	request.POST["age_at_the_init_diag_clas"]
			
		if request.POST["age_at_the_init_diag_clas_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other	=	request.POST["age_at_the_init_diag_clas_other"]
			
		if request.POST["ocul_surgeries_catrct_right"] != "":
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_id	=	request.POST["ocul_surgeries_catrct_right"]
			
		if request.POST["ocul_surgeries_catrct_right_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other	=	request.POST["ocul_surgeries_catrct_right_other"]
			
		if request.POST["age_catrct_surgery_perf_right"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_id	=	request.POST["age_catrct_surgery_perf_right"]
			
		if request.POST["age_catrct_surgery_perf_right_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other	=	request.POST["age_catrct_surgery_perf_right_other"]
			
		if request.POST["no_catrct_surgery_perf_right"] != "":
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_id	=	request.POST["no_catrct_surgery_perf_right"]
			
		if request.POST["no_catrct_surgery_perf_right_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other	=	request.POST["no_catrct_surgery_perf_right_other"]
			
		if request.POST["onset_of_diease_clas"] != "":
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_id	=	request.POST["onset_of_diease_clas"]
			
		if request.POST["onset_of_diease_clas_other"] != "":
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other	=	request.POST["onset_of_diease_clas_other"]
			
		if request.POST["gene_comments"] != "":
			PatientGeneralInfoOphthalmologyInfo.gene_comments	=	request.POST["gene_comments"]
		
		
		PatientGeneralInfoOphthalmologyInfo.patient_id	=	lastPatientId
		PatientGeneralInfoOphthalmologyInfo.save()

		##return HttpResponse(PatientGeneralInfoOphthalmologyInfo.id)
		
		
		
		
		
		
		
		#### save data in PatientGeneralInfoMultiVisitOphthalmologyImages model ####
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'static/ophthalmology/multi_visit_ophthalmology_images/'+str(currentMonth)+str(currentYear)+"/"
		if not os.path.exists(user_folder):
			os.mkdir(user_folder)
		### multiVisitOphthalmologyImagesRight	
		dic = {}
		for k in request.FILES.keys():
			if k.startswith("multiVisitOphthalmologyImagesRight"):
				rest = k[len("multiVisitOphthalmologyImagesRight"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.FILES.get(k)
					
		for k in request.POST.keys():
			if k.startswith("multiVisitOphthalmologyImagesRight"):
				rest = k[len("multiVisitOphthalmologyImagesRight"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
		
		if step_images_name_list_right:
			for key in step_images_name_list_right:
				if dic["multiVisitOphthalmologyImagesRight"]:
					for fromData in dic["multiVisitOphthalmologyImagesRight"]:
						if fromData in dic["multiVisitOphthalmologyImagesRight"] and key in dic["multiVisitOphthalmologyImagesRight"][fromData]:
							images	=	dic["multiVisitOphthalmologyImagesRight"][fromData][key]
							if images != "":
								fs = FileSystemStorage()
								filename = images.name.split(".")[0].lower()
								extension = images.name.split(".")[-1].lower()
								newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
								fs.save(user_folder+newfilename, images)
								fullfilename		=	str(currentMonth)+str(currentYear)+"/"+newfilename
							else:
								fullfilename	=	""
						else:
							fullfilename		=	""
							
						if fromData in dic["multiVisitOphthalmologyImagesRight"] and key+"_comment" in dic["multiVisitOphthalmologyImagesRight"][fromData]:
							comment			=	dic["multiVisitOphthalmologyImagesRight"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["multiVisitOphthalmologyImagesRight"] and key+"_date" in dic["multiVisitOphthalmologyImagesRight"][fromData]:
							date			=	dic["multiVisitOphthalmologyImagesRight"][fromData][key+"_date"]
						else:
							date			=	""
					
						if fullfilename:	
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages()
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.patient_id		=	lastPatientId
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.key				=	key
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.value			=	fullfilename
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_name		=	field_name
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_direction	=	field_direction
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.comments		=	comment
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.date			=	date
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.save()
							
		
		### multiVisitOphthalmologyImagesLeft	
		dic = {}
		for k in request.FILES.keys():
			if k.startswith("multiVisitOphthalmologyImagesLeft"):
				rest = k[len("multiVisitOphthalmologyImagesLeft"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.FILES.get(k)
					
		for k in request.POST.keys():
			if k.startswith("multiVisitOphthalmologyImagesLeft"):
				rest = k[len("multiVisitOphthalmologyImagesLeft"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
		
		if step_images_name_list_left:
			for key in step_images_name_list_left:
				if dic["multiVisitOphthalmologyImagesLeft"]:
					for fromData in dic["multiVisitOphthalmologyImagesLeft"]:
						if fromData in dic["multiVisitOphthalmologyImagesLeft"] and key in dic["multiVisitOphthalmologyImagesLeft"][fromData]:
							images	=	dic["multiVisitOphthalmologyImagesLeft"][fromData][key]
							if images != "":
								fs = FileSystemStorage()
								filename = images.name.split(".")[0].lower()
								extension = images.name.split(".")[-1].lower()
								newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
								fs.save(user_folder+newfilename, images)
								fullfilename		=	str(currentMonth)+str(currentYear)+"/"+newfilename
							else:
								fullfilename	=	""
						else:
							fullfilename		=	""
							
						if fromData in dic["multiVisitOphthalmologyImagesLeft"] and key+"_comment" in dic["multiVisitOphthalmologyImagesLeft"][fromData]:
							comment			=	dic["multiVisitOphthalmologyImagesLeft"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["multiVisitOphthalmologyImagesLeft"] and key+"_date" in dic["multiVisitOphthalmologyImagesLeft"][fromData]:
							date			=	dic["multiVisitOphthalmologyImagesLeft"][fromData][key+"_date"]
						else:
							date			=	""
					
						if fullfilename:	
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages()
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.patient_id		=	lastPatientId
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.key				=	key
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.value			=	fullfilename
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_name		=	field_name
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_direction	=	field_direction
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.comments		=	comment
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.date			=	date
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.save()
							
							
							
							
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'static/ophthalmology/multi_visit_ophthalmology_images/'+str(currentMonth)+str(currentYear)+"/"
		if not os.path.exists(user_folder):
			os.mkdir(user_folder)		
				
		### otherMultiVisitImagesLeft	
		dic = {}
		for k in request.FILES.keys():
			if k.startswith("otherMultiVisitImagesLeft"):
				rest = k[len("otherMultiVisitImagesLeft"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.FILES.get(k)
					
		for k in request.POST.keys():
			if k.startswith("otherMultiVisitImagesLeft"):
				rest = k[len("otherMultiVisitImagesLeft"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
		
		if step_other_multi_visit_images_left:
			for key in step_other_multi_visit_images_left:
				if dic["otherMultiVisitImagesLeft"]:
					for fromData in dic["otherMultiVisitImagesLeft"]:
						if fromData in dic["otherMultiVisitImagesLeft"] and key in dic["otherMultiVisitImagesLeft"][fromData]:
							images	=	dic["otherMultiVisitImagesLeft"][fromData][key]
							if images != "":
								fs = FileSystemStorage()
								filename = images.name.split(".")[0].lower()
								extension = images.name.split(".")[-1].lower()
								newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
								fs.save(user_folder+newfilename, images)
								fullfilename		=	str(currentMonth)+str(currentYear)+"/"+newfilename
							else:
								fullfilename	=	""
						else:
							fullfilename		=	""
							
						if fromData in dic["otherMultiVisitImagesLeft"] and key+"_comment" in dic["otherMultiVisitImagesLeft"][fromData]:
							comment			=	dic["otherMultiVisitImagesLeft"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["otherMultiVisitImagesLeft"] and key+"_date" in dic["otherMultiVisitImagesLeft"][fromData]:
							date			=	dic["otherMultiVisitImagesLeft"][fromData][key+"_date"]
						else:
							date			=	""
					
						if fullfilename:	
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							PatientOtherMultiVisitImagesInfo	=	PatientOtherMultiVisitImages()
							PatientOtherMultiVisitImagesInfo.patient_id		=	lastPatientId
							PatientOtherMultiVisitImagesInfo.key				=	key
							PatientOtherMultiVisitImagesInfo.value			=	fullfilename
							PatientOtherMultiVisitImagesInfo.field_name		=	field_name
							PatientOtherMultiVisitImagesInfo.field_direction	=	field_direction
							PatientOtherMultiVisitImagesInfo.comments		=	comment
							PatientOtherMultiVisitImagesInfo.date			=	date
							PatientOtherMultiVisitImagesInfo.save()			
		
		
		### otherMultiVisitImagesRight	
		dic = {}
		for k in request.FILES.keys():
			if k.startswith("otherMultiVisitImagesRight"):
				rest = k[len("otherMultiVisitImagesRight"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.FILES.get(k)
					
		for k in request.POST.keys():
			if k.startswith("otherMultiVisitImagesRight"):
				rest = k[len("otherMultiVisitImagesRight"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
		
		if step_other_multi_visit_images_right:
			for key in step_other_multi_visit_images_right:
				if dic["otherMultiVisitImagesRight"]:
					for fromData in dic["otherMultiVisitImagesRight"]:
						if fromData in dic["otherMultiVisitImagesRight"] and key in dic["otherMultiVisitImagesRight"][fromData]:
							images	=	dic["otherMultiVisitImagesRight"][fromData][key]
							if images != "":
								fs = FileSystemStorage()
								filename = images.name.split(".")[0].lower()
								extension = images.name.split(".")[-1].lower()
								newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
								fs.save(user_folder+newfilename, images)
								fullfilename		=	str(currentMonth)+str(currentYear)+"/"+newfilename
							else:
								fullfilename	=	""
						else:
							fullfilename		=	""
							
						if fromData in dic["otherMultiVisitImagesRight"] and key+"_comment" in dic["otherMultiVisitImagesRight"][fromData]:
							comment			=	dic["otherMultiVisitImagesRight"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["otherMultiVisitImagesRight"] and key+"_date" in dic["otherMultiVisitImagesRight"][fromData]:
							date			=	dic["otherMultiVisitImagesRight"][fromData][key+"_date"]
						else:
							date			=	""
					
						if fullfilename:	
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							PatientOtherMultiVisitImagesInfo	=	PatientOtherMultiVisitImages()
							PatientOtherMultiVisitImagesInfo.patient_id		=	lastPatientId
							PatientOtherMultiVisitImagesInfo.key				=	key
							PatientOtherMultiVisitImagesInfo.value			=	fullfilename
							PatientOtherMultiVisitImagesInfo.field_name		=	field_name
							PatientOtherMultiVisitImagesInfo.field_direction	=	field_direction
							PatientOtherMultiVisitImagesInfo.comments		=	comment
							PatientOtherMultiVisitImagesInfo.date			=	date
							PatientOtherMultiVisitImagesInfo.save()	

		### generalInfoMultiVisit	
		dic = {}			
		for k in request.POST.keys():
			if k.startswith("generalInfoMultiVisit"):
				rest = k[len("generalInfoMultiVisit"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
				
		patient_general_info_multi_visit_stright	=	["logmar_visual_acuity_right","logmar_visual_acuity_left","logmar_visual_acuity_classification_right","logmar_visual_acuity_classification_left","blood_pressure_systolic_mmhg","blood_pressure_diastolic_mmhg","hypertension_classification","hypertension_medication","blood_total_cholesterol_level_mgdl","blood_ldl_cholesterol_level_mgdl","hypercholestremia_classification","hypercholestremia_medication","fasting_blood_glucose_mgdl","hba1c_percentage","diabetes_mellitus","diabetes_mellitus_medication","clinical_course_of_systemic_disorder_or_no_systemic_disorder","typical"]
		
		if patient_general_info_multi_visit_stright:
			
			for key in patient_general_info_multi_visit_stright:
				if dic["generalInfoMultiVisit"]:
					for fromData in dic["generalInfoMultiVisit"]:
						if fromData in dic["generalInfoMultiVisit"] and key in dic["generalInfoMultiVisit"][fromData]:
							value			=	dic["generalInfoMultiVisit"][fromData][key]
						else:
							value		=	""
							
						if fromData in dic["generalInfoMultiVisit"] and key+"_comment" in dic["generalInfoMultiVisit"][fromData]:
							comment			=	dic["generalInfoMultiVisit"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["generalInfoMultiVisit"] and key+"_date" in dic["generalInfoMultiVisit"][fromData]:
							date			=	dic["generalInfoMultiVisit"][fromData][key+"_date"]
						else:
							date			=	""
						
						if fromData in dic["generalInfoMultiVisit"] and key+"_other" in dic["generalInfoMultiVisit"][fromData]:
							other			=	dic["generalInfoMultiVisit"][fromData][key+"_other"]
						else:
							other			=	""
						
						if value:	
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							elif "_right" in key:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							else:
								field_name			=	key
								field_direction		=	"";
							
							get_model_name		=	value.split("_")
							#return HttpResponse(len(get_model_name))
							if len(get_model_name) > 1:
								value		=	get_model_name[1]
								model_name	=	get_model_name[0]
							else:
								value		=	get_model_name[0]
								model_name	=	""
								
							PatientGeneralInfoMultiVisitInfo					=	PatientGeneralInfoMultiVisit()
							PatientGeneralInfoMultiVisitInfo.patient_id			=	lastPatientId
							PatientGeneralInfoMultiVisitInfo.key				=	key
							PatientGeneralInfoMultiVisitInfo.value				=	value
							PatientGeneralInfoMultiVisitInfo.field_name			=	field_name
							PatientGeneralInfoMultiVisitInfo.field_direction	=	field_direction
							PatientGeneralInfoMultiVisitInfo.other				=	other
							PatientGeneralInfoMultiVisitInfo.comments			=	comment
							PatientGeneralInfoMultiVisitInfo.date				=	date
							PatientGeneralInfoMultiVisitInfo.model_name			=	model_name
							PatientGeneralInfoMultiVisitInfo.save()

		
		### generalInfoMultiVisitOphthalmology	
		dic = {}			
		for k in request.POST.keys():
			if k.startswith("generalInfoMultiVisitOphthalmology"):
				rest = k[len("generalInfoMultiVisitOphthalmology"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
				
		general_info_multi_visit_ophthalmology_static	=	["fund_phot_left","intra_ocul_pres_right","intra_ocul_pres_clas_right","intra_ocul_pres_left","intra_ocul_pres_clas_left","refr_error_sphe_equi_clas_right","refr_error_sphe_equi_left","refr_error_sphe_equi_clas_left","corn_thic_right","corn_thic_left","lens_right","lens_left","axia_leng_right","axia_leng_clas_right","axia_leng_left","axia_leng_clas_left","macu_thic_right","macu_edema_right","macu_schisis_right","epir_memb_right","sub_sensreti_fuild_right","sub_reti_epith_memb_fuild_right","macu_thic_left","macu_edema_left","macu_schisis_left","epir_memb_left","sub_sensreti_fuild_left","sub_reti_epith_memb_fuild_left","foveal_thic_right","foveal_thic_left","choro_thic_right","choro_thic_left","stat_peri_mean_sens_hfa24_2_right","stat_peri_mean_sens_clas_right","stat_peri_mean_sens_hfa24_2_left","stat_peri_mean_sens_clas_left","electro_right","full_field_electphysiol_clas_right","multi_electphysiol_clas_right","electroneg_config_of_dark_apa","electro_left","full_field_electphysiol_clas_left","multi_electphysiol_clas_left","ai_diagnosis_for_others_right","ai_accuracy_for_others_right_per","ai_diagnosis_for_others_left","ai_accuracy_for_others_left_per","ai_comments"]
		
		if general_info_multi_visit_ophthalmology_static:
			
			for key in general_info_multi_visit_ophthalmology_static:
				if dic["generalInfoMultiVisitOphthalmology"]:
					for fromData in dic["generalInfoMultiVisitOphthalmology"]:
						if fromData in dic["generalInfoMultiVisitOphthalmology"] and key in dic["generalInfoMultiVisitOphthalmology"][fromData]:
							value			=	dic["generalInfoMultiVisitOphthalmology"][fromData][key]
						else:
							value		=	""
							
						if fromData in dic["generalInfoMultiVisitOphthalmology"] and key+"_comment" in dic["generalInfoMultiVisitOphthalmology"][fromData]:
							comment			=	dic["generalInfoMultiVisitOphthalmology"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["generalInfoMultiVisitOphthalmology"] and key+"_date" in dic["generalInfoMultiVisitOphthalmology"][fromData]:
							date			=	dic["generalInfoMultiVisitOphthalmology"][fromData][key+"_date"]
						else:
							date			=	""
						
						if fromData in dic["generalInfoMultiVisitOphthalmology"] and key+"_other" in dic["generalInfoMultiVisitOphthalmology"][fromData]:
							other			=	dic["generalInfoMultiVisitOphthalmology"][fromData][key+"_other"]
						else:
							other			=	""
						
						if value:	
							if "_left" in key:
								#field_name			=	key.replace("_left","");
								field_direction		=	"left";
							elif "_right" in key:
								#field_name			=	key.replace("_right","");
								field_direction		=	"right";
							else:
								field_name			=	key
								field_direction		=	"";
							
							field_name				=	key
							
							get_model_name		=	value.split("_")
							#return HttpResponse(len(get_model_name))
							if len(get_model_name) > 1:
								value		=	get_model_name[1]
								model_name	=	get_model_name[0]
							else:
								value		=	get_model_name[0]
								model_name	=	""
								
							PatientGeneralInfoMultiVisitOphthalmologyInfo					=	PatientGeneralInfoMultiVisitOphthalmology()
							PatientGeneralInfoMultiVisitOphthalmologyInfo.patient_id		=	lastPatientId
							PatientGeneralInfoMultiVisitOphthalmologyInfo.key				=	key
							PatientGeneralInfoMultiVisitOphthalmologyInfo.value				=	value
							PatientGeneralInfoMultiVisitOphthalmologyInfo.field_name		=	field_name
							PatientGeneralInfoMultiVisitOphthalmologyInfo.field_direction	=	field_direction
							PatientGeneralInfoMultiVisitOphthalmologyInfo.other				=	other
							PatientGeneralInfoMultiVisitOphthalmologyInfo.comments			=	comment
							PatientGeneralInfoMultiVisitOphthalmologyInfo.date				=	date
							PatientGeneralInfoMultiVisitOphthalmologyInfo.model_name		=	model_name
							PatientGeneralInfoMultiVisitOphthalmologyInfo.save()
							
							
		##return HttpResponse(PatientGeneralInfoMultiVisitOphthalmologyInfo.id)
					
			### multiVisitOphthalmologyAi	
		dic = {}			
		for k in request.POST.keys():
			if k.startswith("multiVisitOphthalmologyAi"):
				rest = k[len("multiVisitOphthalmologyAi"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
					
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
				
		multi_visit_ophthalmology_ai_static	=	["ai_diag_corn_dise_corn_phot_right","ai_accu_corn_diag_corn_phot_right_per","ai_diag_corn_dise_corn_phot_left","ai_accu_corn_diag_corn_phot_left_per","ai_diag_corn_dise_corn_phot_on_fluo_right","ai_accu_corn_diag_corn_phot_on_fluo_right_per","ai_diag_corn_dise_corn_phot_on_fluo_left","ai_accu_corn_diag_corn_phot_on_fluo_left_per","ai_diag_glau_fundus_phot_right","ai_accu_glau_fundus_phot_right_per","ai_diag_glau_fundus_phot_left","ai_accu_glau_fundus_phot_left_per","ai_diag_glau_opti_cohe_tomo_disc_right","ai_accu_glau_opti_cohe_tomo_disc_right_per","ai_diag_glau_opti_cohe_tomo_disc_left","ai_accu_glau_opti_cohe_tomo_disc_left_per","ai_diag_glau_static_perimetry_right","ai_accu_glau_static_perimetry_right_per","ai_diag_glau_static_visual_field_left","ai_accu_glau_static_visual_field_left_per","ai_diag_diab_retino_fundus_phot_right","ai_accu_diab_retino_fundus_phot_right_per","ai_diag_diab_retino_fundus_phot_left","ai_accu_diab_retino_fundus_phot_left_per","ai_diag_diab_retino_fluo_angio_right","ai_accu_diab_retino_fluo_angio_right_per","ai_diagnsis_diab_retino_fluo_angio_left","ai_accu_diab_retino_fluo_angio_left_per","ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right","ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per","ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left","ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per","ai_diag_age_relat_macu_degen_fundus_phot_right","ai_accu_age_relat_macu_degen_fundus_phot_right_per","ai_diag_age_relat_macu_degen_fundus_phot_left","ai_accu_age_relat_macu_degen_fundus_phot_left_per","ai_diag_age_relat_macu_degen_fluo_angio_right","ai_accu_age_relat_macu_degen_fluo_angio_right_per","ai_diag_age_relat_macu_degen_fluo_angio_left","ai_accu_age_relat_macu_degen_fluo_angio_left_per","ai_diag_age_relat_macu_degen_indocy_green_angio_right","ai_accu_age_relat_macu_degen_indocy_green_angio_right_per","ai_diag_age_relat_macu_degen_indocy_green_angio_left","ai_accu_age_relat_macu_degen_indocy_green_angio_left_per","ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right","ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per","ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left","ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per","ai_diag_inheri_retin_dise_fundus_phot_right","ai_accu_inheri_retin_dise_fundus_phot_right_per","ai_diag_inheri_retin_dise_fundus_phot_left","ai_accu_inheri_retin_dise_fundus_phot_left_per","ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right","ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per","ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left","ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per","ai_diag_inheri_retin_dise_full_field_electroret_right","ai_accu_inheri_retin_dise_full_field_electroret_right_per","ai_diag_inheri_retin_dise_full_field_electroret_left","ai_accu_inheri_retin_dise_full_field_electroret_left_per","ai_diag_inheri_retin_dise_multifocal_electroret_right","ai_accu_inheri_retin_dise_multifocal_electroret_right_per","ai_diag_inheri_retin_dise_multifocal_electroret_left","ai_accu_inheri_retin_dise_multifocal_electroret_left_per","ai_diag_inheri_retin_dise_vcf_files_right","ai_accu_inheri_retin_dise_vcf_files_right_per","ai_diag_inheri_retin_dise_vcf_files_left","ai_accu_inheri_retin_dise_vcf_files_left_per"]
		
		if multi_visit_ophthalmology_ai_static:
			
			for key in multi_visit_ophthalmology_ai_static:
				if dic["multiVisitOphthalmologyAi"]:
					for fromData in dic["multiVisitOphthalmologyAi"]:
						if fromData in dic["multiVisitOphthalmologyAi"] and key in dic["multiVisitOphthalmologyAi"][fromData]:
							value			=	dic["multiVisitOphthalmologyAi"][fromData][key]
						else:
							value		=	""
							
						if fromData in dic["multiVisitOphthalmologyAi"] and key+"_comment" in dic["multiVisitOphthalmologyAi"][fromData]:
							comment			=	dic["multiVisitOphthalmologyAi"][fromData][key+"_comment"]
						else:
							comment			=	""
						
						if fromData in dic["multiVisitOphthalmologyAi"] and key+"_date" in dic["multiVisitOphthalmologyAi"][fromData]:
							date			=	dic["multiVisitOphthalmologyAi"][fromData][key+"_date"]
						else:
							date			=	""
						
						if fromData in dic["multiVisitOphthalmologyAi"] and key+"_other" in dic["multiVisitOphthalmologyAi"][fromData]:
							other			=	dic["multiVisitOphthalmologyAi"][fromData][key+"_other"]
						else:
							other			=	""
						
						if value:	
							if "_left" in key:
								#field_name			=	key.replace("_left","");
								field_direction		=	"left";
							elif "_right" in key:
								#field_name			=	key.replace("_right","");
								field_direction		=	"right";
							else:
								field_name			=	key
								field_direction		=	"";
							
							field_name				=	key
							
							get_model_name		=	value.split("_")
							#return HttpResponse(len(get_model_name))
							if len(get_model_name) > 1:
								value		=	get_model_name[1]
								model_name	=	get_model_name[0]
							else:
								value		=	get_model_name[0]
								model_name	=	""
								
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo					=	PatientGeneralInfoMultiVisitOphthalmologyAi()
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.patient_id		=	lastPatientId
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.key				=	key
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.value			=	value
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.field_name		=	field_name
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.field_direction	=	field_direction
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.other			=	other
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.comments		=	comment
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.date			=	date
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.model_name		=	model_name
							PatientGeneralInfoMultiVisitOphthalmologyAiInfo.save()
							
							
		##return HttpResponse(PatientGeneralInfoMultiVisitOphthalmologyAiInfo.id)				
							
							
							
		
		#### save data in PatientOtherCommonInfo model in step 5 ####
		PatientOtherCommonInfoDetial						=	PatientOtherCommonInfo()
		PatientOtherCommonInfoDetial.patient_id				=	lastPatientId
		PatientOtherCommonInfoDetial.direct_sequencing_1_id	=	request.POST.get("direct_sequencing_1","")
		PatientOtherCommonInfoDetial.direct_sequencing_1_other	=	request.POST.get("direct_sequencing_1_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_2_id	=	request.POST.get("direct_sequencing_2","")
		PatientOtherCommonInfoDetial.direct_sequencing_2_other	=	request.POST.get("direct_sequencing_2_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_3_id	=	request.POST.get("direct_sequencing_3","")
		PatientOtherCommonInfoDetial.direct_sequencing_3_other	=	request.POST.get("direct_sequencing_3_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_4_id	=	request.POST.get("direct_sequencing_4","")
		PatientOtherCommonInfoDetial.direct_sequencing_4_other	=	request.POST.get("direct_sequencing_4_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_5_id	=	request.POST.get("direct_sequencing_5","")
		PatientOtherCommonInfoDetial.direct_sequencing_5_other	=	request.POST.get("direct_sequencing_5_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_id	=	request.POST.get("targt_enrichment_ngs_panel_1","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_other	=	request.POST.get("targt_enrichment_ngs_panel_1_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_id	=	request.POST.get("targt_enrichment_ngs_panel_analysis_1","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_id	=	request.POST.get("targt_enrichment_ngs_panel_2","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_other	=	request.POST.get("targt_enrichment_ngs_panel_2_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_id	=	request.POST.get("targt_enrichment_ngs_panel_analysis_2","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_2_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_id	=	request.POST.get("targt_enrichment_ngs_panel_3","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_other	=	request.POST.get("targt_enrichment_ngs_panel_3_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_id	=	request.POST.get("targt_enrichment_ngs_panel_analysis_3","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_3_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_id	=	request.POST.get("targt_enrichment_ngs_panel_4","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_other	=	request.POST.get("targt_enrichment_ngs_panel_4_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_id	=	request.POST.get("targt_enrichment_ngs_panel_analysis_4","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_4_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_id	=	request.POST.get("targt_enrichment_ngs_panel_5","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_other	=	request.POST.get("targt_enrichment_ngs_panel_5_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_id	=	request.POST.get("targt_enrichment_ngs_panel_analysis_5","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_5_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_1_id	=	request.POST.get("targt_exome_sequencing_1","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_1_other	=	request.POST.get("targt_exome_sequencing_1_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other	=	request.POST.get("targt_exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_id	=	request.POST.get("targt_exome_sequencing_analysis_1","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other	=	request.POST.get("targt_exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_2_id	=	request.POST.get("targt_exome_sequencing_2","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_2_other	=	request.POST.get("targt_exome_sequencing_2_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_id	=	request.POST.get("targt_exome_sequencing_analysis_2","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_other	=	request.POST.get("targt_exome_sequencing_analysis_2_other","")
		PatientOtherCommonInfoDetial.exome_sequencing_1_id	=	request.POST.get("exome_sequencing_1","")
		PatientOtherCommonInfoDetial.exome_sequencing_1_other	=	request.POST.get("exome_sequencing_1_other","")
		PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_id	=	request.POST.get("exome_sequencing_analysis_1","")
		PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_other	=	request.POST.get("exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_1_id	=	request.POST.get("whole_exome_sequencing_1","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_1_other	=	request.POST.get("whole_exome_sequencing_1_other","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_id	=	request.POST.get("whole_exome_sequencing_analysis_1","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_other	=	request.POST.get("whole_exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_id	=	request.POST.get("sequencing_other_collaborators_1","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_other	=	request.POST.get("sequencing_other_collaborators_1_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_id	=	request.POST.get("sequencing_other_collaborators_analysis_1","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_other	=	request.POST.get("sequencing_other_collaborators_analysis_1_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_id	=	request.POST.get("sequencing_other_collaborators_2","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_other	=	request.POST.get("sequencing_other_collaborators_2_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_id	=	request.POST.get("sequencing_other_collaborators_analysis_2","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_other	=	request.POST.get("sequencing_other_collaborators_analysis_2_other","")
		PatientOtherCommonInfoDetial.beadarray_platform_1_id	=	request.POST.get("beadarray_platform_1","")
		PatientOtherCommonInfoDetial.beadarray_platform_1_other	=	request.POST.get("beadarray_platform_1_other","")
		PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_id	=	request.POST.get("beadarray_platform_analysis_1","")
		PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_other	=	request.POST.get("beadarray_platform_analysis_1_other","")
		PatientOtherCommonInfoDetial.other_sequencing_id	=	request.POST.get("other_sequencing","")
		PatientOtherCommonInfoDetial.other_sequencing_other	=	request.POST.get("other_sequencing_other","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_id	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_1","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_other	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_1_other","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_id	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_analysis_1","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_other	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_id	=	request.POST.get("targt_mitochondrial_sequence_2","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_other	=	request.POST.get("targt_mitochondrial_sequence_2_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_id	=	request.POST.get("targt_mitochondrial_sequence_analysis_2","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_other	=	request.POST.get("targt_mitochondrial_sequence_analysis_2_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_id	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_3","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_other	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_3_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_id	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_analysis_3","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other","")
		PatientOtherCommonInfoDetial.other_analysis_id	=	request.POST.get("other_analysis","")
		PatientOtherCommonInfoDetial.other_analysis_other	=	request.POST.get("other_analysis_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_1_comments	=	request.POST.get("direct_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_2_comments	=	request.POST.get("direct_sequencing_2_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_3_comments	=	request.POST.get("direct_sequencing_3_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_4_comments	=	request.POST.get("direct_sequencing_4_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_5_comments	=	request.POST.get("direct_sequencing_5_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_comments	=	request.POST.get("targt_enrichment_ngs_panel_1_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_1_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_comments	=	request.POST.get("targt_enrichment_ngs_panel_2_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_2_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_comments	=	request.POST.get("targt_enrichment_ngs_panel_3_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_3_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_comments	=	request.POST.get("targt_enrichment_ngs_panel_4_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_4_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_comments	=	request.POST.get("targt_enrichment_ngs_panel_5_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_5_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_1_comments	=	request.POST.get("targt_exome_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_comments	=	request.POST.get("targt_exome_sequencing_analysis_1_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_2_comments	=	request.POST.get("targt_exome_sequencing_2_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_comments	=	request.POST.get("targt_exome_sequencing_analysis_2_comments","")
		PatientOtherCommonInfoDetial.exome_sequencing_1_comments	=	request.POST.get("exome_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_comments	=	request.POST.get("exome_sequencing_analysis_1_comments","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_1_comments	=	request.POST.get("whole_exome_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_comments	=	request.POST.get("whole_exome_sequencing_analysis_1_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_comments	=	request.POST.get("sequencing_other_collaborators_1_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_comments	=	request.POST.get("sequencing_other_collaborators_analysis_1_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_comments	=	request.POST.get("sequencing_other_collaborators_2_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_comments	=	request.POST.get("sequencing_other_collaborators_analysis_2_comments","")
		PatientOtherCommonInfoDetial.beadarray_platform_1_comments	=	request.POST.get("beadarray_platform_1_comments","")
		PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_comments	=	request.POST.get("beadarray_platform_analysis_1_comments","")
		PatientOtherCommonInfoDetial.other_sequencing_comments	=	request.POST.get("other_sequencing_comments","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_comments	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_1_comments","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_comments	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_analysis_1_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_comments	=	request.POST.get("targt_mitochondrial_sequence_2_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_comments	=	request.POST.get("targt_mitochondrial_sequence_analysis_2_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_comments	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_3_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments","")
		PatientOtherCommonInfoDetial.other_analysis_comments	=	request.POST.get("other_analysis_comments","")
		PatientOtherCommonInfoDetial.save()
		#### save data in PatientOtherCommonInfo model in step 5 ####
		
		#### save data in patientCausativeGeneInfo model in step 5 ####
		dic = {}			
		for k in request.POST.keys():
			if k.startswith("patientCausativeGeneInfo"):
				rest = k[len("patientCausativeGeneInfo"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
				
				if field_name_3 == "freq_local_population" or field_name_3 == "freq_ethnicity":
					dic[field_name_1][field_name_2][field_name_3]		=	request.POST.getlist(k)
				else:
					dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
				
			
		
		
		
		##return HttpResponse(dic["patientCausativeGeneInfo"]["0"])
		if dic["patientCausativeGeneInfo"]:
			for fromData in dic["patientCausativeGeneInfo"]:
				if fromData in dic["patientCausativeGeneInfo"] and "type_old_new" in dic["patientCausativeGeneInfo"][fromData]:
					type_old_new		=	dic["patientCausativeGeneInfo"][fromData]["type_old_new"]
				else:
					type_old_new		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand"]
				else:
					caus_cand		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_gene" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_gene		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_gene"]
				else:
					caus_cand_gene		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "chromosome" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome		=	dic["patientCausativeGeneInfo"][fromData]["chromosome"]
				else:
					chromosome		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "chromosome_comment" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome_comment		=	dic["patientCausativeGeneInfo"][fromData]["chromosome_comment"]
				else:
					chromosome_comment		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "position" in dic["patientCausativeGeneInfo"][fromData]:
					position		=	dic["patientCausativeGeneInfo"][fromData]["position"]
				else:
					position		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "transcript" in dic["patientCausativeGeneInfo"][fromData]:
					transcript		=	dic["patientCausativeGeneInfo"][fromData]["transcript"]
				else:
					transcript		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "exon" in dic["patientCausativeGeneInfo"][fromData]:
					exon		=	dic["patientCausativeGeneInfo"][fromData]["exon"]
				else:
					exon		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "exon_comment" in dic["patientCausativeGeneInfo"][fromData]:
					exon_comment		=	dic["patientCausativeGeneInfo"][fromData]["exon_comment"]
				else:
					exon_comment		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_mutation_nucleotide_amino_acid" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_mutation_nucleotide_amino_acid		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_mutation_nucleotide_amino_acid"]
				else:
					caus_cand_mutation_nucleotide_amino_acid		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_mutation_nucleotide_amino_acid_comment" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_mutation_nucleotide_amino_acid_comment		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_mutation_nucleotide_amino_acid_comment"]
				else:
					caus_cand_mutation_nucleotide_amino_acid_comment		=	""
					
				##return HttpResponse(caus_gene)	
				#Patient_causative_gene_info_arr	=	["type_old_new","caus_gene","chromosome","position","transcript","exon","caus_mutation_nucleotide_change_amino_acid_change","freq_ethnicity","freq_local_population","comment","date"]
				
				PatientCausativeGeneInfoInfo									=	PatientCausativeGeneInfo()
				PatientCausativeGeneInfoInfo.patient_id							=	lastPatientId
				PatientCausativeGeneInfoInfo.type_old_new_id					=	type_old_new
				PatientCausativeGeneInfoInfo.caus_cand_id						=	caus_cand
				PatientCausativeGeneInfoInfo.caus_cand_gene_id					=	caus_cand_gene
				PatientCausativeGeneInfoInfo.chromosome_id						=	chromosome
				PatientCausativeGeneInfoInfo.chromosome_comment					=	chromosome_comment
				PatientCausativeGeneInfoInfo.position							=	position
				PatientCausativeGeneInfoInfo.transcript							=	transcript
				PatientCausativeGeneInfoInfo.exon_id							=	exon
				PatientCausativeGeneInfoInfo.exon_comment						=	exon_comment
				PatientCausativeGeneInfoInfo.caus_cand_mutation_nucleotide_amino_acid	=	caus_cand_mutation_nucleotide_amino_acid
				PatientCausativeGeneInfoInfo.caus_cand_mutation_nucleotide_amino_acid_comment	=	caus_cand_mutation_nucleotide_amino_acid_comment
				PatientCausativeGeneInfoInfo.save()
				

				#return HttpResponse(PatientCausativeGeneInfoInfo.id)
				latTableId	=	PatientCausativeGeneInfoInfo.id
				
				# if dic["patientCausativeGeneInfo"][fromData]["freq_ethnicity"]:
					# if request.POST.getlist(dic["patientCausativeGeneInfo"][fromData]["freq_ethnicity"]) !='':
						# for value in request.POST.getlist(dic["patientCausativeGeneInfo"][fromData]["freq_ethnicity"]):
							# PatientCausativeGeneInfoEthnicityInfo									=	PatientCausativeGeneInfoEthnicity()
							# PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_id					=	value
							# PatientCausativeGeneInfoEthnicityInfo.patient_causative_gene_info_id	=	latTableId
							# PatientCausativeGeneInfoEthnicityInfo.save()
							# return HttpResponse(PatientCausativeGeneInfoEthnicityInfo)
							
				# if dic["patientCausativeGeneInfo"][fromData]["freq_local_population"] !="":
					# if request.POST.getlist(dic["patientCausativeGeneInfo"][fromData]["freq_local_population"]):
						# for value in request.POST.getlist(dic["patientCausativeGeneInfo"][fromData]["freq_local_population"]):
							# PatientCausativeGeneInfoLocalPopulationInfo									=	PatientCausativeGeneInfoLocalPopulation()
							# PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_id			=	value
							# PatientCausativeGeneInfoLocalPopulationInfo.patient_causative_gene_info_id	=	latTableId
							# PatientCausativeGeneInfoLocalPopulationInfo.save()
				
				
		
		
		
		#### save data in PatientCausativeGeneInfo model in step 5 ####
		
		#### save data in PatientGeneralInfoOphthalmologySystAbnormality model in step 5 ####
		dic = {}			
		for k in request.POST.keys():
			if k.startswith("systemicAbnormality"):
				rest = k[len("systemicAbnormality"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
				
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
		
		if dic["systemicAbnormality"]:
			
			for fromData in dic["systemicAbnormality"]:
				##return HttpResponse(dic["systemicAbnormality"][fromData]["systemicAbnormality_name"])
				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name" in dic["systemicAbnormality"][fromData]:
					systemicAbnormality_name		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name"]
				else:
					systemicAbnormality_name		=	""
					
				if fromData in dic["systemicAbnormality"] and "name_comment" in dic["systemicAbnormality"][fromData]:
					name_comment		=	dic["systemicAbnormality"][fromData]["name_comment"]
				else:
					name_comment		=	""
					
				if fromData in dic["systemicAbnormality"] and "name_date" in dic["systemicAbnormality"][fromData]:
					name_date		=	dic["systemicAbnormality"][fromData]["name_date"]
				else:
					name_date		=	""
				
				PatientGeneralInfoOphthalmologySystAbnormalityInfo					=	PatientGeneralInfoOphthalmologySystAbnormality()
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.patient_id		=	lastPatientId
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.name_id				=	systemicAbnormality_name
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.comments			=	name_comment
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.date				=	name_date
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.save()
					
		
		#### save data in PatientGeneralInfoOphthalmologySystAbnormality model in step 5 ####
		dic = {}			
		for k in request.POST.keys():
			if k.startswith("ocularSymptom"):
				rest = k[len("ocularSymptom"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				
				if field_name_1 not in dic:
					dic[field_name_1]								=	{}
				
				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}
				
				dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)
		
		if dic["ocularSymptom"]:
			for fromData in dic["ocularSymptom"]:
				if fromData in dic["ocularSymptom"] and "ocularSymptom_name" in dic["ocularSymptom"][fromData]:
					ocularSymptom_name		=	dic["ocularSymptom"][fromData]["ocularSymptom_name"]
				else:
					ocularSymptom_name		=	""
					
				if fromData in dic["ocularSymptom"] and "name_comment" in dic["ocularSymptom"][fromData]:
					name_comment		=	dic["ocularSymptom"][fromData]["name_comment"]
				else:
					name_comment		=	""
					
				if fromData in dic["ocularSymptom"] and "name_date" in dic["ocularSymptom"][fromData]:
					name_date		=	dic["ocularSymptom"][fromData]["name_date"]
				else:
					name_date		=	""
				
				PatientGeneralInfoOphthalmologyOcularCompliInfo					=	PatientGeneralInfoOphthalmologyOcularCompli()
				PatientGeneralInfoOphthalmologyOcularCompliInfo.patient_id		=	lastPatientId
				PatientGeneralInfoOphthalmologyOcularCompliInfo.name_id				=	ocularSymptom_name
				PatientGeneralInfoOphthalmologyOcularCompliInfo.comments			=	name_comment
				PatientGeneralInfoOphthalmologyOcularCompliInfo.date				=	name_date
				PatientGeneralInfoOphthalmologyOcularCompliInfo.save()
		
		
		##return HttpResponse(PatientGeneralInfoOphthalmologyOcularCompliInfo.id)
		
		
		# step4_image_arr			=	{}
		# if step_images_name_list_right:
			# for field_name in step_images_name_list_right:
				# if len(request.FILES.getlist(field_name)) > 0:
					# field_name_arr	=	request.FILES.getlist(field_name)
					# counter	=	1
					# for images in field_name_arr:
						# fs = FileSystemStorage()
						# filename = images.name.split(".")[0].lower()
						# extension = images.name.split(".")[-1].lower()
						# newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
						# fs.save(user_folder+newfilename, images)
						# step4_image_arr[str(field_name)+"__"+str(counter)]		=	str(currentMonth)+str(currentYear)+"/"+newfilename
						# counter	+=	1
						
		# if step_images_name_list_left:
			# for field_name in step_images_name_list_left:
				# if len(request.FILES.getlist(field_name)) > 0:
					# field_name_arr	=	request.FILES.getlist(field_name)
					# counter	=	1
					# for images in field_name_arr:
						# fs = FileSystemStorage()
						# filename = images.name.split(".")[0].lower()
						# extension = images.name.split(".")[-1].lower()
						# newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
						# fs.save(user_folder+newfilename, images)
						# step4_image_arr[str(field_name)+"__"+str(counter)]		=	str(currentMonth)+str(currentYear)+"/"+newfilename
						# counter	+=	1
		# if step4_image_arr:
			# for key in step4_image_arr:
				# group_key	=	key.split("__")
				# del group_key[-1]
				# if "_left" in group_key[0]:
					# field_name			=	group_key[0].replace("_left","");
					# field_direction		=	"left";
				# else:
					# field_name			=	group_key[0].replace("_right","");
					# field_direction		=	"right";
		
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages()
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.patient_id		=	lastPatientId
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.key				=	key
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.value			=	step4_image_arr[key]
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_name		=	field_name
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_direction	=	field_direction
				# PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.save()
		#### save data in PatientGeneralInfoMultiVisitOphthalmologyImages model ####
		
		messages.success(request,"Patient has been added successfully.")
		return redirect('/ophthalmology/')
			
			

	Institudes	=	InstituteDt.objects.order_by("-name").all()
	RelationshipToProbandDts	=	RelationshipToProbandDt.objects.order_by("-name").all()
	SexDts	=	SexDt.objects.order_by("-name").all()
	DiseaseDts	=	DiseaseDt.objects.order_by("-name").all()
	AffectedDts	=	AffectedDt.objects.order_by("-name").all()
	InheritanceDts	=	InheritanceDt.objects.order_by("-name").all()
	SyndromicDts	=	SyndromicDt.objects.order_by("-name").all()
	BilateralDts	=	BilateralDt.objects.order_by("-name").all()
	OcularSymptomDts	=	OcularSymptomDt.objects.order_by("-name").all()
	ProgressionDts	=	ProgressionDt.objects.order_by("-name").all()
	FluctuationDts	=	FluctuationDt.objects.order_by("-name").all()
	FamilyHistoryDts	=	FamilyHistoryDt.objects.order_by("-name").all()
	ConsanguineousDts	=	ConsanguineousDt.objects.order_by("-name").all()
	NumberOfAffectedMembersInTheSamePedigreeDts	=	NumberOfAffectedMembersInTheSamePedigreeDt.objects.order_by("-name").all()
	EthnicityDts	=	EthnicityDt.objects.order_by("-name").all()
	CountryOfOriginDts	=	CountryOfOriginDt.objects.order_by("-name").all()
	OriginPrefectureInJapanDts	=	OriginPrefectureInJapanDt.objects.order_by("-name").all()
	GeneDts	=	GeneDt.objects.order_by("-name").all()
	MutationDts	=	MutationDt.objects.order_by("-name").all()
	OcularSurgeriesCorneaDts	=	OcularSurgeriesCorneaDt.objects.order_by("-name").all()
	AgeForSurgeryDts	=	AgeForSurgeryDt.objects.order_by("-name").all()
	NumberOfSurgeryDts	=	NumberOfSurgeryDt.objects.order_by("-name").all()
	OcularSurgeriesGlaucomaDts	=	OcularSurgeriesGlaucomaDt.objects.order_by("-name").all()
	OcularSurgeriesRetinaDts	=	OcularSurgeriesRetinaDt.objects.order_by("-name").all()
	OcularSurgeriesLasersDts	=	OcularSurgeriesLasersDt.objects.order_by("-name").all()
	OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDts	=	OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt.objects.order_by("-name").all()
	OcularMedicationInternalDts	=	OcularMedicationInternalDt.objects.order_by("-name").all()
	OcularMedicationTopicalDts	=	OcularMedicationTopicalDt.objects.order_by("-name").all()
	OcularSurgeriesCataractDts		=	OcularSurgeriesCataractDt.objects.order_by("-name").all()
	VisualAcuityDts					=	VisualAcuityDt.objects.order_by("-name").all()
	VisualAcuityClassificationDts	=	VisualAcuityClassificationDt.objects.order_by("-name").all()
	PresentUnpresentDts				=	PresentUnpresentDt.objects.order_by("-name").all()
	OnMedicationOrNotDts			=	OnMedicationOrNotDt.objects.order_by("-name").all()
	HcOnMedicationOrNotStatinDts			=	HcOnMedicationOrNotStatinDt.objects.order_by("-name").all()
	HcOnMedicationOrNotInsulinDts			=	HcOnMedicationOrNotInsulinDt.objects.order_by("-name").all()
	TypicalDts								=	TypicalDt.objects.order_by("-name").all()
	AgeAtOnsetOfOcularSymptomDts			=	AgeAtOnsetOfOcularSymptomDt.objects.order_by("-name").all()
	AgeAtTheInitialDiagnosisDts			=	AgeAtTheInitialDiagnosisDt.objects.order_by("-name").all()
	DnaExtractionInProcessDts			=	DnaExtractionInProcessDt.objects.order_by("-name").all()
	AnalysisDts			=	AnalysisDt.objects.order_by("-name").all()
	AgeAtOnsetClassificationDts			=	AgeAtOnsetClassificationDt.objects.order_by("-name").all()
	AgeAtTheInitialDiagnosisClassificationDts	=	AgeAtTheInitialDiagnosisClassificationDt.objects.order_by("-name").all()
	SequencingDts			=	SequencingDt.objects.order_by("-name").all()
	AiDiagnosisForCornealDiseasesDts			=	AiDiagnosisForCornealDiseasesDt.objects.order_by("-name").all()
	AiDiagnosisForGlaucomaDts			=	AiDiagnosisForGlaucomaDt.objects.order_by("-name").all()
	AiDiagnosisForDiabeticRetinopathyDts			=	AiDiagnosisForDiabeticRetinopathyDt.objects.order_by("-name").all()
	AiDiagnosisForAgeRelatedMacularDegenerationDts	=	AiDiagnosisForAgeRelatedMacularDegenerationDt.objects.order_by("-name").all()
	AiDiagnosisForInheritedRetinalDiseasesDts	=	AiDiagnosisForInheritedRetinalDiseasesDt.objects.order_by("-name").all()
	SequencingStatusDts	=	SequencingStatusDt.objects.order_by("-name").all()
	IntraocularPressureDts	=	IntraocularPressureDt.objects.order_by("-name").all()
	IntraocularPressureClassificationDts	=	IntraocularPressureClassificationDt.objects.order_by("-name").all()
	RefractiveErrorSphericalEquivalentDts	=	RefractiveErrorSphericalEquivalentDt.objects.order_by("-name").all()
	RefractiveErrorSphericalEquivalentClassificationDts	=	RefractiveErrorSphericalEquivalentClassificationDt.objects.order_by("-name").all()
	LensDts	=	LensDt.objects.order_by("-name").all()
	AxialLengthDts	=	AxialLengthDt.objects.order_by("-name").all()
	AxialLengthClassificationDts	=	AxialLengthClassificationDt.objects.order_by("-name").all()
	StaticPerimetryMeanSensitivityDts	=	StaticPerimetryMeanSensitivityDt.objects.order_by("-name").all()
	StaticPerimetryMeanSensitivityClassificationDts	=	StaticPerimetryMeanSensitivityClassificationDt.objects.order_by("-name").all()
	ElectrophysiologicalFindingsDts	=	ElectrophysiologicalFindingsDt.objects.order_by("-name").all()
	FullFieldElectrophysiologicalGroupingDts	=	FullFieldElectrophysiologicalGroupingDt.objects.order_by("-name").all()
	MultifocalElectrophysiologicalGroupingDts	=	MultifocalElectrophysiologicalGroupingDt.objects.order_by("-name").all()
	ChromosomeDts	=	ChromosomeDt.objects.order_by("-name").all()
	ExonDts	=	ExonDt.objects.order_by("-name").all()
	AlleleFrequencyDatabaseDts	=	AlleleFrequencyDatabaseDt.objects.order_by("-name").all()
	SystemicAbnormalityDts	=	SystemicAbnormalityDt.objects.order_by("-name").all()
	CausCandDts	=	CausCandDt.objects.order_by("-name").all()
	TypeOldNewDts	=	TypeOldNewDt.objects.order_by("-name").all()
	context		=	{
		"selected_disease_id":selected_disease_id,
		"assignedDiseases":assignedDiseases,
		"OcularSurgeriesCataractDts":OcularSurgeriesCataractDts,
		"Institudes":Institudes,
		"RelationshipToProbandDts":RelationshipToProbandDts,
		"SexDts":SexDts,
		"DiseaseDts":DiseaseDts,
		"AffectedDts":AffectedDts,
		"InheritanceDts":InheritanceDts,
		"SyndromicDts":SyndromicDts,
		"BilateralDts":BilateralDts,
		"OcularSymptomDts":OcularSymptomDts,
		"ProgressionDts":ProgressionDts,
		"FluctuationDts":FluctuationDts,
		"FamilyHistoryDts":FamilyHistoryDts,
		"ConsanguineousDts":ConsanguineousDts,
		"NumberOfAffectedMembersInTheSamePedigreeDts":NumberOfAffectedMembersInTheSamePedigreeDts,
		"EthnicityDts":EthnicityDts,
		"CountryOfOriginDts":CountryOfOriginDts,
		"OriginPrefectureInJapanDts":OriginPrefectureInJapanDts,
		"GeneDts":GeneDts,
		"MutationDts":MutationDts,
		"OcularSurgeriesCorneaDts":OcularSurgeriesCorneaDts,
		"AgeForSurgeryDts":AgeForSurgeryDts,
		"NumberOfSurgeryDts":NumberOfSurgeryDts,
		"OcularSurgeriesGlaucomaDts":OcularSurgeriesGlaucomaDts,
		"OcularSurgeriesRetinaDts":OcularSurgeriesRetinaDts,
		"OcularSurgeriesLasersDts":OcularSurgeriesLasersDts,
		"OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDts":OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDts,
		"OcularMedicationInternalDts":OcularMedicationInternalDts,
		"OcularMedicationTopicalDts":OcularMedicationTopicalDts,
		"step_images_name_list_left":step_images_name_list_left,
		"step_images_name_list_right":step_images_name_list_right,
		"step4_images_name_list_all":step4_images_name_list_all,
		"step_other_multi_visit_images_right":step_other_multi_visit_images_right,
		"step_other_multi_visit_images_left":step_other_multi_visit_images_left,
		"step_other_multi_visit_images_all":step_other_multi_visit_images_all,
		"VisualAcuityDts":VisualAcuityDts,
		"VisualAcuityClassificationDts":VisualAcuityClassificationDts,
		"PresentUnpresentDts":PresentUnpresentDts,
		"OnMedicationOrNotDts":OnMedicationOrNotDts,
		"HcOnMedicationOrNotStatinDts":HcOnMedicationOrNotStatinDts,
		"HcOnMedicationOrNotInsulinDts":HcOnMedicationOrNotInsulinDts,
		"TypicalDts":TypicalDts,
		"AgeAtOnsetOfOcularSymptomDts":AgeAtOnsetOfOcularSymptomDts,
		"AgeAtTheInitialDiagnosisDts":AgeAtTheInitialDiagnosisDts,
		"DnaExtractionInProcessDts":DnaExtractionInProcessDts,
		"AnalysisDts":AnalysisDts,
		"AgeAtOnsetClassificationDts":AgeAtOnsetClassificationDts,
		"AgeAtTheInitialDiagnosisClassificationDts":AgeAtTheInitialDiagnosisClassificationDts,
		"SequencingDts":SequencingDts,
		"AiDiagnosisForCornealDiseasesDts":AiDiagnosisForCornealDiseasesDts,
		"AiDiagnosisForGlaucomaDts":AiDiagnosisForGlaucomaDts,
		"AiDiagnosisForDiabeticRetinopathyDts":AiDiagnosisForDiabeticRetinopathyDts,
		"AiDiagnosisForAgeRelatedMacularDegenerationDts":AiDiagnosisForAgeRelatedMacularDegenerationDts,
		"AiDiagnosisForInheritedRetinalDiseasesDts":AiDiagnosisForInheritedRetinalDiseasesDts,
		"SequencingStatusDts":SequencingStatusDts,
		"IntraocularPressureDts":IntraocularPressureDts,
		"IntraocularPressureClassificationDts":IntraocularPressureClassificationDts,
		"RefractiveErrorSphericalEquivalentDts":RefractiveErrorSphericalEquivalentDts,
		"RefractiveErrorSphericalEquivalentClassificationDts":RefractiveErrorSphericalEquivalentClassificationDts,
		"LensDts":LensDts,
		"AxialLengthDts":AxialLengthDts,
		"AxialLengthClassificationDts":AxialLengthClassificationDts,
		"StaticPerimetryMeanSensitivityDts":StaticPerimetryMeanSensitivityDts,
		"StaticPerimetryMeanSensitivityClassificationDts":StaticPerimetryMeanSensitivityClassificationDts,
		"ElectrophysiologicalFindingsDts":ElectrophysiologicalFindingsDts,
		"FullFieldElectrophysiologicalGroupingDts":FullFieldElectrophysiologicalGroupingDts,
		"MultifocalElectrophysiologicalGroupingDts":MultifocalElectrophysiologicalGroupingDts,
		"ChromosomeDts":ChromosomeDts,
		"ExonDts":ExonDts,
		"AlleleFrequencyDatabaseDts":AlleleFrequencyDatabaseDts,
		"SystemicAbnormalityDts":SystemicAbnormalityDts,
		"CausCandDts":CausCandDts,
		"TypeOldNewDts":TypeOldNewDts
	}
	return render(request, 'ophthalmology/add_new_patient.html',context)
	

@login_required(login_url='/')
def view_new_patient(request,id):
	PatientGeneralInfoDetial = PatientGeneralInfo.objects.filter(id=id).select_related("institute","relationship_to_proband","sex","disease","affected","inheritance","syndromic","bilateral","ocular_symptom_1","ocular_symptom_2","ocular_symptom_3","progression","flactuation","family_history","consanguineous","number_of_affected_members_in_the_same_pedigree","ethnicity","country_of_origine","origin_prefecture_in_japan","ethnic_of_father","original_country_of_father","origin_of_father_in_japan","ethnic_of_mother","original_country_of_mother","origin_of_mother_in_japan","gene_type","inheritance_type","mutation_type","dna_extraction_process","sequencing","analysis").first()
	
	#return HttpResponse(PatientGeneralInfoDetial.institute_id)
	
	##PatientOtherUncommonInfoOphthalmology
	
	PatientOtherUncommonInfoOphthalmologyInfo	=	PatientOtherUncommonInfoOphthalmology.objects.filter(patient_id=id).select_related("ocul_surgeries_cornea_right","age_corneal_surgery_perf_right","no_corneal_surgery_perf_right","ocul_surgeries_glaucoma_right","age_glaucoma_surgery_perf_right","no_glaucomal_surgery_perf_right","ocul_surgeries_retina_right","age_vitreoretina_surgery_perf_right","no_vitreoretinal_surgery_perf_right","ocul_surgeries_lasers_right","age_ocul_surgeries_lasers_perf_right","no_ofocul_surgeries_lasers_perf_right","opht_medi_subtenon_subconj_injec_right","age_opht_medi_subtenon_subconj_injec_perf_right","no_opht_medi_subtenon_subconj_injec_perf_right","ocul_medi_internal_right","age_ocul_medi_internal_perf_right","no_ocul_medi_internal_perf_right","ocul_medi_topical_right","age_ocul_medi_topical_perf_right","no_ocul_medi_topical_perf_right","ocul_surgeries_cornea_left","age_corneal_surgery_perf_left","no_corneal_surgery_perf_left","ocul_surgeries_glaucoma_left","age_glaucoma_surgery_perf_left","no_glaucomal_surgery_perf_left","ocul_surgeries_retina_left","age_vitreoretina_surgery_perf_left","no_vitreoretinal_surgery_perf_left","ocul_surgeries_lasers_left","age_ocul_surgeries_lasers_perf_left","no_ofocul_surgeries_lasers_perf_left","opht_medi_subtenon_subconj_injec_left","age_opht_medi_subtenon_subconj_injec_perf_left","no_opht_medi_subtenon_subconj_injec_perf_left","ocul_medi_internal_left","age_ocul_medi_internal_perf_left","no_ocul_medi_internal_perf_left","ocul_medi_topical_left","age_ocul_medi_topical_perf_left","no_ocul_medi_topical_perf_left").first()
	
	##PatientGeneralInfoMultiVisit
	## Get PatientGeneralInfoMultiVisit add more fields start 22-12-2018
	logmar_visual_acuity_right					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="logmar_visual_acuity_right").all()
	if logmar_visual_acuity_right:
		for valuess  in logmar_visual_acuity_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	logmar_visual_acuity_left					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="logmar_visual_acuity_left").all()
	if logmar_visual_acuity_left:
		for valuess  in logmar_visual_acuity_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	logmar_visual_acuity_classification_left					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="logmar_visual_acuity_classification_left").all()
	if logmar_visual_acuity_classification_left:
		for valuess  in logmar_visual_acuity_classification_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	logmar_visual_acuity_classification_right					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="logmar_visual_acuity_classification_right").all()
	if logmar_visual_acuity_classification_right:
		for valuess  in logmar_visual_acuity_classification_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	blood_pressure_systolic_mmhg					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="blood_pressure_systolic_mmhg").all()
	if blood_pressure_systolic_mmhg:
		for valuess  in blood_pressure_systolic_mmhg:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	blood_total_cholesterol_level_mgdl					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="blood_total_cholesterol_level_mgdl").all()
	if blood_total_cholesterol_level_mgdl:
		for valuess  in blood_total_cholesterol_level_mgdl:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	blood_pressure_diastolic_mmhg					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="blood_pressure_diastolic_mmhg").all()
	if blood_pressure_diastolic_mmhg:
		for valuess  in blood_pressure_diastolic_mmhg:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	blood_ldl_cholesterol_level_mgdl					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="blood_ldl_cholesterol_level_mgdl").all()
	if blood_ldl_cholesterol_level_mgdl:
		for valuess  in blood_ldl_cholesterol_level_mgdl:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	hypertension_classification					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="hypertension_classification").all()
	if hypertension_classification:
		for valuess  in hypertension_classification:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	hypercholestremia_classification					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="hypercholestremia_classification").all()
	if hypercholestremia_classification:
		for valuess  in hypercholestremia_classification:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	hypertension_medication					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="hypertension_medication").all()
	if hypertension_medication:
		for valuess  in hypertension_medication:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	hypercholestremia_medication					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="hypercholestremia_medication").all()
	if hypercholestremia_medication:
		for valuess  in hypercholestremia_medication:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	fasting_blood_glucose_mgdl					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="fasting_blood_glucose_mgdl").all()
	if fasting_blood_glucose_mgdl:
		for valuess  in fasting_blood_glucose_mgdl:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	hba1c_percentage					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="hba1c_percentage").all()
	if hba1c_percentage:
		for valuess  in hba1c_percentage:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	diabetes_mellitus					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="diabetes_mellitus").all()
	if diabetes_mellitus:
		for valuess  in diabetes_mellitus:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	diabetes_mellitus_medication					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="diabetes_mellitus_medication").all()
	if diabetes_mellitus_medication:
		for valuess  in diabetes_mellitus_medication:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	clinical_course_of_systemic_disorder_or_no_systemic_disorder					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="clinical_course_of_systemic_disorder_or_no_systemic_disorder").all()
	if clinical_course_of_systemic_disorder_or_no_systemic_disorder:
		for valuess  in clinical_course_of_systemic_disorder_or_no_systemic_disorder:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	typical					=	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).filter(key="typical").all()
	if typical:
		for valuess  in typical:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
							
	## Get PatientGeneralInfoMultiVisit add more fields end 22-12-2018
	
	## Get PatientGeneralInfoMultiVisitOphthalmology add more fields for stap 3 view  start 22-12-2018
				
	intra_ocul_pres_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="intra_ocul_pres_left").all()
	if intra_ocul_pres_left:
		for valuess  in intra_ocul_pres_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
			
	intra_ocul_pres_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="intra_ocul_pres_right").all()
	if intra_ocul_pres_right:
		for valuess  in intra_ocul_pres_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	intra_ocul_pres_clas_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="intra_ocul_pres_clas_left").all()
	if intra_ocul_pres_clas_left:
		for valuess  in intra_ocul_pres_clas_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	intra_ocul_pres_clas_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="intra_ocul_pres_clas_right").all()
	if intra_ocul_pres_clas_right:
		for valuess  in intra_ocul_pres_clas_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	refr_error_sphe_equi_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="refr_error_sphe_equi_left").all()
	if refr_error_sphe_equi_left:
		for valuess  in refr_error_sphe_equi_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	refr_error_sphe_equi_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="refr_error_sphe_equi_right").all()
	if refr_error_sphe_equi_right:
		for valuess  in refr_error_sphe_equi_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	refr_error_sphe_equi_clas_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="refr_error_sphe_equi_clas_left").all()
	if refr_error_sphe_equi_clas_left:
		for valuess  in refr_error_sphe_equi_clas_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	refr_error_sphe_equi_clas_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="refr_error_sphe_equi_clas_right").all()
	if refr_error_sphe_equi_clas_right:
		for valuess  in refr_error_sphe_equi_clas_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	corn_thic_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="corn_thic_left").all()
	if corn_thic_left:
		for valuess  in corn_thic_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	corn_thic_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="corn_thic_right").all()
	if corn_thic_right:
		for valuess  in corn_thic_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	lens_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="lens_left").all()
	if lens_left:
		for valuess  in lens_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	lens_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="lens_right").all()
	if lens_right:
		for valuess  in lens_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	axia_leng_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="axia_leng_left").all()
	if axia_leng_left:
		for valuess  in axia_leng_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	axia_leng_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="axia_leng_right").all()
	if axia_leng_right:
		for valuess  in axia_leng_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	axia_leng_clas_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="axia_leng_clas_left").all()
	if axia_leng_clas_left:
		for valuess  in axia_leng_clas_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	axia_leng_clas_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="axia_leng_clas_right").all()
	if axia_leng_clas_right:
		for valuess  in axia_leng_clas_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	macu_thic_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="macu_thic_left").all()
	if macu_thic_left:
		for valuess  in macu_thic_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	macu_thic_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="macu_thic_right").all()
	if macu_thic_right:
		for valuess  in macu_thic_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	macu_edema_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="macu_edema_left").all()
	if macu_edema_left:
		for valuess  in macu_edema_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	macu_edema_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="macu_edema_right").all()
	if macu_edema_right:
		for valuess  in macu_edema_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	macu_schisis_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="macu_schisis_left").all()
	if macu_schisis_left:
		for valuess  in macu_schisis_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	macu_schisis_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="macu_schisis_right").all()
	if macu_schisis_right:
		for valuess  in macu_schisis_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	epir_memb_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="epir_memb_left").all()
	if epir_memb_left:
		for valuess  in epir_memb_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	epir_memb_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="epir_memb_right").all()
	if epir_memb_right:
		for valuess  in epir_memb_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	sub_sensreti_fuild_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="sub_sensreti_fuild_left").all()
	if sub_sensreti_fuild_left:
		for valuess  in sub_sensreti_fuild_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	sub_sensreti_fuild_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="sub_sensreti_fuild_right").all()
	if sub_sensreti_fuild_right:
		for valuess  in sub_sensreti_fuild_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	sub_reti_epith_memb_fuild_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="sub_reti_epith_memb_fuild_left").all()
	if sub_reti_epith_memb_fuild_left:
		for valuess  in sub_reti_epith_memb_fuild_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	sub_reti_epith_memb_fuild_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="sub_reti_epith_memb_fuild_right").all()
	if sub_reti_epith_memb_fuild_right:
		for valuess  in sub_reti_epith_memb_fuild_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	foveal_thic_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="foveal_thic_left").all()
	if foveal_thic_left:
		for valuess  in foveal_thic_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	foveal_thic_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="foveal_thic_right").all()
	if foveal_thic_right:
		for valuess  in foveal_thic_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	choro_thic_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="choro_thic_left").all()
	if choro_thic_left:
		for valuess  in choro_thic_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	choro_thic_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="choro_thic_right").all()
	if choro_thic_right:
		for valuess  in choro_thic_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	stat_peri_mean_sens_hfa24_2_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="stat_peri_mean_sens_hfa24_2_left").all()
	if stat_peri_mean_sens_hfa24_2_left:
		for valuess  in stat_peri_mean_sens_hfa24_2_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	stat_peri_mean_sens_hfa24_2_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="stat_peri_mean_sens_hfa24_2_right").all()
	if stat_peri_mean_sens_hfa24_2_right:
		for valuess  in stat_peri_mean_sens_hfa24_2_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	stat_peri_mean_sens_clas_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="stat_peri_mean_sens_clas_left").all()
	if stat_peri_mean_sens_clas_left:
		for valuess  in stat_peri_mean_sens_clas_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	stat_peri_mean_sens_clas_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="stat_peri_mean_sens_clas_right").all()
	if stat_peri_mean_sens_clas_right:
		for valuess  in stat_peri_mean_sens_clas_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
				
	electro_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="electro_left").all()
	if electro_left:
		for valuess  in electro_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	electro_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="electro_right").all()
	if electro_right:
		for valuess  in electro_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	full_field_electphysiol_clas_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="full_field_electphysiol_clas_left").all()
	if full_field_electphysiol_clas_left:
		for valuess  in full_field_electphysiol_clas_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	full_field_electphysiol_clas_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="full_field_electphysiol_clas_right").all()
	if full_field_electphysiol_clas_right:
		for valuess  in full_field_electphysiol_clas_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	multi_electphysiol_clas_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="multi_electphysiol_clas_left").all()
	if multi_electphysiol_clas_left:
		for valuess  in multi_electphysiol_clas_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	multi_electphysiol_clas_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="multi_electphysiol_clas_right").all()
	if multi_electphysiol_clas_right:
		for valuess  in multi_electphysiol_clas_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	electroneg_config_of_dark_apa					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="electroneg_config_of_dark_apa").all()
	if electroneg_config_of_dark_apa:
		for valuess  in electroneg_config_of_dark_apa:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diagnosis_for_others_left					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="ai_diagnosis_for_others_left").all()
	if ai_diagnosis_for_others_left:
		for valuess  in ai_diagnosis_for_others_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diagnosis_for_others_right					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="ai_diagnosis_for_others_right").all()
	if ai_diagnosis_for_others_right:
		for valuess  in ai_diagnosis_for_others_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accuracy_for_others_left_per					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="ai_accuracy_for_others_left_per").all()
	if ai_accuracy_for_others_left_per:
		for valuess  in ai_accuracy_for_others_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accuracy_for_others_right_per					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="ai_accuracy_for_others_right_per").all()
	if ai_accuracy_for_others_right_per:
		for valuess  in ai_accuracy_for_others_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_comments					=	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).filter(key="ai_comments").all()
	if ai_comments:
		for valuess  in ai_comments:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	PatientGeneralInfoOphthalmologySystAbnormalityInfo			=  PatientGeneralInfoOphthalmologySystAbnormality.objects.filter(patient_id=id).select_related("systemicAbnormality_name").all()
	
	

	## Get PatientGeneralInfoMultiVisitOphthalmology add more fields for stap 3 view  end 22-12-2018
	
	##PatientGeneralInfoMultiVisitOphthalmologyAi add more fields for step 5 view start 23-12-2018
	
				
	ai_diag_corn_dise_corn_phot_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_corn_dise_corn_phot_left").all()
	if ai_diag_corn_dise_corn_phot_left:
		for valuess  in ai_diag_corn_dise_corn_phot_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_corn_dise_corn_phot_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_corn_dise_corn_phot_right").all()
	if ai_diag_corn_dise_corn_phot_right:
		for valuess  in ai_diag_corn_dise_corn_phot_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_corn_diag_corn_phot_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_corn_diag_corn_phot_left_per").all()
	if ai_accu_corn_diag_corn_phot_left_per:
		for valuess  in ai_accu_corn_diag_corn_phot_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_corn_diag_corn_phot_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_corn_diag_corn_phot_right_per").all()
	if ai_accu_corn_diag_corn_phot_right_per:
		for valuess  in ai_accu_corn_diag_corn_phot_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_corn_dise_corn_phot_on_fluo_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_corn_dise_corn_phot_on_fluo_left").all()
	if ai_diag_corn_dise_corn_phot_on_fluo_left:
		for valuess  in ai_diag_corn_dise_corn_phot_on_fluo_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_corn_dise_corn_phot_on_fluo_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_corn_dise_corn_phot_on_fluo_right").all()
	if ai_diag_corn_dise_corn_phot_on_fluo_right:
		for valuess  in ai_diag_corn_dise_corn_phot_on_fluo_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_corn_diag_corn_phot_on_fluo_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_corn_diag_corn_phot_on_fluo_left_per").all()
	if ai_accu_corn_diag_corn_phot_on_fluo_left_per:
		for valuess  in ai_accu_corn_diag_corn_phot_on_fluo_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_corn_diag_corn_phot_on_fluo_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_corn_diag_corn_phot_on_fluo_right_per").all()
	if ai_accu_corn_diag_corn_phot_on_fluo_right_per:
		for valuess  in ai_accu_corn_diag_corn_phot_on_fluo_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_glau_fundus_phot_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_glau_fundus_phot_left").all()
	if ai_diag_glau_fundus_phot_left:
		for valuess  in ai_diag_glau_fundus_phot_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_glau_fundus_phot_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_glau_fundus_phot_right").all()
	if ai_diag_glau_fundus_phot_right:
		for valuess  in ai_diag_glau_fundus_phot_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_glau_fundus_phot_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_glau_fundus_phot_left_per").all()
	if ai_accu_glau_fundus_phot_left_per:
		for valuess  in ai_accu_glau_fundus_phot_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_glau_fundus_phot_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_glau_fundus_phot_right_per").all()
	if ai_accu_glau_fundus_phot_right_per:
		for valuess  in ai_accu_glau_fundus_phot_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_glau_opti_cohe_tomo_disc_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_glau_opti_cohe_tomo_disc_left").all()
	if ai_diag_glau_opti_cohe_tomo_disc_left:
		for valuess  in ai_diag_glau_opti_cohe_tomo_disc_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_glau_opti_cohe_tomo_disc_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_glau_opti_cohe_tomo_disc_right").all()
	if ai_diag_glau_opti_cohe_tomo_disc_right:
		for valuess  in ai_diag_glau_opti_cohe_tomo_disc_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_glau_opti_cohe_tomo_disc_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_glau_opti_cohe_tomo_disc_left_per").all()
	if ai_accu_glau_opti_cohe_tomo_disc_left_per:
		for valuess  in ai_accu_glau_opti_cohe_tomo_disc_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_glau_opti_cohe_tomo_disc_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_glau_opti_cohe_tomo_disc_right_per").all()
	if ai_accu_glau_opti_cohe_tomo_disc_right_per:
		for valuess  in ai_accu_glau_opti_cohe_tomo_disc_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_glau_static_visual_field_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_glau_static_visual_field_left").all()
	if ai_diag_glau_static_visual_field_left:
		for valuess  in ai_diag_glau_static_visual_field_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_glau_static_visual_field_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_glau_static_visual_field_right").all()
	if ai_diag_glau_static_visual_field_right:
		for valuess  in ai_diag_glau_static_visual_field_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_glau_static_visual_field_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_glau_static_visual_field_left_per").all()
	if ai_accu_glau_static_visual_field_left_per:
		for valuess  in ai_accu_glau_static_visual_field_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_glau_static_visual_field_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_glau_static_visual_field_right_per").all()
	if ai_accu_glau_static_visual_field_right_per:
		for valuess  in ai_accu_glau_static_visual_field_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_diab_retino_fundus_phot_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_diab_retino_fundus_phot_left").all()
	if ai_diag_diab_retino_fundus_phot_left:
		for valuess  in ai_diag_diab_retino_fundus_phot_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_diab_retino_fundus_phot_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_diab_retino_fundus_phot_right").all()
	if ai_diag_diab_retino_fundus_phot_right:
		for valuess  in ai_diag_diab_retino_fundus_phot_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_diab_retino_fundus_phot_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_diab_retino_fundus_phot_left_per").all()
	if ai_accu_diab_retino_fundus_phot_left_per:
		for valuess  in ai_accu_diab_retino_fundus_phot_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_diab_retino_fundus_phot_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_diab_retino_fundus_phot_right_per").all()
	if ai_accu_diab_retino_fundus_phot_right_per:
		for valuess  in ai_accu_diab_retino_fundus_phot_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diagnsis_diab_retino_fluo_angio_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diagnsis_diab_retino_fluo_angio_left").all()
	if ai_diagnsis_diab_retino_fluo_angio_left:
		for valuess  in ai_diagnsis_diab_retino_fluo_angio_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diagnsis_diab_retino_fluo_angio_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diagnsis_diab_retino_fluo_angio_right").all()
	if ai_diagnsis_diab_retino_fluo_angio_right:
		for valuess  in ai_diagnsis_diab_retino_fluo_angio_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_diab_retino_fluo_angio_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_diab_retino_fluo_angio_left_per").all()
	if ai_accu_diab_retino_fluo_angio_left_per:
		for valuess  in ai_accu_diab_retino_fluo_angio_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_diab_retino_fluo_angio_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_diab_retino_fluo_angio_right_per").all()
	if ai_accu_diab_retino_fluo_angio_right_per:
		for valuess  in ai_accu_diab_retino_fluo_angio_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left").all()
	if ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left:
		for valuess  in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right").all()
	if ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right:
		for valuess  in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per").all()
	if ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per:
		for valuess  in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per").all()
	if ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per:
		for valuess  in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_fundus_phot_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_fundus_phot_left").all()
	if ai_diag_age_relat_macu_degen_fundus_phot_left:
		for valuess  in ai_diag_age_relat_macu_degen_fundus_phot_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_fundus_phot_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_fundus_phot_right").all()
	if ai_diag_age_relat_macu_degen_fundus_phot_right:
		for valuess  in ai_diag_age_relat_macu_degen_fundus_phot_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_fundus_phot_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_fundus_phot_left_per").all()
	if ai_accu_age_relat_macu_degen_fundus_phot_left_per:
		for valuess  in ai_accu_age_relat_macu_degen_fundus_phot_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_fundus_phot_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_fundus_phot_right_per").all()
	if ai_accu_age_relat_macu_degen_fundus_phot_right_per:
		for valuess  in ai_accu_age_relat_macu_degen_fundus_phot_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_fluo_angio_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_fluo_angio_left").all()
	if ai_diag_age_relat_macu_degen_fluo_angio_left:
		for valuess  in ai_diag_age_relat_macu_degen_fluo_angio_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_fluo_angio_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_fluo_angio_right").all()
	if ai_diag_age_relat_macu_degen_fluo_angio_right:
		for valuess  in ai_diag_age_relat_macu_degen_fluo_angio_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_fluo_angio_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_fluo_angio_left_per").all()
	if ai_accu_age_relat_macu_degen_fluo_angio_left_per:
		for valuess  in ai_accu_age_relat_macu_degen_fluo_angio_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_fluo_angio_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_fluo_angio_right_per").all()
	if ai_accu_age_relat_macu_degen_fluo_angio_right_per:
		for valuess  in ai_accu_age_relat_macu_degen_fluo_angio_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_indocy_green_angio_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_indocy_green_angio_left").all()
	if ai_diag_age_relat_macu_degen_indocy_green_angio_left:
		for valuess  in ai_diag_age_relat_macu_degen_indocy_green_angio_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_indocy_green_angio_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_indocy_green_angio_right").all()
	if ai_diag_age_relat_macu_degen_indocy_green_angio_right:
		for valuess  in ai_diag_age_relat_macu_degen_indocy_green_angio_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_indocy_green_angio_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_indocy_green_angio_left_per").all()
	if ai_accu_age_relat_macu_degen_indocy_green_angio_left_per:
		for valuess  in ai_accu_age_relat_macu_degen_indocy_green_angio_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_indocy_green_angio_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_indocy_green_angio_right_per").all()
	if ai_accu_age_relat_macu_degen_indocy_green_angio_right_per:
		for valuess  in ai_accu_age_relat_macu_degen_indocy_green_angio_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left").all()
	if ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left:
		for valuess  in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right").all()
	if ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right:
		for valuess  in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per").all()
	if ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per:
		for valuess  in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per").all()
	if ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per:
		for valuess  in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_fundus_phot_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_fundus_phot_left").all()
	if ai_diag_inheri_retin_dise_fundus_phot_left:
		for valuess  in ai_diag_inheri_retin_dise_fundus_phot_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_fundus_phot_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_fundus_phot_right").all()
	if ai_diag_inheri_retin_dise_fundus_phot_right:
		for valuess  in ai_diag_inheri_retin_dise_fundus_phot_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_fundus_phot_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_fundus_phot_left_per").all()
	if ai_accu_inheri_retin_dise_fundus_phot_left_per:
		for valuess  in ai_accu_inheri_retin_dise_fundus_phot_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_fundus_phot_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_fundus_phot_right_per").all()
	if ai_accu_inheri_retin_dise_fundus_phot_right_per:
		for valuess  in ai_accu_inheri_retin_dise_fundus_phot_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left").all()
	if ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left:
		for valuess  in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right").all()
	if ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right:
		for valuess  in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per").all()
	if ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per:
		for valuess  in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per").all()
	if ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per:
		for valuess  in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left").all()
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left:
		for valuess  in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right").all()
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right:
		for valuess  in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per").all()
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per:
		for valuess  in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per").all()
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per:
		for valuess  in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left").all()
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left:
		for valuess  in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right").all()
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right:
		for valuess  in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
	
	ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per").all()
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per:
		for valuess  in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per").all()
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per:
		for valuess  in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_full_field_electroret_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_full_field_electroret_left").all()
	if ai_diag_inheri_retin_dise_full_field_electroret_left:
		for valuess  in ai_diag_inheri_retin_dise_full_field_electroret_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_full_field_electroret_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_full_field_electroret_right").all()
	if ai_diag_inheri_retin_dise_full_field_electroret_right:
		for valuess  in ai_diag_inheri_retin_dise_full_field_electroret_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value	
				
	ai_accu_inheri_retin_dise_full_field_electroret_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_full_field_electroret_left_per").all()
	if ai_accu_inheri_retin_dise_full_field_electroret_left_per:
		for valuess  in ai_accu_inheri_retin_dise_full_field_electroret_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_full_field_electroret_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_full_field_electroret_right_per").all()
	if ai_accu_inheri_retin_dise_full_field_electroret_right_per:
		for valuess  in ai_accu_inheri_retin_dise_full_field_electroret_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value	
				
	ai_diag_inheri_retin_dise_multifocal_electroret_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_multifocal_electroret_left").all()
	if ai_diag_inheri_retin_dise_multifocal_electroret_left:
		for valuess  in ai_diag_inheri_retin_dise_multifocal_electroret_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_multifocal_electroret_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_multifocal_electroret_right").all()
	if ai_diag_inheri_retin_dise_multifocal_electroret_right:
		for valuess  in ai_diag_inheri_retin_dise_multifocal_electroret_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value	
				
	ai_accu_inheri_retin_dise_multifocal_electroret_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_multifocal_electroret_left_per").all()
	if ai_accu_inheri_retin_dise_multifocal_electroret_left_per:
		for valuess  in ai_accu_inheri_retin_dise_multifocal_electroret_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_multifocal_electroret_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_multifocal_electroret_right_per").all()
	if ai_accu_inheri_retin_dise_multifocal_electroret_right_per:
		for valuess  in ai_accu_inheri_retin_dise_multifocal_electroret_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_diag_inheri_retin_dise_vcf_files_left					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_vcf_files_left").all()
	if ai_diag_inheri_retin_dise_vcf_files_left:
		for valuess  in ai_diag_inheri_retin_dise_vcf_files_left:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value	
				
	ai_diag_inheri_retin_dise_vcf_files_right					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_diag_inheri_retin_dise_vcf_files_right").all()
	if ai_diag_inheri_retin_dise_vcf_files_right:
		for valuess  in ai_diag_inheri_retin_dise_vcf_files_right:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_vcf_files_left_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_vcf_files_left_per").all()
	if ai_accu_inheri_retin_dise_vcf_files_left_per:
		for valuess  in ai_accu_inheri_retin_dise_vcf_files_left_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
				
	ai_accu_inheri_retin_dise_vcf_files_right_per					=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).filter(key="ai_accu_inheri_retin_dise_vcf_files_right_per").all()
	if ai_accu_inheri_retin_dise_vcf_files_right_per:
		for valuess  in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if valuess.model_name != "":
				modelName				=	apps.get_model("ophthalmology",valuess.model_name)
				valuess1	=	modelName.objects.filter(id=valuess.value).first();
				valuess.fieldvalue		=	valuess1.name;
			else:
				valuess.fieldvalue		=	valuess.value
	
	##return HttpResponse(PatientGeneralInfoMultiVisitOphthalmologyAiInfo)
	
		
	PatientGeneralInfoOphthalmologyInfo	=	PatientGeneralInfoOphthalmology.objects.filter(patient_id=id).select_related("ocul_surgeries_catrct_right","age_catrct_surgery_perf_right","no_catrct_surgery_perf_right","ocul_surgeries_catrct_left","age_catrct_surgery_perf_left","no_catrct_surgery_perf_left","age_at_onset_of_ocul_symp","onset_of_diease_clas","age_at_the_init_diag","age_at_the_init_diag_clas").first()
	
	#PatientGeneralInfoOphthalmologyInfo	=	PatientGeneralInfoOphthalmology.objects.filter(patient_id=id).select_related("ocul_surgeries_catrct_right","age_catrct_surgery_perf_right","no_catrct_surgery_perf_right","ocul_surgeries_catrct_left","age_catrct_surgery_perf_left","no_catrct_surgery_perf_left","age_at_onset_of_ocul_symp","onset_of_diease_clas","age_at_the_init_diag","age_at_the_init_diag_clas","dna_extraction_process","sequencing","analysis").first()
	
	#return HttpResponse(PatientGeneralInfoOphthalmologyInfo)
	
	##PatientGeneralInfoMultiVisitOphthalmologyImages
	
	PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).values("field_name").distinct().all()
	
	if PatientGeneralInfoMultiVisitOphthalmologyImagesInfo:
		for imageData in PatientGeneralInfoMultiVisitOphthalmologyImagesInfo:
			imageData["left"]	=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).filter(field_name=imageData["field_name"]).filter(field_direction="left").all()
			imageData["right"]	=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).filter(field_name=imageData["field_name"]).filter(field_direction="right").all()
			
	##PatientOtherMultiVisitImages
	
	PatientOtherMultiVisitImagesInfo	=	PatientOtherMultiVisitImages.objects.filter(patient_id=id).values("field_name").distinct().all()
	
	if PatientOtherMultiVisitImagesInfo:
		for imageData in PatientOtherMultiVisitImagesInfo:
			imageData["left"]	=	PatientOtherMultiVisitImages.objects.filter(patient_id=id).filter(field_name=imageData["field_name"]).filter(field_direction="left").all()
			imageData["right"]	=	PatientOtherMultiVisitImages.objects.filter(patient_id=id).filter(field_name=imageData["field_name"]).filter(field_direction="right").all()		
			
			
	####PatientOtherCommonInfo
	PatientOtherCommonInfoDetial = PatientOtherCommonInfo.objects.filter(patient_id=id).select_related("direct_sequencing_1","direct_sequencing_2","direct_sequencing_3","direct_sequencing_4","direct_sequencing_5","targt_enrichment_ngs_panel_1","targt_enrichment_ngs_panel_analysis_1","targt_enrichment_ngs_panel_2","targt_enrichment_ngs_panel_analysis_2","targt_enrichment_ngs_panel_3","targt_enrichment_ngs_panel_analysis_3","targt_enrichment_ngs_panel_4","targt_enrichment_ngs_panel_analysis_4","targt_enrichment_ngs_panel_5","targt_enrichment_ngs_panel_analysis_5","targt_exome_sequencing_1","targt_exome_sequencing_analysis_1","targt_exome_sequencing_2","targt_exome_sequencing_analysis_2","exome_sequencing_1","exome_sequencing_analysis_1","whole_exome_sequencing_1","whole_exome_sequencing_analysis_1","sequencing_other_collaborators_1","sequencing_other_collaborators_analysis_1","sequencing_other_collaborators_2","sequencing_other_collaborators_analysis_2","beadarray_platform_1","beadarray_platform_analysis_1","other_sequencing","mitochondria_ngs_whole_gene_sequence_1","mitochondria_ngs_whole_gene_sequence_analysis_1","targt_mitochondrial_sequence_2","targt_mitochondrial_sequence_analysis_2","targt_mitochondrial_hot_spot_panel_sequence_3","targt_mitochondrial_hot_spot_panel_sequence_analysis_3","other_analysis").first()
	####PatientOtherCommonInfo
	context		=	{
		"PatientGeneralInfoMultiVisitOphthalmologyImagesInfo":PatientGeneralInfoMultiVisitOphthalmologyImagesInfo,
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial,
		"PatientGeneralInfoOphthalmologyInfo":PatientGeneralInfoOphthalmologyInfo,
		"PatientOtherUncommonInfoOphthalmologyInfo":PatientOtherUncommonInfoOphthalmologyInfo,
		"PatientOtherMultiVisitImagesInfo":PatientOtherMultiVisitImagesInfo,
		#"PatientGeneralInfoMultiVisitInfo":PatientGeneralInfoMultiVisitInfo,
		#"PatientGeneralInfoMultiVisitOphthalmologyInfo":PatientGeneralInfoMultiVisitOphthalmologyInfo,
		"PatientGeneralInfoMultiVisitOphthalmologyAiInfo":PatientGeneralInfoMultiVisitOphthalmologyAiInfo,
		"PatientOtherCommonInfoDetial":PatientOtherCommonInfoDetial,
		"logmar_visual_acuity_right":logmar_visual_acuity_right,
		"logmar_visual_acuity_left":logmar_visual_acuity_left,
		"logmar_visual_acuity_classification_left":logmar_visual_acuity_classification_left,
		"logmar_visual_acuity_classification_right":logmar_visual_acuity_classification_right,
		"blood_pressure_systolic_mmhg":blood_pressure_systolic_mmhg,
		"blood_total_cholesterol_level_mgdl":blood_total_cholesterol_level_mgdl,
		"blood_pressure_diastolic_mmhg":blood_pressure_diastolic_mmhg,
		"blood_ldl_cholesterol_level_mgdl":blood_ldl_cholesterol_level_mgdl,
		"hypertension_classification":hypertension_classification,
		"hypercholestremia_classification":hypercholestremia_classification,
		"hypertension_medication":hypertension_medication,
		"hypercholestremia_medication":hypercholestremia_medication,
		"fasting_blood_glucose_mgdl":fasting_blood_glucose_mgdl,
		"hba1c_percentage":hba1c_percentage,
		"diabetes_mellitus":diabetes_mellitus,
		"diabetes_mellitus_medication":diabetes_mellitus_medication,
		"clinical_course_of_systemic_disorder_or_no_systemic_disorder":clinical_course_of_systemic_disorder_or_no_systemic_disorder,
		"typical":typical,
		# PatientGeneralInfoMultiVisitOphthalmologyInfo for step3 add more fields.
		"intra_ocul_pres_left":intra_ocul_pres_left,
		"intra_ocul_pres_right":intra_ocul_pres_right,
		"intra_ocul_pres_clas_left":intra_ocul_pres_clas_left,
		"intra_ocul_pres_clas_right":intra_ocul_pres_clas_right,
		"refr_error_sphe_equi_left":refr_error_sphe_equi_left,
		"refr_error_sphe_equi_right":refr_error_sphe_equi_right,
		"refr_error_sphe_equi_clas_left":refr_error_sphe_equi_clas_left,
		"refr_error_sphe_equi_clas_right":refr_error_sphe_equi_clas_right,
		"corn_thic_left":corn_thic_left,
		"corn_thic_right":corn_thic_right,
		"lens_left":lens_left,
		"lens_right":lens_right,
		"axia_leng_left":axia_leng_left,
		"axia_leng_right":axia_leng_right,
		"axia_leng_clas_left":axia_leng_clas_left,
		"axia_leng_clas_right":axia_leng_clas_right,
		"macu_thic_left":macu_thic_left,
		"macu_thic_right":macu_thic_right,
		"macu_edema_left":macu_edema_left,
		"macu_edema_right":macu_edema_right,
		"macu_schisis_left":macu_schisis_left,
		"macu_schisis_right":macu_schisis_right,
		"epir_memb_left":epir_memb_left,
		"epir_memb_right":epir_memb_right,
		"sub_sensreti_fuild_left":sub_sensreti_fuild_left,
		"sub_sensreti_fuild_right":sub_sensreti_fuild_right,
		"sub_reti_epith_memb_fuild_left":sub_reti_epith_memb_fuild_left,
		"sub_reti_epith_memb_fuild_right":sub_reti_epith_memb_fuild_right,
		"foveal_thic_left":foveal_thic_left,
		"foveal_thic_right":foveal_thic_right,
		"choro_thic_left":choro_thic_left,
		"choro_thic_right":choro_thic_right,
		"stat_peri_mean_sens_hfa24_2_left":stat_peri_mean_sens_hfa24_2_left,
		"stat_peri_mean_sens_hfa24_2_right":stat_peri_mean_sens_hfa24_2_right,
		"stat_peri_mean_sens_clas_left":stat_peri_mean_sens_clas_left,
		"stat_peri_mean_sens_clas_right":stat_peri_mean_sens_clas_right,
		"electro_left":electro_left,
		"electro_right":electro_right,
		"full_field_electphysiol_clas_left":full_field_electphysiol_clas_left,
		"full_field_electphysiol_clas_right":full_field_electphysiol_clas_right,
		"multi_electphysiol_clas_left":multi_electphysiol_clas_left,
		"multi_electphysiol_clas_right":multi_electphysiol_clas_right,
		"electroneg_config_of_dark_apa":electroneg_config_of_dark_apa,
		"ai_diagnosis_for_others_left":ai_diagnosis_for_others_left,
		"ai_diagnosis_for_others_right":ai_diagnosis_for_others_right,
		"ai_accuracy_for_others_left_per":ai_accuracy_for_others_left_per,
		"ai_accuracy_for_others_right_per":ai_accuracy_for_others_right_per,
		"ai_comments":ai_comments,
		# PatientGeneralInfoMultiVisitOphthalmologyAi for step5 add more fields.
		"ai_diag_corn_dise_corn_phot_left":ai_diag_corn_dise_corn_phot_left,
		"ai_diag_corn_dise_corn_phot_right":ai_diag_corn_dise_corn_phot_right,
		"ai_accu_corn_diag_corn_phot_left_per":ai_accu_corn_diag_corn_phot_left_per,
		"ai_accu_corn_diag_corn_phot_right_per":ai_accu_corn_diag_corn_phot_right_per,
		"ai_diag_corn_dise_corn_phot_on_fluo_left":ai_diag_corn_dise_corn_phot_on_fluo_left,
		"ai_diag_corn_dise_corn_phot_on_fluo_right":ai_diag_corn_dise_corn_phot_on_fluo_right,
		"ai_accu_corn_diag_corn_phot_on_fluo_left_per":ai_accu_corn_diag_corn_phot_on_fluo_left_per,
		"ai_accu_corn_diag_corn_phot_on_fluo_right_per":ai_accu_corn_diag_corn_phot_on_fluo_right_per,
		"ai_diag_glau_fundus_phot_left":ai_diag_glau_fundus_phot_left,
		"ai_diag_glau_fundus_phot_right":ai_diag_glau_fundus_phot_right,
		"ai_accu_glau_fundus_phot_left_per":ai_accu_glau_fundus_phot_left_per,
		"ai_accu_glau_fundus_phot_right_per":ai_accu_glau_fundus_phot_right_per,
		"ai_diag_glau_opti_cohe_tomo_disc_left":ai_diag_glau_opti_cohe_tomo_disc_left,
		"ai_diag_glau_opti_cohe_tomo_disc_right":ai_diag_glau_opti_cohe_tomo_disc_right,
		"ai_accu_glau_opti_cohe_tomo_disc_left_per":ai_accu_glau_opti_cohe_tomo_disc_left_per,
		"ai_accu_glau_opti_cohe_tomo_disc_right_per":ai_accu_glau_opti_cohe_tomo_disc_right_per,
		"ai_diag_glau_static_visual_field_left":ai_diag_glau_static_visual_field_left,
		"ai_diag_glau_static_visual_field_right":ai_diag_glau_static_visual_field_right,
		"ai_accu_glau_static_visual_field_left_per":ai_accu_glau_static_visual_field_left_per,
		"ai_accu_glau_static_visual_field_right_per":ai_accu_glau_static_visual_field_right_per,
		"ai_diag_diab_retino_fundus_phot_left":ai_diag_diab_retino_fundus_phot_left,
		"ai_diag_diab_retino_fundus_phot_right":ai_diag_diab_retino_fundus_phot_right,
		"ai_accu_diab_retino_fundus_phot_left_per":ai_accu_diab_retino_fundus_phot_left_per,
		"ai_accu_diab_retino_fundus_phot_right_per":ai_accu_diab_retino_fundus_phot_right_per,
		"ai_diagnsis_diab_retino_fluo_angio_left":ai_diagnsis_diab_retino_fluo_angio_left,
		"ai_diagnsis_diab_retino_fluo_angio_right":ai_diagnsis_diab_retino_fluo_angio_right,
		"ai_accu_diab_retino_fluo_angio_left_per":ai_accu_diab_retino_fluo_angio_left_per,
		"ai_accu_diab_retino_fluo_angio_right_per":ai_accu_diab_retino_fluo_angio_right_per,
		"ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left":ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left,
		"ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right":ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right,
		"ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per":ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per,
		"ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per":ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per,
		"ai_diag_age_relat_macu_degen_fundus_phot_left":ai_diag_age_relat_macu_degen_fundus_phot_left,
		"ai_diag_age_relat_macu_degen_fundus_phot_right":ai_diag_age_relat_macu_degen_fundus_phot_right,
		"ai_accu_age_relat_macu_degen_fundus_phot_left_per":ai_accu_age_relat_macu_degen_fundus_phot_left_per,
		"ai_accu_age_relat_macu_degen_fundus_phot_right_per":ai_accu_age_relat_macu_degen_fundus_phot_right_per,
		"ai_diag_age_relat_macu_degen_fluo_angio_left":ai_diag_age_relat_macu_degen_fluo_angio_left,
		"ai_diag_age_relat_macu_degen_fluo_angio_right":ai_diag_age_relat_macu_degen_fluo_angio_right,
		"ai_accu_age_relat_macu_degen_fluo_angio_left_per":ai_accu_age_relat_macu_degen_fluo_angio_left_per,
		"ai_accu_age_relat_macu_degen_fluo_angio_right_per":ai_accu_age_relat_macu_degen_fluo_angio_right_per,
		"ai_diag_age_relat_macu_degen_indocy_green_angio_left":ai_diag_age_relat_macu_degen_indocy_green_angio_left,
		"ai_diag_age_relat_macu_degen_indocy_green_angio_right":ai_diag_age_relat_macu_degen_indocy_green_angio_right,
		"ai_accu_age_relat_macu_degen_indocy_green_angio_left_per":ai_accu_age_relat_macu_degen_indocy_green_angio_left_per,
		"ai_accu_age_relat_macu_degen_indocy_green_angio_right_per":ai_accu_age_relat_macu_degen_indocy_green_angio_right_per,
		"ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left":ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left,
		"ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right":ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right,
		"ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per":ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per,
		"ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per":ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per,
		"ai_diag_inheri_retin_dise_fundus_phot_left":ai_diag_inheri_retin_dise_fundus_phot_left,
		"ai_diag_inheri_retin_dise_fundus_phot_right":ai_diag_inheri_retin_dise_fundus_phot_right,
		"ai_accu_inheri_retin_dise_fundus_phot_left_per":ai_accu_inheri_retin_dise_fundus_phot_left_per,
		"ai_accu_inheri_retin_dise_fundus_phot_right_per":ai_accu_inheri_retin_dise_fundus_phot_right_per,
		"ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left":ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left,
		"ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right":ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right,
		"ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per":ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per,
		"ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per":ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per,
		"ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left":ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left,
		"ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right":ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right,
		"ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per":ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per,
		"ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per":ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per,
		"ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left":ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left,
		"ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right":ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right,
		"ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per":ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per,
		"ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per":ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per,
		"ai_diag_inheri_retin_dise_full_field_electroret_left":ai_diag_inheri_retin_dise_full_field_electroret_left,
		"ai_diag_inheri_retin_dise_full_field_electroret_right":ai_diag_inheri_retin_dise_full_field_electroret_right,
		"ai_accu_inheri_retin_dise_full_field_electroret_left_per":ai_accu_inheri_retin_dise_full_field_electroret_left_per,
		"ai_accu_inheri_retin_dise_full_field_electroret_right_per":ai_accu_inheri_retin_dise_full_field_electroret_right_per,
		"ai_diag_inheri_retin_dise_multifocal_electroret_left":ai_diag_inheri_retin_dise_multifocal_electroret_left,
		"ai_diag_inheri_retin_dise_multifocal_electroret_right":ai_diag_inheri_retin_dise_multifocal_electroret_right,
		"ai_accu_inheri_retin_dise_multifocal_electroret_left_per":ai_accu_inheri_retin_dise_multifocal_electroret_left_per,
		"ai_accu_inheri_retin_dise_multifocal_electroret_right_per":ai_accu_inheri_retin_dise_multifocal_electroret_right_per,
		"ai_diag_inheri_retin_dise_vcf_files_left":ai_diag_inheri_retin_dise_vcf_files_left,
		"ai_diag_inheri_retin_dise_vcf_files_right":ai_diag_inheri_retin_dise_vcf_files_right,
		"ai_accu_inheri_retin_dise_vcf_files_left_per":ai_accu_inheri_retin_dise_vcf_files_left_per,
		"ai_accu_inheri_retin_dise_vcf_files_right_per":ai_accu_inheri_retin_dise_vcf_files_right_per,
		
	}
	return render(request, 'ophthalmology/view_new_patient.html',context)
	
@login_required(login_url='/')
def delete_patient(request,id):
	##return HttpResponse(id)
	PatientGeneralInfoOphthalmologySystAbnormality.objects.filter(patient_id=id).all().delete()
	##PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_id=id).all().delete()
	##PatientCausativeGeneInfoEthnicity.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoOphthalmologyOcularCompli.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoFamily.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoMultiVisit.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoMultiVisitOphthalmology.objects.filter(patient_id=id).all().delete()
	PatientOtherUncommonInfoOphthalmology.objects.filter(patient_id=id).all().delete()
	PatientOtherCommonInfo.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoOphthalmology.objects.filter(patient_id=id).all().delete()
	PatientCausativeGeneInfo.objects.filter(patient_id=id).all().delete()
	PatientOtherMultiVisitImages.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).all().delete()
	PatientGeneralInfo.objects.filter(id=id).all().delete()
	return redirect('/ophthalmology/')
	
@login_required(login_url='/')
def change_status(request,id,status):
	PatientGeneralInfoDetail = PatientGeneralInfo.objects.get(id=id)
	PatientGeneralInfoDetail.is_draft =  status 
	PatientGeneralInfoDetail.save() 
	return redirect('/ophthalmology/')
	