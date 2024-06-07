from django.db import models
from django.utils import timezone

class SubdomainScan(models.Model):
    domain = models.CharField(max_length=255)
    subdomains = models.TextField()
    scan_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.domain
