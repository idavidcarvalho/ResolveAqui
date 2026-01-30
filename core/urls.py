from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]