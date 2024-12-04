from django.contrib import admin
from .models import Patient, IOLCalculation
from django.contrib.auth.models import Group


admin.site.site_header = "IOL Calculator Administration"
admin.site.site_title = "IOL Calculator"
admin.site.index_title = "Welcome to the IOL Calculator Admin"

class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'date_of_birth')  
    search_fields = ('patient_name','date_of_birth')

class IOLCalculationAdmin(admin.ModelAdmin):
    list_display = ('patient_name','eye','iol_model', 'a_constant', 'AL', 'ACD', 'K1', 'K2', 'Target_refraction', 'iol_power', 'REFRACTION', 'calculation_date')
    search_fields = (
        'patient_name__patient_name',  # Foreign key reference for patient name
        'eye',
        'iol_model', 
        'a_constant', 
        'AL', 
        'ACD', 
        'K1', 
        'K2', 
        'Target_refraction', 
        'iol_power', 
        'REFRACTION', 
        'calculation_date'
    )


admin.site.register(Patient, PatientAdmin)
admin.site.register(IOLCalculation, IOLCalculationAdmin)
admin.site.unregister(Group)

