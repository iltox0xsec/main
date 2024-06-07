from django.urls import path
from .views import *


app_name = "scanner"

urlpatterns = [
    path('', index, name='index'),
    path('start_scan/', start_scan, name='start_scan'),
]
