from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,reverse
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
#from datetime import datetime
import time
import calendar
import collections
import xlwt
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.templatetags.staticfiles import static
import re
import shutil
from django.apps import apps
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site

from ophthalmology.models import InstituteDt,RelationshipToProbandDt,SexDt,DiseaseDt,AffectedDt,InheritanceDt,SyndromicDt,BilateralDt,OcularSymptomDt,ProgressionDt,FluctuationDt,FamilyHistoryDt,ConsanguineousDt,NumberOfAffectedMembersInTheSamePedigreeDt,EthnicityDt,CountryOfOriginDt,OriginPrefectureInJapanDt,GeneDt,InheritanceDt,MutationDt,OcularSurgeriesCorneaDt,AgeForSurgeryDt,NumberOfSurgeryDt,OcularSurgeriesGlaucomaDt,OcularSurgeriesRetinaDt,OcularSurgeriesLasersDt,OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt,OcularMedicationInternalDt,OcularMedicationTopicalDt,PatientGeneralInfo,PatientOtherUncommonInfoOphthalmology,OcularSurgeriesCataractDt,PatientGeneralInfoOphthalmology,PatientGeneralInfoMultiVisitOphthalmologyImages,VisualAcuityDt,VisualAcuityClassificationDt,PresentUnpresentDt,OnMedicationOrNotDt,HcOnMedicationOrNotStatinDt,HcOnMedicationOrNotInsulinDt,TypicalDt,AgeAtOnsetOfOcularSymptomDt,AgeAtTheInitialDiagnosisDt,DnaExtractionInProcessDt,AnalysisDt,AgeAtOnsetClassificationDt,AgeAtTheInitialDiagnosisClassificationDt,SequencingDt,AiDiagnosisForCornealDiseasesDt,AiDiagnosisForGlaucomaDt,AiDiagnosisForDiabeticRetinopathyDt,AiDiagnosisForAgeRelatedMacularDegenerationDt,AiDiagnosisForInheritedRetinalDiseasesDt,SequencingStatusDt,IntraocularPressureDt,IntraocularPressureClassificationDt,RefractiveErrorSphericalEquivalentDt,RefractiveErrorSphericalEquivalentClassificationDt,LensDt,AxialLengthDt,AxialLengthClassificationDt,StaticPerimetryMeanSensitivityDt,StaticPerimetryMeanSensitivityClassificationDt,ElectrophysiologicalFindingsDt,FullFieldElectrophysiologicalGroupingDt,MultifocalElectrophysiologicalGroupingDt,ChromosomeDt,ExonDt,AlleleFrequencyDatabaseDt,PatientGeneralInfoMultiVisit,PatientGeneralInfoMultiVisitOphthalmology,PatientOtherMultiVisitImages,PatientGeneralInfoMultiVisitOphthalmologyAi,PatientOtherCommonInfo,PatientCausativeGeneInfo,PatientCausativeGeneInfoEthnicity,PatientCausativeGeneInfoLocalPopulation,PatientGeneralInfoFamily,SystemicAbnormalityDt,PatientGeneralInfoOphthalmologySystAbnormality,PatientGeneralInfoOphthalmologyOcularCompli,CausCandDt,TypeOldNewDt,AdminDiseaseDt,AdminSubDiseaseDt,SubDiseaseDt,DiseaseCausCandGeneDt

from core.models import DoctorDisease,DoctorInstitute,WhichDoctorDocumentCanSee

# Create your views here.

