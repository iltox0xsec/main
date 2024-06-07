from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .utils import scan_subdomains

@shared_task
def scan_subdomains_task(domain):
    return scan_subdomains(domain)
