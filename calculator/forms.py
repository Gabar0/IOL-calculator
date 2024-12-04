

from django import forms

class IOLCalculatorForm(forms.Form):
    patient_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(required=True, input_formats=['%Y-%m-%d', '%d/%m/%Y'])
    keratometric_index = forms.ChoiceField(choices=[('1.3375', '1.3375'), ('1.3315', '1.3315'), ('1.332', '1.332'), ('1.336', '1.336')], required=True)
    
    # Eye selection
    eye = forms.ChoiceField(choices=[('OD', 'Right Eye (OD)'), ('OS', 'Left Eye (OS)'), ('OU', 'Both eyes')], required=True)

    # OD Fields
    od_iol_model = forms.ChoiceField(choices=[('Alcon SA60AT', 'Alcon SA60AT'), ('Alcon SN60WF', 'Alcon SN60WF'), ('Zeiss 829M', 'Zeiss 829M'), ('Zeiss 621P', 'Zeiss 621P'), ('Other Model', 'Other Model')], required=False)
    od_a_constant = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    od_target_refraction = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    od_axial_length = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    od_ac_depth = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    od_k1_flat = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    od_k2_steep = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

    # OS Fields
    os_iol_model = forms.ChoiceField(choices=[('Alcon SA60AT', 'Alcon SA60AT'), ('Alcon SN60WF', 'Alcon SN60WF'), ('Zeiss 829M', 'Zeiss 829M'), ('Zeiss 621P', 'Zeiss 621P'), ('Other Model', 'Other Model')], required=False)
    os_a_constant = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    os_target_refraction = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    os_axial_length = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    os_ac_depth = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    os_k1_flat = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    os_k2_steep = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

    def clean(self):
        cleaned_data = super().clean()
        eye = cleaned_data.get('eye')

        if eye == 'OD':
            required_fields = ['od_iol_model', 'od_a_constant', 'od_axial_length', 'od_ac_depth', 'od_k1_flat', 'od_k2_steep']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for OD.')

        elif eye == 'OS':
            required_fields = ['os_iol_model', 'os_a_constant', 'os_axial_length', 'os_ac_depth', 'os_k1_flat', 'os_k2_steep']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for OS.')

        elif eye == 'OU':
            required_fields_od = ['od_iol_model', 'od_a_constant', 'od_axial_length', 'od_ac_depth', 'od_k1_flat', 'od_k2_steep']
            required_fields_os = ['os_iol_model', 'os_a_constant', 'os_axial_length', 'os_ac_depth', 'os_k1_flat', 'os_k2_steep']
            for field in required_fields_od:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for OD when both eyes are selected.')
            for field in required_fields_os:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for OS when both eyes are selected.')

        return cleaned_data


    


