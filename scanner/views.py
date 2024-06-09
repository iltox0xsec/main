# scanner/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils import scan_subdomains
from .forms import *
import dns.resolver
from django.contrib import messages


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


# DNS


from concurrent.futures import ThreadPoolExecutor, as_completed

def dns_query(domain, record_type):
    # Dummy implementation of DNS query, replace with actual implementation
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return {record_type: [str(rdata) for rdata in answers]}
    except Exception as e:
        return {record_type: [str(e)]}

def scan_domain_dns(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data['domain']
            record_types = form.cleaned_data['record_types']
            all_records = form.cleaned_data['all_records']
            messages.warning(request, 'Your message sent.')
            

            results = {}
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_record = {executor.submit(dns_query, domain, record_type): record_type for record_type in record_types}
                for future in as_completed(future_to_record):
                    record_type = future_to_record[future]
                    try:
                        result = future.result()
                        results.update(result)
                    except Exception as exc:
                        results[record_type] = [str(exc)]

            return JsonResponse(results)
    else:
        form = DomainForm()

    return render(request, 'analyzer/dns/index.html', {'form': form})