from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from accounts.models import Enrollment

from .models import Course, Lesson, LessonProgress, Quiz, QuizAttempt
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


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        course__slug=course_slug,
        slug=lesson_slug,
        published=True,
        course__published=True,
    )

    is_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=lesson.course,
    ).exists()

    if not is_enrolled:
        messages.warning(
            request,
            "Πρέπει πρώτα να εγγραφείς στο μάθημα."
        )

        return redirect(
            "course_detail",
            slug=lesson.course.slug,
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

    is_completed = LessonProgress.objects.filter(
        user=request.user,
        lesson=lesson,
        completed=True,
    ).exists()

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

        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course,
        )

        if created:
            messages.success(
                request,
                "Εγγράφηκες επιτυχώς στο μάθημα!"
            )
        else:
            messages.info(
                request,
                "Είσαι ήδη εγγεγραμμένος σε αυτό το μάθημα."
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

        messages.success(
        request,
        "Η απεγγραφή από το μάθημα ολοκληρώθηκε."
)

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

        if progress.completed:
            messages.info(
                request,
                "Η ενότητα είναι ήδη ολοκληρωμένη."
            )
        else:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

            messages.success(
                request,
                "Η ενότητα σημειώθηκε ως ολοκληρωμένη!"
            )

    return redirect(
        "lesson_detail",
        course_slug=lesson.course.slug,
        lesson_slug=lesson.slug,
    )

@login_required
def quiz_detail(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson,
        course__slug=course_slug,
        slug=lesson_slug,
        published=True,
        course__published=True,
    )

    quiz = get_object_or_404(
        Quiz,
        lesson=lesson,
        published=True,
    )

    results = []
    score = 0
    total_questions = quiz.questions.count()
    percentage = 0

    if request.method == "POST":

        for question in quiz.questions.all():

            selected_choice_id = request.POST.get(
                f"question_{question.id}"
            )

            selected_choice = None
            is_correct = False

            if selected_choice_id:
                selected_choice = question.choices.filter(
                    id=selected_choice_id
                ).first()

                if selected_choice:
                    is_correct = selected_choice.is_correct

                    if is_correct:
                        score += 1

            correct_choice = question.choices.filter(
                is_correct=True
            ).first()

            results.append(
                {
                    "question": question,
                    "selected_choice": selected_choice,
                    "correct_choice": correct_choice,
                    "is_correct": is_correct,
                }
            )

        if total_questions > 0:
            percentage = round(
                score / total_questions * 100
            )

        if request.user.is_authenticated:
            QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
    )

    context = {
        "lesson": lesson,
        "quiz": quiz,
        "results": results,
        "score": score,
        "total_questions": total_questions,
        "percentage": percentage,
    }

    return render(
        request,
        "courses/quiz_detail.html",
        context,
    )

@login_required
def profil(request):
    enrollments = Enrollment.objects.filter(
        user=request.user,
        course_published=True,
    ).select_related("course")

    enrolled_courses = []

    total_completed_lessons = 0

    for enrolment in enrollments:
        course = enrollments.courses

        lessons = course.lessons.filter(published=True,)

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

        total_completed_lessons += completed_lessons

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

    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
    ).select_related(
        "quiz",
        "quiz__lesson",
        "quiz__lesson__course",
    ).order_by("-completed_at")

    context = {
        "enrolled_courses": enrolled_courses,
        "enrollments_count": enrollments.count(),
        "total_completed_lessons": total_completed_lessons,
        "quiz_attempts": quiz_attempts[:10],
        "quiz_attempts_count": quiz_attempts.count(),
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )   