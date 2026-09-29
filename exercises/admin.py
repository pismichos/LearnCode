from django.contrib import admin

# Register your models here.
from .models import ExerciseCategory, ExerciseFile

@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(ExerciseFile)
class ExerciseFileAdmin(admin.ModelAdmin): 
    list_display = ("title", "category", "is_published", "created_at")
    list_filter = ("category", "is_published", "created_at")
    search_fields = ("title", "category__name")
    list_editable = ("is_published",)

