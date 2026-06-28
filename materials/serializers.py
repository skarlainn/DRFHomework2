from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "video_link", "course"]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context["request"].user.pk, course=obj.pk
        ).exists()

    def get_lessons_count(self, instance):
        return instance.lessons.all().count()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]
