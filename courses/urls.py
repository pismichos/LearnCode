from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path("<slug:course_slug>/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
    path("<slug:slug>/", views.course_detail, name="course_detail"),
    
]

