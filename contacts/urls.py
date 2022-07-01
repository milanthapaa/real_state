from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('reconnect', views.reconnect, name='reconnect'),
]
