from django.urls import path
from . import views

urlpatterns = [

    path("",views.course_list,name="course_list",),
    path("<slug:slug>/",views.course_detail,name="course_detail",),
    path("<slug:slug>/enroll/",views.enroll_course,name="enroll_course",),
    path("<slug:slug>/unenroll/",views.unenroll_course,name="unenroll_course", ),
    path("<slug:course_slug>/<slug:lesson_slug>/",views.lesson_detail,name="lesson_detail",),
]