@login_required(login_url='/')
def index(request):

	if request.GET.get('institute_id'):
		institute_id	=	request.GET.get('institute_id')
	else:
		institute_id	=	0

	if request.GET.get('family_id'):
		family_id	=	request.GET.get('family_id')
	else:
		family_id	=	0


	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					#print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data

	DiseaseDts	=	DiseaseDt.objects.order_by("-name").all()
	CountryOfOriginDtGraph	=	CountryOfOriginDt.objects.order_by("-name").all()
	
	Institudes			=	InstituteDt.objects.order_by("-name").all()
	today = datetime.date.today()
	currentYear = today.year
	currentMonth = today.month
	x = 12
	now = time.localtime()
	allMonths =  reversed([time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(x)])
	#return HttpResponse(allMonths)
	
	colors =  ["#63b598", "#ce7d78", "#ea9e70", "#a48a9e", "#c6e1e8", "#648177" ,"#0d5ac1" ,"#f205e6" ,"#1c0365" ,"#14a9ad" ,"#4ca2f9" ,"#a4e43f" ,"#d298e2" ,"#6119d0","#d2737d" ,"#c0a43c" ,"#f2510e" ,"#651be6" ,"#79806e" ,"#61da5e" ,"#cd2f00" ,"#9348af" ,"#01ac53" ,"#c5a4fb" ,"#996635","#b11573" ,"#4bb473" ,"#75d89e" ,"#2f3f94" ,"#2f7b99" ,"#da967d" ,"#34891f" ,"#b0d87b" ,"#ca4751" ,"#7e50a8" ,"#c4d647" ,"#e0eeb8" ,"#11dec1" ,"#289812" ,"#566ca0" ,"#ffdbe1" ,"#2f1179" ,"#935b6d" ,"#916988" ,"#513d98" ,"#aead3a", "#9e6d71", "#4b5bdc", "#0cd36d","#250662", "#cb5bea", "#228916", "#ac3e1b", "#df514a", "#539397", "#880977","#f697c1", "#ba96ce", "#679c9d", "#c6c42c", "#5d2c52", "#48b41b", "#e1cf3b","#5be4f0", "#57c4d8", "#a4d17a", "#225b8", "#be608b", "#96b00c", "#088baf","#f158bf", "#e145ba", "#ee91e3", "#05d371", "#5426e0", "#4834d0", "#802234","#6749e8", "#0971f0", "#8fb413", "#b2b4f0", "#c3c89d", "#c9a941", "#41d158","#fb21a3", "#51aed9", "#5bb32d", "#807fb", "#21538e", "#89d534", "#d36647","#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3","#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec","#1bb699", "#6b2e5f", "#64820f", "#1c271", "#21538e", "#89d534", "#d36647","#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3","#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec","#1bb699", "#6b2e5f", "#64820f", "#1c271", "#9cb64a", "#996c48", "#9ab9b7","#06e052", "#e3a481", "#0eb621", "#fc458e", "#b2db15", "#aa226d", "#792ed8","#73872a", "#520d3a", "#cefcb8", "#a5b3d9", "#7d1d85", "#c4fd57", "#f1ae16","#8fe22a", "#ef6e3c", "#243eeb", "#1dc18", "#dd93fd", "#3f8473", "#e7dbce","#421f79", "#7a3d93", "#635f6d", "#93f2d7", "#9b5c2a", "#15b9ee", "#0f5997","#409188", "#911e20", "#1350ce", "#10e5b1", "#fff4d7", "#cb2582", "#ce00be","#32d5d6", "#17232", "#608572", "#c79bc2", "#00f87c", "#77772a", "#6995ba","#fc6b57", "#f07815", "#8fd883", "#060e27", "#96e591", "#21d52e", "#d00043","#b47162", "#1ec227", "#4f0f6f", "#1d1d58", "#947002", "#bde052", "#e08c56","#28fcfd", "#bb09b", "#36486a", "#d02e29", "#1ae6db", "#3e464c", "#a84a8f","#911e7e", "#3f16d9", "#0f525f", "#ac7c0a", "#b4c086", "#c9d730", "#30cc49","#3d6751", "#fb4c03", "#640fc1", "#62c03e", "#d3493a", "#88aa0b", "#406df9","#615af0", "#4be47", "#2a3434", "#4a543f", "#79bca0", "#a8b8d4", "#00efd4","#7ad236", "#7260d8", "#1deaa7", "#06f43a", "#823c59", "#e3d94c", "#dc1c06","#f53b2a", "#b46238", "#2dfff6", "#a82b89", "#1a8011", "#436a9f", "#1a806a","#4cf09d", "#c188a2", "#67eb4b", "#b308d3", "#fc7e41", "#af3101", "#ff065","#71b1f4", "#a2f8a5", "#e23dd0", "#d3486d", "#00f7f9", "#474893", "#3cec35","#1c65cb", "#5d1d0c", "#2d7d2a", "#ff3420", "#5cdd87", "#a259a4", "#e4ac44","#1bede6", "#8798a4", "#d7790f", "#b2c24f", "#de73c2", "#d70a9c", "#25b67","#88e9b8", "#c2b0e2", "#86e98f", "#ae90e2", "#1a806b", "#436a9e", "#0ec0ff","#f812b3", "#b17fc9", "#8d6c2f", "#d3277a", "#2ca1ae", "#9685eb", "#8a96c6","#dba2e6", "#76fc1b", "#608fa4", "#20f6ba", "#07d7f6", "#dce77a", "#77ecca"]
	
	#return HttpResponse(colors[0])

	yearData = {}

	if request.user.is_superuser == 1:
		PatientGeneralInfoTotalCount = PatientGeneralInfo.objects.count()
		if institute_id != 0:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(institute_id=institute_id).all()
		elif family_id != 0:
			family_detail = PatientGeneralInfoFamily.objects.filter(family_id=family_id).values("patient_id");
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(id__in=family_detail).all()
		else:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.all()
		counterInstitudes = 0
		for Institudesdata in Institudes:
			PatientGeneralInfoinstituideCount = PatientGeneralInfo.objects.filter(is_draft=1).filter( institute_id=Institudesdata.id).count()
			
			if PatientGeneralInfoinstituideCount:
				Institudesdata.count	=	 round(int(PatientGeneralInfoinstituideCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				Institudesdata.count = '0'
			
			Institudesdata.color	=	 colors[counterInstitudes]
			counterInstitudes  += 1
		counterDisease = 0 	
		for DiseaseDtdata in DiseaseDts:
			PatientGeneralInfoDiseaseCount = PatientGeneralInfo.objects.filter(is_draft=1 ).filter(disease_id=DiseaseDtdata.id).count()
			
			if PatientGeneralInfoDiseaseCount:
				DiseaseDtdata.count	=	 round(int(PatientGeneralInfoDiseaseCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				DiseaseDtdata.count = '0'
			
			DiseaseDtdata.color		=	 colors[counterDisease]
			counterDisease  += 1
				
		counterCountry = 0 			
		for CountryOfOriginDtGraphdata in CountryOfOriginDtGraph:
			CountryOfOriginDtGraphdataCount = PatientGeneralInfo.objects.filter(is_draft=1 ).filter( country_of_origine_id=CountryOfOriginDtGraphdata.id).count()
			
			if CountryOfOriginDtGraphdataCount:
				CountryOfOriginDtGraphdata.count	=	 round(int(CountryOfOriginDtGraphdataCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				CountryOfOriginDtGraphdata.count = '0'
				
			CountryOfOriginDtGraphdata.color	=	 colors[counterCountry]
			counterCountry  += 1

		for allMonth in allMonths:
			num_days = calendar.monthrange(allMonth[0], allMonth[1])
			start_date = datetime.date(allMonth[0], allMonth[1], 1)
			last_day = datetime.date(allMonth[0], allMonth[1], num_days[1])

			yearData[str(allMonth[0])+'-'+str(allMonth[1])] = 	PatientGeneralInfo.objects.filter(is_draft=1 ).filter(registration_date__range=(start_date, last_day)).count()


	else:
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		PatientGeneralInfoTotalCount = PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id))).count()

		if institute_id != 0:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(institute_id=institute_id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).all()
		elif family_id != 0:
			family_detail = PatientGeneralInfoFamily.objects.filter(family_id=family_id).values("patient_id");
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(id__in=family_detail) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).all()
		else:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) &((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id))).all()
		counterInstitudes = 0
		for Institudesdata in Institudes:
			PatientGeneralInfoinstituideCount = PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) & (Q(institute_id=Institudesdata.id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).count()
			if PatientGeneralInfoinstituideCount:
				Institudesdata.count	=	 round(int(PatientGeneralInfoinstituideCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				Institudesdata.count = '0'
			Institudesdata.color	=	 colors[counterInstitudes]
			counterInstitudes  += 1
		counterDisease = 0 
		for DiseaseDtdata in DiseaseDts:
			PatientGeneralInfoSubDiseaseCount = PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(admin_sub_disease_id=DiseaseDtdata.id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).count()
			if PatientGeneralInfoSubDiseaseCount:
				DiseaseDtdata.count	=	 round(int(PatientGeneralInfoSubDiseaseCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				DiseaseDtdata.count = '0'
			
			DiseaseDtdata.color		=	 colors[counterDisease]
			counterDisease  += 1
				
		counterCountry = 0		
		for CountryOfOriginDtGraphdata in CountryOfOriginDtGraph:
			CountryOfOriginDtGraphdataCount = PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(country_of_origine_id=CountryOfOriginDtGraphdata.id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).count()
			if CountryOfOriginDtGraphdataCount:
				CountryOfOriginDtGraphdata.count	=	 round(int(CountryOfOriginDtGraphdataCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				CountryOfOriginDtGraphdata.count = '0'
			
			CountryOfOriginDtGraphdata.color	=	 colors[counterCountry]
			counterCountry  += 1

		for allMonth in allMonths:
			num_days = calendar.monthrange(allMonth[0], allMonth[1])
			start_date = datetime.date(allMonth[0], allMonth[1], 1)
			last_day = datetime.date(allMonth[0], allMonth[1], num_days[1])

			yearData[str(allMonth[0])+'-'+str(allMonth[1])] = 	PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(registration_date__range=(start_date, last_day)) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).count()

		#print(PatientGeneralInfoDetial.query)

	if PatientGeneralInfoDetial:
		for PatientGeneralInfoDetial1 in PatientGeneralInfoDetial:
			family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial1.id).values("family_id").first();
			if family_detail:
				PatientGeneralInfoDetial1.family_id = family_detail["family_id"]
			else:
				PatientGeneralInfoDetial1.family_id = ''

				
	if CountryOfOriginDtGraph:
		for CountryOfOriginDtGraph1 in CountryOfOriginDtGraph:
			CountryOfOriginDtGraph1.name	=	CountryOfOriginDtGraph1.name.strip()
			
	#	yearData = collections.OrderedDict(sorted(yearData.items()))
	#return HttpResponse(yearData)
	
	if DiseaseDts:
		for DiseaseDts1 in DiseaseDts:
			DiseaseDts1.name	=	DiseaseDts1.name.strip()
			
	context		=	{
		"family_id":family_id,
		"institute_id":institute_id,
		"assignedDiseases":assignedDiseases,
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial,
		"Institudes":Institudes,
		"DiseaseDts":DiseaseDts,
		"CountryOfOriginDtGraph":CountryOfOriginDtGraph,
		"yearData":yearData
	}
	#return HttpResponse(CountryOfOriginDtGraph[0].name)
	#return HttpResponse(CountryOfOriginDtGraph[0].color)
	return render(request, 'ophthalmology/index.html',context)

@login_required(login_url='/')
def add_new_patient(request,selected_disease_id):
	#return HttpResponse(request.POST)
	detail 	=	AdminSubDiseaseDt.objects.filter(id=selected_disease_id).first();
	if not detail:
		return redirect('/ophthalmology/')

	if request.user.is_superuser != 1:
		AssignedDiseaseList = DoctorDisease.objects.filter(user_id=request.user.id).first()
		if AssignedDiseaseList:
			AssignedDiseases	=	AssignedDiseaseList.disease.values("id")
			#return HttpResponse(selected_disease_id)
			#if not selected_disease_id in AssignedDiseases:
				#return redirect('/ophthalmology/')
		else:
			return redirect('/ophthalmology/')

	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
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
		user_folder = 'ophthalmology/'+str(currentMonth)+str(currentYear)+"/"

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

		if request.POST.get("institute_id") != "" and request.POST.get("registration_date"):
			rend_string = random.randint(1000000, 9999999);
			registration_id	=	request.POST["institute_id"]+''+request.POST["registration_date"].replace("-","")+''+str(rend_string);
			##return HttpResponse(registration_id);
			PatientInfo.registration_id	=	registration_id

		if request.POST.get("institute_id"):
			institute_id	=	InstituteDt.objects.filter(institute_id=request.POST["institute_id"]).values("id").first();
			PatientInfo.institute_id = institute_id["id"];

		if selected_disease_id:
			PatientInfo.admin_sub_disease_id = selected_disease_id;

		if request.POST.get("patient_id"):
			PatientInfo.patient_id	=	request.POST["patient_id"]

		if request.POST.get("relationship_to_proband"):
			PatientInfo.relationship_to_proband_id	=	request.POST["relationship_to_proband"]

		if request.POST.get("relationship_to_proband_other"):
			PatientInfo.relationship_to_proband_other	=	request.POST["relationship_to_proband_other"]

		if request.POST.get("birth_year_month"):
			PatientInfo.birth_year_month	=	request.POST["birth_year_month"]

		if request.POST.get("sex"):
			PatientInfo.sex_id	=	request.POST["sex"]

		if request.POST.get("sex_other"):
			PatientInfo.sex_other	=	request.POST["sex_other"]

		if request.POST.get("registration_date"):
			PatientInfo.registration_date	=	request.POST["registration_date"]

		if request.POST.get("dna_sample_collection_date"):
			PatientInfo.dna_sample_collection_date	=	request.POST["dna_sample_collection_date"]

		if request.POST.get("disease"):
			PatientInfo.disease_id	=	request.POST["disease"]

		if request.POST.get("sub_disease"):
			PatientInfo.sub_disease_id	=	request.POST["sub_disease"]

		if request.POST.get("disease_other"):
			PatientInfo.disease_other	=	request.POST["disease_other"]

		if request.POST.get("affected"):
			PatientInfo.affected_id	=	request.POST["affected"]

		if request.POST.get("affected_other"):
			PatientInfo.affected_other	=	request.POST["affected_other"]

		#return HttpResponse(PatientInfo.affected_id)

		if request.POST.get("inheritance"):
			PatientInfo.inheritance_id	=	request.POST["inheritance"]

		if request.POST.get("inheritance_other"):
			PatientInfo.inheritance_other	=	request.POST["inheritance_other"]

		if request.POST.get("sample_id"):
			PatientInfo.sample_id	=	request.POST["sample_id"]

		if request.POST.get("syndromic"):
			PatientInfo.syndromic_id	=	request.POST["syndromic"]

		if request.POST.get("syndromic_other"):
			PatientInfo.syndromic_other	=	request.POST["syndromic_other"]

		if request.POST.get("bilateral"):
			PatientInfo.bilateral_id	=	request.POST["bilateral"]

		if request.POST.get("bilateral_other"):
			PatientInfo.bilateral_other	=	request.POST["bilateral_other"]

		if request.POST.get("ocular_symptom_1"):
			PatientInfo.ocular_symptom_1_id	=	request.POST["ocular_symptom_1"]

		if request.POST.get("ocular_symptom_1_other"):
			PatientInfo.ocular_symptom_1_other	=	request.POST["ocular_symptom_1_other"]

		if request.POST.get("ocular_symptom_2"):
			PatientInfo.ocular_symptom_2_id	=	request.POST["ocular_symptom_2"]

		if request.POST.get("ocular_symptom_2_other"):
			PatientInfo.ocular_symptom_2_other	=	request.POST["ocular_symptom_2_other"]

		if request.POST.get("ocular_symptom_3"):
			PatientInfo.ocular_symptom_3_id	=	request.POST["ocular_symptom_3"]

		if request.POST.get("ocular_symptom_3_other"):
			PatientInfo.ocular_symptom_3_other	=	request.POST["ocular_symptom_3_other"]

		if request.POST.get("progression"):
			PatientInfo.progression_id	=	request.POST["progression"]

		if request.POST.get("progression_other"):
			PatientInfo.progression_other	=	request.POST["progression_other"]

		if request.POST.get("flactuation"):
			PatientInfo.flactuation_id	=	request.POST["flactuation"]

		if request.POST.get("flactuation_other"):
			PatientInfo.flactuation_other	=	request.POST["flactuation_other"]

		if request.POST.get("family_history"):
			PatientInfo.family_history_id	=	request.POST["family_history"]

		if request.POST.get("family_history_other"):
			PatientInfo.family_history_other	=	request.POST["family_history_other"]

		if request.POST.get("consanguineous"):
			PatientInfo.consanguineous_id	=	request.POST["consanguineous"]

		if request.POST.get("consanguineous_other"):
			PatientInfo.consanguineous_other	=	request.POST["consanguineous_other"]

		if request.POST.get("number_of_affected_members_in_the_same_pedigree"):
			PatientInfo.number_of_affected_members_in_the_same_pedigree_id	=	request.POST["number_of_affected_members_in_the_same_pedigree"]

		if request.POST.get("number_of_affected_members_in_the_same_pedigree_other"):
			PatientInfo.number_of_affected_members_in_the_same_pedigree_other	=	request.POST["number_of_affected_members_in_the_same_pedigree_other"]

		if request.POST.get("ethnicity"):
			PatientInfo.ethnicity_id	=	request.POST["ethnicity"]

		if request.POST.get("ethnicity_other"):
			PatientInfo.ethnicity_other	=	request.POST["ethnicity_other"]

		if request.POST.get("country_of_origine"):
			PatientInfo.country_of_origine_id	=	request.POST["country_of_origine"]

		if request.POST.get("country_of_origine_other"):
			PatientInfo.country_of_origine_other	=	request.POST["country_of_origine_other"]

		if request.POST.get("origin_prefecture_in_japan"):
			PatientInfo.origin_prefecture_in_japan_id	=	request.POST["origin_prefecture_in_japan"]

		if request.POST.get("origin_prefecture_in_japan_other"):
			PatientInfo.origin_prefecture_in_japan_other	=	request.POST["origin_prefecture_in_japan_other"]

		if request.POST.get("ethnic_of_father"):
			PatientInfo.ethnic_of_father_id	=	request.POST["ethnic_of_father"]

		if request.POST.get("ethnic_of_father_other"):
			PatientInfo.ethnic_of_father_other	=	request.POST["ethnic_of_father_other"]

		if request.POST.get("original_country_of_father"):
			PatientInfo.original_country_of_father_id	=	request.POST["original_country_of_father"]

		if request.POST.get("original_country_of_father_other"):
			PatientInfo.original_country_of_father_other	=	request.POST["original_country_of_father_other"]

		if request.POST.get("origin_of_father_in_japan"):
			PatientInfo.origin_of_father_in_japan_id	=	request.POST["origin_of_father_in_japan"]

		if request.POST.get("origin_of_father_in_japan_other"):
			PatientInfo.origin_of_father_in_japan_other	=	request.POST["origin_of_father_in_japan_other"]

		if request.POST.get("ethnic_of_mother"):
			PatientInfo.ethnic_of_mother_id	=	request.POST["ethnic_of_mother"]

		if request.POST.get("ethnic_of_mother_other"):
			PatientInfo.ethnic_of_mother_other	=	request.POST["ethnic_of_mother_other"]

		if request.POST.get("original_country_of_mother"):
			PatientInfo.original_country_of_mother_id	=	request.POST["original_country_of_mother"]

		if request.POST.get("original_country_of_mother_other"):
			PatientInfo.original_country_of_mother_other	=	request.POST["original_country_of_mother_other"]

		if request.POST.get("origin_of_mother_in_japan"):
			PatientInfo.origin_of_mother_in_japan_id	=	request.POST["origin_of_mother_in_japan"]

		if request.POST.get("origin_of_mother_in_japan_other"):
			PatientInfo.origin_of_mother_in_japan_other	=	request.POST["origin_of_mother_in_japan_other"]

		#if request.POST.get("registration"):
			#PatientInfo.registration	=	request.POST["registration"]

		if request.POST.get("gene_type"):
			PatientInfo.gene_type_id	=	request.POST["gene_type"]

		if request.POST.get("gene_type_other"):
			PatientInfo.gene_type_other	=	request.POST["gene_type_other"]

		if request.POST.get("family_history"):
			PatientInfo.family_history_id	=	request.POST["family_history"]

		if request.POST.get("family_history_other"):
			PatientInfo.family_history_other	=	request.POST["family_history_other"]

		if request.POST.get("inheritance_type"):
			PatientInfo.inheritance_type_id	=	request.POST["inheritance_type"]

		if request.POST.get("inheritance_type_other"):
			PatientInfo.inheritance_type_other	=	request.POST["inheritance_type_other"]

		if request.POST.get("mutation_type"):
			PatientInfo.mutation_type_id	=	request.POST["mutation_type"]

		if request.POST.get("mutation_type_other"):
			PatientInfo.mutation_type_other	=	request.POST["mutation_type_other"]

		if request.POST.get("gene_inheritance_mutation_comments"):
			PatientInfo.gene_inheritance_mutation_comments	=	request.POST["gene_inheritance_mutation_comments"]

		if request.POST.get("sequencing"):
			PatientInfo.sequencing_id	=	request.POST["sequencing"]

		if request.POST.get("sequencing_other"):
			PatientInfo.sequencing_other	=	request.POST["sequencing_other"]

		if request.POST.get("analysis"):
			PatientInfo.analysis_id	=	request.POST["analysis"]

		if request.POST.get("analysis_other"):
			PatientInfo.analysis_other	=	request.POST["analysis_other"]

		if request.POST.get("dna_extraction_process"):
			PatientInfo.dna_extraction_process_id	=	request.POST["dna_extraction_process"]

		if request.POST.get("dna_extraction_process_other"):
			PatientInfo.dna_extraction_process_other	=	request.POST["dna_extraction_process_other"]

		if request.POST.get("overall_comments"):
			PatientInfo.overall_comments	=	request.POST["overall_comments"]




		PatientInfo.pedigree_chart	=	pedigree_chart
		PatientInfo.is_draft		=	request.POST["is_draft"]
		PatientInfo.user_id			=	request.user.id
		PatientInfo.save()
		lastPatientId		=	PatientInfo.id

		PatientGeneralInfoFamilyInfo   			= PatientGeneralInfoFamily()

		if request.POST.get("family_id"):
			PatientGeneralInfoFamilyInfo.family_id	=	request.POST["family_id"]

		PatientGeneralInfoFamilyInfo.patient_id	=	lastPatientId

		PatientGeneralInfoFamilyInfo.save()




		PatientOtherUncommonInfoOphthalmologyInfo	=	PatientOtherUncommonInfoOphthalmology()
		if request.POST.get("ocul_surgeries_cornea_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_id	=	request.POST["ocul_surgeries_cornea_right"]

		if request.POST.get("ocul_surgeries_cornea_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other	=	request.POST["ocul_surgeries_cornea_right_other"]

		if request.POST.get("ocul_surgeries_cornea_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_id	=	request.POST["ocul_surgeries_cornea_left"]

		if request.POST.get("ocul_surgeries_cornea_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other	=	request.POST["ocul_surgeries_cornea_left_other"]

		if request.POST.get("age_corneal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_id	=	request.POST["age_corneal_surgery_perf_right"]

		if request.POST.get("age_corneal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other	=	request.POST["age_corneal_surgery_perf_right_other"]

		if request.POST.get("age_corneal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_id	=	request.POST["age_corneal_surgery_perf_left"]

		if request.POST.get("age_corneal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other	=	request.POST["age_corneal_surgery_perf_left_other"]

		if request.POST.get("no_corneal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_id	=	request.POST["no_corneal_surgery_perf_right"]

		if request.POST.get("no_corneal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other	=	request.POST["no_corneal_surgery_perf_right_other"]

		if request.POST.get("no_corneal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_id	=	request.POST["no_corneal_surgery_perf_left"]

		if request.POST.get("no_corneal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other	=	request.POST["no_corneal_surgery_perf_left_other"]

		if request.POST.get("ocul_surgeries_glaucoma_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_id	=	request.POST["ocul_surgeries_glaucoma_right"]

		if request.POST.get("ocul_surgeries_glaucoma_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other	=	request.POST["ocul_surgeries_glaucoma_right_other"]

		if request.POST.get("ocul_surgeries_glaucoma_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_id	=	request.POST["ocul_surgeries_glaucoma_left"]

		if request.POST.get("ocul_surgeries_glaucoma_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other	=	request.POST["ocul_surgeries_glaucoma_left_other"]

		if request.POST.get("age_glaucoma_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_id	=	request.POST["age_glaucoma_surgery_perf_right"]

		if request.POST.get("age_glaucoma_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other	=	request.POST["age_glaucoma_surgery_perf_right_other"]

		if request.POST.get("age_glaucoma_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_id	=	request.POST["age_glaucoma_surgery_perf_left"]

		if request.POST.get("age_glaucoma_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other	=	request.POST["age_glaucoma_surgery_perf_left_other"]

		if request.POST.get("no_glaucomal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_id	=	request.POST["no_glaucomal_surgery_perf_right"]

		if request.POST.get("no_glaucomal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other	=	request.POST["no_glaucomal_surgery_perf_right_other"]

		if request.POST.get("no_glaucomal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_id	=	request.POST["no_glaucomal_surgery_perf_left"]

		if request.POST.get("no_glaucomal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other	=	request.POST["no_glaucomal_surgery_perf_left_other"]

		if request.POST.get("ocul_surgeries_retina_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_id	=	request.POST["ocul_surgeries_retina_right"]

		if request.POST.get("ocul_surgeries_retina_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other	=	request.POST["ocul_surgeries_retina_right_other"]

		if request.POST.get("ocul_surgeries_retina_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_id	=	request.POST["ocul_surgeries_retina_left"]

		if request.POST.get("ocul_surgeries_retina_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other	=	request.POST["ocul_surgeries_retina_left_other"]

		if request.POST.get("age_vitreoretina_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_id	=	request.POST["age_vitreoretina_surgery_perf_right"]

		if request.POST.get("age_vitreoretina_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other	=	request.POST["age_vitreoretina_surgery_perf_right_other"]

		if request.POST.get("age_vitreoretina_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_id	=	request.POST["age_vitreoretina_surgery_perf_left"]

		if request.POST.get("age_vitreoretina_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other	=	request.POST["age_vitreoretina_surgery_perf_left_other"]

		if request.POST.get("no_vitreoretinal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_id	=	request.POST["no_vitreoretinal_surgery_perf_right"]

		if request.POST.get("no_vitreoretinal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other	=	request.POST["no_vitreoretinal_surgery_perf_right_other"]

		if request.POST.get("no_vitreoretinal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_id	=	request.POST["no_vitreoretinal_surgery_perf_left"]

		if request.POST.get("no_vitreoretinal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other	=	request.POST["no_vitreoretinal_surgery_perf_left_other"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_id	=	request.POST["age_ocul_surgeries_lasers_perf_right"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other	=	request.POST["age_ocul_surgeries_lasers_perf_right_other"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_id	=	request.POST["age_ocul_surgeries_lasers_perf_left"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other	=	request.POST["age_ocul_surgeries_lasers_perf_left_other"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_id	=	request.POST["no_ofocul_surgeries_lasers_perf_right"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other	=	request.POST["no_ofocul_surgeries_lasers_perf_right_other"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_id	=	request.POST["no_ofocul_surgeries_lasers_perf_left"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other	=	request.POST["no_ofocul_surgeries_lasers_perf_left_other"]

		if request.POST.get("ocul_surgeries_lasers_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_id	=	request.POST["ocul_surgeries_lasers_right"]

		if request.POST.get("ocul_surgeries_lasers_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other	=	request.POST["ocul_surgeries_lasers_right_other"]

		if request.POST.get("ocul_surgeries_lasers_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_id	=	request.POST["ocul_surgeries_lasers_left"]

		if request.POST.get("ocul_surgeries_lasers_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other	=	request.POST["ocul_surgeries_lasers_left_other"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_id	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_right"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_right_other"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_id	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_left"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_left_other"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_id	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_right"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_right_other"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_id	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_left"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_left_other"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_id	=	request.POST["opht_medi_subtenon_subconj_injec_right"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other	=	request.POST["opht_medi_subtenon_subconj_injec_right_other"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_id	=	request.POST["opht_medi_subtenon_subconj_injec_left"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other	=	request.POST["opht_medi_subtenon_subconj_injec_left_other"]

		if request.POST.get("ocul_medi_internal_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_id	=	request.POST["ocul_medi_internal_right"]

		if request.POST.get("ocul_medi_internal_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other	=	request.POST["ocul_medi_internal_right_other"]

		if request.POST.get("ocul_medi_internal_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_id	=	request.POST["ocul_medi_internal_left"]

		if request.POST.get("ocul_medi_internal_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other	=	request.POST["ocul_medi_internal_left_other"]

		if request.POST.get("age_ocul_medi_internal_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_id	=	request.POST["age_ocul_medi_internal_perf_right"]

		if request.POST.get("age_ocul_medi_internal_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other	=	request.POST["age_ocul_medi_internal_perf_right_other"]

		if request.POST.get("age_ocul_medi_internal_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_id	=	request.POST["age_ocul_medi_internal_perf_left"]

		if request.POST.get("age_ocul_medi_internal_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other	=	request.POST["age_ocul_medi_internal_perf_left_other"]

		if request.POST.get("no_ocul_medi_internal_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_id	=	request.POST["no_ocul_medi_internal_perf_right"]

		if request.POST.get("no_ocul_medi_internal_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other	=	request.POST["no_ocul_medi_internal_perf_right_other"]

		if request.POST.get("no_ocul_medi_internal_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_id	=	request.POST["no_ocul_medi_internal_perf_left"]

		if request.POST.get("no_ocul_medi_internal_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other	=	request.POST["no_ocul_medi_internal_perf_left_other"]

		if request.POST.get("ocul_medi_topical_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_id	=	request.POST["ocul_medi_topical_right"]

		if request.POST.get("ocul_medi_topical_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other	=	request.POST["ocul_medi_topical_right_other"]

		if request.POST.get("ocul_medi_topical_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_id	=	request.POST["ocul_medi_topical_left"]

		if request.POST.get("ocul_medi_topical_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other	=	request.POST["ocul_medi_topical_left_other"]

		if request.POST.get("age_ocul_medi_topical_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_id	=	request.POST["age_ocul_medi_topical_perf_right"]

		if request.POST.get("age_ocul_medi_topical_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other	=	request.POST["age_ocul_medi_topical_perf_right_other"]

		if request.POST.get("age_ocul_medi_topical_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_id	=	request.POST["age_ocul_medi_topical_perf_left"]

		if request.POST.get("age_ocul_medi_topical_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other	=	request.POST["age_ocul_medi_topical_perf_left_other"]

		if request.POST.get("no_ocul_medi_topical_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_id	=	request.POST["no_ocul_medi_topical_perf_right"]

		if request.POST.get("no_ocul_medi_topical_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other	=	request.POST["no_ocul_medi_topical_perf_right_other"]

		if request.POST.get("no_ocul_medi_topical_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_id	=	request.POST["no_ocul_medi_topical_perf_left"]

		if request.POST.get("no_ocul_medi_topical_perf_left_other"):
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

		if request.POST.get("ocul_surgeries_catrct_left"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_id	=	request.POST["ocul_surgeries_catrct_left"]

		if request.POST.get("ocul_surgeries_catrct_left_other"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other	=	request.POST["ocul_surgeries_catrct_left_other"]

		if request.POST.get("age_catrct_surgery_perf_left"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_id	=	request.POST["age_catrct_surgery_perf_left"]

		if request.POST.get("age_catrct_surgery_perf_left_other"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other	=	request.POST["age_catrct_surgery_perf_left_other"]

		if request.POST.get("no_catrct_surgery_perf_left"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_id	=	request.POST["no_catrct_surgery_perf_left"]

		if request.POST.get("no_catrct_surgery_perf_left_other"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other	=	request.POST["no_catrct_surgery_perf_left_other"]

		if request.POST.get("age_at_onset_of_ocul_symp"):
			PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_id	=	request.POST["age_at_onset_of_ocul_symp"]

		if request.POST.get("age_at_onset_of_ocul_symp_other"):
			PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other	=	request.POST["age_at_onset_of_ocul_symp_other"]

		if request.POST.get("age_at_the_init_diag"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_id	=	request.POST["age_at_the_init_diag"]

		if request.POST.get("age_at_the_init_diag_other"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other	=	request.POST["age_at_the_init_diag_other"]

		if request.POST.get("age_at_the_init_diag_clas"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_id	=	request.POST["age_at_the_init_diag_clas"]

		if request.POST.get("age_at_the_init_diag_clas_other"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other	=	request.POST["age_at_the_init_diag_clas_other"]

		if request.POST.get("ocul_surgeries_catrct_right"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_id	=	request.POST["ocul_surgeries_catrct_right"]

		if request.POST.get("ocul_surgeries_catrct_right_other"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other	=	request.POST["ocul_surgeries_catrct_right_other"]

		if request.POST.get("age_catrct_surgery_perf_right"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_id	=	request.POST["age_catrct_surgery_perf_right"]

		if request.POST.get("age_catrct_surgery_perf_right_other"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other	=	request.POST["age_catrct_surgery_perf_right_other"]

		if request.POST.get("no_catrct_surgery_perf_right"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_id	=	request.POST["no_catrct_surgery_perf_right"]

		if request.POST.get("no_catrct_surgery_perf_right_other"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other	=	request.POST["no_catrct_surgery_perf_right_other"]

		if request.POST.get("onset_of_diease_clas"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_id	=	request.POST["onset_of_diease_clas"]

		if request.POST.get("onset_of_diease_clas_other"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other	=	request.POST["onset_of_diease_clas_other"]

		if request.POST.get("gene_comments"):
			PatientGeneralInfoOphthalmologyInfo.gene_comments	=	request.POST["gene_comments"]


		PatientGeneralInfoOphthalmologyInfo.patient_id	=	lastPatientId
		PatientGeneralInfoOphthalmologyInfo.save()

		##return HttpResponse(PatientGeneralInfoOphthalmologyInfo.id)







		#### save data in PatientGeneralInfoMultiVisitOphthalmologyImages model ####
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'ophthalmology/multi_visit_ophthalmology_images/'+str(currentMonth)+str(currentYear)+"/"

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
		user_folder = 'ophthalmology/multi_visit_ophthalmology_images/'+str(currentMonth)+str(currentYear)+"/"

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

		general_info_multi_visit_ophthalmology_static	=	["intra_ocul_pres_right","intra_ocul_pres_clas_right","intra_ocul_pres_left","intra_ocul_pres_clas_left","refr_error_sphe_equi_clas_right","refr_error_sphe_equi_left","refr_error_sphe_equi_right","refr_error_sphe_equi_clas_left","corn_thic_right","corn_thic_left","lens_right","lens_left","axia_leng_right","axia_leng_clas_right","axia_leng_left","axia_leng_clas_left","macu_thic_right","macu_edema_right","macu_schisis_right","epir_memb_right","sub_sensreti_fuild_right","sub_reti_epith_memb_fuild_right","macu_thic_left","macu_edema_left","macu_schisis_left","epir_memb_left","sub_sensreti_fuild_left","sub_reti_epith_memb_fuild_left","foveal_thic_right","foveal_thic_left","choro_thic_right","choro_thic_left","stat_peri_mean_sens_hfa24_2_right","stat_peri_mean_sens_clas_right","stat_peri_mean_sens_hfa24_2_left","stat_peri_mean_sens_clas_left","electro_right","full_field_electphysiol_clas_right","multi_electphysiol_clas_right","electroneg_config_of_dark_apa","electro_left","full_field_electphysiol_clas_left","multi_electphysiol_clas_left","ai_diagnosis_for_others_right","ai_accuracy_for_others_right_per","ai_diagnosis_for_others_left","ai_accuracy_for_others_left_per","ai_comments"]

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
				if field_name_3 == "freq_ethnicity_per" or field_name_3 == "freq_ethnicity" or field_name_3 == "freq_ethnicity_other" or field_name_3 == "freq_local_population_other" or field_name_3 == "freq_local_population" or field_name_3 == "freq_local_population_per":
					field_name_4	=	full_field_name[3]
				else:
					field_name_4	=	""



				if field_name_1 not in dic:
					dic[field_name_1]								=	{}

				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}

				if "addmore_left" not in dic[field_name_1][field_name_2]:
					dic[field_name_1][field_name_2]["addmore_left"]		=	{}

				if "addmore_right" not in dic[field_name_1][field_name_2]:
					dic[field_name_1][field_name_2]["addmore_right"]		=	{}

				if field_name_3 == "freq_ethnicity_per" or field_name_3 == "freq_ethnicity" or field_name_3 == "freq_ethnicity_other":
					if field_name_4 not in dic[field_name_1][field_name_2]["addmore_left"]:
						dic[field_name_1][field_name_2]["addmore_left"][field_name_4]				=	{}

					dic[field_name_1][field_name_2]["addmore_left"][field_name_4][field_name_3]		=	request.POST.get(k)
				elif field_name_3 == "freq_local_population" or field_name_3 == "freq_local_population_per" or field_name_3 == "freq_local_population_other":
					if field_name_4 not in dic[field_name_1][field_name_2]["addmore_right"]:
						dic[field_name_1][field_name_2]["addmore_right"][field_name_4]				=	{}

					dic[field_name_1][field_name_2]["addmore_right"][field_name_4][field_name_3]		=	request.POST.get(k)
				else:
					dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)






		if dic["patientCausativeGeneInfo"]:
			is_not_empty = 0
			for fromData in dic["patientCausativeGeneInfo"]:
				if fromData in dic["patientCausativeGeneInfo"] and "type_old_new" in dic["patientCausativeGeneInfo"][fromData]:
					type_old_new		=	dic["patientCausativeGeneInfo"][fromData]["type_old_new"]
					is_not_empty 		= 1
				else:
					type_old_new		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "type_old_new_other" in dic["patientCausativeGeneInfo"][fromData]:
					type_old_new_other		=	dic["patientCausativeGeneInfo"][fromData]["type_old_new_other"]
				else:
					type_old_new_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand"]
					is_not_empty 		= 1
				else:
					caus_cand		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_other" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_other		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_other"]
				else:
					caus_cand_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_gene" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_gene		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_gene"]
					is_not_empty 		= 1
				else:
					caus_cand_gene		=	""
					
					
				if fromData in dic["patientCausativeGeneInfo"] and "disease_caus_cand_gene" in dic["patientCausativeGeneInfo"][fromData]:
					disease_caus_cand_gene		=	dic["patientCausativeGeneInfo"][fromData]["disease_caus_cand_gene"]
					is_not_empty 		= 1
				else:
					disease_caus_cand_gene		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_gene_other" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_gene_other		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_gene_other"]
				else:
					caus_cand_gene_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "chromosome" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome		=	dic["patientCausativeGeneInfo"][fromData]["chromosome"]
					is_not_empty 		= 1
				else:
					chromosome		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "chromosome_other" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome_other		=	dic["patientCausativeGeneInfo"][fromData]["chromosome_other"]
				else:
					chromosome_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "chromosome_comment" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome_comment		=	dic["patientCausativeGeneInfo"][fromData]["chromosome_comment"]
					is_not_empty 		= 1
				else:
					chromosome_comment		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "position" in dic["patientCausativeGeneInfo"][fromData]:
					position		=	dic["patientCausativeGeneInfo"][fromData]["position"]
					is_not_empty 		= 1
				else:
					position		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "transcript" in dic["patientCausativeGeneInfo"][fromData]:
					transcript		=	dic["patientCausativeGeneInfo"][fromData]["transcript"]
					is_not_empty 		= 1
				else:
					transcript		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "exon" in dic["patientCausativeGeneInfo"][fromData]:
					exon		=	dic["patientCausativeGeneInfo"][fromData]["exon"]
					is_not_empty 		= 1
				else:
					exon		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "exon_other" in dic["patientCausativeGeneInfo"][fromData]:
					exon_other		=	dic["patientCausativeGeneInfo"][fromData]["exon_other"]
				else:
					exon_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "exon_comment" in dic["patientCausativeGeneInfo"][fromData]:
					exon_comment		=	dic["patientCausativeGeneInfo"][fromData]["exon_comment"]
					is_not_empty 		= 1
				else:
					exon_comment		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_mutation_nucleotide_amino_acid" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_mutation_nucleotide_amino_acid		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_mutation_nucleotide_amino_acid"]
					is_not_empty 		= 1
				else:
					caus_cand_mutation_nucleotide_amino_acid		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_mutation_nucleotide_amino_acid_comment" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_mutation_nucleotide_amino_acid_comment		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_mutation_nucleotide_amino_acid_comment"]
					is_not_empty 		= 1
				else:
					caus_cand_mutation_nucleotide_amino_acid_comment		=	""
				latTableId = ''
				if type_old_new or caus_cand or caus_cand_gene or disease_caus_cand_gene or chromosome or chromosome_comment or position or transcript or exon or exon_comment or caus_cand_mutation_nucleotide_amino_acid or caus_cand_mutation_nucleotide_amino_acid_comment:
					PatientCausativeGeneInfoInfo									=	PatientCausativeGeneInfo()
					PatientCausativeGeneInfoInfo.patient_id							=	lastPatientId
					PatientCausativeGeneInfoInfo.type_old_new_id					=	type_old_new
					PatientCausativeGeneInfoInfo.type_old_new_other					=	type_old_new_other
					PatientCausativeGeneInfoInfo.caus_cand_id						=	caus_cand
					PatientCausativeGeneInfoInfo.caus_cand_other					=	caus_cand_other
					PatientCausativeGeneInfoInfo.caus_cand_gene_id					=	caus_cand_gene
					PatientCausativeGeneInfoInfo.disease_caus_cand_gene_id			=	disease_caus_cand_gene
					PatientCausativeGeneInfoInfo.caus_cand_gene_other				=	caus_cand_gene_other
					PatientCausativeGeneInfoInfo.chromosome_id						=	chromosome
					PatientCausativeGeneInfoInfo.chromosome_other					=	chromosome_other
					PatientCausativeGeneInfoInfo.chromosome_comment					=	chromosome_comment
					PatientCausativeGeneInfoInfo.position							=	position
					PatientCausativeGeneInfoInfo.transcript							=	transcript
					PatientCausativeGeneInfoInfo.exon_id							=	exon
					PatientCausativeGeneInfoInfo.exon_other							=	exon_other
					PatientCausativeGeneInfoInfo.exon_comment						=	exon_comment
					PatientCausativeGeneInfoInfo.caus_cand_mutation_nucleotide_amino_acid	=	caus_cand_mutation_nucleotide_amino_acid
					PatientCausativeGeneInfoInfo.caus_cand_mutation_nucleotide_amino_acid_comment	=	caus_cand_mutation_nucleotide_amino_acid_comment
					PatientCausativeGeneInfoInfo.save()

					latTableId	=	PatientCausativeGeneInfoInfo.id
				if latTableId :
					for fromData2 in dic["patientCausativeGeneInfo"][fromData]["addmore_left"]:
						freq_ethnicity			=	""
						freq_ethnicity_per		=	""
						freq_ethnicity_other	=	""

						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity"]:
							freq_ethnicity	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_per"]:
							freq_ethnicity_per	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_per"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_other"]:
							freq_ethnicity_other	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_other"]

						if freq_ethnicity:
							PatientCausativeGeneInfoEthnicityInfo	=	PatientCausativeGeneInfoEthnicity()
							PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_per					=	freq_ethnicity_per
							PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_id						=	freq_ethnicity
							PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_other					=	freq_ethnicity_other
							PatientCausativeGeneInfoEthnicityInfo.patient_causative_gene_info_id		=	latTableId
							PatientCausativeGeneInfoEthnicityInfo.save()

					for fromData2 in dic["patientCausativeGeneInfo"][fromData]["addmore_right"]:
						freq_local_population			=	""
						freq_local_population_per		=	""
						freq_local_population_other	=	""

						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population"]:
							freq_local_population	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_per"]:
							freq_local_population_per	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_per"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_other"]:
							freq_local_population_other	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_other"]

						if freq_local_population:
							PatientCausativeGeneInfoLocalPopulationInfo =	PatientCausativeGeneInfoLocalPopulation()
							PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_per		=	freq_local_population_per
							PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_id		=	freq_local_population
							PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_other	=	freq_local_population_other
							PatientCausativeGeneInfoLocalPopulationInfo.patient_causative_gene_info_id =	latTableId
							PatientCausativeGeneInfoLocalPopulationInfo.save()

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

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_other" in dic["systemicAbnormality"][fromData]:
					name_other		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_other"]
				else:
					name_other		=	""

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_comment" in dic["systemicAbnormality"][fromData]:
					name_comment		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_comment"]
				else:
					name_comment		=	""

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_date" in dic["systemicAbnormality"][fromData]:
					name_date		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_date"]
				else:
					name_date		=	""

				PatientGeneralInfoOphthalmologySystAbnormalityInfo					=	PatientGeneralInfoOphthalmologySystAbnormality()
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.patient_id		=	lastPatientId
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.name_id				=	systemicAbnormality_name
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.comments			=	name_comment
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.other			=	name_other
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

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_other" in dic["ocularSymptom"][fromData]:
					name_other		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_other"]
				else:
					name_other		=	""

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_comment" in dic["ocularSymptom"][fromData]:
					name_comment		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_comment"]
				else:
					name_comment		=	""

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_date" in dic["ocularSymptom"][fromData]:
					name_date		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_date"]
				else:
					name_date		=	""

				PatientGeneralInfoOphthalmologyOcularCompliInfo						=	PatientGeneralInfoOphthalmologyOcularCompli()
				PatientGeneralInfoOphthalmologyOcularCompliInfo.patient_id			=	lastPatientId
				PatientGeneralInfoOphthalmologyOcularCompliInfo.name_id				=	ocularSymptom_name
				PatientGeneralInfoOphthalmologyOcularCompliInfo.comments			=	name_comment
				PatientGeneralInfoOphthalmologyOcularCompliInfo.other				=	name_other
				PatientGeneralInfoOphthalmologyOcularCompliInfo.date				=	name_date
				PatientGeneralInfoOphthalmologyOcularCompliInfo.save()



		messages.success(request,"Patient has been added successfully.")
		return redirect('/ophthalmology/')



	Institudes	=	InstituteDt.objects.order_by("id").all()
	RelationshipToProbandDts	=	RelationshipToProbandDt.objects.order_by("id").all()
	SexDts	=	SexDt.objects.order_by("id").all()
	DiseaseDts	=	DiseaseDt.objects.order_by("id").all()
	AffectedDts	=	AffectedDt.objects.order_by("id").all()
	InheritanceDts	=	InheritanceDt.objects.order_by("id").all()
	SyndromicDts	=	SyndromicDt.objects.order_by("id").all()
	BilateralDts	=	BilateralDt.objects.order_by("id").all()
	OcularSymptomDts	=	OcularSymptomDt.objects.order_by("id").all()
	ProgressionDts	=	ProgressionDt.objects.order_by("id").all()
	FluctuationDts	=	FluctuationDt.objects.order_by("id").all()
	FamilyHistoryDts	=	FamilyHistoryDt.objects.order_by("id").all()
	ConsanguineousDts	=	ConsanguineousDt.objects.order_by("id").all()
	NumberOfAffectedMembersInTheSamePedigreeDts	=	NumberOfAffectedMembersInTheSamePedigreeDt.objects.order_by("id").all()
	EthnicityDts	=	EthnicityDt.objects.order_by("id").all()
	CountryOfOriginDts	=	CountryOfOriginDt.objects.order_by("id").all()
	OriginPrefectureInJapanDts	=	OriginPrefectureInJapanDt.objects.order_by("id").all()
	GeneDts	=	GeneDt.objects.order_by("id").all()
	MutationDts	=	MutationDt.objects.order_by("id").all()
	OcularSurgeriesCorneaDts	=	OcularSurgeriesCorneaDt.objects.order_by("id").all()
	AgeForSurgeryDts	=	AgeForSurgeryDt.objects.order_by("id").all()
	NumberOfSurgeryDts	=	NumberOfSurgeryDt.objects.order_by("id").all()
	OcularSurgeriesGlaucomaDts	=	OcularSurgeriesGlaucomaDt.objects.order_by("id").all()
	OcularSurgeriesRetinaDts	=	OcularSurgeriesRetinaDt.objects.order_by("id").all()
	OcularSurgeriesLasersDts	=	OcularSurgeriesLasersDt.objects.order_by("id").all()
	OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDts	=	OphthalmicMedicationSubtenonOrSubconjunctivalInjectionDt.objects.order_by("id").all()
	OcularMedicationInternalDts	=	OcularMedicationInternalDt.objects.order_by("id").all()
	OcularMedicationTopicalDts	=	OcularMedicationTopicalDt.objects.order_by("id").all()
	OcularSurgeriesCataractDts		=	OcularSurgeriesCataractDt.objects.order_by("id").all()
	VisualAcuityDts					=	VisualAcuityDt.objects.order_by("id").all()
	VisualAcuityClassificationDts	=	VisualAcuityClassificationDt.objects.order_by("id").all()
	PresentUnpresentDts				=	PresentUnpresentDt.objects.order_by("id").all()
	OnMedicationOrNotDts			=	OnMedicationOrNotDt.objects.order_by("id").all()
	HcOnMedicationOrNotStatinDts			=	HcOnMedicationOrNotStatinDt.objects.order_by("id").all()
	HcOnMedicationOrNotInsulinDts			=	HcOnMedicationOrNotInsulinDt.objects.order_by("id").all()
	TypicalDts								=	TypicalDt.objects.order_by("id").all()
	AgeAtOnsetOfOcularSymptomDts			=	AgeAtOnsetOfOcularSymptomDt.objects.order_by("id").all()
	AgeAtTheInitialDiagnosisDts			=	AgeAtTheInitialDiagnosisDt.objects.order_by("id").all()
	DnaExtractionInProcessDts			=	DnaExtractionInProcessDt.objects.order_by("id").all()
	AnalysisDts			=	AnalysisDt.objects.order_by("id").all()
	AgeAtOnsetClassificationDts			=	AgeAtOnsetClassificationDt.objects.order_by("id").all()
	AgeAtTheInitialDiagnosisClassificationDts	=	AgeAtTheInitialDiagnosisClassificationDt.objects.order_by("id").all()
	SequencingDts			=	SequencingDt.objects.order_by("id").all()
	AiDiagnosisForCornealDiseasesDts			=	AiDiagnosisForCornealDiseasesDt.objects.order_by("id").all()
	AiDiagnosisForGlaucomaDts			=	AiDiagnosisForGlaucomaDt.objects.order_by("id").all()
	AiDiagnosisForDiabeticRetinopathyDts			=	AiDiagnosisForDiabeticRetinopathyDt.objects.order_by("id").all()
	AiDiagnosisForAgeRelatedMacularDegenerationDts	=	AiDiagnosisForAgeRelatedMacularDegenerationDt.objects.order_by("id").all()
	AiDiagnosisForInheritedRetinalDiseasesDts	=	AiDiagnosisForInheritedRetinalDiseasesDt.objects.order_by("id").all()
	SequencingStatusDts	=	SequencingStatusDt.objects.order_by("id").all()
	IntraocularPressureDts	=	IntraocularPressureDt.objects.order_by("id").all()
	IntraocularPressureClassificationDts	=	IntraocularPressureClassificationDt.objects.order_by("id").all()
	RefractiveErrorSphericalEquivalentDts	=	RefractiveErrorSphericalEquivalentDt.objects.order_by("id").all()
	RefractiveErrorSphericalEquivalentClassificationDts	=	RefractiveErrorSphericalEquivalentClassificationDt.objects.order_by("id").all()
	LensDts	=	LensDt.objects.order_by("id").all()
	AxialLengthDts	=	AxialLengthDt.objects.order_by("id").all()
	AxialLengthClassificationDts	=	AxialLengthClassificationDt.objects.order_by("id").all()
	StaticPerimetryMeanSensitivityDts	=	StaticPerimetryMeanSensitivityDt.objects.order_by("id").all()
	StaticPerimetryMeanSensitivityClassificationDts	=	StaticPerimetryMeanSensitivityClassificationDt.objects.order_by("id").all()
	ElectrophysiologicalFindingsDts	=	ElectrophysiologicalFindingsDt.objects.order_by("id").all()
	FullFieldElectrophysiologicalGroupingDts	=	FullFieldElectrophysiologicalGroupingDt.objects.order_by("id").all()
	MultifocalElectrophysiologicalGroupingDts	=	MultifocalElectrophysiologicalGroupingDt.objects.order_by("id").all()
	ChromosomeDts	=	ChromosomeDt.objects.order_by("id").all()
	ExonDts	=	ExonDt.objects.order_by("id").all()
	AlleleFrequencyDatabaseDts	=	AlleleFrequencyDatabaseDt.objects.order_by("id").all()
	SystemicAbnormalityDts	=	SystemicAbnormalityDt.objects.order_by("id").all()
	CausCandDts	=	CausCandDt.objects.order_by("id").all()
	TypeOldNewDts	=	TypeOldNewDt.objects.order_by("id").all()
	DiseaseCausCandGeneDts	=	DiseaseCausCandGeneDt.objects.order_by("id").all()
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
		"TypeOldNewDts":TypeOldNewDts,
		"DiseaseCausCandGeneDts":DiseaseCausCandGeneDts,
	}
	return render(request, 'ophthalmology/add_new_patient.html',context)


@login_required(login_url='/')
def view_new_patient(request,id):
	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data


	#set permission doctor has access or not
	record = PatientGeneralInfo.objects.filter(id=id).first()
	if not record:
		return redirect('/ophthalmology/')

	if request.user.is_superuser != 1:
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) & (Q(id=id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).first()
		if not PatientGeneralInfoDetial:
			return redirect('/ophthalmology/')
	#set permission doctor has access or not


	PatientGeneralInfoDetial = PatientGeneralInfo.objects.filter(id=id).select_related("institute","relationship_to_proband","sex","disease","affected","inheritance","syndromic","bilateral","ocular_symptom_1","ocular_symptom_2","ocular_symptom_3","progression","flactuation","family_history","consanguineous","number_of_affected_members_in_the_same_pedigree","ethnicity","country_of_origine","origin_prefecture_in_japan","ethnic_of_father","original_country_of_father","origin_of_father_in_japan","ethnic_of_mother","original_country_of_mother","origin_of_mother_in_japan","gene_type","inheritance_type","mutation_type","dna_extraction_process","sequencing","analysis","sub_disease").first()

	family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial.id).values("family_id").first();
	if family_detail:
		PatientGeneralInfoDetial.family_id = family_detail["family_id"]
	else:
		PatientGeneralInfoDetial.family_id = ''

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

	##PatientGeneralInfoOphthalmologySystAbnormality
	PatientGeneralInfoOphthalmologySystAbnormalityInfo			=  PatientGeneralInfoOphthalmologySystAbnormality.objects.filter(patient_id=id).select_related("name").all()

	##PatientGeneralInfoOphthalmologyOcularCompli
	PatientGeneralInfoOphthalmologyOcularCompliInfo			=  PatientGeneralInfoOphthalmologyOcularCompli.objects.filter(patient_id=id).select_related("name").all()





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

	##PatientGeneralInfoMultiVisitOphthalmologyImages for step 4


	step4_images_name_list_all	=	["corn_phot_left","corn_phot_right","corn_phot_on_fluor_left","corn_phot_on_fluor_right","corn_topography_left","corn_topography_right","corn_endotherial_photy_left","corn_endotherial_photy_right","opt_cohe_tomo_of_anterior_segment_left","opt_cohe_tomo_of_anterior_segment_right","ax_length_left","ax_length_right","lens_phot_left","lens_phot_right","fund_phot_wide_field_left","fund_phot_wide_field_right","fund_autoflu_left","fund_autoflu_right","fund_autoflu_wide_field_left","fund_autoflu_wide_field_right","infra_imaging_left","infra_imaging_right","infra_imaging_wide_field_left","infra_imaging_wide_field_right","fluor_angi_left","fluor_angi_right","fluor_angi_wide_field_left","fluor_angi_wide_field_right","indo_green_angi_left","indo_green_angi_right","indo_green_angi_wide_field_left","indo_green_angi_wide_field_right","opt_cohe_tomo_disc_left","opt_cohe_tomo_disc_right","opt_cohe_tomo_macula_line_left","opt_cohe_tomo_macula_line_right","opt_cohe_tomo_macula_3d_left","opt_cohe_tomo_macula_3d_right","opt_cohe_tomo_macula_en_face_left","opt_cohe_tomo_macula_en_face_right","opt_cohe_tomo_angi_left","opt_cohe_tomo_angi_right","adap_optic_imaging_left","adap_optic_imaging_right","full_field_elect_left","full_field_elect_right","mult_elect_left","mult_elect_right","focal_macu_elect_left","focal_macu_elect_right","patt_elect_left","patt_elect_right","patt_visual_evoked_potential_left","patt_visual_evoked_potential_right","flash_visual_evoked_potential_left","flash_visual_evoked_potential_right","pupilometry_left","pupilometry_right","dark_adaptmetry_left","dark_adaptmetry_right","kine_visual_field_test_left","kine_visual_field_test_right","static_visual_field_test_left","static_visual_field_test_right","microperimetry_left","microperimetry_right","color_vision_test_left","color_vision_test_right","image_comments","image_others"]

	PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	{}
	if step4_images_name_list_all:
		for imageData in step4_images_name_list_all:
			imageData1		=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).filter(key=imageData).all()
			PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[imageData]	=	imageData1

	#return HttpResponse(PatientGeneralInfoMultiVisitOphthalmologyImagesInfo["corn_phot_left"][0].value)
	##PatientOtherMultiVisitImages for step6

	step_other_multi_visit_images_all	=	["fund_phot_left","fund_phot_right","corn_phot_ai_diag_corn_dise_left","corn_phot_ai_diag_corn_dise_right","corn_phot_on_fluo_ai_diag_corn_dise_left","corn_phot_on_fluo_ai_diag_corn_dise_right","fund_phot_ai_diag_glau_left","fund_phot_ai_diag_glau_right","opti_cohe_tomo_disc_ai_diag_glau_left","opti_cohe_tomo_disc_ai_diag_glau_right","stat_visual_field_ai_diag_glau_left","stat_visual_field_ai_diag_glau_right","fund_phot_ai_diag_diab_retino_left","fund_phot_ai_diag_diab_retino_right","fluo_angio_ai_diag_diaet_retino_left","fluo_angio_ai_diag_diaet_retino_right","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right","fund_phot_ai_diag_age_rela_macu_dege_left","fund_phot_ai_diag_age_rela_macu_dege_right","fluo_angio_ai_diag_age_rela_macu_dege_left","fluo_angio_ai_diag_age_rela_macu_dege_right","indocy_green_angio_ai_diag_age_rela_macu_dege_left","indocy_green_angio_ai_diag_age_rela_macu_dege_right","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right","fund_phot_ai_diag_inher_reti_dise_left","fund_phot_ai_diag_inher_reti_dise_right","fund_autofluo_wide_field_ai_diag_inher_reti_dise_left","fund_autofluo_wide_field_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right","full_field_elect_ai_diag_inher_reti_dise_left","full_field_elect_ai_diag_inher_reti_dise_right","multifocal_elect_ai_diag_inher_reti_dise_left","multifocal_elect_ai_diag_inher_reti_dise_right","vcf_files_ai_diag_inher_reti_dise_left","vcf_files_ai_diag_inher_reti_dise_right","others_ai_diag_left","others_ai_diag_right"]


	PatientOtherMultiVisitImagesInfo	=	{}
	if step_other_multi_visit_images_all:
		for imageData in step_other_multi_visit_images_all:
			imageData1		=	PatientOtherMultiVisitImages.objects.filter(patient_id=id).filter(key=imageData).all()
			PatientOtherMultiVisitImagesInfo[imageData]	=	imageData1


	####PatientOtherCommonInfo
	PatientOtherCommonInfoDetial = PatientOtherCommonInfo.objects.filter(patient_id=id).select_related("direct_sequencing_1","direct_sequencing_2","direct_sequencing_3","direct_sequencing_4","direct_sequencing_5","targt_enrichment_ngs_panel_1","targt_enrichment_ngs_panel_analysis_1","targt_enrichment_ngs_panel_2","targt_enrichment_ngs_panel_analysis_2","targt_enrichment_ngs_panel_3","targt_enrichment_ngs_panel_analysis_3","targt_enrichment_ngs_panel_4","targt_enrichment_ngs_panel_analysis_4","targt_enrichment_ngs_panel_5","targt_enrichment_ngs_panel_analysis_5","targt_exome_sequencing_1","targt_exome_sequencing_analysis_1","targt_exome_sequencing_2","targt_exome_sequencing_analysis_2","exome_sequencing_1","exome_sequencing_analysis_1","whole_exome_sequencing_1","whole_exome_sequencing_analysis_1","sequencing_other_collaborators_1","sequencing_other_collaborators_analysis_1","sequencing_other_collaborators_2","sequencing_other_collaborators_analysis_2","beadarray_platform_1","beadarray_platform_analysis_1","other_sequencing","mitochondria_ngs_whole_gene_sequence_1","mitochondria_ngs_whole_gene_sequence_analysis_1","targt_mitochondrial_sequence_2","targt_mitochondrial_sequence_analysis_2","targt_mitochondrial_hot_spot_panel_sequence_3","targt_mitochondrial_hot_spot_panel_sequence_analysis_3","other_analysis").first()
	####PatientOtherCommonInfo



	PatientCausativeGeneInfo1	=	PatientCausativeGeneInfo.objects.filter(patient_id=id).all()
	if PatientCausativeGeneInfo1:
		for PatientCausativeGeneInfoData in PatientCausativeGeneInfo1:
			PatientCausativeGeneInfoData.leftAddMore		=	PatientCausativeGeneInfoEthnicity.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()
			PatientCausativeGeneInfoData.rightAddMore		=	PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()

	#return HttpResponse(PatientCausativeGeneInfo1[0].rightAddMore)

	context		=	{
		"PatientCausativeGeneInfo1":PatientCausativeGeneInfo1,
		"step4_images_name_list_all":step4_images_name_list_all,
		"PatientGeneralInfoMultiVisitOphthalmologyImagesInfo":PatientGeneralInfoMultiVisitOphthalmologyImagesInfo,
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial,
		"PatientGeneralInfoOphthalmologyInfo":PatientGeneralInfoOphthalmologyInfo,
		"PatientOtherUncommonInfoOphthalmologyInfo":PatientOtherUncommonInfoOphthalmologyInfo,
		"PatientOtherMultiVisitImagesInfo":PatientOtherMultiVisitImagesInfo,
		#"PatientGeneralInfoMultiVisitInfo":PatientGeneralInfoMultiVisitInfo,
		#"PatientGeneralInfoMultiVisitOphthalmologyAiInfo":PatientGeneralInfoMultiVisitOphthalmologyAiInfo,
		"PatientOtherCommonInfoDetial":PatientOtherCommonInfoDetial,
		## PatientGeneralInfoMultiVisit fields for step 1 22-12-2018
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
		"assignedDiseases":assignedDiseases,
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
		"PatientGeneralInfoOphthalmologySystAbnormalityInfo":PatientGeneralInfoOphthalmologySystAbnormalityInfo,
		"PatientGeneralInfoOphthalmologyOcularCompliInfo":PatientGeneralInfoOphthalmologyOcularCompliInfo,
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

	AllPatientCausativeGeneInfo = PatientCausativeGeneInfo.objects.filter(patient_id=id).all()
	for data in AllPatientCausativeGeneInfo:
		PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_causative_gene_info_id=data.id).all().delete()
		PatientCausativeGeneInfoEthnicity.objects.filter(patient_causative_gene_info_id=data.id).all().delete()

	PatientGeneralInfoOphthalmologySystAbnormality.objects.filter(patient_id=id).all().delete()
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

	messages.success(request,"Patient has been deleted successfully.")
	return redirect('/ophthalmology/')
	
@login_required(login_url='/')
def delete_all_patient_data(request):
	##return HttpResponse(id)
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute("TRUNCATE TABLE patient_causative_gene_info_local_population")
	cursor.execute("TRUNCATE TABLE patient_causative_gene_info_ethnicity")
	cursor.execute("TRUNCATE TABLE patient_general_info_ophthalmology_syst_abnormality")
	cursor.execute("TRUNCATE TABLE patient_general_info_ophthalmology_ocular_compli")
	cursor.execute("TRUNCATE TABLE patient_general_info_family")
	cursor.execute("TRUNCATE TABLE patient_general_info_multi_visit")
	cursor.execute("TRUNCATE TABLE patient_general_info_multi_visit_ophthalmology")
	cursor.execute("TRUNCATE TABLE patient_other_uncommon_info_ophthalmology")
	cursor.execute("TRUNCATE TABLE patient_other_common_info")
	cursor.execute("TRUNCATE TABLE patient_general_info_multi_visit_ophthalmology_ai")
	cursor.execute("TRUNCATE TABLE patient_general_info_ophthalmology")
	cursor.execute("TRUNCATE TABLE patient_causative_gene_info")
	cursor.execute("TRUNCATE TABLE patient_other_multi_visit_images")
	cursor.execute("TRUNCATE TABLE patient_general_info_multi_visit_ophthalmology_images")
	cursor.execute("TRUNCATE TABLE patient_general_info")
	messages.success(request,"All Patients has been deleted successfully.")
	return redirect('/ophthalmology/')

@login_required(login_url='/')
def change_status(request,id,status):
	##return HttpResponse(id)

	PatientGeneralInfoDetail = PatientGeneralInfo.objects.get(id=id)
	PatientGeneralInfoDetail.is_draft =  status
	PatientGeneralInfoDetail.save()
	messages.success(request,"Status has been changed successfully.")
	return redirect('/ophthalmology/')

@login_required(login_url='/admin/login/')
def view_profile(request):
	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					#print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data

	instituteDetail				=	DoctorInstitute.objects.filter(user_id=request.user.id).first()
	whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
	which_doctor_document_can_see		=	[]

	#return HttpResponse(request.user.is_superuser)
	if request.user.is_superuser != 1:
		if whichDoctorDocumentCanSee:
			which_doctor_document_can_see	=	whichDoctorDocumentCanSee.doctor.values("username")
	else:
		which_doctor_document_can_see		=	User.objects.filter(~Q(id=request.user.id)).values("username")


	context		=	{
		"instituteDetail":instituteDetail,
		"assignedDiseases":assignedDiseases,
		"which_doctor_document_can_see":which_doctor_document_can_see
	}
	return render(request,"ophthalmology/view_profile.html",context)

@login_required(login_url='/')
def edit_new_patient(request,id):
	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data

	#set permission doctor has access or not
	record = PatientGeneralInfo.objects.filter(id=id).first()
	if not record:
		return redirect('/ophthalmology/')

	if request.user.is_superuser != 1:
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) & (Q(id=id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).first()
		if not PatientGeneralInfoDetial:
			return redirect('/ophthalmology/')
	#set permission doctor has access or not






	step_images_name_list_right	=	["corn_phot_right","corn_phot_on_fluor_right","corn_topography_right","corn_endotherial_photy_right","opt_cohe_tomo_of_anterior_segment_right","ax_length_right","lens_phot_right","fund_phot_wide_field_right","fund_autoflu_right","fund_autoflu_wide_field_right","infra_imaging_right","infra_imaging_wide_field_right","fluor_angi_right","fluor_angi_wide_field_right","indo_green_angi_right","indo_green_angi_wide_field_right","opt_cohe_tomo_disc_right","opt_cohe_tomo_macula_line_right","opt_cohe_tomo_macula_3d_right","opt_cohe_tomo_macula_en_face_right","opt_cohe_tomo_angi_right","adap_optic_imaging_right","full_field_elect_right","mult_elect_right","focal_macu_elect_right","patt_elect_right","patt_visual_evoked_potential_right","flash_visual_evoked_potential_right","pupilometry_right","dark_adaptmetry_right","kine_visual_field_test_right","static_visual_field_test_right","microperimetry_right","color_vision_test_right","image_others"]

	step_images_name_list_left	=	["corn_phot_left","corn_phot_on_fluor_left","corn_topography_left","corn_endotherial_photy_left","opt_cohe_tomo_of_anterior_segment_left","ax_length_left","lens_phot_left","fund_phot_wide_field_left","fund_autoflu_left","fund_autoflu_wide_field_left","infra_imaging_left","infra_imaging_wide_field_left","fluor_angi_left","fluor_angi_wide_field_left","indo_green_angi_left","indo_green_angi_wide_field_left","opt_cohe_tomo_disc_left","opt_cohe_tomo_macula_line_left","opt_cohe_tomo_macula_3d_left","opt_cohe_tomo_macula_en_face_left","opt_cohe_tomo_angi_left","adap_optic_imaging_left","full_field_elect_left","mult_elect_left","focal_macu_elect_left","patt_elect_left","patt_visual_evoked_potential_left","flash_visual_evoked_potential_left","pupilometry_left","dark_adaptmetry_left","kine_visual_field_test_left","static_visual_field_test_left","microperimetry_left","color_vision_test_left","image_comments"]

	step_other_multi_visit_images_right	=	["fund_phot_right","corn_phot_ai_diag_corn_dise_right","corn_phot_on_fluo_ai_diag_corn_dise_right","fund_phot_ai_diag_glau_right","opti_cohe_tomo_disc_ai_diag_glau_right","stat_visual_field_ai_diag_glau_right","fund_phot_ai_diag_diab_retino_right","fluo_angio_ai_diag_diaet_retino_right","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right","fund_phot_ai_diag_age_rela_macu_dege_right","fluo_angio_ai_diag_age_rela_macu_dege_right","indocy_green_angio_ai_diag_age_rela_macu_dege_right","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right","fund_phot_ai_diag_inher_reti_dise_right","fund_autofluo_wide_field_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right","full_field_elect_ai_diag_inher_reti_dise_right","multifocal_elect_ai_diag_inher_reti_dise_right","vcf_files_ai_diag_inher_reti_dise_right","others_ai_diag_right"]

	step_other_multi_visit_images_left	=	["fund_phot_left","corn_phot_ai_diag_corn_dise_left","corn_phot_on_fluo_ai_diag_corn_dise_left","fund_phot_ai_diag_glau_left","opti_cohe_tomo_disc_ai_diag_glau_left","stat_visual_field_ai_diag_glau_left","fund_phot_ai_diag_diab_retino_left","fluo_angio_ai_diag_diaet_retino_left","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left","fund_phot_ai_diag_age_rela_macu_dege_left","fluo_angio_ai_diag_age_rela_macu_dege_left","indocy_green_angio_ai_diag_age_rela_macu_dege_left","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left","fund_phot_ai_diag_inher_reti_dise_left","fund_autofluo_wide_field_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left","full_field_elect_ai_diag_inher_reti_dise_left","multifocal_elect_ai_diag_inher_reti_dise_left","vcf_files_ai_diag_inher_reti_dise_left","others_ai_diag_left"]

	multi_visit_ophthalmology_ai_static	=	["ai_diag_corn_dise_corn_phot_right","ai_accu_corn_diag_corn_phot_right_per","ai_diag_corn_dise_corn_phot_left","ai_accu_corn_diag_corn_phot_left_per","ai_diag_corn_dise_corn_phot_on_fluo_right","ai_accu_corn_diag_corn_phot_on_fluo_right_per","ai_diag_corn_dise_corn_phot_on_fluo_left","ai_accu_corn_diag_corn_phot_on_fluo_left_per","ai_diag_glau_fundus_phot_right","ai_accu_glau_fundus_phot_right_per","ai_diag_glau_fundus_phot_left","ai_accu_glau_fundus_phot_left_per","ai_diag_glau_opti_cohe_tomo_disc_right","ai_accu_glau_opti_cohe_tomo_disc_right_per","ai_diag_glau_opti_cohe_tomo_disc_left","ai_accu_glau_opti_cohe_tomo_disc_left_per","ai_diag_glau_static_perimetry_right","ai_accu_glau_static_perimetry_right_per","ai_diag_glau_static_visual_field_left","ai_accu_glau_static_visual_field_left_per","ai_diag_diab_retino_fundus_phot_right","ai_accu_diab_retino_fundus_phot_right_per","ai_diag_diab_retino_fundus_phot_left","ai_accu_diab_retino_fundus_phot_left_per","ai_diag_diab_retino_fluo_angio_right","ai_accu_diab_retino_fluo_angio_right_per","ai_diagnsis_diab_retino_fluo_angio_left","ai_accu_diab_retino_fluo_angio_left_per","ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right","ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per","ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left","ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per","ai_diag_age_relat_macu_degen_fundus_phot_right","ai_accu_age_relat_macu_degen_fundus_phot_right_per","ai_diag_age_relat_macu_degen_fundus_phot_left","ai_accu_age_relat_macu_degen_fundus_phot_left_per","ai_diag_age_relat_macu_degen_fluo_angio_right","ai_accu_age_relat_macu_degen_fluo_angio_right_per","ai_diag_age_relat_macu_degen_fluo_angio_left","ai_accu_age_relat_macu_degen_fluo_angio_left_per","ai_diag_age_relat_macu_degen_indocy_green_angio_right","ai_accu_age_relat_macu_degen_indocy_green_angio_right_per","ai_diag_age_relat_macu_degen_indocy_green_angio_left","ai_accu_age_relat_macu_degen_indocy_green_angio_left_per","ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right","ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per","ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left","ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per","ai_diag_inheri_retin_dise_fundus_phot_right","ai_accu_inheri_retin_dise_fundus_phot_right_per","ai_diag_inheri_retin_dise_fundus_phot_left","ai_accu_inheri_retin_dise_fundus_phot_left_per","ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right","ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per","ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left","ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per","ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left","ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per","ai_diag_inheri_retin_dise_full_field_electroret_right","ai_accu_inheri_retin_dise_full_field_electroret_right_per","ai_diag_inheri_retin_dise_full_field_electroret_left","ai_accu_inheri_retin_dise_full_field_electroret_left_per","ai_diag_inheri_retin_dise_multifocal_electroret_right","ai_accu_inheri_retin_dise_multifocal_electroret_right_per","ai_diag_inheri_retin_dise_multifocal_electroret_left","ai_accu_inheri_retin_dise_multifocal_electroret_left_per","ai_diag_inheri_retin_dise_vcf_files_right","ai_accu_inheri_retin_dise_vcf_files_right_per","ai_diag_inheri_retin_dise_vcf_files_left","ai_accu_inheri_retin_dise_vcf_files_left_per"]

	## Save Updated data on edit Start
	if request.method	==	"POST":
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'ophthalmology/'+str(currentMonth)+str(currentYear)+"/"

		## Save Step 1 data start
		PatientInfo 				=   PatientGeneralInfo.objects.get(id=id)
		if request.method == 'POST' and len(request.FILES) != 0:
			if request.FILES.get("pedigree_chart"):
				myfile = request.FILES.get("pedigree_chart")
				fs = FileSystemStorage()
				filename = myfile.name.split(".")[0].lower()
				extension = myfile.name.split(".")[-1].lower()
				newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
				fs.save(user_folder+newfilename, myfile)
				pedigree_chart	=	str(currentMonth)+str(currentYear)+"/"+newfilename
				PatientInfo.pedigree_chart	=	pedigree_chart

		#return HttpResponse(request.POST["institute_id"])

		##PatientInfo					=	PatientGeneralInfo()


		

		

		if request.POST.get("patient_id"):
			PatientInfo.patient_id	=	request.POST["patient_id"]

		if request.POST.get("relationship_to_proband"):
			PatientInfo.relationship_to_proband_id	=	request.POST["relationship_to_proband"]

		if request.POST.get("relationship_to_proband_other"):
			PatientInfo.relationship_to_proband_other	=	request.POST["relationship_to_proband_other"]

		if request.POST.get("birth_year_month"):
			PatientInfo.birth_year_month	=	request.POST["birth_year_month"]

		if request.POST.get("sex"):
			PatientInfo.sex_id	=	request.POST["sex"]

		if request.POST.get("sex_other"):
			PatientInfo.sex_other	=	request.POST["sex_other"]

		if request.POST.get("registration_date"):
			PatientInfo.registration_date	=	request.POST["registration_date"]

		if request.POST.get("dna_sample_collection_date"):
			PatientInfo.dna_sample_collection_date	=	request.POST["dna_sample_collection_date"]

		if request.POST.get("disease"):
			PatientInfo.disease_id	=	request.POST["disease"]

		if request.POST.get("sub_disease"):
			PatientInfo.sub_disease_id	=	request.POST["sub_disease"]

		if request.POST.get("disease_other"):
			PatientInfo.disease_other	=	request.POST["disease_other"]

		if request.POST.get("affected"):
			PatientInfo.affected_id	=	request.POST["affected"]

		if request.POST.get("affected_other"):
			PatientInfo.affected_other	=	request.POST["affected_other"]

		#return HttpResponse(PatientInfo.affected_id)

		if request.POST.get("inheritance"):
			PatientInfo.inheritance_id	=	request.POST["inheritance"]

		if request.POST.get("inheritance_other"):
			PatientInfo.inheritance_other	=	request.POST["inheritance_other"]

		

		if request.POST.get("syndromic"):
			PatientInfo.syndromic_id	=	request.POST["syndromic"]

		if request.POST.get("syndromic_other"):
			PatientInfo.syndromic_other	=	request.POST["syndromic_other"]

		if request.POST.get("bilateral"):
			PatientInfo.bilateral_id	=	request.POST["bilateral"]

		if request.POST.get("bilateral_other"):
			PatientInfo.bilateral_other	=	request.POST["bilateral_other"]

		if request.POST.get("ocular_symptom_1"):
			PatientInfo.ocular_symptom_1_id	=	request.POST["ocular_symptom_1"]

		if request.POST.get("ocular_symptom_1_other"):
			PatientInfo.ocular_symptom_1_other	=	request.POST["ocular_symptom_1_other"]

		if request.POST.get("ocular_symptom_2"):
			PatientInfo.ocular_symptom_2_id	=	request.POST["ocular_symptom_2"]

		if request.POST.get("ocular_symptom_2_other"):
			PatientInfo.ocular_symptom_2_other	=	request.POST["ocular_symptom_2_other"]

		if request.POST.get("ocular_symptom_3"):
			PatientInfo.ocular_symptom_3_id	=	request.POST["ocular_symptom_3"]

		if request.POST.get("ocular_symptom_3_other"):
			PatientInfo.ocular_symptom_3_other	=	request.POST["ocular_symptom_3_other"]

		if request.POST.get("progression"):
			PatientInfo.progression_id	=	request.POST["progression"]

		if request.POST.get("progression_other"):
			PatientInfo.progression_other	=	request.POST["progression_other"]

		if request.POST.get("flactuation"):
			PatientInfo.flactuation_id	=	request.POST["flactuation"]

		if request.POST.get("flactuation_other"):
			PatientInfo.flactuation_other	=	request.POST["flactuation_other"]

		if request.POST.get("family_history"):
			PatientInfo.family_history_id	=	request.POST["family_history"]

		if request.POST.get("family_history_other"):
			PatientInfo.family_history_other	=	request.POST["family_history_other"]

		if request.POST.get("consanguineous"):
			PatientInfo.consanguineous_id	=	request.POST["consanguineous"]

		if request.POST.get("consanguineous_other"):
			PatientInfo.consanguineous_other	=	request.POST["consanguineous_other"]

		if request.POST.get("number_of_affected_members_in_the_same_pedigree"):
			PatientInfo.number_of_affected_members_in_the_same_pedigree_id	=	request.POST["number_of_affected_members_in_the_same_pedigree"]

		if request.POST.get("number_of_affected_members_in_the_same_pedigree_other"):
			PatientInfo.number_of_affected_members_in_the_same_pedigree_other	=	request.POST["number_of_affected_members_in_the_same_pedigree_other"]

		if request.POST.get("ethnicity"):
			PatientInfo.ethnicity_id	=	request.POST["ethnicity"]

		if request.POST.get("ethnicity_other"):
			PatientInfo.ethnicity_other	=	request.POST["ethnicity_other"]

		if request.POST.get("country_of_origine"):
			PatientInfo.country_of_origine_id	=	request.POST["country_of_origine"]

		if request.POST.get("country_of_origine_other"):
			PatientInfo.country_of_origine_other	=	request.POST["country_of_origine_other"]

		if request.POST.get("origin_prefecture_in_japan"):
			PatientInfo.origin_prefecture_in_japan_id	=	request.POST["origin_prefecture_in_japan"]

		if request.POST.get("origin_prefecture_in_japan_other"):
			PatientInfo.origin_prefecture_in_japan_other	=	request.POST["origin_prefecture_in_japan_other"]

		if request.POST.get("ethnic_of_father"):
			PatientInfo.ethnic_of_father_id	=	request.POST["ethnic_of_father"]

		if request.POST.get("ethnic_of_father_other"):
			PatientInfo.ethnic_of_father_other	=	request.POST["ethnic_of_father_other"]

		if request.POST.get("original_country_of_father"):
			PatientInfo.original_country_of_father_id	=	request.POST["original_country_of_father"]

		if request.POST.get("original_country_of_father_other"):
			PatientInfo.original_country_of_father_other	=	request.POST["original_country_of_father_other"]

		if request.POST.get("origin_of_father_in_japan"):
			PatientInfo.origin_of_father_in_japan_id	=	request.POST["origin_of_father_in_japan"]

		if request.POST.get("origin_of_father_in_japan_other"):
			PatientInfo.origin_of_father_in_japan_other	=	request.POST["origin_of_father_in_japan_other"]

		if request.POST.get("ethnic_of_mother"):
			PatientInfo.ethnic_of_mother_id	=	request.POST["ethnic_of_mother"]

		if request.POST.get("ethnic_of_mother_other"):
			PatientInfo.ethnic_of_mother_other	=	request.POST["ethnic_of_mother_other"]

		if request.POST.get("original_country_of_mother"):
			PatientInfo.original_country_of_mother_id	=	request.POST["original_country_of_mother"]

		if request.POST.get("original_country_of_mother_other"):
			PatientInfo.original_country_of_mother_other	=	request.POST["original_country_of_mother_other"]

		if request.POST.get("origin_of_mother_in_japan"):
			PatientInfo.origin_of_mother_in_japan_id	=	request.POST["origin_of_mother_in_japan"]

		if request.POST.get("origin_of_mother_in_japan_other"):
			PatientInfo.origin_of_mother_in_japan_other	=	request.POST["origin_of_mother_in_japan_other"]

		#if request.POST.get("registration"):
			#PatientInfo.registration	=	request.POST["registration"]

		if request.POST.get("gene_type"):
			PatientInfo.gene_type_id	=	request.POST["gene_type"]

		if request.POST.get("gene_type_other"):
			PatientInfo.gene_type_other	=	request.POST["gene_type_other"]

		if request.POST.get("family_history"):
			PatientInfo.family_history_id	=	request.POST["family_history"]

		if request.POST.get("family_history_other"):
			PatientInfo.family_history_other	=	request.POST["family_history_other"]

		if request.POST.get("inheritance_type"):
			PatientInfo.inheritance_type_id	=	request.POST["inheritance_type"]

		if request.POST.get("inheritance_type_other"):
			PatientInfo.inheritance_type_other	=	request.POST["inheritance_type_other"]

		if request.POST.get("mutation_type"):
			PatientInfo.mutation_type_id	=	request.POST["mutation_type"]

		if request.POST.get("mutation_type_other"):
			PatientInfo.mutation_type_other	=	request.POST["mutation_type_other"]

		if request.POST.get("gene_inheritance_mutation_comments"):
			PatientInfo.gene_inheritance_mutation_comments	=	request.POST["gene_inheritance_mutation_comments"]

		if request.POST.get("sequencing"):
			PatientInfo.sequencing_id	=	request.POST["sequencing"]

		if request.POST.get("sequencing_other"):
			PatientInfo.sequencing_other	=	request.POST["sequencing_other"]

		if request.POST.get("analysis"):
			PatientInfo.analysis_id	=	request.POST["analysis"]

		if request.POST.get("analysis_other"):
			PatientInfo.analysis_other	=	request.POST["analysis_other"]

		if request.POST.get("dna_extraction_process"):
			PatientInfo.dna_extraction_process_id	=	request.POST["dna_extraction_process"]

		if request.POST.get("dna_extraction_process_other"):
			PatientInfo.dna_extraction_process_other	=	request.POST["dna_extraction_process_other"]

		if request.POST.get("overall_comments"):
			PatientInfo.overall_comments	=	request.POST["overall_comments"]





		PatientInfo.is_draft		=	request.POST["is_draft"]
		PatientInfo.user_id			=	request.user.id
		PatientInfo.save()
		lastPatientId		=	PatientInfo.id

		


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

						if fromData in dic["generalInfoMultiVisit"] and key+"_id" in dic["generalInfoMultiVisit"][fromData]:
							entryID			=	dic["generalInfoMultiVisit"][fromData][key+"_id"]
						else:
							entryID			=	""

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

							if entryID:
								PatientGeneralInfoMultiVisitInfo					=	PatientGeneralInfoMultiVisit.objects.get(id=entryID)
							else:
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
							
		#### save data in patientCausativeGeneInfo model in step 5 ####
		dic = {}
		for k in request.POST.keys():
			if k.startswith("patientCausativeGeneInfo"):
				rest = k[len("patientCausativeGeneInfo"):]
				full_field_name		=	k.split('__')
				field_name_1	=	full_field_name[0]
				field_name_2	=	full_field_name[2]
				field_name_3	=	full_field_name[1]
				if field_name_3 == "freq_ethnicity_per" or field_name_3 == "freq_ethnicity" or field_name_3 == "freq_ethnicity_other" or field_name_3 == "freq_ethnicity_id" or field_name_3 == "freq_local_population_other" or field_name_3 == "freq_local_population" or field_name_3 == "freq_local_population_per" or field_name_3 == "freq_local_population_id":
					field_name_4	=	full_field_name[3]
				else:
					field_name_4	=	""



				if field_name_1 not in dic:
					dic[field_name_1]								=	{}

				if field_name_2 not in dic[field_name_1]:
					dic[field_name_1][field_name_2]					=	{}

				if "addmore_left" not in dic[field_name_1][field_name_2]:
					dic[field_name_1][field_name_2]["addmore_left"]		=	{}

				if "addmore_right" not in dic[field_name_1][field_name_2]:
					dic[field_name_1][field_name_2]["addmore_right"]		=	{}

				if field_name_3 == "freq_ethnicity_per" or field_name_3 == "freq_ethnicity" or field_name_3 == "freq_ethnicity_other" or field_name_3 == "freq_ethnicity_id":
					if field_name_4 not in dic[field_name_1][field_name_2]["addmore_left"]:
						dic[field_name_1][field_name_2]["addmore_left"][field_name_4]				=	{}

					dic[field_name_1][field_name_2]["addmore_left"][field_name_4][field_name_3]		=	request.POST.get(k)
				elif field_name_3 == "freq_local_population" or field_name_3 == "freq_local_population_per" or field_name_3 == "freq_local_population_other" or field_name_3 == "freq_local_population_id":
					if field_name_4 not in dic[field_name_1][field_name_2]["addmore_right"]:
						dic[field_name_1][field_name_2]["addmore_right"][field_name_4]				=	{}

					dic[field_name_1][field_name_2]["addmore_right"][field_name_4][field_name_3]		=	request.POST.get(k)
				else:
					dic[field_name_1][field_name_2][field_name_3]		=	request.POST.get(k)






		if dic["patientCausativeGeneInfo"]:
			is_not_empty = 0
			for fromData in dic["patientCausativeGeneInfo"]:
				if fromData in dic["patientCausativeGeneInfo"] and "type_old_new" in dic["patientCausativeGeneInfo"][fromData]:
					type_old_new		=	dic["patientCausativeGeneInfo"][fromData]["type_old_new"]
					is_not_empty = 1
				else:
					type_old_new		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "type_old_new_other" in dic["patientCausativeGeneInfo"][fromData]:
					type_old_new_other		=	dic["patientCausativeGeneInfo"][fromData]["type_old_new_other"]
				else:
					type_old_new_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand"]
					is_not_empty = 1
				else:
					caus_cand		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_other" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_other		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_other"]
				else:
					caus_cand_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_gene" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_gene		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_gene"]
					is_not_empty = 1
				else:
					caus_cand_gene		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "disease_caus_cand_gene" in dic["patientCausativeGeneInfo"][fromData]:
					disease_caus_cand_gene		=	dic["patientCausativeGeneInfo"][fromData]["disease_caus_cand_gene"]
					is_not_empty = 1
				else:
					disease_caus_cand_gene		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_gene_other" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_gene_other		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_gene_other"]
				else:
					caus_cand_gene_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "chromosome" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome		=	dic["patientCausativeGeneInfo"][fromData]["chromosome"]
					is_not_empty = 1
				else:
					chromosome		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "chromosome_other" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome_other		=	dic["patientCausativeGeneInfo"][fromData]["chromosome_other"]
				else:
					chromosome_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "chromosome_comment" in dic["patientCausativeGeneInfo"][fromData]:
					chromosome_comment		=	dic["patientCausativeGeneInfo"][fromData]["chromosome_comment"]
					is_not_empty = 1
				else:
					chromosome_comment		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "position" in dic["patientCausativeGeneInfo"][fromData]:
					position		=	dic["patientCausativeGeneInfo"][fromData]["position"]
					is_not_empty = 1
				else:
					position		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "transcript" in dic["patientCausativeGeneInfo"][fromData]:
					transcript		=	dic["patientCausativeGeneInfo"][fromData]["transcript"]
					is_not_empty = 1
				else:
					transcript		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "exon" in dic["patientCausativeGeneInfo"][fromData]:
					exon		=	dic["patientCausativeGeneInfo"][fromData]["exon"]
					is_not_empty = 1
				else:
					exon		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "exon_other" in dic["patientCausativeGeneInfo"][fromData]:
					exon_other		=	dic["patientCausativeGeneInfo"][fromData]["exon_other"]
				else:
					exon_other		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "exon_comment" in dic["patientCausativeGeneInfo"][fromData]:
					exon_comment		=	dic["patientCausativeGeneInfo"][fromData]["exon_comment"]
					is_not_empty = 1
				else:
					exon_comment		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_mutation_nucleotide_amino_acid" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_mutation_nucleotide_amino_acid		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_mutation_nucleotide_amino_acid"]
					is_not_empty = 1
				else:
					caus_cand_mutation_nucleotide_amino_acid		=	""

				if fromData in dic["patientCausativeGeneInfo"] and "caus_cand_mutation_nucleotide_amino_acid_comment" in dic["patientCausativeGeneInfo"][fromData]:
					caus_cand_mutation_nucleotide_amino_acid_comment		=	dic["patientCausativeGeneInfo"][fromData]["caus_cand_mutation_nucleotide_amino_acid_comment"]
					is_not_empty = 1
				else:
					caus_cand_mutation_nucleotide_amino_acid_comment		=	""
					
				if fromData in dic["patientCausativeGeneInfo"] and "id" in dic["patientCausativeGeneInfo"][fromData]:
					entryID		=	dic["patientCausativeGeneInfo"][fromData]["id"]
				else:
					entryID		=	""
				latTableId = ''
				if type_old_new or caus_cand or caus_cand_gene or disease_caus_cand_gene or chromosome or chromosome_comment or position or transcript or exon or exon_comment or caus_cand_mutation_nucleotide_amino_acid or caus_cand_mutation_nucleotide_amino_acid_comment:
					if entryID:
						PatientCausativeGeneInfoInfo		=	PatientCausativeGeneInfo.objects.get(id=entryID)
					else:
						PatientCausativeGeneInfoInfo		=	PatientCausativeGeneInfo()
					
					PatientCausativeGeneInfoInfo.patient_id							=	lastPatientId
					PatientCausativeGeneInfoInfo.type_old_new_id					=	type_old_new
					PatientCausativeGeneInfoInfo.type_old_new_other					=	type_old_new_other
					PatientCausativeGeneInfoInfo.caus_cand_id						=	caus_cand
					PatientCausativeGeneInfoInfo.caus_cand_other					=	caus_cand_other
					PatientCausativeGeneInfoInfo.caus_cand_gene_id					=	caus_cand_gene
					PatientCausativeGeneInfoInfo.disease_caus_cand_gene_id					=	disease_caus_cand_gene
					PatientCausativeGeneInfoInfo.caus_cand_gene_other				=	caus_cand_gene_other
					PatientCausativeGeneInfoInfo.chromosome_id						=	chromosome
					PatientCausativeGeneInfoInfo.chromosome_other					=	chromosome_other
					PatientCausativeGeneInfoInfo.chromosome_comment					=	chromosome_comment
					PatientCausativeGeneInfoInfo.position							=	position
					PatientCausativeGeneInfoInfo.transcript							=	transcript
					PatientCausativeGeneInfoInfo.exon_id							=	exon
					PatientCausativeGeneInfoInfo.exon_other							=	exon_other
					PatientCausativeGeneInfoInfo.exon_comment						=	exon_comment
					PatientCausativeGeneInfoInfo.caus_cand_mutation_nucleotide_amino_acid	=	caus_cand_mutation_nucleotide_amino_acid
					PatientCausativeGeneInfoInfo.caus_cand_mutation_nucleotide_amino_acid_comment	=	caus_cand_mutation_nucleotide_amino_acid_comment
					PatientCausativeGeneInfoInfo.save()

					latTableId	=	PatientCausativeGeneInfoInfo.id
				if latTableId :
					for fromData2 in dic["patientCausativeGeneInfo"][fromData]["addmore_left"]:
						freq_ethnicity			=	""
						freq_ethnicity_per		=	""
						freq_ethnicity_other	=	""
						freq_ethnicity_id_old	=	""

						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity"]:
							freq_ethnicity	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_per"]:
							freq_ethnicity_per	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_per"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_other"]:
							freq_ethnicity_other	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_other"]
							
						if dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_id"]:
							freq_ethnicity_id_old	=	dic["patientCausativeGeneInfo"][fromData]["addmore_left"][fromData2]["freq_ethnicity_id"]

						
						
						if freq_ethnicity_id_old:
							PatientCausativeGeneInfoEthnicityInfo		=	PatientCausativeGeneInfoEthnicity.objects.get(id=freq_ethnicity_id_old)
						else:
							PatientCausativeGeneInfoEthnicityInfo		=	PatientCausativeGeneInfoEthnicity()
							
						PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_per					=	freq_ethnicity_per
						PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_id						=	freq_ethnicity
						PatientCausativeGeneInfoEthnicityInfo.freq_ethnicity_other					=	freq_ethnicity_other
						PatientCausativeGeneInfoEthnicityInfo.patient_causative_gene_info_id		=	latTableId
						PatientCausativeGeneInfoEthnicityInfo.save()

					for fromData2 in dic["patientCausativeGeneInfo"][fromData]["addmore_right"]:
						freq_local_population			=	""
						freq_local_population_per		=	""
						freq_local_population_other	=	""
						freq_local_population_id_old	=	""

						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population"]:
							freq_local_population	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_per"]:
							freq_local_population_per	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_per"]

						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_other"]:
							freq_local_population_other	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_other"]
							
						if dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_id"]:
							freq_local_population_id_old	=	dic["patientCausativeGeneInfo"][fromData]["addmore_right"][fromData2]["freq_local_population_id"]

						if freq_local_population_id_old:
							PatientCausativeGeneInfoLocalPopulationInfo		=	PatientCausativeGeneInfoLocalPopulation.objects.get(id=freq_local_population_id_old)
						else:
							PatientCausativeGeneInfoLocalPopulationInfo =	PatientCausativeGeneInfoLocalPopulation()
						
						
						PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_per		=	freq_local_population_per
						PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_id		=	freq_local_population
						PatientCausativeGeneInfoLocalPopulationInfo.freq_local_population_other	=	freq_local_population_other
						PatientCausativeGeneInfoLocalPopulationInfo.patient_causative_gene_info_id =	latTableId
						PatientCausativeGeneInfoLocalPopulationInfo.save()

		#### save data in PatientCausativeGeneInfo model in step 5 ####

		## Save Step 1 data end
		## Save Step 2 data start
		PatientOtherCommonInfoDetial 												=   PatientOtherCommonInfo.objects.filter(patient_id=id).first()
		if(not PatientOtherCommonInfoDetial):
			PatientOtherCommonInfoDetial										=	PatientOtherCommonInfo()
			PatientOtherCommonInfoDetial.patient_id								=	id
		
		PatientOtherCommonInfoDetial.direct_sequencing_1_id							=	request.POST.get("direct_sequencing_1","")
		PatientOtherCommonInfoDetial.direct_sequencing_1_other						=	request.POST.get("direct_sequencing_1_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_2_id							=	request.POST.get("direct_sequencing_2","")
		PatientOtherCommonInfoDetial.direct_sequencing_2_other						=	request.POST.get("direct_sequencing_2_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_3_id							=	request.POST.get("direct_sequencing_3","")
		PatientOtherCommonInfoDetial.direct_sequencing_3_other						=	request.POST.get("direct_sequencing_3_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_4_id							=	request.POST.get("direct_sequencing_4","")
		PatientOtherCommonInfoDetial.direct_sequencing_4_other						=	request.POST.get("direct_sequencing_4_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_5_id							=	request.POST.get("direct_sequencing_5","")
		PatientOtherCommonInfoDetial.direct_sequencing_5_other						=	request.POST.get("direct_sequencing_5_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_id				=	request.POST.get("targt_enrichment_ngs_panel_1","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_other				=	request.POST.get("targt_enrichment_ngs_panel_1_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_id		=	request.POST.get("targt_enrichment_ngs_panel_analysis_1","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_id				=	request.POST.get("targt_enrichment_ngs_panel_2","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_other				=	request.POST.get("targt_enrichment_ngs_panel_2_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_id		=	request.POST.get("targt_enrichment_ngs_panel_analysis_2","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_2_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_id				=	request.POST.get("targt_enrichment_ngs_panel_3","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_other				=	request.POST.get("targt_enrichment_ngs_panel_3_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_id		=	request.POST.get("targt_enrichment_ngs_panel_analysis_3","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_3_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_id				=	request.POST.get("targt_enrichment_ngs_panel_4","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_other				=	request.POST.get("targt_enrichment_ngs_panel_4_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_id		=	request.POST.get("targt_enrichment_ngs_panel_analysis_4","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_4_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_id				=	request.POST.get("targt_enrichment_ngs_panel_5","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_other				=	request.POST.get("targt_enrichment_ngs_panel_5_other","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_id		=	request.POST.get("targt_enrichment_ngs_panel_analysis_5","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_other	=	request.POST.get("targt_enrichment_ngs_panel_analysis_5_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_1_id					=	request.POST.get("targt_exome_sequencing_1","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_1_other					=	request.POST.get("targt_exome_sequencing_1_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other		=	request.POST.get("targt_exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_id			=	request.POST.get("targt_exome_sequencing_analysis_1","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other		=	request.POST.get("targt_exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_2_id					=	request.POST.get("targt_exome_sequencing_2","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_2_other					=	request.POST.get("targt_exome_sequencing_2_other","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_id			=	request.POST.get("targt_exome_sequencing_analysis_2","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_other		=	request.POST.get("targt_exome_sequencing_analysis_2_other","")
		PatientOtherCommonInfoDetial.exome_sequencing_1_id							=	request.POST.get("exome_sequencing_1","")
		PatientOtherCommonInfoDetial.exome_sequencing_1_other						=	request.POST.get("exome_sequencing_1_other","")
		PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_id					=	request.POST.get("exome_sequencing_analysis_1","")
		PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_other				=	request.POST.get("exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_1_id					=	request.POST.get("whole_exome_sequencing_1","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_1_other					=	request.POST.get("whole_exome_sequencing_1_other","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_id			=	request.POST.get("whole_exome_sequencing_analysis_1","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_other		=	request.POST.get("whole_exome_sequencing_analysis_1_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_id			=	request.POST.get("sequencing_other_collaborators_1","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_other			=	request.POST.get("sequencing_other_collaborators_1_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_id	=	request.POST.get("sequencing_other_collaborators_analysis_1","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_other =	request.POST.get("sequencing_other_collaborators_analysis_1_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_id			=	request.POST.get("sequencing_other_collaborators_2","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_other			=	request.POST.get("sequencing_other_collaborators_2_other","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_id	=	request.POST.get("sequencing_other_collaborators_analysis_2","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_other =	request.POST.get("sequencing_other_collaborators_analysis_2_other","")
		PatientOtherCommonInfoDetial.beadarray_platform_1_id						=	request.POST.get("beadarray_platform_1","")
		PatientOtherCommonInfoDetial.beadarray_platform_1_other						=	request.POST.get("beadarray_platform_1_other","")
		PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_id				=	request.POST.get("beadarray_platform_analysis_1","")
		PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_other			=	request.POST.get("beadarray_platform_analysis_1_other","")
		PatientOtherCommonInfoDetial.other_sequencing_id							=	request.POST.get("other_sequencing","")
		PatientOtherCommonInfoDetial.other_sequencing_other							=	request.POST.get("other_sequencing_other","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_id		=	request.POST.get("mitochondria_ngs_whole_gene_sequence_1","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_other	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_1_other","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_id	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_analysis_1","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_other	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_analysis_1_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_id				=	request.POST.get("targt_mitochondrial_sequence_2","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_other			=	request.POST.get("targt_mitochondrial_sequence_2_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_id		=	request.POST.get("targt_mitochondrial_sequence_analysis_2","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_other	=	request.POST.get("targt_mitochondrial_sequence_analysis_2_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_id	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_3","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_other =	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_3_other","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_id	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_analysis_3","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other","")
		PatientOtherCommonInfoDetial.other_analysis_id								=	request.POST.get("other_analysis","")
		PatientOtherCommonInfoDetial.other_analysis_other							=	request.POST.get("other_analysis_other","")
		PatientOtherCommonInfoDetial.direct_sequencing_1_comments					=	request.POST.get("direct_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_2_comments					=	request.POST.get("direct_sequencing_2_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_3_comments					=	request.POST.get("direct_sequencing_3_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_4_comments					=	request.POST.get("direct_sequencing_4_comments","")
		PatientOtherCommonInfoDetial.direct_sequencing_5_comments					=	request.POST.get("direct_sequencing_5_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_comments			=	request.POST.get("targt_enrichment_ngs_panel_1_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_1_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_comments			=	request.POST.get("targt_enrichment_ngs_panel_2_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_2_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_comments			=	request.POST.get("targt_enrichment_ngs_panel_3_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_3_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_comments			=	request.POST.get("targt_enrichment_ngs_panel_4_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_4_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_comments			=	request.POST.get("targt_enrichment_ngs_panel_5_comments","")
		PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_comments	=	request.POST.get("targt_enrichment_ngs_panel_analysis_5_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_1_comments				=	request.POST.get("targt_exome_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_comments		=	request.POST.get("targt_exome_sequencing_analysis_1_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_2_comments				=	request.POST.get("targt_exome_sequencing_2_comments","")
		PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_comments		=	request.POST.get("targt_exome_sequencing_analysis_2_comments","")
		PatientOtherCommonInfoDetial.exome_sequencing_1_comments					=	request.POST.get("exome_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_comments			=	request.POST.get("exome_sequencing_analysis_1_comments","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_1_comments				=	request.POST.get("whole_exome_sequencing_1_comments","")
		PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_comments		=	request.POST.get("whole_exome_sequencing_analysis_1_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_comments		=	request.POST.get("sequencing_other_collaborators_1_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_comments	=	request.POST.get("sequencing_other_collaborators_analysis_1_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_comments		=	request.POST.get("sequencing_other_collaborators_2_comments","")
		PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_comments	=	request.POST.get("sequencing_other_collaborators_analysis_2_comments","")
		PatientOtherCommonInfoDetial.beadarray_platform_1_comments					=	request.POST.get("beadarray_platform_1_comments","")
		PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_comments			=	request.POST.get("beadarray_platform_analysis_1_comments","")
		PatientOtherCommonInfoDetial.other_sequencing_comments	=	request.POST.get("other_sequencing_comments","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_comments	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_1_comments","")
		PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_comments	=	request.POST.get("mitochondria_ngs_whole_gene_sequence_analysis_1_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_comments	=	request.POST.get("targt_mitochondrial_sequence_2_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_comments	=	request.POST.get("targt_mitochondrial_sequence_analysis_2_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_comments	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_3_comments","")
		PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments	=	request.POST.get("targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments","")
		PatientOtherCommonInfoDetial.other_analysis_comments	=	request.POST.get("other_analysis_comments","")
		PatientOtherCommonInfoDetial.save()
		## Save Step 2 data end

		## Save Step 3 data start
		
		PatientGeneralInfoOphthalmologyInfo =   PatientGeneralInfoOphthalmology.objects.filter(patient_id=id).first()
		if(not PatientGeneralInfoOphthalmologyInfo):
			PatientGeneralInfoOphthalmologyInfo	=	PatientGeneralInfoOphthalmology()
			PatientGeneralInfoOphthalmologyInfo.patient_id								=	id
		

		if request.FILES.get("gene_middle_results"):
			myfile1 = request.FILES['gene_middle_results']
			fs = FileSystemStorage()
			filename = myfile1.name.split(".")[0].lower()
			extension = myfile1.name.split(".")[-1].lower()
			newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
			fs.save(user_folder+newfilename, myfile1)
			gene_middle_results	=	str(currentMonth)+str(currentYear)+"/"+newfilename
			PatientGeneralInfoOphthalmologyInfo.gene_middle_results			=	gene_middle_results

		if request.FILES.get('vcf_whole_exome_sequencing'):
			myfile2 = request.FILES['vcf_whole_exome_sequencing']
			fs = FileSystemStorage()
			filename = myfile2.name.split(".")[0].lower()
			extension = myfile2.name.split(".")[-1].lower()
			newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
			fs.save(user_folder+newfilename, myfile2)
			vcf_whole_exome_sequencing	=	str(currentMonth)+str(currentYear)+"/"+newfilename
			PatientGeneralInfoOphthalmologyInfo.vcf_whole_exome_sequencing	=	vcf_whole_exome_sequencing

		if request.FILES.get('vcf_whole_genome_sequencing'):
			myfile3 = request.FILES['vcf_whole_genome_sequencing']
			fs = FileSystemStorage()
			filename = myfile3.name.split(".")[0].lower()
			extension = myfile3.name.split(".")[-1].lower()
			newfilename = filename+str(int(datetime.datetime.now().timestamp()))+"."+extension
			fs.save(user_folder+newfilename, myfile3)
			vcf_whole_genome_sequencing	=	str(currentMonth)+str(currentYear)+"/"+newfilename
			PatientGeneralInfoOphthalmologyInfo.vcf_whole_genome_sequencing	=	vcf_whole_genome_sequencing

		if request.POST.get("ocul_surgeries_catrct_left"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_id	=	request.POST["ocul_surgeries_catrct_left"]

		if request.POST.get("ocul_surgeries_catrct_left_other"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other	=	request.POST["ocul_surgeries_catrct_left_other"]

		if request.POST.get("age_catrct_surgery_perf_left"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_id	=	request.POST["age_catrct_surgery_perf_left"]

		if request.POST.get("age_catrct_surgery_perf_left_other"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other	=	request.POST["age_catrct_surgery_perf_left_other"]

		if request.POST.get("no_catrct_surgery_perf_left"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_id	=	request.POST["no_catrct_surgery_perf_left"]

		if request.POST.get("no_catrct_surgery_perf_left_other"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other	=	request.POST["no_catrct_surgery_perf_left_other"]

		if request.POST.get("age_at_onset_of_ocul_symp"):
			PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_id	=	request.POST["age_at_onset_of_ocul_symp"]

		if request.POST.get("age_at_onset_of_ocul_symp_other"):
			PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other	=	request.POST["age_at_onset_of_ocul_symp_other"]

		if request.POST.get("age_at_the_init_diag"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_id	=	request.POST["age_at_the_init_diag"]

		if request.POST.get("age_at_the_init_diag_other"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other	=	request.POST["age_at_the_init_diag_other"]

		if request.POST.get("age_at_the_init_diag_clas"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_id	=	request.POST["age_at_the_init_diag_clas"]

		if request.POST.get("age_at_the_init_diag_clas_other"):
			PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other	=	request.POST["age_at_the_init_diag_clas_other"]

		if request.POST.get("ocul_surgeries_catrct_right"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_id	=	request.POST["ocul_surgeries_catrct_right"]
		else:
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_id	=	""

		if request.POST.get("ocul_surgeries_catrct_right_other"):
			PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other	=	request.POST["ocul_surgeries_catrct_right_other"]

		if request.POST.get("age_catrct_surgery_perf_right"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_id	=	request.POST["age_catrct_surgery_perf_right"]

		if request.POST.get("age_catrct_surgery_perf_right_other"):
			PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other	=	request.POST["age_catrct_surgery_perf_right_other"]

		if request.POST.get("no_catrct_surgery_perf_right"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_id	=	request.POST["no_catrct_surgery_perf_right"]

		if request.POST.get("no_catrct_surgery_perf_right_other"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other	=	request.POST["no_catrct_surgery_perf_right_other"]

		if request.POST.get("onset_of_diease_clas"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_id	=	request.POST["onset_of_diease_clas"]

		if request.POST.get("onset_of_diease_clas_other"):
			PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other	=	request.POST["onset_of_diease_clas_other"]

		if request.POST.get("gene_comments"):
			PatientGeneralInfoOphthalmologyInfo.gene_comments	=	request.POST["gene_comments"]


		PatientGeneralInfoOphthalmologyInfo.save()

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

		general_info_multi_visit_ophthalmology_static	=	["intra_ocul_pres_right","intra_ocul_pres_clas_right","intra_ocul_pres_left","intra_ocul_pres_clas_left","refr_error_sphe_equi_clas_right","refr_error_sphe_equi_left","refr_error_sphe_equi_right","refr_error_sphe_equi_clas_left","corn_thic_right","corn_thic_left","lens_right","lens_left","axia_leng_right","axia_leng_clas_right","axia_leng_left","axia_leng_clas_left","macu_thic_right","macu_edema_right","macu_schisis_right","epir_memb_right","sub_sensreti_fuild_right","sub_reti_epith_memb_fuild_right","macu_thic_left","macu_edema_left","macu_schisis_left","epir_memb_left","sub_sensreti_fuild_left","sub_reti_epith_memb_fuild_left","foveal_thic_right","foveal_thic_left","choro_thic_right","choro_thic_left","stat_peri_mean_sens_hfa24_2_right","stat_peri_mean_sens_clas_right","stat_peri_mean_sens_hfa24_2_left","stat_peri_mean_sens_clas_left","electro_right","full_field_electphysiol_clas_right","multi_electphysiol_clas_right","electroneg_config_of_dark_apa","electro_left","full_field_electphysiol_clas_left","multi_electphysiol_clas_left","ai_diagnosis_for_others_right","ai_accuracy_for_others_right_per","ai_diagnosis_for_others_left","ai_accuracy_for_others_left_per","ai_comments"]

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

						if fromData in dic["generalInfoMultiVisitOphthalmology"] and key+"_id" in dic["generalInfoMultiVisitOphthalmology"][fromData]:
							entryID			=	dic["generalInfoMultiVisitOphthalmology"][fromData][key+"_id"]
						else:
							entryID			=	""

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

							if entryID:
								PatientGeneralInfoMultiVisitOphthalmologyInfo		=	PatientGeneralInfoMultiVisitOphthalmology.objects.get(id=entryID)
							else:
								PatientGeneralInfoMultiVisitOphthalmologyInfo		=	PatientGeneralInfoMultiVisitOphthalmology()


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

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_other" in dic["systemicAbnormality"][fromData]:
					name_other		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_other"]
				else:
					name_other		=	""

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_comment" in dic["systemicAbnormality"][fromData]:
					name_comment		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_comment"]
				else:
					name_comment		=	""

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_date" in dic["systemicAbnormality"][fromData]:
					name_date		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_date"]
				else:
					name_date		=	""

				if fromData in dic["systemicAbnormality"] and "systemicAbnormality_name_id" in dic["systemicAbnormality"][fromData]:
					entryID		=	dic["systemicAbnormality"][fromData]["systemicAbnormality_name_id"]
				else:
					entryID		=	""

				if entryID:
					PatientGeneralInfoOphthalmologySystAbnormalityInfo		=	PatientGeneralInfoOphthalmologySystAbnormality.objects.get(id=entryID)
				else:
					PatientGeneralInfoOphthalmologySystAbnormalityInfo		=	PatientGeneralInfoOphthalmologySystAbnormality()
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.patient_id		=	lastPatientId
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.name_id			=	systemicAbnormality_name
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.comments			=	name_comment
				PatientGeneralInfoOphthalmologySystAbnormalityInfo.other			=	name_other
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

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_other" in dic["ocularSymptom"][fromData]:
					name_other		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_other"]
				else:
					name_other		=	""

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_comment" in dic["ocularSymptom"][fromData]:
					name_comment		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_comment"]
				else:
					name_comment		=	""

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_date" in dic["ocularSymptom"][fromData]:
					name_date		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_date"]
				else:
					name_date		=	""

				if fromData in dic["ocularSymptom"] and "ocularSymptom_name_id" in dic["ocularSymptom"][fromData]:
					entryID		=	dic["ocularSymptom"][fromData]["ocularSymptom_name_id"]
				else:
					entryID		=	""

				if entryID:
					PatientGeneralInfoOphthalmologyOcularCompliInfo		=	PatientGeneralInfoOphthalmologyOcularCompli.objects.get(id=entryID)
				else:
					PatientGeneralInfoOphthalmologyOcularCompliInfo		=	PatientGeneralInfoOphthalmologyOcularCompli()
				PatientGeneralInfoOphthalmologyOcularCompliInfo.patient_id			=	lastPatientId
				PatientGeneralInfoOphthalmologyOcularCompliInfo.name_id				=	ocularSymptom_name
				PatientGeneralInfoOphthalmologyOcularCompliInfo.comments			=	name_comment
				PatientGeneralInfoOphthalmologyOcularCompliInfo.other				=	name_other
				PatientGeneralInfoOphthalmologyOcularCompliInfo.date				=	name_date
				PatientGeneralInfoOphthalmologyOcularCompliInfo.save()
		## Save Step 3 data end

		## Save Step 4 data Start
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'ophthalmology/multi_visit_ophthalmology_images/'+str(currentMonth)+str(currentYear)+"/"

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

						if fromData in dic["multiVisitOphthalmologyImagesRight"] and key+"_id" in dic["multiVisitOphthalmologyImagesRight"][fromData]:
							entryID			=	dic["multiVisitOphthalmologyImagesRight"][fromData][key+"_id"]
						else:
							entryID			=	""

						if fullfilename:
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";



							if entryID:
								PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.get(id=entryID)
							else:
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

						if fromData in dic["multiVisitOphthalmologyImagesLeft"] and key+"_id" in dic["multiVisitOphthalmologyImagesLeft"][fromData]:
							entryID			=	dic["multiVisitOphthalmologyImagesLeft"][fromData][key+"_id"]
						else:
							entryID			=	""

						if fullfilename:
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";

							if entryID:
								PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.get(id=entryID)
							else:
								PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	PatientGeneralInfoMultiVisitOphthalmologyImages()
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.patient_id		=	lastPatientId
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.key				=	key
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.value			=	fullfilename
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_name		=	field_name
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.field_direction	=	field_direction
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.comments		=	comment
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.date			=	date
							PatientGeneralInfoMultiVisitOphthalmologyImagesInfo.save()
		## Save Step 4 data end

		## Save Step 5 data start
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

						if fromData in dic["multiVisitOphthalmologyAi"] and key+"_id" in dic["multiVisitOphthalmologyAi"][fromData]:
							entryID			=	dic["multiVisitOphthalmologyAi"][fromData][key+"_id"]
						else:
							entryID			=	""

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

							if entryID:
								PatientGeneralInfoMultiVisitOphthalmologyAiInfo			=	PatientGeneralInfoMultiVisitOphthalmologyAi.objects.get(id=entryID)
							else:
								PatientGeneralInfoMultiVisitOphthalmologyAiInfo			=	PatientGeneralInfoMultiVisitOphthalmologyAi()
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


		
		PatientOtherUncommonInfoOphthalmologyInfo =   PatientOtherUncommonInfoOphthalmology.objects.filter(patient_id=id).first()
		if(not PatientOtherUncommonInfoOphthalmologyInfo):
			PatientOtherUncommonInfoOphthalmologyInfo				=	PatientOtherUncommonInfoOphthalmology()
			PatientOtherUncommonInfoOphthalmologyInfo.patient_id	=	id
			
		if request.POST.get("ocul_surgeries_cornea_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_id	=	request.POST["ocul_surgeries_cornea_right"]

		if request.POST.get("ocul_surgeries_cornea_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other	=	request.POST["ocul_surgeries_cornea_right_other"]

		if request.POST.get("ocul_surgeries_cornea_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_id	=	request.POST["ocul_surgeries_cornea_left"]

		if request.POST.get("ocul_surgeries_cornea_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other	=	request.POST["ocul_surgeries_cornea_left_other"]

		if request.POST.get("age_corneal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_id	=	request.POST["age_corneal_surgery_perf_right"]

		if request.POST.get("age_corneal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other	=	request.POST["age_corneal_surgery_perf_right_other"]

		if request.POST.get("age_corneal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_id	=	request.POST["age_corneal_surgery_perf_left"]

		if request.POST.get("age_corneal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other	=	request.POST["age_corneal_surgery_perf_left_other"]

		if request.POST.get("no_corneal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_id	=	request.POST["no_corneal_surgery_perf_right"]

		if request.POST.get("no_corneal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other	=	request.POST["no_corneal_surgery_perf_right_other"]

		if request.POST.get("no_corneal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_id	=	request.POST["no_corneal_surgery_perf_left"]

		if request.POST.get("no_corneal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other	=	request.POST["no_corneal_surgery_perf_left_other"]

		if request.POST.get("ocul_surgeries_glaucoma_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_id	=	request.POST["ocul_surgeries_glaucoma_right"]

		if request.POST.get("ocul_surgeries_glaucoma_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other	=	request.POST["ocul_surgeries_glaucoma_right_other"]

		if request.POST.get("ocul_surgeries_glaucoma_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_id	=	request.POST["ocul_surgeries_glaucoma_left"]

		if request.POST.get("ocul_surgeries_glaucoma_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other	=	request.POST["ocul_surgeries_glaucoma_left_other"]

		if request.POST.get("age_glaucoma_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_id	=	request.POST["age_glaucoma_surgery_perf_right"]

		if request.POST.get("age_glaucoma_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other	=	request.POST["age_glaucoma_surgery_perf_right_other"]

		if request.POST.get("age_glaucoma_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_id	=	request.POST["age_glaucoma_surgery_perf_left"]

		if request.POST.get("age_glaucoma_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other	=	request.POST["age_glaucoma_surgery_perf_left_other"]

		if request.POST.get("no_glaucomal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_id	=	request.POST["no_glaucomal_surgery_perf_right"]

		if request.POST.get("no_glaucomal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other	=	request.POST["no_glaucomal_surgery_perf_right_other"]

		if request.POST.get("no_glaucomal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_id	=	request.POST["no_glaucomal_surgery_perf_left"]

		if request.POST.get("no_glaucomal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other	=	request.POST["no_glaucomal_surgery_perf_left_other"]

		if request.POST.get("ocul_surgeries_retina_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_id	=	request.POST["ocul_surgeries_retina_right"]

		if request.POST.get("ocul_surgeries_retina_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other	=	request.POST["ocul_surgeries_retina_right_other"]

		if request.POST.get("ocul_surgeries_retina_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_id	=	request.POST["ocul_surgeries_retina_left"]

		if request.POST.get("ocul_surgeries_retina_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other	=	request.POST["ocul_surgeries_retina_left_other"]

		if request.POST.get("age_vitreoretina_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_id	=	request.POST["age_vitreoretina_surgery_perf_right"]

		if request.POST.get("age_vitreoretina_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other	=	request.POST["age_vitreoretina_surgery_perf_right_other"]

		if request.POST.get("age_vitreoretina_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_id	=	request.POST["age_vitreoretina_surgery_perf_left"]

		if request.POST.get("age_vitreoretina_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other	=	request.POST["age_vitreoretina_surgery_perf_left_other"]

		if request.POST.get("no_vitreoretinal_surgery_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_id	=	request.POST["no_vitreoretinal_surgery_perf_right"]

		if request.POST.get("no_vitreoretinal_surgery_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other	=	request.POST["no_vitreoretinal_surgery_perf_right_other"]

		if request.POST.get("no_vitreoretinal_surgery_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_id	=	request.POST["no_vitreoretinal_surgery_perf_left"]

		if request.POST.get("no_vitreoretinal_surgery_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other	=	request.POST["no_vitreoretinal_surgery_perf_left_other"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_id	=	request.POST["age_ocul_surgeries_lasers_perf_right"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other	=	request.POST["age_ocul_surgeries_lasers_perf_right_other"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_id	=	request.POST["age_ocul_surgeries_lasers_perf_left"]

		if request.POST.get("age_ocul_surgeries_lasers_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other	=	request.POST["age_ocul_surgeries_lasers_perf_left_other"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_id	=	request.POST["no_ofocul_surgeries_lasers_perf_right"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other	=	request.POST["no_ofocul_surgeries_lasers_perf_right_other"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_id	=	request.POST["no_ofocul_surgeries_lasers_perf_left"]

		if request.POST.get("no_ofocul_surgeries_lasers_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other	=	request.POST["no_ofocul_surgeries_lasers_perf_left_other"]

		if request.POST.get("ocul_surgeries_lasers_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_id	=	request.POST["ocul_surgeries_lasers_right"]

		if request.POST.get("ocul_surgeries_lasers_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other	=	request.POST["ocul_surgeries_lasers_right_other"]

		if request.POST.get("ocul_surgeries_lasers_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_id	=	request.POST["ocul_surgeries_lasers_left"]

		if request.POST.get("ocul_surgeries_lasers_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other	=	request.POST["ocul_surgeries_lasers_left_other"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_id	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_right"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_right_other"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_id	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_left"]

		if request.POST.get("age_opht_medi_subtenon_subconj_injec_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other	=	request.POST["age_opht_medi_subtenon_subconj_injec_perf_left_other"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_id	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_right"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_right_other"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_id	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_left"]

		if request.POST.get("no_opht_medi_subtenon_subconj_injec_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other	=	request.POST["no_opht_medi_subtenon_subconj_injec_perf_left_other"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_id	=	request.POST["opht_medi_subtenon_subconj_injec_right"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other	=	request.POST["opht_medi_subtenon_subconj_injec_right_other"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_id	=	request.POST["opht_medi_subtenon_subconj_injec_left"]

		if request.POST.get("opht_medi_subtenon_subconj_injec_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other	=	request.POST["opht_medi_subtenon_subconj_injec_left_other"]

		if request.POST.get("ocul_medi_internal_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_id	=	request.POST["ocul_medi_internal_right"]

		if request.POST.get("ocul_medi_internal_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other	=	request.POST["ocul_medi_internal_right_other"]

		if request.POST.get("ocul_medi_internal_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_id	=	request.POST["ocul_medi_internal_left"]

		if request.POST.get("ocul_medi_internal_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other	=	request.POST["ocul_medi_internal_left_other"]

		if request.POST.get("age_ocul_medi_internal_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_id	=	request.POST["age_ocul_medi_internal_perf_right"]

		if request.POST.get("age_ocul_medi_internal_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other	=	request.POST["age_ocul_medi_internal_perf_right_other"]

		if request.POST.get("age_ocul_medi_internal_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_id	=	request.POST["age_ocul_medi_internal_perf_left"]

		if request.POST.get("age_ocul_medi_internal_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other	=	request.POST["age_ocul_medi_internal_perf_left_other"]

		if request.POST.get("no_ocul_medi_internal_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_id	=	request.POST["no_ocul_medi_internal_perf_right"]

		if request.POST.get("no_ocul_medi_internal_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other	=	request.POST["no_ocul_medi_internal_perf_right_other"]

		if request.POST.get("no_ocul_medi_internal_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_id	=	request.POST["no_ocul_medi_internal_perf_left"]

		if request.POST.get("no_ocul_medi_internal_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other	=	request.POST["no_ocul_medi_internal_perf_left_other"]

		if request.POST.get("ocul_medi_topical_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_id	=	request.POST["ocul_medi_topical_right"]

		if request.POST.get("ocul_medi_topical_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other	=	request.POST["ocul_medi_topical_right_other"]

		if request.POST.get("ocul_medi_topical_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_id	=	request.POST["ocul_medi_topical_left"]

		if request.POST.get("ocul_medi_topical_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other	=	request.POST["ocul_medi_topical_left_other"]

		if request.POST.get("age_ocul_medi_topical_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_id	=	request.POST["age_ocul_medi_topical_perf_right"]

		if request.POST.get("age_ocul_medi_topical_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other	=	request.POST["age_ocul_medi_topical_perf_right_other"]

		if request.POST.get("age_ocul_medi_topical_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_id	=	request.POST["age_ocul_medi_topical_perf_left"]

		if request.POST.get("age_ocul_medi_topical_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other	=	request.POST["age_ocul_medi_topical_perf_left_other"]

		if request.POST.get("no_ocul_medi_topical_perf_right"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_id	=	request.POST["no_ocul_medi_topical_perf_right"]

		if request.POST.get("no_ocul_medi_topical_perf_right_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other	=	request.POST["no_ocul_medi_topical_perf_right_other"]

		if request.POST.get("no_ocul_medi_topical_perf_left"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_id	=	request.POST["no_ocul_medi_topical_perf_left"]

		if request.POST.get("no_ocul_medi_topical_perf_left_other"):
			PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_other	=	request.POST["no_ocul_medi_topical_perf_left_other"]

		PatientOtherUncommonInfoOphthalmologyInfo.save()
		## Save Step 5 data end

		## Save Step 6 data start
		currentMonth = datetime.datetime.now().month
		currentYear = datetime.datetime.now().year
		user_folder = 'ophthalmology/multi_visit_ophthalmology_images/'+str(currentMonth)+str(currentYear)+"/"

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

						if fromData in dic["otherMultiVisitImagesLeft"] and key+"_id" in dic["otherMultiVisitImagesLeft"][fromData]:
							entryID			=	dic["otherMultiVisitImagesLeft"][fromData][key+"_id"]
						else:
							entryID			=	""

						if fullfilename:
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							if entryID:
								PatientOtherMultiVisitImagesInfo					=	PatientOtherMultiVisitImages.objects.get(id=entryID)
							else:
								PatientOtherMultiVisitImagesInfo					=	PatientOtherMultiVisitImages()

							PatientOtherMultiVisitImagesInfo.patient_id			=	lastPatientId
							PatientOtherMultiVisitImagesInfo.key				=	key
							PatientOtherMultiVisitImagesInfo.value				=	fullfilename
							PatientOtherMultiVisitImagesInfo.field_name			=	field_name
							PatientOtherMultiVisitImagesInfo.field_direction	=	field_direction
							PatientOtherMultiVisitImagesInfo.comments			=	comment
							PatientOtherMultiVisitImagesInfo.date				=	date
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

						if fromData in dic["otherMultiVisitImagesRight"] and key+"_id" in dic["otherMultiVisitImagesRight"][fromData]:
							entryID			=	dic["otherMultiVisitImagesRight"][fromData][key+"_id"]
						else:
							entryID			=	""

						if fullfilename:
							if "_left" in key:
								field_name			=	key.replace("_left","");
								field_direction		=	"left";
							else:
								field_name			=	key.replace("_right","");
								field_direction		=	"right";
							if entryID:
								PatientOtherMultiVisitImagesInfo	=	PatientOtherMultiVisitImages.objects.get(id=entryID)
							else:
								PatientOtherMultiVisitImagesInfo	=	PatientOtherMultiVisitImages()

							PatientOtherMultiVisitImagesInfo.patient_id			=	lastPatientId
							PatientOtherMultiVisitImagesInfo.key				=	key
							PatientOtherMultiVisitImagesInfo.value				=	fullfilename
							PatientOtherMultiVisitImagesInfo.field_name			=	field_name
							PatientOtherMultiVisitImagesInfo.field_direction 	=	field_direction
							PatientOtherMultiVisitImagesInfo.comments			=	comment
							PatientOtherMultiVisitImagesInfo.date				=	date
							PatientOtherMultiVisitImagesInfo.save()
		## Save Step 6 data end



		messages.success(request,"Patient has been updated successfully.")
		return redirect('/ophthalmology/')



	## Save Updated data on edit end


	PatientGeneralInfoDetial = PatientGeneralInfo.objects.filter(id=id).select_related("institute","relationship_to_proband","sex","disease","affected","inheritance","syndromic","bilateral","ocular_symptom_1","ocular_symptom_2","ocular_symptom_3","progression","flactuation","family_history","consanguineous","number_of_affected_members_in_the_same_pedigree","ethnicity","country_of_origine","origin_prefecture_in_japan","ethnic_of_father","original_country_of_father","origin_of_father_in_japan","ethnic_of_mother","original_country_of_mother","origin_of_mother_in_japan","gene_type","inheritance_type","mutation_type","dna_extraction_process","sequencing","analysis","sub_disease").first()

	family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial.id).values("family_id").first();
	if family_detail:
		PatientGeneralInfoDetial.family_id = family_detail["family_id"]
	else:
		PatientGeneralInfoDetial.family_id = ''

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

	##PatientGeneralInfoOphthalmologySystAbnormality
	PatientGeneralInfoOphthalmologySystAbnormalityInfo			=  PatientGeneralInfoOphthalmologySystAbnormality.objects.filter(patient_id=id).select_related("name").all()

	##PatientGeneralInfoOphthalmologyOcularCompli
	PatientGeneralInfoOphthalmologyOcularCompliInfo			=  PatientGeneralInfoOphthalmologyOcularCompli.objects.filter(patient_id=id).select_related("name").all()

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


	##PatientGeneralInfoMultiVisitOphthalmologyImages for step 4


	step4_images_name_list_all	=	["corn_phot_left","corn_phot_right","corn_phot_on_fluor_left","corn_phot_on_fluor_right","corn_topography_left","corn_topography_right","corn_endotherial_photy_left","corn_endotherial_photy_right","opt_cohe_tomo_of_anterior_segment_left","opt_cohe_tomo_of_anterior_segment_right","ax_length_left","ax_length_right","lens_phot_left","lens_phot_right","fund_phot_wide_field_left","fund_phot_wide_field_right","fund_autoflu_left","fund_autoflu_right","fund_autoflu_wide_field_left","fund_autoflu_wide_field_right","infra_imaging_left","infra_imaging_right","infra_imaging_wide_field_left","infra_imaging_wide_field_right","fluor_angi_left","fluor_angi_right","fluor_angi_wide_field_left","fluor_angi_wide_field_right","indo_green_angi_left","indo_green_angi_right","indo_green_angi_wide_field_left","indo_green_angi_wide_field_right","opt_cohe_tomo_disc_left","opt_cohe_tomo_disc_right","opt_cohe_tomo_macula_line_left","opt_cohe_tomo_macula_line_right","opt_cohe_tomo_macula_3d_left","opt_cohe_tomo_macula_3d_right","opt_cohe_tomo_macula_en_face_left","opt_cohe_tomo_macula_en_face_right","opt_cohe_tomo_angi_left","opt_cohe_tomo_angi_right","adap_optic_imaging_left","adap_optic_imaging_right","full_field_elect_left","full_field_elect_right","mult_elect_left","mult_elect_right","focal_macu_elect_left","focal_macu_elect_right","patt_elect_left","patt_elect_right","patt_visual_evoked_potential_left","patt_visual_evoked_potential_right","flash_visual_evoked_potential_left","flash_visual_evoked_potential_right","pupilometry_left","pupilometry_right","dark_adaptmetry_left","dark_adaptmetry_right","kine_visual_field_test_left","kine_visual_field_test_right","static_visual_field_test_left","static_visual_field_test_right","microperimetry_left","microperimetry_right","color_vision_test_left","color_vision_test_right","image_comments","image_others"]

	PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	{}
	if step4_images_name_list_all:
		for imageData in step4_images_name_list_all:
			imageData1		=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).filter(key=imageData).all()
			PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[imageData]	=	imageData1

	#return HttpResponse(PatientGeneralInfoMultiVisitOphthalmologyImagesInfo["corn_phot_left"][0].value)
	##PatientOtherMultiVisitImages for step6

	step_other_multi_visit_images_all	=	["fund_phot_left","fund_phot_right","corn_phot_ai_diag_corn_dise_left","corn_phot_ai_diag_corn_dise_right","corn_phot_on_fluo_ai_diag_corn_dise_left","corn_phot_on_fluo_ai_diag_corn_dise_right","fund_phot_ai_diag_glau_left","fund_phot_ai_diag_glau_right","opti_cohe_tomo_disc_ai_diag_glau_left","opti_cohe_tomo_disc_ai_diag_glau_right","stat_visual_field_ai_diag_glau_left","stat_visual_field_ai_diag_glau_right","fund_phot_ai_diag_diab_retino_left","fund_phot_ai_diag_diab_retino_right","fluo_angio_ai_diag_diaet_retino_left","fluo_angio_ai_diag_diaet_retino_right","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right","fund_phot_ai_diag_age_rela_macu_dege_left","fund_phot_ai_diag_age_rela_macu_dege_right","fluo_angio_ai_diag_age_rela_macu_dege_left","fluo_angio_ai_diag_age_rela_macu_dege_right","indocy_green_angio_ai_diag_age_rela_macu_dege_left","indocy_green_angio_ai_diag_age_rela_macu_dege_right","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right","fund_phot_ai_diag_inher_reti_dise_left","fund_phot_ai_diag_inher_reti_dise_right","fund_autofluo_wide_field_ai_diag_inher_reti_dise_left","fund_autofluo_wide_field_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right","full_field_elect_ai_diag_inher_reti_dise_left","full_field_elect_ai_diag_inher_reti_dise_right","multifocal_elect_ai_diag_inher_reti_dise_left","multifocal_elect_ai_diag_inher_reti_dise_right","vcf_files_ai_diag_inher_reti_dise_left","vcf_files_ai_diag_inher_reti_dise_right","others_ai_diag_left","others_ai_diag_right"]


	PatientOtherMultiVisitImagesInfo	=	{}
	if step_other_multi_visit_images_all:
		for imageData in step_other_multi_visit_images_all:
			imageData1		=	PatientOtherMultiVisitImages.objects.filter(patient_id=id).filter(key=imageData).all()
			PatientOtherMultiVisitImagesInfo[imageData]	=	imageData1


	####PatientOtherCommonInfo
	PatientOtherCommonInfoDetial = PatientOtherCommonInfo.objects.filter(patient_id=id).select_related("direct_sequencing_1","direct_sequencing_2","direct_sequencing_3","direct_sequencing_4","direct_sequencing_5","targt_enrichment_ngs_panel_1","targt_enrichment_ngs_panel_analysis_1","targt_enrichment_ngs_panel_2","targt_enrichment_ngs_panel_analysis_2","targt_enrichment_ngs_panel_3","targt_enrichment_ngs_panel_analysis_3","targt_enrichment_ngs_panel_4","targt_enrichment_ngs_panel_analysis_4","targt_enrichment_ngs_panel_5","targt_enrichment_ngs_panel_analysis_5","targt_exome_sequencing_1","targt_exome_sequencing_analysis_1","targt_exome_sequencing_2","targt_exome_sequencing_analysis_2","exome_sequencing_1","exome_sequencing_analysis_1","whole_exome_sequencing_1","whole_exome_sequencing_analysis_1","sequencing_other_collaborators_1","sequencing_other_collaborators_analysis_1","sequencing_other_collaborators_2","sequencing_other_collaborators_analysis_2","beadarray_platform_1","beadarray_platform_analysis_1","other_sequencing","mitochondria_ngs_whole_gene_sequence_1","mitochondria_ngs_whole_gene_sequence_analysis_1","targt_mitochondrial_sequence_2","targt_mitochondrial_sequence_analysis_2","targt_mitochondrial_hot_spot_panel_sequence_3","targt_mitochondrial_hot_spot_panel_sequence_analysis_3","other_analysis").first()
	####PatientOtherCommonInfo



	PatientCausativeGeneInfo1	=	PatientCausativeGeneInfo.objects.filter(patient_id=id).all()
	if PatientCausativeGeneInfo1:
		for PatientCausativeGeneInfoData in PatientCausativeGeneInfo1:
			PatientCausativeGeneInfoData.leftAddMore		=	PatientCausativeGeneInfoEthnicity.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()
			PatientCausativeGeneInfoData.rightAddMore		=	PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()

	#return HttpResponse(PatientCausativeGeneInfo1[0].rightAddMore)



	Institudes	=	InstituteDt.objects.order_by("-name").all()
	RelationshipToProbandDts	=	RelationshipToProbandDt.objects.order_by("-name").all()
	SexDts	=	SexDt.objects.order_by("-name").all()
	DiseaseDts	=	DiseaseDt.objects.order_by("-name").all()
	if PatientGeneralInfoDetial.disease:
		SubDiseaseDts	=	SubDiseaseDt.objects.filter(disease_id=PatientGeneralInfoDetial.disease.id).order_by("-name").all()
		DiseaseCausCandGeneDts	=	DiseaseCausCandGeneDt.objects.filter(disease_id=PatientGeneralInfoDetial.disease.id).order_by("-name").all()
	else:
		SubDiseaseDts = ''
		DiseaseCausCandGeneDts = ''
		
	
		

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
		## Dropdown Options start
		"id":id,
		"assignedDiseases":assignedDiseases,
		"OcularSurgeriesCataractDts":OcularSurgeriesCataractDts,
		"Institudes":Institudes,
		"RelationshipToProbandDts":RelationshipToProbandDts,
		"SexDts":SexDts,
		"DiseaseDts":DiseaseDts,
		"SubDiseaseDts":SubDiseaseDts,
		"AffectedDts":AffectedDts,
		"DiseaseCausCandGeneDts":DiseaseCausCandGeneDts,
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
		"TypeOldNewDts":TypeOldNewDts,
		## Dropdown Options End
		"PatientCausativeGeneInfo1":PatientCausativeGeneInfo1,
		"step4_images_name_list_all":step4_images_name_list_all,
		"PatientGeneralInfoMultiVisitOphthalmologyImagesInfo":PatientGeneralInfoMultiVisitOphthalmologyImagesInfo,
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial,
		"PatientGeneralInfoOphthalmologyInfo":PatientGeneralInfoOphthalmologyInfo,
		"PatientOtherUncommonInfoOphthalmologyInfo":PatientOtherUncommonInfoOphthalmologyInfo,
		"PatientOtherMultiVisitImagesInfo":PatientOtherMultiVisitImagesInfo,
		#"PatientGeneralInfoMultiVisitInfo":PatientGeneralInfoMultiVisitInfo,
		#"PatientGeneralInfoMultiVisitOphthalmologyAiInfo":PatientGeneralInfoMultiVisitOphthalmologyAiInfo,
		"PatientOtherCommonInfoDetial":PatientOtherCommonInfoDetial,
		## PatientGeneralInfoMultiVisit fields for step 1 22-12-2018
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
		"assignedDiseases":assignedDiseases,
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
		"PatientGeneralInfoOphthalmologySystAbnormalityInfo":PatientGeneralInfoOphthalmologySystAbnormalityInfo,
		"PatientGeneralInfoOphthalmologyOcularCompliInfo":PatientGeneralInfoOphthalmologyOcularCompliInfo,
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
		"selected_disease_id":'1',
	}
	return render(request, 'ophthalmology/edit_new_patient.html',context)

@login_required(login_url='/')
def delete_addmore(request):
	data = {}
	id = request.GET.get('id', None)
	modal_name = request.GET.get('modal_name', None)

	ggg = apps.get_model("ophthalmology",modal_name).objects.filter(id=id).all().delete()
	if ggg:
		data['success1'] = 1
	else:
		data['error'] = 1
	return JsonResponse(data)

@login_required(login_url='/')
def delete_image(request):
	data = {}
	id 				= request.GET.get('id', None)
	if id:
		modal_name 		= request.GET.get('modal_name', None)
		apps.get_model("ophthalmology",modal_name).objects.filter(id=id).all().delete()
		data['success1'] = 1
	else:
		data['error'] = 1
	return JsonResponse(data)

@login_required(login_url='/')
def get_sub_disease(request):
	data = {}
	options = {}
	options2 = {}
	id 				= request.GET.get('id', None)
	if id:
		SubDiseaseDts	=	SubDiseaseDt.objects.filter(disease_id=id).order_by("-name").all()
		for SubDiseaseDt1 in SubDiseaseDts:
			options[SubDiseaseDt1.id] = SubDiseaseDt1.name
			
		DiseaseCausCandGeneDts	=	DiseaseCausCandGeneDt.objects.filter(disease_id=id).order_by("-name").all()
		for DiseaseCausCandGeneDt1 in DiseaseCausCandGeneDts:
			options2[DiseaseCausCandGeneDt1.id] = DiseaseCausCandGeneDt1.name

		data['success1'] = 1
		data['options'] = options
		data['options2'] = options2
	else:
		data['error'] = 1
	return JsonResponse(data)

@login_required(login_url='/')
def delete_addmore_section(request):
	data = {}
	id = request.GET.get('id', None)
	PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_causative_gene_info_id=id).all().delete()
	PatientCausativeGeneInfoEthnicity.objects.filter(patient_causative_gene_info_id=id).all().delete()
	ggg = PatientCausativeGeneInfo.objects.filter(id=id).all().delete()


	if ggg:



		data['success1'] = 1
	else:
		data['error'] = 1
	return JsonResponse(data)

@login_required(login_url='/')
def import_dropdown(request):
	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					#print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data

	if request.method == 'POST':
		if request.FILES.get("import_file"):
			csv_file 	= request.FILES.get("import_file")
			modal_name 	= request.POST.get("modal_name")
			table_name 	= request.POST.get("table_name")

			if not csv_file.name.endswith('.csv'):
				messages.error(request,'File is not CSV type')
				return HttpResponseRedirect(reverse("ophthalmology:import_dropdown"))
			
			from django.db import connection
			cursor = connection.cursor()
			cursor.execute("TRUNCATE TABLE "+str(table_name))
			
			file_data = csv_file.read().decode("utf-8")
			lines = file_data.split("\n")
			for line in lines:
				fields = line.split(",")
				input_value = fields[0].replace('"', '')
				if input_value:
					modelNameinfo						= apps.get_model("ophthalmology",modal_name)()
					modelNameinfo.name 					= input_value
					modelNameinfo.save()

			messages.success(request,'File has been imported successfully.')
			return redirect("ophthalmology:import_dropdown")

	context = {"assignedDiseases":assignedDiseases}
	return render(request, 'ophthalmology/import_dropdown.html',context)

@login_required(login_url='/')
def export_patient(request,id):
	prefix = 'https://' if request.is_secure() else 'http://'
	ophthalmology_static_http_url = prefix + request.get_host() + "/media/ophthalmology/"

	#set permission doctor has access or not
	record = PatientGeneralInfo.objects.filter(id=id).first()
	if not record:
		return redirect('/ophthalmology/')

	if request.user.is_superuser != 1:
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) & (Q(id=id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).first()
		if not PatientGeneralInfoDetial:
			return redirect('/ophthalmology/')
	#set permission doctor has access or not

	PatientGeneralInfoDetial = PatientGeneralInfo.objects.filter(id=id).select_related("institute","relationship_to_proband","sex","disease","affected","inheritance","syndromic","bilateral","ocular_symptom_1","ocular_symptom_2","ocular_symptom_3","progression","flactuation","family_history","consanguineous","number_of_affected_members_in_the_same_pedigree","ethnicity","country_of_origine","origin_prefecture_in_japan","ethnic_of_father","original_country_of_father","origin_of_father_in_japan","ethnic_of_mother","original_country_of_mother","origin_of_mother_in_japan","gene_type","inheritance_type","mutation_type","dna_extraction_process","sequencing","analysis","sub_disease").first()

	family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial.id).values("family_id").first();
	if family_detail:
		PatientGeneralInfoDetial.family_id = family_detail["family_id"]
	else:
		PatientGeneralInfoDetial.family_id = ''

	PatientCausativeGeneInfo1	=	PatientCausativeGeneInfo.objects.filter(patient_id=id).all()
	if PatientCausativeGeneInfo1:
		for PatientCausativeGeneInfoData in PatientCausativeGeneInfo1:
			PatientCausativeGeneInfoData.leftAddMore		=	PatientCausativeGeneInfoEthnicity.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()
			PatientCausativeGeneInfoData.rightAddMore		=	PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()

	#return HttpResponse(PatientGeneralInfoDetial)

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
	#Step 2
	####PatientOtherCommonInfo
	PatientOtherCommonInfoDetial = PatientOtherCommonInfo.objects.filter(patient_id=id).select_related("direct_sequencing_1","direct_sequencing_2","direct_sequencing_3","direct_sequencing_4","direct_sequencing_5","targt_enrichment_ngs_panel_1","targt_enrichment_ngs_panel_analysis_1","targt_enrichment_ngs_panel_2","targt_enrichment_ngs_panel_analysis_2","targt_enrichment_ngs_panel_3","targt_enrichment_ngs_panel_analysis_3","targt_enrichment_ngs_panel_4","targt_enrichment_ngs_panel_analysis_4","targt_enrichment_ngs_panel_5","targt_enrichment_ngs_panel_analysis_5","targt_exome_sequencing_1","targt_exome_sequencing_analysis_1","targt_exome_sequencing_2","targt_exome_sequencing_analysis_2","exome_sequencing_1","exome_sequencing_analysis_1","whole_exome_sequencing_1","whole_exome_sequencing_analysis_1","sequencing_other_collaborators_1","sequencing_other_collaborators_analysis_1","sequencing_other_collaborators_2","sequencing_other_collaborators_analysis_2","beadarray_platform_1","beadarray_platform_analysis_1","other_sequencing","mitochondria_ngs_whole_gene_sequence_1","mitochondria_ngs_whole_gene_sequence_analysis_1","targt_mitochondrial_sequence_2","targt_mitochondrial_sequence_analysis_2","targt_mitochondrial_hot_spot_panel_sequence_3","targt_mitochondrial_hot_spot_panel_sequence_analysis_3","other_analysis").first()
	####PatientOtherCommonInfo

	#Step3
	PatientGeneralInfoOphthalmologyInfo	=	PatientGeneralInfoOphthalmology.objects.filter(patient_id=id).select_related("ocul_surgeries_catrct_right","age_catrct_surgery_perf_right","no_catrct_surgery_perf_right","ocul_surgeries_catrct_left","age_catrct_surgery_perf_left","no_catrct_surgery_perf_left","age_at_onset_of_ocul_symp","onset_of_diease_clas","age_at_the_init_diag","age_at_the_init_diag_clas").first()

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

	##PatientGeneralInfoOphthalmologySystAbnormality
	PatientGeneralInfoOphthalmologySystAbnormalityInfo			=  PatientGeneralInfoOphthalmologySystAbnormality.objects.filter(patient_id=id).select_related("name").all()

	##PatientGeneralInfoOphthalmologyOcularCompli
	PatientGeneralInfoOphthalmologyOcularCompliInfo			=  PatientGeneralInfoOphthalmologyOcularCompli.objects.filter(patient_id=id).select_related("name").all()

	#Step4
	step4_images_name_list_all	=	["corn_phot_left","corn_phot_right","corn_phot_on_fluor_left","corn_phot_on_fluor_right","corn_topography_left","corn_topography_right","corn_endotherial_photy_left","corn_endotherial_photy_right","opt_cohe_tomo_of_anterior_segment_left","opt_cohe_tomo_of_anterior_segment_right","ax_length_left","ax_length_right","lens_phot_left","lens_phot_right","fund_phot_wide_field_left","fund_phot_wide_field_right","fund_autoflu_left","fund_autoflu_right","fund_autoflu_wide_field_left","fund_autoflu_wide_field_right","infra_imaging_left","infra_imaging_right","infra_imaging_wide_field_left","infra_imaging_wide_field_right","fluor_angi_left","fluor_angi_right","fluor_angi_wide_field_left","fluor_angi_wide_field_right","indo_green_angi_left","indo_green_angi_right","indo_green_angi_wide_field_left","indo_green_angi_wide_field_right","opt_cohe_tomo_disc_left","opt_cohe_tomo_disc_right","opt_cohe_tomo_macula_line_left","opt_cohe_tomo_macula_line_right","opt_cohe_tomo_macula_3d_left","opt_cohe_tomo_macula_3d_right","opt_cohe_tomo_macula_en_face_left","opt_cohe_tomo_macula_en_face_right","opt_cohe_tomo_angi_left","opt_cohe_tomo_angi_right","adap_optic_imaging_left","adap_optic_imaging_right","full_field_elect_left","full_field_elect_right","mult_elect_left","mult_elect_right","focal_macu_elect_left","focal_macu_elect_right","patt_elect_left","patt_elect_right","patt_visual_evoked_potential_left","patt_visual_evoked_potential_right","flash_visual_evoked_potential_left","flash_visual_evoked_potential_right","pupilometry_left","pupilometry_right","dark_adaptmetry_left","dark_adaptmetry_right","kine_visual_field_test_left","kine_visual_field_test_right","static_visual_field_test_left","static_visual_field_test_right","microperimetry_left","microperimetry_right","color_vision_test_left","color_vision_test_right","image_comments","image_others"]

	PatientGeneralInfoMultiVisitOphthalmologyImagesInfo	=	{}
	if step4_images_name_list_all:
		for imageData in step4_images_name_list_all:
			imageData1		=	PatientGeneralInfoMultiVisitOphthalmologyImages.objects.filter(patient_id=id).filter(key=imageData).all()
			PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[imageData]	=	imageData1

	#Step5
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

	PatientOtherUncommonInfoOphthalmologyInfo	=	PatientOtherUncommonInfoOphthalmology.objects.filter(patient_id=id).select_related("ocul_surgeries_cornea_right","age_corneal_surgery_perf_right","no_corneal_surgery_perf_right","ocul_surgeries_glaucoma_right","age_glaucoma_surgery_perf_right","no_glaucomal_surgery_perf_right","ocul_surgeries_retina_right","age_vitreoretina_surgery_perf_right","no_vitreoretinal_surgery_perf_right","ocul_surgeries_lasers_right","age_ocul_surgeries_lasers_perf_right","no_ofocul_surgeries_lasers_perf_right","opht_medi_subtenon_subconj_injec_right","age_opht_medi_subtenon_subconj_injec_perf_right","no_opht_medi_subtenon_subconj_injec_perf_right","ocul_medi_internal_right","age_ocul_medi_internal_perf_right","no_ocul_medi_internal_perf_right","ocul_medi_topical_right","age_ocul_medi_topical_perf_right","no_ocul_medi_topical_perf_right","ocul_surgeries_cornea_left","age_corneal_surgery_perf_left","no_corneal_surgery_perf_left","ocul_surgeries_glaucoma_left","age_glaucoma_surgery_perf_left","no_glaucomal_surgery_perf_left","ocul_surgeries_retina_left","age_vitreoretina_surgery_perf_left","no_vitreoretinal_surgery_perf_left","ocul_surgeries_lasers_left","age_ocul_surgeries_lasers_perf_left","no_ofocul_surgeries_lasers_perf_left","opht_medi_subtenon_subconj_injec_left","age_opht_medi_subtenon_subconj_injec_perf_left","no_opht_medi_subtenon_subconj_injec_perf_left","ocul_medi_internal_left","age_ocul_medi_internal_perf_left","no_ocul_medi_internal_perf_left","ocul_medi_topical_left","age_ocul_medi_topical_perf_left","no_ocul_medi_topical_perf_left").first()

	#Step 6
	step_other_multi_visit_images_all	=	["fund_phot_left","fund_phot_right","corn_phot_ai_diag_corn_dise_left","corn_phot_ai_diag_corn_dise_right","corn_phot_on_fluo_ai_diag_corn_dise_left","corn_phot_on_fluo_ai_diag_corn_dise_right","fund_phot_ai_diag_glau_left","fund_phot_ai_diag_glau_right","opti_cohe_tomo_disc_ai_diag_glau_left","opti_cohe_tomo_disc_ai_diag_glau_right","stat_visual_field_ai_diag_glau_left","stat_visual_field_ai_diag_glau_right","fund_phot_ai_diag_diab_retino_left","fund_phot_ai_diag_diab_retino_right","fluo_angio_ai_diag_diaet_retino_left","fluo_angio_ai_diag_diaet_retino_right","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_left","opti_cohe_tomo_macu_3d_ai_diag_diaet_retino_right","fund_phot_ai_diag_age_rela_macu_dege_left","fund_phot_ai_diag_age_rela_macu_dege_right","fluo_angio_ai_diag_age_rela_macu_dege_left","fluo_angio_ai_diag_age_rela_macu_dege_right","indocy_green_angio_ai_diag_age_rela_macu_dege_left","indocy_green_angio_ai_diag_age_rela_macu_dege_right","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_left","opti_cohe_tomo_macu_3d_ai_diag_age_rela_macu_dege_right","fund_phot_ai_diag_inher_reti_dise_left","fund_phot_ai_diag_inher_reti_dise_right","fund_autofluo_wide_field_ai_diag_inher_reti_dise_left","fund_autofluo_wide_field_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_line_ai_diag_inher_reti_dise_right","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_left","opti_cohe_tomo_macula_en_face_ai_diag_inher_reti_dise_right","full_field_elect_ai_diag_inher_reti_dise_left","full_field_elect_ai_diag_inher_reti_dise_right","multifocal_elect_ai_diag_inher_reti_dise_left","multifocal_elect_ai_diag_inher_reti_dise_right","vcf_files_ai_diag_inher_reti_dise_left","vcf_files_ai_diag_inher_reti_dise_right","others_ai_diag_left","others_ai_diag_right"]


	PatientOtherMultiVisitImagesInfo	=	{}
	if step_other_multi_visit_images_all:
		for imageData in step_other_multi_visit_images_all:
			imageData1		=	PatientOtherMultiVisitImages.objects.filter(patient_id=id).filter(key=imageData).all()
			PatientOtherMultiVisitImagesInfo[imageData]	=	imageData1



	response = HttpResponse(content_type='application/ms-excel')
	if PatientGeneralInfoDetial.registration_id:
		response['Content-Disposition'] = 'attachment; filename="'+PatientGeneralInfoDetial.registration_id+'.xls"'
	else:
		response['Content-Disposition'] = 'attachment; filename="patient.xls"'

	wb = xlwt.Workbook(encoding='utf-8')

	##Export Step 1 Start
	ws = wb.add_sheet('General & Clinical Information')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['name','value']
	custom_width = 60
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		ws.col(col_num).width = int(custom_width*260)

	font_style = xlwt.XFStyle()

	row_num += 1
	ws.write(row_num, 0, 'Institude ID', font_style)
	ws.write(row_num, 1, PatientGeneralInfoDetial.institute.name, font_style)

	row_num += 1
	ws.write(row_num, 0, 'Family ID', font_style)
	ws.write(row_num, 1, PatientGeneralInfoDetial.family_id, font_style)

	row_num += 1
	ws.write(row_num, 0, 'Sample ID', font_style)
	ws.write(row_num, 1, PatientGeneralInfoDetial.sample_id, font_style)

	#relationship_to_proband
	row_num += 1
	if PatientGeneralInfoDetial.relationship_to_proband:
		if PatientGeneralInfoDetial.relationship_to_proband_other == None or PatientGeneralInfoDetial.relationship_to_proband_other == "None" or PatientGeneralInfoDetial.relationship_to_proband_other == "":
			value = PatientGeneralInfoDetial.relationship_to_proband.name
		else:
			value = PatientGeneralInfoDetial.relationship_to_proband_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Relationship To Proband', font_style)
	ws.write(row_num, 1, value, font_style)

	#birth_year_month
	row_num += 1
	if PatientGeneralInfoDetial.birth_year_month:
		value = PatientGeneralInfoDetial.birth_year_month
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Birth year / month', font_style)
	ws.write(row_num, 1, value, font_style)

	#sex
	row_num += 1
	if PatientGeneralInfoDetial.sex:
		if PatientGeneralInfoDetial.sex_other == None or PatientGeneralInfoDetial.sex_other == "None" or PatientGeneralInfoDetial.sex_other == "":
			value = PatientGeneralInfoDetial.sex.name
		else:
			value = PatientGeneralInfoDetial.sex_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sex', font_style)
	ws.write(row_num, 1, value, font_style)

	#pedigree_chart
	row_num += 1
	if PatientGeneralInfoDetial.pedigree_chart:
		value = ophthalmology_static_http_url + str(PatientGeneralInfoDetial.pedigree_chart)
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Pedigree Chart', font_style)
	ws.write(row_num, 1, value, font_style)

	#registration_date
	row_num += 1
	if PatientGeneralInfoDetial.registration_date:
		from datetime import datetime
		value = PatientGeneralInfoDetial.registration_date
		value = datetime.utcnow().strftime(str(value))
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Registration Date', font_style)
	ws.write(row_num, 1, value, font_style)

	#dna_sample_collection_date
	row_num += 1
	if PatientGeneralInfoDetial.dna_sample_collection_date:
		from datetime import datetime
		value = PatientGeneralInfoDetial.dna_sample_collection_date
		value = datetime.utcnow().strftime(str(value))
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'DNA Sample Collection Date', font_style)
	ws.write(row_num, 1, value, font_style)

	#disease
	row_num += 1
	if PatientGeneralInfoDetial.disease:
		if PatientGeneralInfoDetial.disease_other == None or PatientGeneralInfoDetial.disease_other == "None" or PatientGeneralInfoDetial.disease_other == "":
			value = PatientGeneralInfoDetial.disease.name
		else:
			value = PatientGeneralInfoDetial.disease_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Disease', font_style)
	ws.write(row_num, 1, value, font_style)

	#sub_disease
	row_num += 1
	if PatientGeneralInfoDetial.sub_disease:
		value = PatientGeneralInfoDetial.sub_disease.name
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sub Disease', font_style)
	ws.write(row_num, 1, value, font_style)

	#inheritance
	row_num += 1
	if PatientGeneralInfoDetial.inheritance:
		if PatientGeneralInfoDetial.inheritance_other == None or PatientGeneralInfoDetial.inheritance_other == "None" or PatientGeneralInfoDetial.inheritance_other == "":
			value = PatientGeneralInfoDetial.inheritance.name
		else:
			value = PatientGeneralInfoDetial.inheritance_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Inheritance', font_style)
	ws.write(row_num, 1, value, font_style)

	#syndromic
	row_num += 1
	if PatientGeneralInfoDetial.syndromic:
		if PatientGeneralInfoDetial.syndromic_other == None or PatientGeneralInfoDetial.syndromic_other == "None" or PatientGeneralInfoDetial.syndromic_other == "":
			value = PatientGeneralInfoDetial.syndromic.name
		else:
			value = PatientGeneralInfoDetial.syndromic_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Syndromic', font_style)
	ws.write(row_num, 1, value, font_style)

	#affected
	row_num += 1
	if PatientGeneralInfoDetial.affected:
		if PatientGeneralInfoDetial.affected_other == None or PatientGeneralInfoDetial.affected_other == "None" or PatientGeneralInfoDetial.affected_other == "":
			value = PatientGeneralInfoDetial.affected.name
		else:
			value = PatientGeneralInfoDetial.affected_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Affected', font_style)
	ws.write(row_num, 1, value, font_style)

	#bilateral
	row_num += 1
	if PatientGeneralInfoDetial.bilateral:
		if PatientGeneralInfoDetial.bilateral_other == None or PatientGeneralInfoDetial.bilateral_other == "None" or PatientGeneralInfoDetial.bilateral_other == "":
			value = PatientGeneralInfoDetial.bilateral.name
		else:
			value = PatientGeneralInfoDetial.bilateral_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Bilateral', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocular_symptom_1
	row_num += 1
	if PatientGeneralInfoDetial.ocular_symptom_1:
		if PatientGeneralInfoDetial.ocular_symptom_1_other == None or PatientGeneralInfoDetial.ocular_symptom_1_other == "None" or PatientGeneralInfoDetial.ocular_symptom_1_other == "":
			value = PatientGeneralInfoDetial.ocular_symptom_1.name
		else:
			value = PatientGeneralInfoDetial.ocular_symptom_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocular Symptom 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocular_symptom_2
	row_num += 1
	if PatientGeneralInfoDetial.ocular_symptom_2:
		if PatientGeneralInfoDetial.ocular_symptom_2_other == None or PatientGeneralInfoDetial.ocular_symptom_2_other == "None" or PatientGeneralInfoDetial.ocular_symptom_2_other == "":
			value = PatientGeneralInfoDetial.ocular_symptom_2.name
		else:
			value = PatientGeneralInfoDetial.ocular_symptom_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocular Symptom 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocular_symptom_3
	row_num += 1
	if PatientGeneralInfoDetial.ocular_symptom_3:
		if PatientGeneralInfoDetial.ocular_symptom_3_other == None or PatientGeneralInfoDetial.ocular_symptom_3_other == "None" or PatientGeneralInfoDetial.ocular_symptom_3_other == "":
			value = PatientGeneralInfoDetial.ocular_symptom_3.name
		else:
			value = PatientGeneralInfoDetial.ocular_symptom_3_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocular Symptom 3', font_style)
	ws.write(row_num, 1, value, font_style)

	#number_of_affected_members_in_the_same_pedigree
	row_num += 1
	if PatientGeneralInfoDetial.number_of_affected_members_in_the_same_pedigree:
		if PatientGeneralInfoDetial.number_of_affected_members_in_the_same_pedigree_other == None or PatientGeneralInfoDetial.number_of_affected_members_in_the_same_pedigree_other == "None" or PatientGeneralInfoDetial.number_of_affected_members_in_the_same_pedigree_other == "":
			value = PatientGeneralInfoDetial.number_of_affected_members_in_the_same_pedigree.name
		else:
			value = PatientGeneralInfoDetial.number_of_affected_members_in_the_same_pedigree_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Number Of Affected Members In The Same Pedigree', font_style)
	ws.write(row_num, 1, value, font_style)

	#ethnicity
	row_num += 1
	if PatientGeneralInfoDetial.ethnicity:
		if PatientGeneralInfoDetial.ethnicity_other == None or PatientGeneralInfoDetial.ethnicity_other == "None" or PatientGeneralInfoDetial.ethnicity_other == "":
			value = PatientGeneralInfoDetial.ethnicity.name
		else:
			value = PatientGeneralInfoDetial.ethnicity_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ethnicity', font_style)
	ws.write(row_num, 1, value, font_style)

	#country_of_origine
	row_num += 1
	if PatientGeneralInfoDetial.country_of_origine:
		if PatientGeneralInfoDetial.country_of_origine_other == None or PatientGeneralInfoDetial.country_of_origine_other == "None" or PatientGeneralInfoDetial.country_of_origine_other == "":
			value = PatientGeneralInfoDetial.country_of_origine.name
		else:
			value = PatientGeneralInfoDetial.country_of_origine_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Country Of Origine', font_style)
	ws.write(row_num, 1, value, font_style)

	#origin_prefecture_in_japan
	row_num += 1
	if PatientGeneralInfoDetial.origin_prefecture_in_japan:
		if PatientGeneralInfoDetial.origin_prefecture_in_japan_other == None or PatientGeneralInfoDetial.origin_prefecture_in_japan_other == "None" or PatientGeneralInfoDetial.origin_prefecture_in_japan_other == "":
			value = PatientGeneralInfoDetial.origin_prefecture_in_japan.name
		else:
			value = PatientGeneralInfoDetial.origin_prefecture_in_japan_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Origin Prefecture In Japan', font_style)
	ws.write(row_num, 1, value, font_style)

	#progression
	row_num += 1
	if PatientGeneralInfoDetial.progression:
		if PatientGeneralInfoDetial.progression_other == None or PatientGeneralInfoDetial.progression_other == "None" or PatientGeneralInfoDetial.progression_other == "":
			value = PatientGeneralInfoDetial.progression.name
		else:
			value = PatientGeneralInfoDetial.progression_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Progression', font_style)
	ws.write(row_num, 1, value, font_style)

	#family_history
	row_num += 1
	if PatientGeneralInfoDetial.family_history:
		if PatientGeneralInfoDetial.family_history_other == None or PatientGeneralInfoDetial.family_history_other == "None" or PatientGeneralInfoDetial.family_history_other == "":
			value = PatientGeneralInfoDetial.family_history.name
		else:
			value = PatientGeneralInfoDetial.family_history_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Family History', font_style)
	ws.write(row_num, 1, value, font_style)

	#consanguineous
	row_num += 1
	if PatientGeneralInfoDetial.consanguineous:
		if PatientGeneralInfoDetial.consanguineous_other == None or PatientGeneralInfoDetial.consanguineous_other == "None" or PatientGeneralInfoDetial.consanguineous_other == "":
			value = PatientGeneralInfoDetial.consanguineous.name
		else:
			value = PatientGeneralInfoDetial.consanguineous_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Consanguineous', font_style)
	ws.write(row_num, 1, value, font_style)

	#flactuation
	row_num += 1
	if PatientGeneralInfoDetial.flactuation:
		if PatientGeneralInfoDetial.flactuation_other == None or PatientGeneralInfoDetial.flactuation_other == "None" or PatientGeneralInfoDetial.flactuation_other == "":
			value = PatientGeneralInfoDetial.flactuation.name
		else:
			value = PatientGeneralInfoDetial.flactuation_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Flactuation', font_style)
	ws.write(row_num, 1, value, font_style)

	#ethnic_of_father
	row_num += 1
	if PatientGeneralInfoDetial.ethnic_of_father:
		if PatientGeneralInfoDetial.ethnic_of_father_other == None or PatientGeneralInfoDetial.ethnic_of_father_other == "None" or PatientGeneralInfoDetial.ethnic_of_father_other == "":
			value = PatientGeneralInfoDetial.ethnic_of_father.name
		else:
			value = PatientGeneralInfoDetial.ethnic_of_father_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ethnic Of Father', font_style)
	ws.write(row_num, 1, value, font_style)

	#original_country_of_father
	row_num += 1
	if PatientGeneralInfoDetial.original_country_of_father:
		if PatientGeneralInfoDetial.original_country_of_father_other == None or PatientGeneralInfoDetial.original_country_of_father_other == "None" or PatientGeneralInfoDetial.original_country_of_father_other == "":
			value = PatientGeneralInfoDetial.original_country_of_father.name
		else:
			value = PatientGeneralInfoDetial.original_country_of_father_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Original Country Of Father', font_style)
	ws.write(row_num, 1, value, font_style)

	#origin_of_father_in_japan
	row_num += 1
	if PatientGeneralInfoDetial.origin_of_father_in_japan:
		if PatientGeneralInfoDetial.origin_of_father_in_japan_other == None or PatientGeneralInfoDetial.origin_of_father_in_japan_other == "None" or PatientGeneralInfoDetial.origin_of_father_in_japan_other == "":
			value = PatientGeneralInfoDetial.origin_of_father_in_japan.name
		else:
			value = PatientGeneralInfoDetial.origin_of_father_in_japan_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Origin Of Father In Japan', font_style)
	ws.write(row_num, 1, value, font_style)

	#ethnic_of_mother
	row_num += 1
	if PatientGeneralInfoDetial.ethnic_of_mother:
		if PatientGeneralInfoDetial.ethnic_of_mother_other == None or PatientGeneralInfoDetial.ethnic_of_mother_other == "None" or PatientGeneralInfoDetial.ethnic_of_mother_other == "":
			value = PatientGeneralInfoDetial.ethnic_of_mother.name
		else:
			value = PatientGeneralInfoDetial.ethnic_of_mother_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ethnic Of Mother', font_style)
	ws.write(row_num, 1, value, font_style)

	#original_country_of_mother
	row_num += 1
	if PatientGeneralInfoDetial.original_country_of_mother:
		if PatientGeneralInfoDetial.original_country_of_mother_other == None or PatientGeneralInfoDetial.original_country_of_mother_other == "None" or PatientGeneralInfoDetial.original_country_of_mother_other == "":
			value = PatientGeneralInfoDetial.original_country_of_mother.name
		else:
			value = PatientGeneralInfoDetial.original_country_of_mother_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Original Country Of Mother', font_style)
	ws.write(row_num, 1, value, font_style)

	#origin_of_mother_in_japan
	row_num += 1
	if PatientGeneralInfoDetial.origin_of_mother_in_japan:
		if PatientGeneralInfoDetial.origin_of_mother_in_japan_other == None or PatientGeneralInfoDetial.origin_of_mother_in_japan_other == "None" or PatientGeneralInfoDetial.origin_of_mother_in_japan_other == "":
			value = PatientGeneralInfoDetial.origin_of_mother_in_japan.name
		else:
			value = PatientGeneralInfoDetial.origin_of_mother_in_japan_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Origin Of Mother In Japan', font_style)
	ws.write(row_num, 1, value, font_style)

	#gene_type
	row_num += 1
	if PatientGeneralInfoDetial.gene_type:
		if PatientGeneralInfoDetial.gene_type_other == None or PatientGeneralInfoDetial.gene_type_other == "None" or PatientGeneralInfoDetial.gene_type_other == "":
			value = PatientGeneralInfoDetial.gene_type.name
		else:
			value = PatientGeneralInfoDetial.gene_type_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Gene Type', font_style)
	ws.write(row_num, 1, value, font_style)

	#inheritance_type
	row_num += 1
	if PatientGeneralInfoDetial.inheritance_type:
		if PatientGeneralInfoDetial.inheritance_type_other == None or PatientGeneralInfoDetial.inheritance_type_other == "None" or PatientGeneralInfoDetial.inheritance_type_other == "":
			value = PatientGeneralInfoDetial.inheritance_type.name
		else:
			value = PatientGeneralInfoDetial.inheritance_type_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Inheritance Type', font_style)
	ws.write(row_num, 1, value, font_style)

	#mutation_type
	row_num += 1
	if PatientGeneralInfoDetial.mutation_type:
		if PatientGeneralInfoDetial.mutation_type_other == None or PatientGeneralInfoDetial.mutation_type_other == "None" or PatientGeneralInfoDetial.mutation_type_other == "":
			value = PatientGeneralInfoDetial.mutation_type.name
		else:
			value = PatientGeneralInfoDetial.mutation_type_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Mutation Type', font_style)
	ws.write(row_num, 1, value, font_style)

	#gene_inheritance_mutation_comments
	row_num += 1
	if PatientGeneralInfoDetial.gene_inheritance_mutation_comments:
		value = PatientGeneralInfoDetial.gene_inheritance_mutation_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Gene Inheritance Mutation Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	

	#dna_extraction_process
	row_num += 1
	if PatientGeneralInfoDetial.dna_extraction_process:
		if PatientGeneralInfoDetial.dna_extraction_process_other == None or PatientGeneralInfoDetial.dna_extraction_process_other == "None" or PatientGeneralInfoDetial.dna_extraction_process_other == "":
			value = PatientGeneralInfoDetial.dna_extraction_process.name
		else:
			value = PatientGeneralInfoDetial.dna_extraction_process_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Dna Extraction Process', font_style)
	ws.write(row_num, 1, value, font_style)


	#analysis
	row_num += 1
	if PatientGeneralInfoDetial.analysis:
		if PatientGeneralInfoDetial.analysis_other == None or PatientGeneralInfoDetial.analysis_other == "None" or PatientGeneralInfoDetial.analysis_other == "":
			value = PatientGeneralInfoDetial.analysis.name
		else:
			value = PatientGeneralInfoDetial.analysis_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Analysis', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing
	row_num += 1
	if PatientGeneralInfoDetial.sequencing:
		if PatientGeneralInfoDetial.sequencing_other == None or PatientGeneralInfoDetial.sequencing_other == "None" or PatientGeneralInfoDetial.sequencing_other == "":
			value = PatientGeneralInfoDetial.sequencing.name
		else:
			value = PatientGeneralInfoDetial.sequencing_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing', font_style)
	ws.write(row_num, 1, value, font_style)

	#PatientCausativeGeneInfo1
	row_num += 2
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.type_old_new:
				value = datas.type_old_new.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Type Old New', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
	row_num += 1
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.caus_cand:
				value = datas.caus_cand.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Caus Cand', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.chromosome:
				value = datas.chromosome.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Chromosome', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.chromosome_comment:
				value = datas.chromosome_comment
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Chromosome Comment', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
	
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.disease_caus_cand_gene:
				value = datas.disease_caus_cand_gene.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Caus Cand Gene', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.caus_cand_gene:
				value = datas.caus_cand_gene.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Gene Type', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.exon:
				value = datas.exon.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Exon', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.exon_comment:
				value = datas.exon_comment
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Exon Comment', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.caus_cand_mutation_nucleotide_amino_acid:
				value = datas.caus_cand_mutation_nucleotide_amino_acid
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Caus Mutation Nucleotide Change Amino Acid', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.caus_cand_mutation_nucleotide_amino_acid_comment:
				value = datas.caus_cand_mutation_nucleotide_amino_acid_comment
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Caus Cand Mutation Nucleotide Amino Acid Comment', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.transcript:
				value = datas.transcript
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Transcript', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	row_num += 1		
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			if datas.position:
				value = datas.position
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Position', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
			
	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			row_num += 1
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Freq Ethnicity', font_style)
			col_num1 = 0
			if datas.leftAddMore:
				for datas1 in datas.leftAddMore:
					col_num1 += 1
					if datas1.freq_ethnicity_other != "":
						value = datas1.freq_ethnicity_other
					else:
						value = datas1.freq_ethnicity.name

					ws.col(col_num).width = int(custom_width*260)
					ws.write(row_num, col_num1, value, font_style)
			else:
				value = 'No Entry Found'
				col_num1 += 1
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num1, value, font_style)

	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			row_num += 1
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Freq Ethnicity Percentage', font_style)
			col_num1 = 0
			if datas.leftAddMore:
				for datas1 in datas.leftAddMore:
					col_num1 += 1
					if datas1.freq_ethnicity_per != "":
						value = datas1.freq_ethnicity_per
					else:
						value = 'No Entry Found'
					ws.col(col_num).width = int(custom_width*260)
					ws.write(row_num, col_num1, value, font_style)
			else:
				value = 'No Entry Found'
				col_num1 += 1
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num1, value, font_style)

	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			row_num += 1
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Freq Local Population', font_style)
			col_num1 = 0
			if datas.rightAddMore:
				for datas1 in datas.rightAddMore:
					col_num1 += 1
					if datas1.freq_local_population_other != "":
						value = datas1.freq_local_population_other
					else:
						value = datas1.freq_local_population.name

					ws.col(col_num).width = int(custom_width*260)
					ws.write(row_num, col_num1, value, font_style)
			else:
				value = 'No Entry Found'
				col_num1 += 1
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num1, value, font_style)

	if PatientCausativeGeneInfo1:
		col_num = 0
		for datas in PatientCausativeGeneInfo1:
			row_num += 1
			col_num += 1
			if col_num == 1:
				ws.write(row_num, 0, 'Freq Local Population Percentage', font_style)
			col_num1 = 0
			if datas.rightAddMore:
				for datas1 in datas.rightAddMore:
					col_num1 += 1
					if datas1.freq_local_population_per != "":
						value = datas1.freq_local_population_per
					else:
						value = 'No Entry Found'
					ws.col(col_num).width = int(custom_width*260)
					ws.write(row_num, col_num1, value, font_style)
			else:
				value = 'No Entry Found'
				col_num1 += 1
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num1, value, font_style)
	#logmar_visual_acuity_left
	row_num += 2
	if logmar_visual_acuity_left:
		col_num = 1
		ws.write(row_num, 0, 'Logmar Visual Acuity Left', font_style)
		for data in logmar_visual_acuity_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Logmar Visual Acuity Left', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#logmar_visual_acuity_right
	row_num += 2
	if logmar_visual_acuity_right:
		col_num = 1
		ws.write(row_num, 0, 'Logmar Visual Acuity Right', font_style)
		for data in logmar_visual_acuity_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Logmar Visual Acuity Right', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#logmar_visual_acuity_classification_left
	row_num += 2
	if logmar_visual_acuity_classification_left:
		col_num = 1
		ws.write(row_num, 0, 'Logmar Visual Acuity Classification Left', font_style)
		for data in logmar_visual_acuity_classification_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_classification_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_classification_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Logmar Visual Acuity Classification Left', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#logmar_visual_acuity_classification_right
	row_num += 2
	if logmar_visual_acuity_classification_right:
		col_num = 1
		ws.write(row_num, 0, 'Logmar Visual Acuity Classification Right', font_style)
		for data in logmar_visual_acuity_classification_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_classification_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in logmar_visual_acuity_classification_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Logmar Visual Acuity Classification Right', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#blood_pressure_systolic_mmhg
	row_num += 2
	if blood_pressure_systolic_mmhg:
		col_num = 1
		ws.write(row_num, 0, 'Blood Pressure Systolic Mmhg', font_style)
		for data in blood_pressure_systolic_mmhg:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_pressure_systolic_mmhg:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_pressure_systolic_mmhg:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Blood Pressure Systolic Mmhg', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#blood_total_cholesterol_level_mgdl
	row_num += 2
	if blood_total_cholesterol_level_mgdl:
		col_num = 1
		ws.write(row_num, 0, 'Blood Total Cholesterol Level Mgdl', font_style)
		for data in blood_total_cholesterol_level_mgdl:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_total_cholesterol_level_mgdl:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_total_cholesterol_level_mgdl:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Blood Total Cholesterol Level Mgdl', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#blood_pressure_diastolic_mmhg
	row_num += 2
	if blood_pressure_diastolic_mmhg:
		col_num = 1
		ws.write(row_num, 0, 'Blood Pressure Diastolic Mmhg', font_style)
		for data in blood_pressure_diastolic_mmhg:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_pressure_diastolic_mmhg:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_pressure_diastolic_mmhg:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Blood Pressure Diastolic Mmhg', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#blood_pressure_diastolic_mmhg
	row_num += 2
	if blood_ldl_cholesterol_level_mgdl:
		col_num = 1
		ws.write(row_num, 0, 'Blood Ldl Cholesterol Level Mgdl', font_style)
		for data in blood_ldl_cholesterol_level_mgdl:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_ldl_cholesterol_level_mgdl:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in blood_ldl_cholesterol_level_mgdl:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Blood Ldl Cholesterol Level Mgdl', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#hypertension_classification
	row_num += 2
	if hypertension_classification:
		col_num = 1
		ws.write(row_num, 0, 'Hypertension Classification', font_style)
		for data in hypertension_classification:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypertension_classification:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypertension_classification:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Hypertension Classification', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#hypercholestremia_classification
	row_num += 2
	if hypercholestremia_classification:
		col_num = 1
		ws.write(row_num, 0, 'Hypercholestremia Classification', font_style)
		for data in hypercholestremia_classification:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypercholestremia_classification:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypercholestremia_classification:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Hypercholestremia Classification', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#hypertension_medication
	row_num += 2
	if hypertension_medication:
		col_num = 1
		ws.write(row_num, 0, 'Hypertension Medication', font_style)
		for data in hypertension_medication:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypertension_medication:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypertension_medication:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Hypertension Medication', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#hypercholestremia_medication
	row_num += 2
	if hypercholestremia_medication:
		col_num = 1
		ws.write(row_num, 0, 'Hypercholestremia Medication', font_style)
		for data in hypercholestremia_medication:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypercholestremia_medication:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hypercholestremia_medication:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Hypercholestremia Medication', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#fasting_blood_glucose_mgdl
	row_num += 2
	if fasting_blood_glucose_mgdl:
		col_num = 1
		ws.write(row_num, 0, 'Fasting Blood Glucose Mgdl', font_style)
		for data in fasting_blood_glucose_mgdl:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in fasting_blood_glucose_mgdl:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in fasting_blood_glucose_mgdl:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Fasting Blood Glucose Mgdl', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#hba1c_percentage
	row_num += 2
	if hba1c_percentage:
		col_num = 1
		ws.write(row_num, 0, 'Hba1c Percentage', font_style)
		for data in hba1c_percentage:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hba1c_percentage:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in hba1c_percentage:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Hba1c Percentage', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#diabetes_mellitus
	row_num += 2
	if diabetes_mellitus:
		col_num = 1
		ws.write(row_num, 0, 'Diabetes Mellitus', font_style)
		for data in diabetes_mellitus:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in diabetes_mellitus:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in diabetes_mellitus:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Diabetes Mellitus', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#diabetes_mellitus_medication
	row_num += 2
	if diabetes_mellitus_medication:
		col_num = 1
		ws.write(row_num, 0, 'Diabetes Mellitus Medication', font_style)
		for data in diabetes_mellitus_medication:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in diabetes_mellitus_medication:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in diabetes_mellitus_medication:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Diabetes Mellitus Medication', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#clinical_course_of_systemic_disorder_or_no_systemic_disorder
	row_num += 2
	if clinical_course_of_systemic_disorder_or_no_systemic_disorder:
		col_num = 1
		ws.write(row_num, 0, 'Clinical Course Of Systemic Disorder Or No Systemic Disorder', font_style)
		for data in clinical_course_of_systemic_disorder_or_no_systemic_disorder:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in clinical_course_of_systemic_disorder_or_no_systemic_disorder:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in clinical_course_of_systemic_disorder_or_no_systemic_disorder:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Clinical Course Of Systemic Disorder Or No Systemic Disorder', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#typical
	row_num += 2
	if typical:
		col_num = 1
		ws.write(row_num, 0, 'Typical', font_style)
		for data in typical:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in typical:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in typical:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		ws.write(row_num, 0, 'Typical', font_style)
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#Export Step 1 end

	#Export Step 2 Start
	ws = wb.add_sheet('Clinical Information II')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['name','value']
	custom_width = 60
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		ws.col(col_num).width = int(custom_width*260)

	font_style = xlwt.XFStyle()

	#direct_sequencing_1
	row_num += 1
	if PatientOtherCommonInfoDetial.direct_sequencing_1:
		if PatientOtherCommonInfoDetial.direct_sequencing_1_other == None or PatientOtherCommonInfoDetial.direct_sequencing_1_other == "None" or PatientOtherCommonInfoDetial.direct_sequencing_1_other == "":
			value = PatientOtherCommonInfoDetial.direct_sequencing_1.name
		else:
			value = PatientOtherCommonInfoDetial.direct_sequencing_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.direct_sequencing_1_comments:
		value = PatientOtherCommonInfoDetial.direct_sequencing_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_2
	row_num += 2
	if PatientOtherCommonInfoDetial.direct_sequencing_2:
		if PatientOtherCommonInfoDetial.direct_sequencing_2_other == None or PatientOtherCommonInfoDetial.direct_sequencing_2_other == "None" or PatientOtherCommonInfoDetial.direct_sequencing_2_other == "":
			value = PatientOtherCommonInfoDetial.direct_sequencing_2.name
		else:
			value = PatientOtherCommonInfoDetial.direct_sequencing_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.direct_sequencing_2_comments:
		value = PatientOtherCommonInfoDetial.direct_sequencing_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_3
	row_num += 2
	if PatientOtherCommonInfoDetial.direct_sequencing_3:
		if PatientOtherCommonInfoDetial.direct_sequencing_3_other == None or PatientOtherCommonInfoDetial.direct_sequencing_3_other == "None" or PatientOtherCommonInfoDetial.direct_sequencing_3_other == "":
			value = PatientOtherCommonInfoDetial.direct_sequencing_3.name
		else:
			value = PatientOtherCommonInfoDetial.direct_sequencing_3_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 3', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_3_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.direct_sequencing_3_comments:
		value = PatientOtherCommonInfoDetial.direct_sequencing_3_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 3 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_4
	row_num += 2
	if PatientOtherCommonInfoDetial.direct_sequencing_4:
		if PatientOtherCommonInfoDetial.direct_sequencing_4_other == None or PatientOtherCommonInfoDetial.direct_sequencing_4_other == "None" or PatientOtherCommonInfoDetial.direct_sequencing_4_other == "":
			value = PatientOtherCommonInfoDetial.direct_sequencing_4.name
		else:
			value = PatientOtherCommonInfoDetial.direct_sequencing_4_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 4', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_4_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.direct_sequencing_4_comments:
		value = PatientOtherCommonInfoDetial.direct_sequencing_4_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 4 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_5
	row_num += 2
	if PatientOtherCommonInfoDetial.direct_sequencing_5:
		if PatientOtherCommonInfoDetial.direct_sequencing_5_other == None or PatientOtherCommonInfoDetial.direct_sequencing_5_other == "None" or PatientOtherCommonInfoDetial.direct_sequencing_5_other == "":
			value = PatientOtherCommonInfoDetial.direct_sequencing_5.name
		else:
			value = PatientOtherCommonInfoDetial.direct_sequencing_5_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 5', font_style)
	ws.write(row_num, 1, value, font_style)

	#direct_sequencing_5_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.direct_sequencing_5_comments:
		value = PatientOtherCommonInfoDetial.direct_sequencing_5_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Direct Sequencing 5 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_1
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 1 comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_2
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_2
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 2 comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_3
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 3', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_3_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_3_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 3 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_3
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 3', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_3_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_3_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 3 comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_4
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 4', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_4_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_4_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 4 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_4
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 4', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_4_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_4_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 4 comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_5
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 5', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_5_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_5_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel 5 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_5
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5:
		if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_other == None or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_other == "None" or PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_other == "":
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5.name
		else:
			value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 5', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_enrichment_ngs_panel_analysis_5_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_comments:
		value = PatientOtherCommonInfoDetial.targt_enrichment_ngs_panel_analysis_5_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Enrichment Ngs Panel Analysis 5 comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_1
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_1:
		if PatientOtherCommonInfoDetial.targt_exome_sequencing_1_other == None or PatientOtherCommonInfoDetial.targt_exome_sequencing_1_other == "None" or PatientOtherCommonInfoDetial.targt_exome_sequencing_1_other == "":
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_1.name
		else:
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_1_comments:
		value = PatientOtherCommonInfoDetial.targt_exome_sequencing_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1:
		if PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other == None or PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other == "None" or PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing Analysis 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_2
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_2:
		if PatientOtherCommonInfoDetial.targt_exome_sequencing_2_other == None or PatientOtherCommonInfoDetial.targt_exome_sequencing_2_other == "None" or PatientOtherCommonInfoDetial.targt_exome_sequencing_2_other == "":
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_2.name
		else:
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_2_comments:
		value = PatientOtherCommonInfoDetial.targt_exome_sequencing_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_analysis_2
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2:
		if PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_other == None or PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_other == "None" or PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_other == "":
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2.name
		else:
			value = PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing Analysis 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_exome_sequencing_analysis_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_comments:
		value = PatientOtherCommonInfoDetial.targt_exome_sequencing_analysis_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Exome Sequencing Analysis 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#exome_sequencing_1
	row_num += 2
	if PatientOtherCommonInfoDetial.exome_sequencing_1:
		if PatientOtherCommonInfoDetial.exome_sequencing_1_other == None or PatientOtherCommonInfoDetial.exome_sequencing_1_other == "None" or PatientOtherCommonInfoDetial.exome_sequencing_1_other == "":
			value = PatientOtherCommonInfoDetial.exome_sequencing_1.name
		else:
			value = PatientOtherCommonInfoDetial.exome_sequencing_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Exome Sequencing 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#exome_sequencing_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.exome_sequencing_1_comments:
		value = PatientOtherCommonInfoDetial.exome_sequencing_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Exome Sequencing 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#exome_sequencing_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.exome_sequencing_analysis_1:
		if PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_other == None or PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_other == "None" or PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.exome_sequencing_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Exome Sequencing Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#exome_sequencing_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.exome_sequencing_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Exome Sequencing Analysis 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#whole_exome_sequencing_1
	row_num += 2
	if PatientOtherCommonInfoDetial.whole_exome_sequencing_1:
		if PatientOtherCommonInfoDetial.whole_exome_sequencing_1_other == None or PatientOtherCommonInfoDetial.whole_exome_sequencing_1_other == "None" or PatientOtherCommonInfoDetial.whole_exome_sequencing_1_other == "":
			value = PatientOtherCommonInfoDetial.whole_exome_sequencing_1.name
		else:
			value = PatientOtherCommonInfoDetial.whole_exome_sequencing_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Whole Exome Sequencing 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#whole_exome_sequencing_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.whole_exome_sequencing_1_comments:
		value = PatientOtherCommonInfoDetial.whole_exome_sequencing_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Whole Exome Sequencing 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#whole_exome_sequencing_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1:
		if PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_other == None or PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_other == "None" or PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Whole Exome Sequencing Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#whole_exome_sequencing_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.whole_exome_sequencing_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Whole Exome Sequencing Analysis 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_1
	row_num += 2
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_1:
		if PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_other == None or PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_other == "None" or PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_other == "":
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_1.name
		else:
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing Other Collaborators 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_comments:
		value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing other Collaborators 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1:
		if PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_other == None or PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_other == "None" or PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing Other Collaborators Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing other Collaborators Analysis 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_2
	row_num += 2
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_2:
		if PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_other == None or PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_other == "None" or PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_other == "":
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_2.name
		else:
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing Other Collaborators 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_comments:
		value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing other Collaborators 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_analysis_2
	row_num += 2
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2:
		if PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_other == None or PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_other == "None" or PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_other == "":
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2.name
		else:
			value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing Other Collaborators Analysis 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#sequencing_other_collaborators_analysis_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_comments:
		value = PatientOtherCommonInfoDetial.sequencing_other_collaborators_analysis_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Sequencing other Collaborators Analysis 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#beadarray_platform_1
	row_num += 2
	if PatientOtherCommonInfoDetial.beadarray_platform_1:
		if PatientOtherCommonInfoDetial.beadarray_platform_1_other == None or PatientOtherCommonInfoDetial.beadarray_platform_1_other == "None" or PatientOtherCommonInfoDetial.beadarray_platform_1_other == "":
			value = PatientOtherCommonInfoDetial.beadarray_platform_1.name
		else:
			value = PatientOtherCommonInfoDetial.beadarray_platform_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Beadarray Platform 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#beadarray_platform_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.beadarray_platform_1_comments:
		value = PatientOtherCommonInfoDetial.beadarray_platform_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Beadarray Platform 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#beadarray_platform_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.beadarray_platform_analysis_1:
		if PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_other == None or PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_other == "None" or PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.beadarray_platform_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Beadarray Platform Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#beadarray_platform_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.beadarray_platform_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Beadarray Platform Analysis 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#other_sequencing
	row_num += 2
	if PatientOtherCommonInfoDetial.other_sequencing:
		if PatientOtherCommonInfoDetial.other_sequencing_other == None or PatientOtherCommonInfoDetial.other_sequencing_other == "None" or PatientOtherCommonInfoDetial.other_sequencing_other == "":
			value = PatientOtherCommonInfoDetial.other_sequencing.name
		else:
			value = PatientOtherCommonInfoDetial.other_sequencing_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Other Sequencing', font_style)
	ws.write(row_num, 1, value, font_style)

	#other_sequencing_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.other_sequencing_comments:
		value = PatientOtherCommonInfoDetial.other_sequencing_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Other Sequencing Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#mitochondria_ngs_whole_gene_sequence_1
	row_num += 2
	if PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1:
		if PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_other == None or PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_other == "None" or PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_other == "":
			value = PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1.name
		else:
			value = PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Mitochondria Ngs Whole Gene Sequence 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#mitochondria_ngs_whole_gene_sequence_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_comments:
		value = PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Mitochondria Ngs Whole Gene Sequence 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#mitochondria_ngs_whole_gene_sequence_analysis_1
	row_num += 2
	if PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1:
		if PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_other == None or PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_other == "None" or PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_other == "":
			value = PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1.name
		else:
			value = PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Mitochondria Ngs Whole Gene Sequence Analysis 1', font_style)
	ws.write(row_num, 1, value, font_style)

	#mitochondria_ngs_whole_gene_sequence_analysis_1_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_comments:
		value = PatientOtherCommonInfoDetial.mitochondria_ngs_whole_gene_sequence_analysis_1_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Mitochondria Ngs Whole Gene Sequence Analysis 1 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_sequence_2
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2:
		if PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_other == None or PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_other == "None" or PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_other == "":
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2.name
		else:
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Sequence 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_sequence_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_comments:
		value = PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Sequence 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_sequence_analysis_2
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2:
		if PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_other == None or PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_other == "None" or PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_other == "":
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2.name
		else:
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Sequence Analysis 2', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_sequence_analysis_2_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_comments:
		value = PatientOtherCommonInfoDetial.targt_mitochondrial_sequence_analysis_2_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Sequence Analysis 2 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_hot_spot_panel_sequence_3
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3:
		if PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_other == None or PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_other == "None" or PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_other == "":
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3.name
		else:
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Hot Spot Panel Sequence 3', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_hot_spot_panel_sequence_3_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_comments:
		value = PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_3_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Hot Spot Panel Sequence 3 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_hot_spot_panel_sequence_analysis_3
	row_num += 2
	if PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3:
		if PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other == None or PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other == "None" or PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other == "":
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3.name
		else:
			value = PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Hot Spot Panel Sequence Analysis 3', font_style)
	ws.write(row_num, 1, value, font_style)

	#targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments:
		value = PatientOtherCommonInfoDetial.targt_mitochondrial_hot_spot_panel_sequence_analysis_3_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Targt Mitochondrial Hot Spot Panel Sequence Analysis 3 Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#other_analysis
	row_num += 2
	if PatientOtherCommonInfoDetial.other_analysis:
		if PatientOtherCommonInfoDetial.other_analysis_other == None or PatientOtherCommonInfoDetial.other_analysis_other == "None" or PatientOtherCommonInfoDetial.other_analysis_other == "":
			value = PatientOtherCommonInfoDetial.other_analysis.name
		else:
			value = PatientOtherCommonInfoDetial.other_analysis_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Other Analysis', font_style)
	ws.write(row_num, 1, value, font_style)

	#other_analysis_comments
	row_num += 1
	if PatientOtherCommonInfoDetial.other_analysis_comments:
		value = PatientOtherCommonInfoDetial.other_analysis_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Other Analysis Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#Export Step 2 End

	#Export Step 3 Start
	ws = wb.add_sheet('Ophthalmology Data')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Value']
	custom_width = 60
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		ws.col(col_num).width = int(custom_width*260)

	font_style = xlwt.XFStyle()

	#ocul_surgeries_catrct_left
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left:
		if PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other == None or PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other == "None" or PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Catrct Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_catrct_right
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right:
		if PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other == None or PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other == "None" or PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.ocul_surgeries_catrct_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Catrct Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_catrct_surgery_perf_left
	row_num += 2
	if PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left:
		if PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other == None or PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other == "None" or PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Catrct Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_catrct_surgery_perf_right
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right:
		if PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other == None or PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other == "None" or PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.age_catrct_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Catrct Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_catrct_surgery_perf_left
	row_num += 2
	if PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left:
		if PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other == None or PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other == "None" or PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Catrct Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_catrct_surgery_perf_right
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right:
		if PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other == None or PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other == "None" or PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.no_catrct_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Catrct Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_at_onset_of_ocul_symp
	row_num += 2
	if PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp:
		if PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other == None or PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other == "None" or PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.age_at_onset_of_ocul_symp_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age At Onset Of Ocul Symp', font_style)
	ws.write(row_num, 1, value, font_style)

	#onset_of_diease_clas
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.onset_of_diease_clas:
		if PatientGeneralInfoOphthalmologyInfo.onset_of_diease_clas_other == None or PatientGeneralInfoOphthalmologyInfo.onset_of_diease_clas_other == "None" or PatientGeneralInfoOphthalmologyInfo.onset_of_diease_clas_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.onset_of_diease_clas.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.onset_of_diease_clas_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Onset Of Diease Clas', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_at_the_init_diag
	row_num += 2
	if PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag:
		if PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other == None or PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other == "None" or PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age At The Init Diag', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_at_the_init_diag_clas
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas:
		if PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other == None or PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other == "None" or PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other == "":
			value = PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas.name
		else:
			value = PatientGeneralInfoOphthalmologyInfo.age_at_the_init_diag_clas_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age At The Init Diag Clas', font_style)

	#gene_middle_results
	row_num += 2
	if PatientGeneralInfoOphthalmologyInfo.gene_middle_results:
		value = ophthalmology_static_http_url + str(PatientGeneralInfoOphthalmologyInfo.gene_middle_results)
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Gene Middle Results', font_style)
	ws.write(row_num, 1, value, font_style)

	#gene_comments
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.gene_comments:
		value = PatientGeneralInfoOphthalmologyInfo.gene_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Gene Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#vcf_whole_exome_sequencing
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.vcf_whole_exome_sequencing:
		value = ophthalmology_static_http_url + str(PatientGeneralInfoOphthalmologyInfo.vcf_whole_exome_sequencing)
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Vcf Whole Exome Sequencing', font_style)
	ws.write(row_num, 1, value, font_style)

	#vcf_whole_genome_sequencing
	row_num += 1
	if PatientGeneralInfoOphthalmologyInfo.vcf_whole_genome_sequencing:
		value = ophthalmology_static_http_url + str(PatientGeneralInfoOphthalmologyInfo.vcf_whole_genome_sequencing)
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Vcf Whole Genome Sequencing', font_style)
	ws.write(row_num, 1, value, font_style)


	#intra_ocul_pres_left
	row_num += 2
	ws.write(row_num, 0, 'Intra Ocul Pres Left', font_style)
	if intra_ocul_pres_left:
		col_num = 1
		for data in intra_ocul_pres_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#intra_ocul_pres_right
	row_num += 2
	ws.write(row_num, 0, 'Intra Ocul Pres Right', font_style)
	if intra_ocul_pres_right:
		col_num = 1
		for data in intra_ocul_pres_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#intra_ocul_pres_clas_left
	row_num += 2
	ws.write(row_num, 0, 'Intra Ocul Pres Clas Left', font_style)
	if intra_ocul_pres_clas_left:
		col_num = 1
		for data in intra_ocul_pres_clas_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_clas_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_clas_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#intra_ocul_pres_clas_right
	row_num += 2
	ws.write(row_num, 0, 'Intra Ocul Pres Clas Right', font_style)
	if intra_ocul_pres_clas_right:
		col_num = 1
		for data in intra_ocul_pres_clas_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_clas_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in intra_ocul_pres_clas_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#refr_error_sphe_equi_left
	row_num += 2
	ws.write(row_num, 0, 'Refr Error Sphe Equi Left', font_style)
	if refr_error_sphe_equi_left:
		col_num = 1
		for data in refr_error_sphe_equi_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#refr_error_sphe_equi_right
	row_num += 2
	ws.write(row_num, 0, 'Refr Error Sphe Equi Right', font_style)
	if refr_error_sphe_equi_right:
		col_num = 1
		for data in refr_error_sphe_equi_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#refr_error_sphe_equi_clas_left
	row_num += 2
	ws.write(row_num, 0, 'Refr Error Sphe Equi Clas Left', font_style)
	if refr_error_sphe_equi_clas_left:
		col_num = 1
		for data in refr_error_sphe_equi_clas_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_clas_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_clas_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#refr_error_sphe_equi_clas_right
	row_num += 2
	ws.write(row_num, 0, 'Refr Error Sphe Equi Clas Right', font_style)
	if refr_error_sphe_equi_clas_right:
		col_num = 1
		for data in refr_error_sphe_equi_clas_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_clas_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in refr_error_sphe_equi_clas_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#corn_thic_left
	row_num += 2
	ws.write(row_num, 0, 'Corn Thic Left', font_style)
	if corn_thic_left:
		col_num = 1
		for data in corn_thic_left:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in corn_thic_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in corn_thic_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#corn_thic_right
	row_num += 2
	ws.write(row_num, 0, 'Corn Thic Right', font_style)
	if corn_thic_right:
		col_num = 1
		for data in corn_thic_right:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in corn_thic_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in corn_thic_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#lens_left
	row_num += 2
	ws.write(row_num, 0, 'Lens Left', font_style)
	if lens_left:
		col_num = 1
		for data in lens_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in lens_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in lens_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#lens_right
	row_num += 2
	ws.write(row_num, 0, 'Lens Right', font_style)
	if lens_right:
		col_num = 1
		for data in lens_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in lens_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in lens_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#axia_leng_left
	row_num += 2
	ws.write(row_num, 0, 'Axia Leng Left', font_style)
	if axia_leng_left:
		col_num = 1
		for data in axia_leng_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#axia_leng_right
	row_num += 2
	ws.write(row_num, 0, 'Axia Leng Right', font_style)
	if axia_leng_right:
		col_num = 1
		for data in axia_leng_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#axia_leng_clas_left
	row_num += 2
	ws.write(row_num, 0, 'Axia Leng Clas Left', font_style)
	if axia_leng_clas_left:
		col_num = 1
		for data in axia_leng_clas_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_clas_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_clas_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#axia_leng_clas_right
	row_num += 2
	ws.write(row_num, 0, 'Axia Leng Clas Right', font_style)
	if axia_leng_clas_right:
		col_num = 1
		for data in axia_leng_clas_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_clas_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in axia_leng_clas_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#macu_thic_left
	row_num += 2
	ws.write(row_num, 0, 'Macu Thic Left', font_style)
	if macu_thic_left:
		col_num = 1
		for data in macu_thic_left:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_thic_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_thic_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#macu_thic_right
	row_num += 2
	ws.write(row_num, 0, 'Macu Thic Right', font_style)
	if macu_thic_right:
		col_num = 1
		for data in macu_thic_right:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_thic_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_thic_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#macu_edema_left
	row_num += 2
	ws.write(row_num, 0, 'Macu Edema Left', font_style)
	if macu_edema_left:
		col_num = 1
		for data in macu_edema_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_edema_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_edema_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#macu_edema_right
	row_num += 2
	ws.write(row_num, 0, 'Macu Edema Right', font_style)
	if macu_edema_right:
		col_num = 1
		for data in macu_edema_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_edema_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_edema_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#macu_schisis_left
	row_num += 2
	ws.write(row_num, 0, 'Macu Schisis Left', font_style)
	if macu_schisis_left:
		col_num = 1
		for data in macu_schisis_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_schisis_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_schisis_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#macu_schisis_right
	row_num += 2
	ws.write(row_num, 0, 'Macu Schisis Right', font_style)
	if macu_schisis_right:
		col_num = 1
		for data in macu_schisis_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_schisis_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in macu_schisis_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#epir_memb_left
	row_num += 2
	ws.write(row_num, 0, 'Epir Memb Left', font_style)
	if epir_memb_left:
		col_num = 1
		for data in epir_memb_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in epir_memb_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in epir_memb_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#epir_memb_right
	row_num += 2
	ws.write(row_num, 0, 'Epir Memb Right', font_style)
	if epir_memb_right:
		col_num = 1
		for data in epir_memb_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in epir_memb_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in epir_memb_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#sub_sensreti_fuild_left
	row_num += 2
	ws.write(row_num, 0, 'Sub Sensreti Fuild Left', font_style)
	if sub_sensreti_fuild_left:
		col_num = 1
		for data in sub_sensreti_fuild_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_sensreti_fuild_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_sensreti_fuild_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#sub_sensreti_fuild_right
	row_num += 2
	ws.write(row_num, 0, 'Sub Sensreti Fuild Right', font_style)
	if sub_sensreti_fuild_right:
		col_num = 1
		for data in sub_sensreti_fuild_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_sensreti_fuild_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_sensreti_fuild_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#sub_reti_epith_memb_fuild_left
	row_num += 2
	ws.write(row_num, 0, 'Sub Reti Epith Memb Fuild Left', font_style)
	if sub_reti_epith_memb_fuild_left:
		col_num = 1
		for data in sub_reti_epith_memb_fuild_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_reti_epith_memb_fuild_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_reti_epith_memb_fuild_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#sub_reti_epith_memb_fuild_right
	row_num += 2
	ws.write(row_num, 0, 'Sub Reti Epith Memb Fuild Right', font_style)
	if sub_reti_epith_memb_fuild_right:
		col_num = 1
		for data in sub_reti_epith_memb_fuild_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_reti_epith_memb_fuild_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in sub_reti_epith_memb_fuild_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#foveal_thic_left
	row_num += 2
	ws.write(row_num, 0, 'Foveal Thic Left', font_style)
	if foveal_thic_left:
		col_num = 1
		for data in foveal_thic_left:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in foveal_thic_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in foveal_thic_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#foveal_thic_right
	row_num += 2
	ws.write(row_num, 0, 'Foveal Thic Right', font_style)
	if foveal_thic_right:
		col_num = 1
		for data in foveal_thic_right:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in foveal_thic_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in foveal_thic_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#choro_thic_left
	row_num += 2
	ws.write(row_num, 0, 'Choro Thic Left', font_style)
	if choro_thic_left:
		col_num = 1
		for data in choro_thic_left:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in choro_thic_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in choro_thic_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#choro_thic_right
	row_num += 2
	ws.write(row_num, 0, 'Choro Thic Right', font_style)
	if choro_thic_right:
		col_num = 1
		for data in choro_thic_right:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in choro_thic_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in choro_thic_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#stat_peri_mean_sens_hfa24_2_left
	row_num += 2
	ws.write(row_num, 0, 'Stat Peri Mean Sens Hfa24 2 Left', font_style)
	if stat_peri_mean_sens_hfa24_2_left:
		col_num = 1
		for data in stat_peri_mean_sens_hfa24_2_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_hfa24_2_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_hfa24_2_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#stat_peri_mean_sens_hfa24_2_right
	row_num += 2
	ws.write(row_num, 0, 'Stat Peri Mean Sens Hfa24 2 Right', font_style)
	if stat_peri_mean_sens_hfa24_2_right:
		col_num = 1
		for data in stat_peri_mean_sens_hfa24_2_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_hfa24_2_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_hfa24_2_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#stat_peri_mean_sens_clas_left
	row_num += 2
	ws.write(row_num, 0, 'Stat Peri Mean Sens Clas Left', font_style)
	if stat_peri_mean_sens_clas_left:
		col_num = 1
		for data in stat_peri_mean_sens_clas_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_clas_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_clas_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#stat_peri_mean_sens_clas_right
	row_num += 2
	ws.write(row_num, 0, 'Stat Peri Mean Sens Clas Right', font_style)
	if stat_peri_mean_sens_clas_right:
		col_num = 1
		for data in stat_peri_mean_sens_clas_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_clas_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in stat_peri_mean_sens_clas_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#electro_left
	row_num += 2
	ws.write(row_num, 0, 'Electro Left', font_style)
	if electro_left:
		col_num = 1
		for data in electro_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in electro_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in electro_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#electro_right
	row_num += 2
	ws.write(row_num, 0, 'Electro Right', font_style)
	if electro_right:
		col_num = 1
		for data in electro_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in electro_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in electro_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#full_field_electphysiol_clas_left
	row_num += 2
	ws.write(row_num, 0, 'Full Field Electphysiol Clas Left', font_style)
	if full_field_electphysiol_clas_left:
		col_num = 1
		for data in full_field_electphysiol_clas_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in full_field_electphysiol_clas_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in full_field_electphysiol_clas_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#full_field_electphysiol_clas_right
	row_num += 2
	ws.write(row_num, 0, 'Full Field Electphysiol Clas Right', font_style)
	if full_field_electphysiol_clas_right:
		col_num = 1
		for data in full_field_electphysiol_clas_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in full_field_electphysiol_clas_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in full_field_electphysiol_clas_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#multi_electphysiol_clas_left
	row_num += 2
	ws.write(row_num, 0, 'Multi Electphysiol Clas Left', font_style)
	if multi_electphysiol_clas_left:
		col_num = 1
		for data in multi_electphysiol_clas_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in multi_electphysiol_clas_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in multi_electphysiol_clas_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#multi_electphysiol_clas_right
	row_num += 2
	ws.write(row_num, 0, 'Multi Electphysiol Clas Right', font_style)
	if multi_electphysiol_clas_right:
		col_num = 1
		for data in multi_electphysiol_clas_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in multi_electphysiol_clas_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in multi_electphysiol_clas_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#electroneg_config_of_dark_apa
	row_num += 2
	ws.write(row_num, 0, 'Electroneg Config Of Dark Apa', font_style)
	if electroneg_config_of_dark_apa:
		col_num = 1
		for data in electroneg_config_of_dark_apa:
			if data.fieldvalue:
				value = data.other
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in electroneg_config_of_dark_apa:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in electroneg_config_of_dark_apa:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diagnosis_for_others_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diagnosis For Others Left', font_style)
	if ai_diagnosis_for_others_left:
		col_num = 1
		for data in ai_diagnosis_for_others_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnosis_for_others_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnosis_for_others_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diagnosis_for_others_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diagnosis For Others Right', font_style)
	if ai_diagnosis_for_others_right:
		col_num = 1
		for data in ai_diagnosis_for_others_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnosis_for_others_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnosis_for_others_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accuracy_for_others_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accuracy For Others Left Per', font_style)
	if ai_accuracy_for_others_left_per:
		col_num = 1
		for data in ai_accuracy_for_others_left_per:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accuracy_for_others_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accuracy_for_others_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accuracy_for_others_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accuracy For Others Right Per', font_style)
	if ai_accuracy_for_others_right_per:
		col_num = 1
		for data in ai_accuracy_for_others_right_per:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accuracy_for_others_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accuracy_for_others_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_comments
	row_num += 2
	ws.write(row_num, 0, 'Ai Comments', font_style)
	if ai_comments:
		col_num = 1
		for data in ai_comments:
			if data.fieldvalue:
				value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_comments:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_comments:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#PatientGeneralInfoOphthalmologySystAbnormalityInfo
	row_num += 2
	ws.write(row_num, 0, 'Systemic Abnormality Name', font_style)
	if PatientGeneralInfoOphthalmologySystAbnormalityInfo:
		col_num = 1
		for data in PatientGeneralInfoOphthalmologySystAbnormalityInfo:
			if data.name:
				if data.other != "":
					value = data.other
				else:
					value = data.name.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in PatientGeneralInfoOphthalmologySystAbnormalityInfo:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in PatientGeneralInfoOphthalmologySystAbnormalityInfo:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#PatientGeneralInfoOphthalmologyOcularCompliInfo
	row_num += 2
	ws.write(row_num, 0, 'Ocular Symptom Name', font_style)
	if PatientGeneralInfoOphthalmologyOcularCompliInfo:
		col_num = 1
		for data in PatientGeneralInfoOphthalmologyOcularCompliInfo:
			if data.name:
				if data.other != "":
					value = data.other
				else:
					value = data.name.name
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in PatientGeneralInfoOphthalmologyOcularCompliInfo:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in PatientGeneralInfoOphthalmologyOcularCompliInfo:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)


	#Export Step 3 End

	#Export Step 4 Start

	ophthalmology_multi_static_http_url = prefix + request.get_host() + "/media/ophthalmology/multi_visit_ophthalmology_images/"
	ws = wb.add_sheet('Ophthalmology Images')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Value']
	custom_width = 50
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		if col_num == 0:
			ws.col(col_num).width = int(50*260)

	font_style = xlwt.XFStyle()
	for step4_images_all in PatientGeneralInfoMultiVisitOphthalmologyImagesInfo:
		if PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[step4_images_all]:
			custom_width = 100
			row_num += 2
			ws.write(row_num, 0, step4_images_all.replace("_"," ").title(), font_style)
			col_num = 1
			for step4_images_all1 in PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[step4_images_all]:
				if step4_images_all1.value:
					value =  ophthalmology_multi_static_http_url + str(step4_images_all1.value)
				else:
					value = 'No Entry Found'
				col_num += 1
				if col_num == 2:
					ws.write(row_num, 1, 'Image', font_style)
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num, value, font_style)
			col_num = 1
			row_num += 1
			for step4_images_all1 in PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[step4_images_all]:
				if step4_images_all1.date:
					date = step4_images_all1.date
				else:
					date = 'No Entry Found'
				col_num += 1
				if col_num == 2:
					ws.write(row_num, 1, 'Date', font_style)
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num, date, font_style)
			col_num = 1
			row_num += 1
			for step4_images_all1 in PatientGeneralInfoMultiVisitOphthalmologyImagesInfo[step4_images_all]:
				if step4_images_all1.comments:
					comments = step4_images_all1.comments
				else:
					comments = 'No Entry Found'
				col_num += 1
				if col_num == 2:
					ws.write(row_num, 1, 'Comment', font_style)
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num, comments, font_style)
		else:
			col_num = 1
			col_num += 1
			row_num += 2
			ws.write(row_num, 0, step4_images_all.replace("_"," ").title(), font_style)
			ws.write(row_num, 1, 'Image', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, 'No Entry Found', font_style)
			row_num += 1
			ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, 'No Entry Found', font_style)
			row_num += 1
			ws.write(row_num, 1, 'Comment', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, 'No Entry Found', font_style)

	#Export Step 4 End
	#Export Step 5 Start
	ws = wb.add_sheet('AI Diagnosis & Ophthalmology')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Value']
	custom_width = 50
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		if col_num == 0:
			ws.col(col_num).width = int(custom_width*260)

	font_style = xlwt.XFStyle()

	#ai_diag_corn_dise_corn_phot_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Corn Dise Corn Phot Left', font_style)
	if ai_diag_corn_dise_corn_phot_left:
		col_num = 1
		for data in ai_diag_corn_dise_corn_phot_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_corn_dise_corn_phot_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Corn Dise Corn Phot Right', font_style)
	if ai_diag_corn_dise_corn_phot_right:
		col_num = 1
		for data in ai_diag_corn_dise_corn_phot_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_corn_diag_corn_phot_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Corn Diag Corn Phot Left Per', font_style)
	if ai_accu_corn_diag_corn_phot_left_per:
		col_num = 1
		for data in ai_accu_corn_diag_corn_phot_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_corn_diag_corn_phot_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Corn Diag Corn Phot Right Per', font_style)
	if ai_accu_corn_diag_corn_phot_right_per:
		col_num = 1
		for data in ai_accu_corn_diag_corn_phot_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_corn_dise_corn_phot_on_fluo_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Corn Dise Corn Phot On Fluo Left', font_style)
	if ai_diag_corn_dise_corn_phot_on_fluo_left:
		col_num = 1
		for data in ai_diag_corn_dise_corn_phot_on_fluo_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_on_fluo_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_on_fluo_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_corn_dise_corn_phot_on_fluo_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Corn Dise Corn Phot On Fluo Right', font_style)
	if ai_diag_corn_dise_corn_phot_on_fluo_right:
		col_num = 1
		for data in ai_diag_corn_dise_corn_phot_on_fluo_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_on_fluo_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_corn_dise_corn_phot_on_fluo_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_corn_diag_corn_phot_on_fluo_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Corn Diag Corn Phot On Fluo Left Per', font_style)
	if ai_accu_corn_diag_corn_phot_on_fluo_left_per:
		col_num = 1
		for data in ai_accu_corn_diag_corn_phot_on_fluo_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_on_fluo_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_on_fluo_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_corn_diag_corn_phot_on_fluo_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Corn Diag Corn Phot On Fluo Right Per', font_style)
	if ai_accu_corn_diag_corn_phot_on_fluo_right_per:
		col_num = 1
		for data in ai_accu_corn_diag_corn_phot_on_fluo_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_on_fluo_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_corn_diag_corn_phot_on_fluo_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_glau_fundus_phot_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Glau Fundus Phot Left', font_style)
	if ai_diag_glau_fundus_phot_left:
		col_num = 1
		for data in ai_diag_glau_fundus_phot_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_fundus_phot_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_fundus_phot_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_glau_fundus_phot_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Glau Fundus Phot Right', font_style)
	if ai_diag_glau_fundus_phot_right:
		col_num = 1
		for data in ai_diag_glau_fundus_phot_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_fundus_phot_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_fundus_phot_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_glau_fundus_phot_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Glau Fundus Phot Left Per', font_style)
	if ai_accu_glau_fundus_phot_left_per:
		col_num = 1
		for data in ai_accu_glau_fundus_phot_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_fundus_phot_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_fundus_phot_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_glau_fundus_phot_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Glau Fundus Phot Right Per', font_style)
	if ai_accu_glau_fundus_phot_right_per:
		col_num = 1
		for data in ai_accu_glau_fundus_phot_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_fundus_phot_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_fundus_phot_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_glau_opti_cohe_tomo_disc_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Glau Opti Cohe Tomo Disc Left', font_style)
	if ai_diag_glau_opti_cohe_tomo_disc_left:
		col_num = 1
		for data in ai_diag_glau_opti_cohe_tomo_disc_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_opti_cohe_tomo_disc_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_opti_cohe_tomo_disc_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_glau_opti_cohe_tomo_disc_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Glau Opti Cohe Tomo Disc Right', font_style)
	if ai_diag_glau_opti_cohe_tomo_disc_right:
		col_num = 1
		for data in ai_diag_glau_opti_cohe_tomo_disc_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_opti_cohe_tomo_disc_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_opti_cohe_tomo_disc_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_glau_opti_cohe_tomo_disc_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Glau Opti Cohe Tomo Disc Left Per', font_style)
	if ai_accu_glau_opti_cohe_tomo_disc_left_per:
		col_num = 1
		for data in ai_accu_glau_opti_cohe_tomo_disc_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_opti_cohe_tomo_disc_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_opti_cohe_tomo_disc_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_glau_opti_cohe_tomo_disc_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Glau Opti Cohe Tomo Disc Right Per', font_style)
	if ai_accu_glau_opti_cohe_tomo_disc_right_per:
		col_num = 1
		for data in ai_accu_glau_opti_cohe_tomo_disc_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_opti_cohe_tomo_disc_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_opti_cohe_tomo_disc_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_glau_static_visual_field_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Glau Static Visual Field Left', font_style)
	if ai_diag_glau_static_visual_field_left:
		col_num = 1
		for data in ai_diag_glau_static_visual_field_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_static_visual_field_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_static_visual_field_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_glau_static_visual_field_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Glau Static Visual Field Right', font_style)
	if ai_diag_glau_static_visual_field_right:
		col_num = 1
		for data in ai_diag_glau_static_visual_field_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_static_visual_field_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_glau_static_visual_field_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_glau_static_visual_field_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Glau Static Visual Field Left Per', font_style)
	if ai_accu_glau_static_visual_field_left_per:
		col_num = 1
		for data in ai_accu_glau_static_visual_field_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_static_visual_field_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_static_visual_field_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_glau_static_visual_field_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Glau Static Visual Field Right Per', font_style)
	if ai_accu_glau_static_visual_field_right_per:
		col_num = 1
		for data in ai_accu_glau_static_visual_field_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_static_visual_field_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_glau_static_visual_field_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_diab_retino_fundus_phot_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Diab Retino Fundus Phot Left', font_style)
	if ai_diag_diab_retino_fundus_phot_left:
		col_num = 1
		for data in ai_diag_diab_retino_fundus_phot_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_fundus_phot_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_fundus_phot_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_diab_retino_fundus_phot_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Diab Retino Fundus Phot Right', font_style)
	if ai_diag_diab_retino_fundus_phot_right:
		col_num = 1
		for data in ai_diag_diab_retino_fundus_phot_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_fundus_phot_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_fundus_phot_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_diab_retino_fundus_phot_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Diab Retino Fundus Phot Left Per', font_style)
	if ai_accu_diab_retino_fundus_phot_left_per:
		col_num = 1
		for data in ai_accu_diab_retino_fundus_phot_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fundus_phot_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fundus_phot_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_diab_retino_fundus_phot_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Diab Retino Fundus Phot Right Per', font_style)
	if ai_accu_diab_retino_fundus_phot_right_per:
		col_num = 1
		for data in ai_accu_diab_retino_fundus_phot_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fundus_phot_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fundus_phot_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diagnsis_diab_retino_fluo_angio_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diagnsis Diab Retino Fluo Angio Left', font_style)
	if ai_diagnsis_diab_retino_fluo_angio_left:
		col_num = 1
		for data in ai_diagnsis_diab_retino_fluo_angio_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnsis_diab_retino_fluo_angio_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnsis_diab_retino_fluo_angio_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diagnsis_diab_retino_fluo_angio_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diagnsis Diab Retino Fluo Angio Right', font_style)
	if ai_diagnsis_diab_retino_fluo_angio_right:
		col_num = 1
		for data in ai_diagnsis_diab_retino_fluo_angio_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnsis_diab_retino_fluo_angio_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diagnsis_diab_retino_fluo_angio_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_diab_retino_fluo_angio_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Diab Retino Fluo Angio Left Per', font_style)
	if ai_accu_diab_retino_fluo_angio_left_per:
		col_num = 1
		for data in ai_accu_diab_retino_fluo_angio_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fluo_angio_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fluo_angio_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_diab_retino_fluo_angio_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Diab Retino Fluo Angio Right Per', font_style)
	if ai_accu_diab_retino_fluo_angio_right_per:
		col_num = 1
		for data in ai_accu_diab_retino_fluo_angio_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fluo_angio_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_fluo_angio_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Diab Retino Opti Cohe Tomo Macula 3d left', font_style)
	if ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left:
		col_num = 1
		for data in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Diab Retino Opti Cohe Tomo Macula 3d Right', font_style)
	if ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right:
		col_num = 1
		for data in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_diab_retino_opti_cohe_tomo_macula_3d_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Diab Retino Opti Cohe Tomo Macula 3d Left Per', font_style)
	if ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per:
		col_num = 1
		for data in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Diab Retino Opti Cohe Tomo Macula 3d Right Per', font_style)
	if ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per:
		col_num = 1
		for data in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_diab_retino_opti_cohe_tomo_macula_3d_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_fundus_phot_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Fundus Phot Left', font_style)
	if ai_diag_age_relat_macu_degen_fundus_phot_left:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_fundus_phot_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fundus_phot_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fundus_phot_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_fundus_phot_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Fundus Phot Right', font_style)
	if ai_diag_age_relat_macu_degen_fundus_phot_right:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_fundus_phot_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fundus_phot_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fundus_phot_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_fundus_phot_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Fundus Phot Left Per', font_style)
	if ai_accu_age_relat_macu_degen_fundus_phot_left_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_fundus_phot_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fundus_phot_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fundus_phot_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_fundus_phot_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Fundus Phot Right Per', font_style)
	if ai_accu_age_relat_macu_degen_fundus_phot_right_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_fundus_phot_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fundus_phot_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fundus_phot_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_fluo_angio_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Fluo Angio Left', font_style)
	if ai_diag_age_relat_macu_degen_fluo_angio_left:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_fluo_angio_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fluo_angio_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fluo_angio_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_fluo_angio_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Fluo Angio Right', font_style)
	if ai_diag_age_relat_macu_degen_fluo_angio_right:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_fluo_angio_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fluo_angio_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_fluo_angio_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_fluo_angio_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Fluo Angio Left Per', font_style)
	if ai_accu_age_relat_macu_degen_fluo_angio_left_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_fluo_angio_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fluo_angio_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fluo_angio_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_fluo_angio_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Fluo Angio Right Per', font_style)
	if ai_accu_age_relat_macu_degen_fluo_angio_right_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_fluo_angio_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fluo_angio_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_fluo_angio_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_indocy_green_angio_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Indocy Green Angio Left', font_style)
	if ai_diag_age_relat_macu_degen_indocy_green_angio_left:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_indocy_green_angio_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_indocy_green_angio_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_indocy_green_angio_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_indocy_green_angio_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Indocy Green Angio Right', font_style)
	if ai_diag_age_relat_macu_degen_indocy_green_angio_right:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_indocy_green_angio_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_indocy_green_angio_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_indocy_green_angio_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_indocy_green_angio_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Indocy Green Angio Left Per', font_style)
	if ai_accu_age_relat_macu_degen_indocy_green_angio_left_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_indocy_green_angio_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_indocy_green_angio_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_indocy_green_angio_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_indocy_green_angio_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Indocy Green Angio Right Per', font_style)
	if ai_accu_age_relat_macu_degen_indocy_green_angio_right_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_indocy_green_angio_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_indocy_green_angio_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_indocy_green_angio_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Opti Cohe Tomo Macula 3d Left', font_style)
	if ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Age Relat Macu Degen Opti Cohe Tomo Macula 3d Right', font_style)
	if ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right:
		col_num = 1
		for data in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Opti Cohe Tomo Macula 3d Left Per', font_style)
	if ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Age Relat Macu Degen Opti Cohe Tomo Macula 3d Right Per', font_style)
	if ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per:
		col_num = 1
		for data in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_age_relat_macu_degen_opti_cohe_tomo_macula_3d_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_fundus_phot_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Fundus Phot Left', font_style)
	if ai_diag_inheri_retin_dise_fundus_phot_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_fundus_phot_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_phot_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_phot_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_fundus_phot_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Fundus Phot Right', font_style)
	if ai_diag_inheri_retin_dise_fundus_phot_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_fundus_phot_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_phot_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_phot_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_fundus_phot_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Fundus Phot Left Per', font_style)
	if ai_accu_inheri_retin_dise_fundus_phot_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_fundus_phot_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_phot_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_phot_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_fundus_phot_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Fundus Phot Right Per', font_style)
	if ai_accu_inheri_retin_dise_fundus_phot_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_fundus_phot_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_phot_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_phot_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Fundus Autofluo Wide Field Left', font_style)
	if ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Fundus Autofluo Wide Field Right', font_style)
	if ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_fundus_autofluo_wide_field_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Fundus Autofluo Wide Field Left Per', font_style)
	if ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Fundus Autofluo Wide Field Right Per', font_style)
	if ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_fundus_autofluo_wide_field_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Opti Cohe Tomo Macula Line Left', font_style)
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Opti Cohe Tomo Macula Line Right', font_style)
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_line_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Opti Cohe Tomo Macula Line Left Per', font_style)
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Opti Cohe Tomo Macula Line Right Per', font_style)
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_line_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Opti Cohe Tomo Macula Face Left', font_style)
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Opti Cohe Tomo Macula Face Right', font_style)
	if ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_opti_cohe_tomo_macula_face_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Opti Cohe Tomo Macula Face Left Per', font_style)
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Opti Cohe Tomo Macula Face Right Per', font_style)
	if ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_opti_cohe_tomo_macula_face_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_full_field_electroret_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Full Field Electroret Left', font_style)
	if ai_diag_inheri_retin_dise_full_field_electroret_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_full_field_electroret_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_full_field_electroret_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_full_field_electroret_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_full_field_electroret_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Full Field Electroret Right', font_style)
	if ai_diag_inheri_retin_dise_full_field_electroret_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_full_field_electroret_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_full_field_electroret_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_full_field_electroret_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_full_field_electroret_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Full Field Electroret Left Per', font_style)
	if ai_accu_inheri_retin_dise_full_field_electroret_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_full_field_electroret_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_full_field_electroret_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_full_field_electroret_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_full_field_electroret_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Full Field Electroret Right Per', font_style)
	if ai_accu_inheri_retin_dise_full_field_electroret_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_full_field_electroret_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_full_field_electroret_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_full_field_electroret_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_multifocal_electroret_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Multifocal Electroret Left', font_style)
	if ai_diag_inheri_retin_dise_multifocal_electroret_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_multifocal_electroret_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_multifocal_electroret_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_multifocal_electroret_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_multifocal_electroret_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Multifocal Electroret Right', font_style)
	if ai_diag_inheri_retin_dise_multifocal_electroret_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_multifocal_electroret_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_multifocal_electroret_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_multifocal_electroret_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_multifocal_electroret_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Multifocal Electroret Left Per', font_style)
	if ai_accu_inheri_retin_dise_multifocal_electroret_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_multifocal_electroret_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_multifocal_electroret_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_multifocal_electroret_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_multifocal_electroret_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Multifocal Electroret Right Per', font_style)
	if ai_accu_inheri_retin_dise_multifocal_electroret_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_multifocal_electroret_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_multifocal_electroret_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_multifocal_electroret_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_vcf_files_left
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Vcf Files Left', font_style)
	if ai_diag_inheri_retin_dise_vcf_files_left:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_vcf_files_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_vcf_files_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_vcf_files_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_diag_inheri_retin_dise_vcf_files_right
	row_num += 2
	ws.write(row_num, 0, 'Ai Diag Inheri Retin Dise Vcf Files Right', font_style)
	if ai_diag_inheri_retin_dise_vcf_files_right:
		col_num = 1
		for data in ai_diag_inheri_retin_dise_vcf_files_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_vcf_files_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_diag_inheri_retin_dise_vcf_files_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_vcf_files_left_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Vcf Files Left Per', font_style)
	if ai_accu_inheri_retin_dise_vcf_files_left_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_vcf_files_left_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_vcf_files_left_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_vcf_files_left_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_vcf_files_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Vcf Files Right Per', font_style)
	if ai_accu_inheri_retin_dise_vcf_files_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ai_accu_inheri_retin_dise_vcf_files_right_per
	row_num += 2
	ws.write(row_num, 0, 'Ai Accu Inheri Retin Dise Vcf Files Right Per', font_style)
	if ai_accu_inheri_retin_dise_vcf_files_right_per:
		col_num = 1
		for data in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'value', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Comments', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)
		col_num = 1
		row_num += 1
		for data in ai_accu_inheri_retin_dise_vcf_files_right_per:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			col_num += 1
			if col_num == 2:
				ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, value, font_style)

	else:
		col_num = 1
		value = 'No Entry Found'
		ws.col(col_num).width = int(custom_width*260)
		ws.write(row_num, col_num, value, font_style)

	#ocul_surgeries_cornea_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Cornea Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_cornea_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_cornea_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Cornea Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_corneal_surgery_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Corneal Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_corneal_surgery_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_corneal_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Corneal Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_corneal_surgery_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Corneal Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_corneal_surgery_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_corneal_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Corneal Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_glaucoma_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Glaucoma Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_glaucoma_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_glaucoma_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Glaucoma Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_glaucoma_surgery_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Glaucoma Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_glaucoma_surgery_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_glaucoma_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Glaucoma Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_glaucomal_surgery_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Glaucomal Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_glaucomal_surgery_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_glaucomal_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Glaucomal Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_retina_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Retina Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_retina_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_retina_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Retina Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_vitreoretina_surgery_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Vitreoretina Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_vitreoretina_surgery_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_vitreoretina_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Vitreoretina Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_vitreoretinal_surgery_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Vitreoretinal Surgery Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_vitreoretinal_surgery_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_vitreoretinal_surgery_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Vitreoretinal Surgery Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_lasers_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Lasers Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_surgeries_lasers_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_surgeries_lasers_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Surgeries Lasers Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_ocul_surgeries_lasers_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Ocul Surgeries Lasers Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_ocul_surgeries_lasers_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_surgeries_lasers_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Ocul Surgeries Lasers Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_ofocul_surgeries_lasers_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Ofocul Surgeries Lasers Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_ofocul_surgeries_lasers_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ofocul_surgeries_lasers_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Ofocul Surgeries Lasers Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#opht_medi_subtenon_subconj_injec_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Opht Medi Subtenon Subconj Injec Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#opht_medi_subtenon_subconj_injec_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.opht_medi_subtenon_subconj_injec_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Opht Medi Subtenon Subconj Injec Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_opht_medi_subtenon_subconj_injec_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Opht Medi Subtenon Subconj Injec Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_opht_medi_subtenon_subconj_injec_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_opht_medi_subtenon_subconj_injec_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Opht Medi Subtenon Subconj Injec Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_opht_medi_subtenon_subconj_injec_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Opht Medi Subtenon Subconj Injec Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_opht_medi_subtenon_subconj_injec_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_opht_medi_subtenon_subconj_injec_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Opht Medi Subtenon Subconj Injec Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_medi_internal_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Medi Internal Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_medi_internal_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_internal_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Medi Internal Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_ocul_medi_internal_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Ocul Medi Internal Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_ocul_medi_internal_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_internal_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Ocul Medi Internal Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_ocul_medi_internal_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Ocul Medi Internal Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_ocul_medi_internal_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_internal_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Ocul Medi Internal Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_medi_topical_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Medi Topical Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#ocul_medi_topical_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.ocul_medi_topical_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Ocul Medi Topical Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_ocul_medi_topical_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Ocul Medi Topical Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#age_ocul_medi_topical_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.age_ocul_medi_topical_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Age Ocul Medi Topical Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_ocul_medi_topical_perf_left
	row_num += 2
	if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_left_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Ocul Medi Topical Perf Left', font_style)
	ws.write(row_num, 1, value, font_style)

	#no_ocul_medi_topical_perf_right
	row_num += 1
	if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right:
		if PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other == None or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other == "None" or PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other == "":
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right.name
		else:
			value = PatientOtherUncommonInfoOphthalmologyInfo.no_ocul_medi_topical_perf_right_other
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'No Ocul Medi Topical Perf Right', font_style)
	ws.write(row_num, 1, value, font_style)


	#Export Step 5 End

	#Export Step 6 Start

	ophthalmology_multi_static_http_url = prefix + request.get_host() + "/media/ophthalmology/multi_visit_ophthalmology_images/"
	ws = wb.add_sheet('Other Images')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Value']
	custom_width = 50
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		if col_num == 0:
			ws.col(col_num).width = int(50*260)

	font_style = xlwt.XFStyle()
	for step4_images_all in PatientOtherMultiVisitImagesInfo:
		if PatientOtherMultiVisitImagesInfo[step4_images_all]:
			custom_width = 100
			row_num += 2
			ws.write(row_num, 0, step4_images_all.replace("_"," ").title(), font_style)
			col_num = 1
			for step4_images_all1 in PatientOtherMultiVisitImagesInfo[step4_images_all]:
				if step4_images_all1.value:
					value =  ophthalmology_multi_static_http_url + str(step4_images_all1.value)
				else:
					value = 'No Entry Found'
				col_num += 1
				if col_num == 2:
					ws.write(row_num, 1, 'Image', font_style)
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num, value, font_style)
			col_num = 1
			row_num += 1
			for step4_images_all1 in PatientOtherMultiVisitImagesInfo[step4_images_all]:
				if step4_images_all1.date:
					date = step4_images_all1.date
				else:
					date = 'No Entry Found'
				col_num += 1
				if col_num == 2:
					ws.write(row_num, 1, 'Date', font_style)
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num, date, font_style)
			col_num = 1
			row_num += 1
			for step4_images_all1 in PatientOtherMultiVisitImagesInfo[step4_images_all]:
				if step4_images_all1.comments:
					comments = step4_images_all1.comments
				else:
					comments = 'No Entry Found'
				col_num += 1
				if col_num == 2:
					ws.write(row_num, 1, 'Comment', font_style)
				ws.col(col_num).width = int(custom_width*260)
				ws.write(row_num, col_num, comments, font_style)
		else:
			row_num += 2
			col_num = 1
			col_num += 1
			ws.write(row_num, 0, step4_images_all.replace("_"," ").title(), font_style)
			ws.write(row_num, 1, 'Image', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, 'No Entry Found', font_style)
			row_num += 1
			ws.write(row_num, 1, 'Date', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, 'No Entry Found', font_style)
			row_num += 1
			ws.write(row_num, 1, 'Comment', font_style)
			ws.col(col_num).width = int(custom_width*260)
			ws.write(row_num, col_num, 'No Entry Found', font_style)

	#Export Step 6 End

	#Export Step 7 Start
	ws = wb.add_sheet('All Comments')


	row_num = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Name','Value']
	custom_width = 50
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		if col_num == 1:
			ws.col(col_num).width = int(50*260)

	font_style = xlwt.XFStyle()
	#overall_comments
	row_num += 1
	if PatientGeneralInfoDetial.overall_comments:
		value = PatientGeneralInfoDetial.overall_comments
	else:
		value = 'No Entry Found'
	ws.write(row_num, 0, 'Overall Comments', font_style)
	ws.write(row_num, 1, value, font_style)

	#Export Step 7 End


	wb.save(response)
	return response
	return HttpResponse(id)
 

@login_required(login_url='/')
def get_institude_data_on_grap(request):
	data = {}
	institude_name = request.GET.get('institude_name', None)
	institute_id_data	=	InstituteDt.objects.filter(name=institude_name).values("id").first();
	institute_id = institute_id_data["id"]
	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					#print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data
	if request.user.is_superuser == 1:
		if institute_id != 0:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(is_draft=1).filter(institute_id=institute_id).all()
		
	else:
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(is_draft=1).filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		

		if institute_id != 0:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(institute_id=institute_id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).all()
		
		#print(PatientGeneralInfoDetial.query)

	if PatientGeneralInfoDetial:
		for PatientGeneralInfoDetial1 in PatientGeneralInfoDetial:
			family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial1.id).values("family_id").first();
			if family_detail:
				PatientGeneralInfoDetial1.family_id = family_detail["family_id"]
			else:
				PatientGeneralInfoDetial1.family_id = ''
	family_id = 0
	context		=	{
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial,
		"family_id":family_id,
		"institute_id":institute_id,
	}
	return render(request, 'ophthalmology/institude_data_on_grap.html',context)
	
@login_required(login_url='/')
def get_sub_disease_data_on_grap(request):
	data = {}
	disease_name = request.GET.get('disease_name', None)
	
	disease_id_data	=	DiseaseDt.objects.filter(name__contains=disease_name).first();
	disease_id = disease_id_data.id
	
	#left menu bar query data
	userAssignedDiseases = 	DoctorDisease.objects.filter(user_id=request.user.id).first()
	assignedDiseases	 =	AdminDiseaseDt.objects.all()
	if assignedDiseases:
		for AdminDiseaseDtDetail in assignedDiseases:
			if request.user.is_superuser == 1:
				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(disease_id=AdminDiseaseDtDetail.id).all();
			else:
				if userAssignedDiseases:
					AssignedDiseases	=	userAssignedDiseases.disease.values("id")
					#print(AssignedDiseases)
				else:
					AssignedDiseases	=	[]

				AdminDiseaseDtDetail.SubDiseases = AdminSubDiseaseDt.objects.filter(id__in=AssignedDiseases).filter(disease_id=AdminDiseaseDtDetail.id).all();
	#left menu bar query data
	
	SubDiseaseDts	=	SubDiseaseDt.objects.filter(disease_id=disease_id).order_by("-name").all()
	#return HttpResponse(allMonths)
	
	colors =  ["#63b598", "#ce7d78", "#ea9e70", "#a48a9e", "#c6e1e8", "#648177" ,"#0d5ac1" ,"#f205e6" ,"#1c0365" ,"#14a9ad" ,"#4ca2f9" ,"#a4e43f" ,"#d298e2" ,"#6119d0","#d2737d" ,"#c0a43c" ,"#f2510e" ,"#651be6" ,"#79806e" ,"#61da5e" ,"#cd2f00" ,"#9348af" ,"#01ac53" ,"#c5a4fb" ,"#996635","#b11573" ,"#4bb473" ,"#75d89e" ,"#2f3f94" ,"#2f7b99" ,"#da967d" ,"#34891f" ,"#b0d87b" ,"#ca4751" ,"#7e50a8" ,"#c4d647" ,"#e0eeb8" ,"#11dec1" ,"#289812" ,"#566ca0" ,"#ffdbe1" ,"#2f1179" ,"#935b6d" ,"#916988" ,"#513d98" ,"#aead3a", "#9e6d71", "#4b5bdc", "#0cd36d","#250662", "#cb5bea", "#228916", "#ac3e1b", "#df514a", "#539397", "#880977","#f697c1", "#ba96ce", "#679c9d", "#c6c42c", "#5d2c52", "#48b41b", "#e1cf3b","#5be4f0", "#57c4d8", "#a4d17a", "#225b8", "#be608b", "#96b00c", "#088baf","#f158bf", "#e145ba", "#ee91e3", "#05d371", "#5426e0", "#4834d0", "#802234","#6749e8", "#0971f0", "#8fb413", "#b2b4f0", "#c3c89d", "#c9a941", "#41d158","#fb21a3", "#51aed9", "#5bb32d", "#807fb", "#21538e", "#89d534", "#d36647","#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3","#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec","#1bb699", "#6b2e5f", "#64820f", "#1c271", "#21538e", "#89d534", "#d36647","#7fb411", "#0023b8", "#3b8c2a", "#986b53", "#f50422", "#983f7a", "#ea24a3","#79352c", "#521250", "#c79ed2", "#d6dd92", "#e33e52", "#b2be57", "#fa06ec","#1bb699", "#6b2e5f", "#64820f", "#1c271", "#9cb64a", "#996c48", "#9ab9b7","#06e052", "#e3a481", "#0eb621", "#fc458e", "#b2db15", "#aa226d", "#792ed8","#73872a", "#520d3a", "#cefcb8", "#a5b3d9", "#7d1d85", "#c4fd57", "#f1ae16","#8fe22a", "#ef6e3c", "#243eeb", "#1dc18", "#dd93fd", "#3f8473", "#e7dbce","#421f79", "#7a3d93", "#635f6d", "#93f2d7", "#9b5c2a", "#15b9ee", "#0f5997","#409188", "#911e20", "#1350ce", "#10e5b1", "#fff4d7", "#cb2582", "#ce00be","#32d5d6", "#17232", "#608572", "#c79bc2", "#00f87c", "#77772a", "#6995ba","#fc6b57", "#f07815", "#8fd883", "#060e27", "#96e591", "#21d52e", "#d00043","#b47162", "#1ec227", "#4f0f6f", "#1d1d58", "#947002", "#bde052", "#e08c56","#28fcfd", "#bb09b", "#36486a", "#d02e29", "#1ae6db", "#3e464c", "#a84a8f","#911e7e", "#3f16d9", "#0f525f", "#ac7c0a", "#b4c086", "#c9d730", "#30cc49","#3d6751", "#fb4c03", "#640fc1", "#62c03e", "#d3493a", "#88aa0b", "#406df9","#615af0", "#4be47", "#2a3434", "#4a543f", "#79bca0", "#a8b8d4", "#00efd4","#7ad236", "#7260d8", "#1deaa7", "#06f43a", "#823c59", "#e3d94c", "#dc1c06","#f53b2a", "#b46238", "#2dfff6", "#a82b89", "#1a8011", "#436a9f", "#1a806a","#4cf09d", "#c188a2", "#67eb4b", "#b308d3", "#fc7e41", "#af3101", "#ff065","#71b1f4", "#a2f8a5", "#e23dd0", "#d3486d", "#00f7f9", "#474893", "#3cec35","#1c65cb", "#5d1d0c", "#2d7d2a", "#ff3420", "#5cdd87", "#a259a4", "#e4ac44","#1bede6", "#8798a4", "#d7790f", "#b2c24f", "#de73c2", "#d70a9c", "#25b67","#88e9b8", "#c2b0e2", "#86e98f", "#ae90e2", "#1a806b", "#436a9e", "#0ec0ff","#f812b3", "#b17fc9", "#8d6c2f", "#d3277a", "#2ca1ae", "#9685eb", "#8a96c6","#dba2e6", "#76fc1b", "#608fa4", "#20f6ba", "#07d7f6", "#dce77a", "#77ecca"]
	
	
	
	if request.user.is_superuser == 1:
		if disease_id != 0:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(is_draft=1).filter(disease_id=disease_id).all()
			PatientGeneralInfoTotalCount	=	PatientGeneralInfo.objects.filter(is_draft=1).filter(disease_id=disease_id).count()
		
		counterDisease = 0 	
		for SubDiseaseDtdata in SubDiseaseDts:
			PatientGeneralInfoDiseaseCount = PatientGeneralInfo.objects.filter(is_draft=1).filter(sub_disease_id=SubDiseaseDtdata.id).count()
			
			if PatientGeneralInfoDiseaseCount:
				SubDiseaseDtdata.count	=	 round(int(PatientGeneralInfoDiseaseCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				SubDiseaseDtdata.count = '0'
			
			SubDiseaseDtdata.color		=	 colors[counterDisease]
			counterDisease  += 1
	else:
		
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		

		if disease_id != 0:
			PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(disease_id=disease_id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).all()
			
			PatientGeneralInfoTotalCount	=	PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(disease_id=disease_id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).count()
			
		counterDisease = 0 
		for SubDiseaseDtdata in SubDiseaseDts:
			PatientGeneralInfoSubDiseaseCount = PatientGeneralInfo.objects.filter(Q(is_draft=1) & Q(admin_sub_disease_id__in=AssignedDiseases) &(Q(sub_disease_id=SubDiseaseDtdata.id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).count()
			if PatientGeneralInfoSubDiseaseCount:
				SubDiseaseDtdata.count	=	 round(int(PatientGeneralInfoSubDiseaseCount * 100) / PatientGeneralInfoTotalCount,2)
			else:
				SubDiseaseDtdata.count = '0'
			
			SubDiseaseDtdata.color		=	 colors[counterDisease]
			counterDisease  += 1
		
		#print(PatientGeneralInfoDetial.query)

	if PatientGeneralInfoDetial:
		for PatientGeneralInfoDetial1 in PatientGeneralInfoDetial:
			family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial1.id).values("family_id").first();
			if family_detail:
				PatientGeneralInfoDetial1.family_id = family_detail["family_id"]
			else:
				PatientGeneralInfoDetial1.family_id = ''
				
	if SubDiseaseDts:
		for SubDiseaseDt1 in SubDiseaseDts:
			SubDiseaseDt1.name	=	SubDiseaseDt1.name.strip()
	
	family_id = 0
	institute_id = 0
	context		=	{
		"PatientGeneralInfoDetial":PatientGeneralInfoDetial,
		"family_id":family_id,
		"institute_id":institute_id,
		"SubDiseaseDts":SubDiseaseDts,
	}
	return render(request, 'ophthalmology/sub_disease_data_on_grap.html',context)
	
@login_required(login_url='/')
def export_patient_new(request,id):
	prefix = 'https://' if request.is_secure() else 'http://'
	ophthalmology_static_http_url = prefix + request.get_host() + "/static/ophthalmology/"

	#set permission doctor has access or not
	record = PatientGeneralInfo.objects.filter(id=id).first()
	if not record:
		return redirect('/ophthalmology/')

	if request.user.is_superuser != 1:
		whichDoctorDocumentCanSee	=	WhichDoctorDocumentCanSee.objects.filter(user_id=request.user.id).first()
		if whichDoctorDocumentCanSee:
			assignedDoctors				=	whichDoctorDocumentCanSee.doctor.values("id")
		else :
			assignedDoctors				=	[]

		PatientGeneralInfoDetial	=	PatientGeneralInfo.objects.filter(Q(admin_sub_disease_id__in=AssignedDiseases) & (Q(id=id) & ((Q(is_draft=1) & Q(user_id__in=assignedDoctors)) | Q(user_id=request.user.id)))).first()
		if not PatientGeneralInfoDetial:
			return redirect('/ophthalmology/')
	#set permission doctor has access or not

	PatientGeneralInfoDetial = PatientGeneralInfo.objects.filter(id=id).select_related("institute","relationship_to_proband","sex","disease","affected","inheritance","syndromic","bilateral","ocular_symptom_1","ocular_symptom_2","ocular_symptom_3","progression","flactuation","family_history","consanguineous","number_of_affected_members_in_the_same_pedigree","ethnicity","country_of_origine","origin_prefecture_in_japan","ethnic_of_father","original_country_of_father","origin_of_father_in_japan","ethnic_of_mother","original_country_of_mother","origin_of_mother_in_japan","gene_type","inheritance_type","mutation_type","dna_extraction_process","sequencing","analysis","sub_disease").first()

	family_detail = PatientGeneralInfoFamily.objects.filter(patient_id=PatientGeneralInfoDetial.id).values("family_id").first();
	if family_detail:
		PatientGeneralInfoDetial.family_id = family_detail["family_id"]
	else:
		PatientGeneralInfoDetial.family_id = ''

	PatientCausativeGeneInfo1	=	PatientCausativeGeneInfo.objects.filter(patient_id=id).all()
	if PatientCausativeGeneInfo1:
		for PatientCausativeGeneInfoData in PatientCausativeGeneInfo1:
			PatientCausativeGeneInfoData.leftAddMore		=	PatientCausativeGeneInfoEthnicity.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()
			PatientCausativeGeneInfoData.rightAddMore		=	PatientCausativeGeneInfoLocalPopulation.objects.filter(patient_causative_gene_info_id=PatientCausativeGeneInfoData.id).all()
			
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
			
	response = HttpResponse(content_type='application/ms-excel')
	if PatientGeneralInfoDetial.registration_id:
		response['Content-Disposition'] = 'attachment; filename="'+PatientGeneralInfoDetial.registration_id+'.xls"'
	else:
		response['Content-Disposition'] = 'attachment; filename="patient.xls"'

	wb = xlwt.Workbook(encoding='utf-8')

	##Export Step 1 Start
	ws = wb.add_sheet('General & Clinical Information')


	row_num = 0
	col_num_new = 0
	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Institude ID','Family ID','Sample ID','Logmar Visual Acuity Left value','Logmar Visual Acuity left comment','Logmar Visual Acuity left date','Logmar Visual Acuity Right value','Logmar Visual Acuity Right comment','Logmar Visual Acuity Right date','Type Old New','Caus Cand','Freq Ethnicity','Freq Ethnicity Percentage','Freq Local Population','Freq Local Population Percentage']
	custom_width = 60
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)
		ws.col(col_num).width = int(custom_width*260)

	font_style = xlwt.XFStyle()

	
	row_num += 1
	ws.write(row_num, col_num_new, PatientGeneralInfoDetial.institute.name, font_style)

	col_num_new += 1
	ws.write(row_num, col_num_new, PatientGeneralInfoDetial.family_id, font_style)

	col_num_new += 1
	ws.write(row_num, col_num_new, PatientGeneralInfoDetial.sample_id, font_style)

	#logmar_visual_acuity_left
	
	if logmar_visual_acuity_left:
		col_num_new += 1
		row_num_new = row_num
		for data in logmar_visual_acuity_left:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			
			
			ws.col(col_num_new).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new, value, font_style)
			row_num_new += 1

		col_num_new += 1
		row_num_new = row_num
		for data in logmar_visual_acuity_left:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			
			ws.col(col_num_new).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new, value, font_style)
			row_num_new += 1
			
		col_num_new += 1
		row_num_new = row_num
		for data in logmar_visual_acuity_left:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			
			
			ws.col(col_num_new).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new, value, font_style)
			row_num_new += 1
	else:
		col_num_new += 1
		value = 'No Entry Found'
		ws.col(col_num_new).width = int(custom_width*260)
		ws.write(row_num, col_num_new, value, font_style)
		col_num_new += 1
		value = 'No Entry Found'
		ws.col(col_num_new).width = int(custom_width*260)
		ws.write(row_num, col_num_new, value, font_style)
		col_num_new += 1
		value = 'No Entry Found'
		ws.col(col_num_new).width = int(custom_width*260)
		ws.write(row_num, col_num_new, value, font_style)
		
	#logmar_visual_acuity_right
	
	if logmar_visual_acuity_right:
		col_num_new += 1
		row_num_new = row_num
		for data in logmar_visual_acuity_right:
			if data.fieldvalue:
				if data.other != "":
					value = data.other
				else:
					value = data.fieldvalue
			else:
				value = 'No Entry Found'
			
			
			ws.col(col_num_new).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new, value, font_style)
			row_num_new += 1

		col_num_new += 1
		row_num_new = row_num
		for data in logmar_visual_acuity_right:
			if data.comments:
				value = data.comments
			else:
				value = 'No Entry Found'
			
			ws.col(col_num_new).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new, value, font_style)
			row_num_new += 1
			
		col_num_new += 1
		row_num_new = row_num
		for data in logmar_visual_acuity_right:
			if data.date:
				value = data.date
			else:
				value = 'No Entry Found'
			
			
			ws.col(col_num_new).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new, value, font_style)
			row_num_new += 1
	else:
		col_num_new += 1
		value = 'No Entry Found'
		ws.col(col_num_new).width = int(custom_width*260)
		ws.write(row_num, col_num_new, value, font_style)
		col_num_new += 1
		value = 'No Entry Found'
		ws.col(col_num_new).width = int(custom_width*260)
		ws.write(row_num, col_num_new, value, font_style)
		col_num_new += 1
		value = 'No Entry Found'
		ws.col(col_num_new).width = int(custom_width*260)
		ws.write(row_num, col_num_new, value, font_style)

	#PatientCausativeGeneInfo1
	col_num_new += 1
	row_num_new = row_num
	if PatientCausativeGeneInfo1:
			
		for datas in PatientCausativeGeneInfo1:
			col_num_new1 = col_num_new
			if datas.type_old_new:
				value = datas.type_old_new.name
			else:
				value = 'No Entry Found'
			
			ws.col(col_num_new1).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new1, value, font_style)	
			if datas.caus_cand:
				value = datas.caus_cand.name
			else:
				value = 'No Entry Found'
			col_num_new1 += 1
			ws.col(col_num_new1).width = int(custom_width*260)
			ws.write(row_num_new, col_num_new1, value, font_style)
			
			col_num_new1 += 1
			row_num_new1 = row_num_new
			if datas.leftAddMore:
				for datas1 in datas.leftAddMore:
					if datas1.freq_ethnicity_other != "":
						value = datas1.freq_ethnicity_other
					else:
						value = datas1.freq_ethnicity.name

					ws.col(col_num_new1).width = int(custom_width*260)
					ws.write(row_num_new1, col_num_new1, value, font_style)
					row_num_new1 += 1
			else:
				value = 'No Entry Found'
				ws.col(col_num_new1).width = int(custom_width*260)
				ws.write(row_num_new1, col_num_new1, value, font_style)
			col_num_new1 += 1
			row_num_new1 = row_num_new	
			if datas.leftAddMore:
				for datas1 in datas.leftAddMore:
					if datas1.freq_ethnicity_per != "":
						value = datas1.freq_ethnicity_per
					else:
						value = 'No Entry Found'
					ws.col(col_num_new1).width = int(custom_width*260)
					ws.write(row_num_new1, col_num_new1, value, font_style)
					row_num_new1 += 1
			else:
				value = 'No Entry Found'
				ws.col(col_num_new1).width = int(custom_width*260)
				ws.write(row_num_new1, col_num_new1, value, font_style)
			row_num_new = row_num_new1
			
		
	
			
	

	#Export Step 1 end
	wb.save(response)
	return response
	return HttpResponse(id)