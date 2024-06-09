from django.urls import path
from .views import *


app_name = "chat"

urlpatterns = [
    path('', index, name='index'),
    path('create-room/', create_room, name='create_room'),
    path('room/<str:url_path>/', room, name='room'),
    path('join-room/', join_room, name='join_room'),
    path('room/<str:url_path>/get_new_messages/', get_new_messages, name='get_new_messages'),


]
