from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("panelladikes/", views.panelladikes, name="panelladikes"),
]