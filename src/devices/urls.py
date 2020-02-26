from django.urls import path

from .views import device_list, device_detail

urlpatterns = [
    path('', device_list, name='device_list'),
    path('<uuid:device_uuid>/', device_detail, name='device_detail'),
]