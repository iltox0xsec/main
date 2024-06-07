# scanner/utils.py
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
from .models import SubdomainScan
from django.utils import timezone
from datetime import timedelta

def get_subdomains_from_api(domain):
    try:
        res = DNSDumpsterAPI(True).search(domain)
        subdomains = []
        for record in res['dns_records']['host']:
            subdomains.append(record['domain'])
        return subdomains
    except Exception as e:
        print(f"Error retrieving subdomains: {e}")
        return []

def scan_subdomains(domain):
    one_month_ago = timezone.now() - timedelta(days=30)
    recent_scan = SubdomainScan.objects.filter(domain=domain, scan_date__gte=one_month_ago).first()

    if recent_scan:
        print("Using cached results")
        return recent_scan.subdomains.split(','), recent_scan.scan_date
    else:
        print("Performing new scan")
        subdomains = get_subdomains_from_api(domain)
        if subdomains:
            new_scan = SubdomainScan.objects.create(domain=domain, subdomains=','.join(subdomains))
            return subdomains, new_scan.scan_date
        return subdomains, None
