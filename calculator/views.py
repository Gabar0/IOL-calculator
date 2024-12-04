# views.py

from django.shortcuts import render, redirect
from .forms import IOLCalculatorForm
from .utils.Logic import calculate_iol_power, SRKT_SE
from .models import IOLCalculation, Patient
from datetime import datetime
import requests
from xml.etree import ElementTree

def IOlSpecifications(request):
    if request.method == 'GET' and 'manufacturer' in request.GET and 'model' in request.GET:
        manufacturer = request.GET.get('manufacturer')
        model = request.GET.get('model')

        if not manufacturer or not model:
            return render(request, 'calculator/IOlSpecifications.html', {'error': 'Please select both manufacturer and model.'})

        model_to_id = {
            "1stQ 611HPS": 2299,
            "1stQ BASW00": 182,
            "Afidera Softec 1": 1087,
            "AJL Ophthalmic F601250": 160,
            "AJL Ophthalmic LLY360": 161,
            "AJL Ophthalmic LLY6002": 162,
            "AJL Ophthalmic P651300": 158,
            "AJL Ophthalmic Y601075": 163,
            "Alcon AcrySof MA50BM": 883,
            "Alcon AcrySof MA60AC": 882,
            "Alcon AcrySof MA60MA (+D)": 886,
            "Alcon AcrySof MA60MA (-D)": 887,
            "Alcon AcrySof MN60AC": 881,
            "Alcon AcrySof MN60MA (+D)": 884,
            "Alcon AcrySof MN60MA (-D)": 885,
            "Alcon AcrySof SA60AT": 879,
            "Alcon AcrySof SN60AT": 878,
            "Alcon PMMA MTA3U0": 888,
            "Alcon PMMA MTA4U0": 889,
            "Bausch + Lomb Akreos Adapt AO": 190,
            "Bausch + Lomb Eye-CEE": 198,
            "Biotech Europe Meditech Optiflex MPS6": 907,
            "Biotech Vision Care EYECRYL PLUS 600": 820,
            "Cristalens Lucis": 2287,
            "Hanita Lenses B-Lens": 707,
            "Hanita Lenses SeeLens": 708,
            "HOYA 150": 130,
            "HOYA 151": 131,
            "HOYA PC-60R": 134,
            "HOYA PY-60R": 135,
            "HOYA VA-60BB": 138,
            "HOYA VA-65BB": 139,
            "HOYA YA-60BB": 137,
            "HOYA YA-60BBR": 136,
            "HOYA YA-65BB": 140,
            "HumanOptics AS": 1632,
            "Johnson and Johnson Vision AAB00": 576,
            "Johnson and Johnson Vision AR40e": 700,
            "Johnson and Johnson Vision AR40E": 699,
            "Johnson and Johnson Vision AR40M": 698,
            "Lenstec Softec 1": 1090,
            "Ophtec AC 205": 653,
            "Ophtec AC 205 (duplicate)": 654,
            "PhysIOL Slimflex": 922,
            "Polytech Domilens Domicryl S+": 960,
            "Polytech Domilens Nidek Nex Acri": 965,
            "Polytech Domilens Nidek Nexload System NZ1": 966,
            "Polytech Domilens Wuxi MS60A": 1817,
            "Rayner RayOne Spheric": 892,
            "Teleon L-302-1": 1691,
            "Teleon L-303": 1709,
            "Teleon PCA81": 1828,
            "W2O Medizintechnik Care Flex II": 1118,
            "W2O Medizintechnik SDHB6130S": 1681,
            "ZEISS CT 13A": 991,
            "ZEISS CT 27SF <10 D": 992,
            "ZEISS CT 27SF >=10 D": 993,
            "ZEISS CT 47S": 996,
            "ZEISS CT LUCIA 201P": 1006,
            "ZEISS CT LUCIA 202": 1007,
            "ZEISS CT LUCIA 211P": 1008,
            "ZEISS CT LUCIA 211PY": 1009,
            "ZEISS CT LUCIA 221P": 1139,
            "ZEISS CT SPHERIS 203": 1864,
            "ZEISS CT SPHERIS 203P": 1863,
            "ZEISS CT SPHERIS 204": 1016,
            "ZEISS CT SPHERIS 209M": 1017
        }

        lens_id = model_to_id.get(f"{manufacturer} {model}")
        if not lens_id:
            return render(request, 'calculator/IOlSpecifications.html', {'error': 'Invalid model selected.'})

        url = f'https://iolcon.org/downloadLenses.php?action=download&lenses={lens_id}'
        response = requests.get(url)

        if response.status_code != 200:
            return render(request, 'calculator/IOlSpecifications.html', {'error': 'Failed to retrieve lens information.'})

        lens_info,constants = parse_xml(response.content)
        return render(request, 'calculator/IOlSpecifications.html', {'lens_info': lens_info})

    return render(request, 'calculator/IOlSpecifications.html')

