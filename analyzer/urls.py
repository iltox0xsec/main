from django.urls import path
from .views import *


app_name = "analyzer"

urlpatterns = [
    path('', index, name='index'),
    # eml
    path('eml/', upload_eml, name='upload_eml'),
    path('result/<path:uploaded_file_url>/', show_result, name='show_result'),
    # any file
    path('upload/file-analyze/', upload_any_file, name='upload_any_file'),
    path('download/file-analyze/', download_any_file, name='download_any_file'),

    #jwt
    path('jwt/', jwt, name='jwt'),
    path('analyze_jwt/', analyze_jwt, name='analyze_jwt'),


]
