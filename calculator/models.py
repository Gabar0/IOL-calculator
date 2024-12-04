from django.db import models

class Patient(models.Model):
    
    patient_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.patient_name

class IOLCalculation(models.Model):
    EYE_CHOICES = [
        ('OD', 'Right Eye'),
        ('OS', 'Left Eye'),
    ]
    
    patient_name = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    eye = models.CharField(max_length=2, choices=EYE_CHOICES, default='OD')
    iol_model = models.CharField(max_length=50)
    a_constant = models.DecimalField(max_digits=5, decimal_places=2)
    AL = models.DecimalField(max_digits=5, decimal_places=2)
    ACD = models.DecimalField(max_digits=5, decimal_places=2)
    K1 = models.DecimalField(max_digits=5, decimal_places=2)
    K2 = models.DecimalField(max_digits=5, decimal_places=2)
    Target_refraction = models.DecimalField(max_digits=5, decimal_places=2)
    iol_power = models.DecimalField(max_digits=5, decimal_places=2)
    REFRACTION= models.DecimalField(max_digits=5, decimal_places=2)
    calculation_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.patient_name} - {self.iol_model} - {self.eye}'


