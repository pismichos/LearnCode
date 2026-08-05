from django.contrib import admin
from .models import Course, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "level",
        "published",
        "created_at",
    )

    list_filter = (
        "level",
        "published",
    )

    search_fields = (
        "title",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "order",
        "published",
    )

    list_filter = (
        "course",
        "published",
    )

    search_fields = (
        "title",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    ordering = (
        "course",
        "order",
    )

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "lesson",
        "completed",
        "last_accessed",
    )

    list_filter = (
        "completed",
    )

    search_fields = (
        "user__username",
        "lesson__title",
    )