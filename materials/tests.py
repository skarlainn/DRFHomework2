from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru")
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            name="Lesson",
            video_link="https://www.youtube.com/lesson1/",
            owner=self.user,
        )

    def test_lesson_detail(self):
        url = reverse("materials:lesson", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(self.lesson.owner, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:create_lesson")
        data = {
            "name": "test_lesson",
            "video_link": "https://www.youtube.com/testlesson/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_invalid_link(self):
        url = reverse("materials:create_lesson")
        data = {
            "name": "test_lesson",
            "video_link": "https://www.vkvideo.com/testlesson/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json().get("video_link"),
            ["Неверная ссылка на видео. Добавьте ссылку на видео с YouTube"],
        )
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_update(self):
        url = reverse("materials:update_lesson", args=(self.lesson.pk,))
        data = {"name": "test_lesson1"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test_lesson1")

    def test_lesson_delete(self):
        url = reverse("materials:delete_lesson", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": None,
                    "video_link": self.lesson.video_link,
                    "course": None,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(name="Course")
        self.lesson = Lesson.objects.create(
            name="Lesson",
            video_link="https://www.youtube.com/lesson/",
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscription", args=(self.course.pk,))
        response = self.client.post(url, data={"course": self.course.pk})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "Подписка добавлена")

