
#URL configuration for iol_calculator project.
from django.contrib import admin
from django.urls import include, path, re_path
from calculator import views 
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculator/', include('calculator.urls')), 
     re_path(r'^$', RedirectView.as_view(url='/calculator/', permanent=True)),  

]


