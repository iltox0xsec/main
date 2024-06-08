from django.urls import path
from .views import *


app_name = "scanner"

urlpatterns = [
    path('', index, name='index'),
    path('subdomain/', subdomain, name='subdomain'),
    path('subdomain_scan/', subdomain_scan, name='subdomain_scan'),

]
