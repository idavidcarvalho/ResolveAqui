from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.my_tickets, name='my_tickets'),
    path('create/', views.create_ticket, name='create'),
    path('<int:pk>/', views.ticket_detail, name='detail'),
]
