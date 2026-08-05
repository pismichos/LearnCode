from django.shortcuts import render, get_object_or_404
from courses.models import Course

def home(request):
    return render(request, "core/home.html")

def panelladikes(request):
    course = get_object_or_404(
        Course,
        slug="aepp-panelladikes",
        published=True,
    )

    lessons = course.lessons.filter(
        published=True,
    ).order_by("order")

    context = {
        "course": course,
        "lessons": lessons,
    }
    return render(request, "core/panelladikes.html", context)

