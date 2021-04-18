from django.contrib import admin
from django.urls import path, re_path
from reservation.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', Index.as_view(), name='index'),
    path('add_room/', Add_room.as_view(), name='add_room'),
    path('all_room/',All_room.as_view(), name='all_room'),
    path('search/', Search.as_view(), name='search'),

    re_path(r'^room_delete/(?P<id>\d+)/$', Delete_room.as_view(), name="delete_room"),
    re_path(r'^room_modify/(?P<id>\d+)/$', room_modify, name='room_modify'),
    re_path(r'^room_reservation/(?P<id>\d+)/$', room_reservation, name='room_reservation'),
    re_path(r'^room/(?P<id>\d+)/$', room_detail, name='room_detail'),
]

