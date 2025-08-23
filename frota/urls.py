from django.urls import path
from frota import views

urlpatterns = [
    path('', views.index, name="index"),
]