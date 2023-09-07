from django.urls import path
from . import views


urlpatterns = [
    path('', views.csv_in_bulk),
]
