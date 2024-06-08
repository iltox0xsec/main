# scanner/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils import scan_subdomains

def index(request):
    return render(request, 'scanner/index.html')

def subdomain_scan(request):
    domain = request.GET.get('domain')
    subdomains, scan_date = scan_subdomains(domain)
    response_data = {
        'subdomains': subdomains,
        'scan_date': scan_date.strftime('%Y-%m-%d %H:%M:%S') if scan_date else None
    }
    return JsonResponse(response_data)

def subdomain(request):
    return render(request, 'scanner/subdomain/index.html')
