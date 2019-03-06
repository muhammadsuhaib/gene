from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from ophthalmology.models import InstituteDt,DiseaseDt,AdminSubDiseaseDt

@python_2_unicode_compatible
class DoctorDisease(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	disease = models.ManyToManyField(AdminSubDiseaseDt, blank=True, null=True,related_name='+')
	
	class Meta:
		db_table = 'doctor_assigned_diseases'
		verbose_name_plural = 'doctor_assigned_diseases'
		
		
@python_2_unicode_compatible
class DoctorInstitute(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.ForeignKey(InstituteDt,models.SET_NULL,blank=True,null=True)

    class Meta:
        db_table = 'doctor_institutes'
        verbose_name_plural = 'doctor_institutes'
		
		
@python_2_unicode_compatible
class WhichDoctorDocumentCanSee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	doctor = models.ManyToManyField(User, blank=True, null=True,related_name='+')
	class Meta:
		db_table = 'which_doctor_document_can_see'
		verbose_name_plural = 'which_doctor_document_can_see'
