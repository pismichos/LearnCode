from django.shortcuts import get_object_or_404, render
from .models import Course


def course_list(request):
    courses = Course.objects.filter(published=True)

    context = {
        "courses": courses,
    }

    return render(
        request,
        "courses/course_list.html",
        context,
    )


def course_detail(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug,
        published=True,
    )

    context = {
        "course": course,
    }

    return render(
        request,
        "courses/course_detail.html",
        context,
    )