def parse_xml(xml_content):
    root = ElementTree.fromstring(xml_content)
    lens_info = {}
    constants = {}
    lens_info['Manufacturer'] = root.findtext('.//Manufacturer')
    lens_info['Name'] = root.findtext('.//Name')
    lens_info['SinglePiece'] = root.findtext('.//SinglePiece')
    lens_info['OpticMaterial'] = root.findtext('.//OpticMaterial')
    lens_info['Filter'] = root.findtext('.//Filter')
    lens_info['Preloaded'] = root.findtext('.//Preloaded')
    lens_info['Foldable'] = root.findtext('.//Foldable')
    lens_info['RefractiveIndex'] = root.findtext('.//RefractiveIndex')
    lens_info['OpticDiameter'] = root.findtext('.//OpticDiameter')
    lens_info['HapticDiameter'] = root.findtext('.//HapticDiameter')
    lens_info['IntendedLocation'] = root.findtext('.//IntendedLocation')
    lens_info['OpticConcept'] = root.findtext('.//OpticConcept')
    lens_info['HapticDesign'] = root.findtext('.//HapticDesign')
    lens_info['OpticDesign'] = root.findtext('.//OpticDesign')
    lens_info['Aberration'] = root.findtext('.//Aberration')
    lens_info['Toric'] = root.findtext('.//Toric')
    lens_info['A-Constant'] = root.findtext('.//SRKt')
    constants['A-Constant'] = root.findtext('.//SRKt')
    return lens_info,constants


def index(request):
    form = IOLCalculatorForm()
    return render(request, 'calculator/index.html', {'form': form})

def results(request):

    return render(request, 'calculator/results.html')


def about(request):
    return render(request, 'calculator/about.html')

def constants(request):
    return render(request, 'calculator/constants.html')



