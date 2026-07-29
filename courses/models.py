from django.db import models
from django.utils.text import slugify


class Course(models.Model):

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default="beginner"
    )
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "slug"],
                name="unique_lesson_slug_per_course"
            )
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"