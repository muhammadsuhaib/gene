from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import DoctorDisease,DoctorInstitute,WhichDoctorDocumentCanSee


class DoctorDiseaseInline(admin.StackedInline):
    model = DoctorDisease
    can_delete = False
    verbose_name_plural = 'Assigned Diseases'
    fk_name = 'user'
	
class DoctorInstituteInline(admin.StackedInline):
    model = DoctorInstitute
    can_delete = False
    verbose_name_plural = 'Assigned Institute'
    fk_name = 'user'
	
class WhichDoctorDocumentCanSeeInline(admin.StackedInline):
    model = WhichDoctorDocumentCanSee
    can_delete = False
    verbose_name_plural = 'Which doctor documents can see'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
	inlines = (DoctorDiseaseInline,DoctorInstituteInline,WhichDoctorDocumentCanSeeInline, )
	
	class Media:
		css = { "all" : ("admin/admin.css",) }


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