def calculation(request):
    if request.method == 'POST':
        form = IOLCalculatorForm(request.POST)
        if form.is_valid():
            try:
                print("Form is valid, processing data...")
                eye = form.cleaned_data['eye']
                print(f"Eye: {eye}")
                
                
                patient, patient_created = Patient.objects.get_or_create(
                    patient_name=form.cleaned_data['patient_name'],
                    date_of_birth=form.cleaned_data['date_of_birth'],
                    
                )
                print(f"Patient: {patient}")

                od_calculation = None
                os_calculation = None

                if eye in ['OD', 'OU']:
                    od_iol_power = calculate_iol_power(
                        form.cleaned_data['od_axial_length'],
                        form.cleaned_data['od_k1_flat'],
                        form.cleaned_data['od_k2_steep'],
                        form.cleaned_data['od_a_constant']
                    )
                    print(f"OD IOL Power: {od_iol_power}")
                    od_refraction = SRKT_SE(
                        form.cleaned_data['od_axial_length'],
                        form.cleaned_data['od_k1_flat'],
                        form.cleaned_data['od_k2_steep'],
                        form.cleaned_data['od_a_constant'],
                        od_iol_power,
                        form.cleaned_data['od_ac_depth']
                    )
                    print(f"OD Refraction: {od_refraction}")
                    od_calculation = IOLCalculation.objects.create(
                        patient_name=patient,
                        eye='OD',
                        iol_model=form.cleaned_data['od_iol_model'],
                        a_constant=form.cleaned_data['od_a_constant'],
                        AL=form.cleaned_data['od_axial_length'],
                        ACD=form.cleaned_data['od_ac_depth'],
                        K1=form.cleaned_data['od_k1_flat'],
                        K2=form.cleaned_data['od_k2_steep'],
                        Target_refraction=form.cleaned_data['od_target_refraction'],
                        iol_power=od_iol_power,
                        REFRACTION=od_refraction,
                        calculation_date=datetime.now()
                    )
                    print(f"OD Calculation: {od_calculation}")

                if eye in ['OS', 'OU']:
                    os_iol_power = calculate_iol_power(
                        form.cleaned_data['os_axial_length'],
                        form.cleaned_data['os_k1_flat'],
                        form.cleaned_data['os_k2_steep'],
                        form.cleaned_data['os_a_constant']
                    )
                    print("OS fields provided, performing calculations...")
                    os_refraction = SRKT_SE(
                        form.cleaned_data['os_axial_length'],
                        form.cleaned_data['os_k1_flat'],
                        form.cleaned_data['os_k2_steep'],
                        form.cleaned_data['os_a_constant'],
                        os_iol_power,
                        form.cleaned_data['os_ac_depth']
                    )
                    print(f"OS Refraction: {os_refraction}")

                    os_calculation = IOLCalculation.objects.create(
                        patient_name=patient,
                        
                        eye='OS',
                        iol_model=form.cleaned_data['os_iol_model'],
                        a_constant=form.cleaned_data['os_a_constant'],
                        AL=form.cleaned_data['os_axial_length'],
                        ACD=form.cleaned_data['os_ac_depth'],
                        K1=form.cleaned_data['os_k1_flat'],
                        K2=form.cleaned_data['os_k2_steep'],
                        Target_refraction=form.cleaned_data['os_target_refraction'],
                        iol_power=os_iol_power,
                        REFRACTION=os_refraction,
                        calculation_date=datetime.now()
                    )
                    print(f"OS Calculation: {os_calculation}")

                if od_calculation and os_calculation:
                    print("Redirecting to results with OD and OS calculations")
                    return redirect('calculator:results_with_ou', od_id=od_calculation.id, os_id=os_calculation.id)
                elif od_calculation:
                    print("Redirecting to results with OD calculation only")
                    return redirect('calculator:results_with_od', od_id=od_calculation.id)
                elif os_calculation:
                    print("Redirecting to results with OS calculation only")
                    return redirect('calculator:results_with_os', os_id=os_calculation.id)

            except Exception as e:
                print(f"Error calculating IOL power: {e}")
                return render(request, 'calculator/index.html', {'form': form, 'error': str(e)})
        else:
            print("Form is not valid")
            print(form.errors)
            return render(request, 'calculator/index.html', {'form': form, 'error': 'Form validation failed', 'form_errors': form.errors})
    else:
        form = IOLCalculatorForm()
    return render(request, 'calculator/index.html', {'form': form})






def results_with_od(request, od_id):
    try:
        od_calculation = IOLCalculation.objects.get(id=od_id)
        patient = od_calculation.patient_name
        return render(request, 'calculator/results.html', {
            'od_calculation': od_calculation,
            'os_calculation': None,
            'patient_name': patient.patient_name,
            'date_of_birth': patient.date_of_birth,
        })
    except IOLCalculation.DoesNotExist:
        return render(request, 'calculator/results.html', {'error': 'Calculation not found'})

def results_with_os(request, os_id):
    try:
        os_calculation = IOLCalculation.objects.get(id=os_id)
        patient = os_calculation.patient_name
        
        return render(request, 'calculator/results.html', {
            'od_calculation': None,
            'os_calculation': os_calculation,
            'patient_name': patient.patient_name,
            'date_of_birth': patient.date_of_birth,
               
        })
    except IOLCalculation.DoesNotExist:
        return render(request, 'calculator/results.html', {'error': 'Calculation not found'})

def results_with_ou(request, od_id, os_id):
    try:
        od_calculation = IOLCalculation.objects.get(id=od_id)
        os_calculation = IOLCalculation.objects.get(id=os_id)
        patient = od_calculation.patient_name

        return render(request, 'calculator/results.html', {
            'od_calculation': od_calculation,
            'os_calculation': os_calculation,
            'patient_name': patient.patient_name,
            'date_of_birth': patient.date_of_birth,
        })
    except IOLCalculation.DoesNotExist:
        return render(request, 'calculator/results.html', {'error': 'Calculation not found'})






