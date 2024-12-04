"""calculator app"""
from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('results/od/<int:od_id>/', views.results_with_od, name='results_with_od'),
    path('results/os/<int:os_id>/', views.results_with_os, name='results_with_os'),
    path('results/<int:od_id>/<int:os_id>/', views.results_with_ou, name='results_with_ou'),
    path('about/', views.about, name='about'),
    path('IOLSpecifications/', views.IOlSpecifications, name='IOlSpecifications'),
    path('calculation/', views.calculation, name='calculation'),
]

#http://127.0.0.1:8000/calculator/index/
#http://127.0.0.1:8000/admin/
#http://127.0.0.1:8000/calculator/results/
#http://127.0.0.1:8000/calculator/about/
##http://127.0.0.1:8000/calculator/iol_calculator/







