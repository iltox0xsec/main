from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


app_name = "analyzer"

urlpatterns = [
    path('', login_required(index), name='index'),
    # eml
    path('eml/', login_required(upload_eml), name='upload_eml'),
    path('result/<path:uploaded_file_url>/', login_required(show_result), name='show_result'),
    # any file
    path('upload/file-analyze/', login_required(upload_any_file), name='upload_any_file'),
    path('download/file-analyze/', login_required(download_any_file), name='download_any_file'),

]
