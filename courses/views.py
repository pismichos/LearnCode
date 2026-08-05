from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Enrollment

from .models import Course, Lesson, LessonProgress
from django.utils import timezone


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

    is_enrolled = False
    total_lessons = course.lessons.filter(published=True,).count()

    completed_lessons = 0
    progress_percentage = 0

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course,
        ).exists()

    completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            lesson__published=True,
            completed=True,
        ).count()

    if total_lessons > 0:
        progress_percentage = round(completed_lessons / total_lessons * 100)

    context = {
        "course": course,
        "is_enrolled": is_enrolled,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percentage": progress_percentage,
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

    is_completed = False
    if request.user.is_authenticated:
        is_completed = LessonProgress.objects.filter(user=request.user, lesson=lesson, completed=True).exists()

    context = {
        "lesson": lesson,
        "previous_lesson": previous_lesson,
        "next_lesson": next_lesson,
        "is_completed": is_completed,
    }

    return render(
        request,
        "courses/lesson_detail.html",
        context,
    )


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug,
        published=True,
    )

    if request.method == "POST":
        Enrollment.objects.get_or_create(
            user=request.user,
            course=course,
        )

    return redirect(
        "course_detail",
        slug=course.slug,
    )

@login_required
def unenroll_course(request, slug):
    course = get_object_or_404(
        Course,
        slug=slug,
        published=True,
    )

    if request.method == "POST":
        Enrollment.objects.filter(
            user=request.user,
            course=course,
        ).delete()

    return redirect(
        "course_detail",
        slug=course.slug,
    )

@login_required
def complete_lesson(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        course__slug=course_slug,
        slug=lesson_slug,
        published=True,
        course__published=True,
    )

    if request.method == "POST":
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
        )

        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save(
                update_fields=["completed", "completed_at"]
            )

    return redirect(
        "lesson_detail",
        course_slug=lesson.course.slug,
        lesson_slug=lesson.slug,
    )