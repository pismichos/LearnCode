from django.shortcuts import get_object_or_404, render
from .models import Course, Lesson


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

def lesson_detail(request, course_slug, lesson_slug):

    lesson = get_object_or_404(
        Lesson,
        course__slug=course_slug,
        slug=lesson_slug,
        published=True,
        course__published=True,
    )

    previous_lesson = Lesson.objects.filter(
        course=lesson.course,
        published=True,
        order__lt=lesson.order,
    ).order_by("-order").first()

    next_lesson = Lesson.objects.filter(
        course=lesson.course,
        published=True,
        order__gt=lesson.order,
    ).order_by("order").first()

    context = {
        "lesson": lesson,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson,
    }

    return render(
        request,
        "courses/lesson_detail.html",
        context,
    )