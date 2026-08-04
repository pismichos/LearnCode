from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from courses.models import Course, Lesson

@login_required
def profile(request):

    courses_count = Course.objects.filter(published=True).count()
    lessons_count = Lesson.objects.filter(published=True).count()

    context = {
        "courses_count": courses_count,
        "lessons_count": lessons_count,
    }

    return render(request, "accounts/profile.html", context)

