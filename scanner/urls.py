from django.urls import path
from .views import *


app_name = "scanner"

urlpatterns = [
    path('', index, name='index'),
    #subdomain
    path('subdomain/', subdomain, name='subdomain'),
    path('subdomain_scan/', subdomain_scan, name='subdomain_scan'),
    # dns
    path('domain_dns/', scan_domain_dns, name='scan_domain_dns'),
]
