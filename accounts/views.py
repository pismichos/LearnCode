from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from courses.models import Course, Lesson, LessonProgress
from django.contrib import messages

from .models import Enrollment
from .forms import RegisterForm


@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(
        user=request.user,
        course__published=True,
    ).select_related("course")

    enrolled_courses = []

    for enrollment in enrollments:
        course = enrollment.course

        lessons = course.lessons.filter(
            published=True,
        )

        total_lessons = lessons.count()

        completed_lesson_ids = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            lesson__published=True,
            completed=True,
        ).values_list(
            "lesson_id",
            flat=True,
        )

        completed_lessons = completed_lesson_ids.count()

        progress_percentage = 0

        if total_lessons > 0:
            progress_percentage = round(
                completed_lessons / total_lessons * 100
            )

        next_lesson = lessons.exclude(
            id__in=completed_lesson_ids,
        ).order_by("order").first()

        enrolled_courses.append(
            {
                "course": course,
                "completed_lessons": completed_lessons,
                "total_lessons": total_lessons,
                "progress_percentage": progress_percentage,
                "next_lesson": next_lesson,
            }
        )

    context = {
        "enrolled_courses": enrolled_courses,
        "enrollments_count": enrollments.count(),
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
            request,
            "Ο λογαριασμός σου δημιουργήθηκε επιτυχώς. Μπορείς τώρα να συνδεθείς."
)
            return redirect("login")

    else:
        form = RegisterForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "accounts/register.html",
        context,
    )
