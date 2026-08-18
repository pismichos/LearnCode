from django.contrib import admin
from .models import Course, Lesson, LessonProgress, LessonMaterial, LessonVideo, Exercise, Quiz, Question, Choice, QuizAttempt

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "level",
        "published",
        "order",
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

@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "uploaded_at",
    )

    list_filter = (
        "lesson__course",
        "lesson",
    )

    search_fields = (
        "title",
        "lesson__title",
        "lesson__course__title",
    )

@admin.register(LessonVideo)
class LessonVideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "order",
        "published",
        "created_at",
    )

    list_filter = (
        "published",
        "lesson__course",
        "lesson",
    )

    search_fields = (
        "title",
        "lesson__title",
        "lesson__course__title",
    )

    ordering = (
        "lesson",
        "order",
    )   

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "difficulty",
        "order",
        "published",
    )

    list_filter = (
        "difficulty",
        "published",
        "lesson__course",
    )

    search_fields = (
        "title",
        "description",
        "lesson__title",
    )

    ordering = (
        "lesson",
        "order",
    )

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "published"
    )

    list_filter =(
        "published",
        "lesson__course",
    )
    
    search_fields = (
        "title",
        "lesson__title",
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "quiz",
        "order",
    )

    list_filter = (
        "quiz__lesson__course",
        "quiz",
    )

    search_fields = (
        "text",
        "quiz__title",
    )

    ordering = (
        "quiz",
        "order",
    )

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "question",
        "is_correct",
    )

    list_filter = (
        "question__quiz",
        "is_correct",
    )
    
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "quiz",
        "score",
        "total_questions",
        "percentage",
        "completed_at",
    )
    list_filter = (
        "quiz",
        "completed_at",
    )
    search_fields = (
        "user__username",
        "quiz__title",
    )