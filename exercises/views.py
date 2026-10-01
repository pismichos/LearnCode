from django.shortcuts import render

from .models import ExerciseCategory


def exercise_list(request):
    categories = (
        ExerciseCategory.objects
        .prefetch_related("files")
        .filter(files__is_published=True)
        .distinct()
    )

    return render(
        request,
        "exercises/exercise_list.html",
        {
            "categories": categories,
        },
    )