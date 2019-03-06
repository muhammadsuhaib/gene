from django.urls import path,include
from . import views

app_name = 'ophthalmology'

urlpatterns = [
    path('', views.index, name='index'),
    path('ophthalmology/', views.index, name='index'),
    path('ophthalmology/import-dropdown-data', views.import_dropdown, name='import_dropdown'),
    path('add_new_patient/<selected_disease_id>', views.add_new_patient, name='add_new_patient'),
	path('ophthalmology/view_new_patient/<id>', views.view_new_patient, name='view_new_patient'),
	path('ophthalmology/edit_new_patient/<id>', views.edit_new_patient, name='edit_new_patient'),
	path('ophthalmology/delete_patient/<id>', views.delete_patient, name='delete_patient'),
	path('ophthalmology/export_patient/<id>', views.export_patient, name='export_patient'),
	path('ophthalmology/change_status/<id>/<status>', views.change_status, name='change_status'),
	path('view-profile/', views.view_profile, name='view_profile'),
	path('ajax/delete-addmore/', views.delete_addmore, name='delete_addmore'),
	path('ajax/delete-image/', views.delete_image, name='delete_image'),
	path('ajax/get-sub-disease/', views.get_sub_disease, name='get_sub_disease'),
	path('ajax/delete-addmore-section/', views.delete_addmore_section, name='delete_addmore_section'),
	path('ajax/get-institude-data-on-grap/', views.get_institude_data_on_grap, name='get_institude_data_on_grap'),
	path('ajax/get-sub-disease-data-on-grap/', views.get_sub_disease_data_on_grap, name='get_sub_disease_data_on_grap'),
	path('ophthalmology/delete-all-patient-data/', views.delete_all_patient_data, name='delete_all_patient_data'),
	path('ophthalmology/export_patient_new/<id>', views.export_patient_new, name='export_patient_new'),
]
