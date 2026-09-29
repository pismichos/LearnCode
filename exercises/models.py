from django.db import models

class ExerciseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ενότητα Άσκησης"
        verbose_name_plural = "Ενότητες Ασκήσεων"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ExerciseFile(models.Model):
    category = models.ForeignKey(
        ExerciseCategory,
        on_delete=models.CASCADE,
        related_name="files",
    )

    title = models.CharField(max_length=200)

    file = models.FileField(
        upload_to="exercises/"
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True   
    )

    class Meta:
        verbose_name = "Αρχείο Ασκήσεων"
        verbose_name_plural = "Αρχεία Ασκήσεων"
        ordering = ["title"]

    def __str__(self):
        return self.title
