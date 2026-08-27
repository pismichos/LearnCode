from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Enrollment

from .models import (
    Course,
    Lesson,
    LessonProgress,
    Quiz,
    Question,
    Choice,
    QuizAttempt,
)


class CourseFlowTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="StrongPassword123!",
        )

        self.course = Course.objects.create(
            title="ΑΕΠΠ Πανελλαδικές",
            slug="aepp-panelladikes",
            description="Test course",
            published=True,
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Δομή Επιλογής",
            slug="domi-epilogis",
            content="Test lesson content",
            order=1,
            duration=30,
            published=True,
        )

        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title="Quiz Δομής Επιλογής",
            published=True,
        )

        self.question = Question.objects.create(
            quiz=self.quiz,
            text="Ποια εντολή χρησιμοποιείται για έλεγχο συνθήκης;",
            order=1,
        )

        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="ΑΝ",
            is_correct=True,
        )

        self.wrong_choice = Choice.objects.create(
            question=self.question,
            text="ΟΣΟ",
            is_correct=False,
        )


    def test_user_can_enroll(self):
        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        response = self.client.post(
            reverse(
                "enroll_course",
                kwargs={
                    "slug": self.course.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Enrollment.objects.filter(
                user=self.user,
                course=self.course,
            ).exists()
        )


    def test_user_can_unenroll(self):
        Enrollment.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        response = self.client.post(
            reverse(
                "unenroll_course",
                kwargs={
                    "slug": self.course.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Enrollment.objects.filter(
                user=self.user,
                course=self.course,
            ).exists()
        )


    def test_lesson_requires_login(self):
        response = self.client.get(
            reverse(
                "lesson_detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "lesson_slug": self.lesson.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 302)


    def test_lesson_requires_enrollment(self):
        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        response = self.client.get(
            reverse(
                "lesson_detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "lesson_slug": self.lesson.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 302)


    def test_enrolled_user_can_open_lesson(self):
        Enrollment.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        response = self.client.get(
            reverse(
                "lesson_detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "lesson_slug": self.lesson.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Δομή Επιλογής",
        )


    def test_user_can_complete_lesson(self):
        Enrollment.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        response = self.client.post(
            reverse(
                "complete_lesson",
                kwargs={
                    "course_slug": self.course.slug,
                    "lesson_slug": self.lesson.slug,
                },
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            LessonProgress.objects.filter(
                user=self.user,
                lesson=self.lesson,
                completed=True,
            ).exists()
        )


    def test_quiz_correct_answer(self):
        Enrollment.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        response = self.client.post(
            reverse(
                "quiz_detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "lesson_slug": self.lesson.slug,
                },
            ),
            {
                f"question_{self.question.id}":
                    self.correct_choice.id,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["score"],
            1,
        )

        self.assertEqual(
            response.context["percentage"],
            100,
        )


    def test_quiz_attempt_is_saved(self):
        Enrollment.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.login(
            username="student1",
            password="StrongPassword123!",
        )

        self.client.post(
            reverse(
                "quiz_detail",
                kwargs={
                    "course_slug": self.course.slug,
                    "lesson_slug": self.lesson.slug,
                },
            ),
            {
                f"question_{self.question.id}":
                    self.correct_choice.id,
            },
        )

        attempt = QuizAttempt.objects.filter(
            user=self.user,
            quiz=self.quiz,
        ).first()

        self.assertIsNotNone(attempt)

        self.assertEqual(
            attempt.score,
            1,
        )

        self.assertEqual(
            attempt.total_questions,
            1,
        )

        self.assertEqual(
            attempt.percentage,
            100,
        )