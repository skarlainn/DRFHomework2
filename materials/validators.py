from rest_framework import serializers
from urllib.parse import urlparse

VALID_DOMAINS = ("youtube.com", "www.youtube.com", "youtu.be")


def validate_video_link(value: str) -> None:
    if not value:
        raise serializers.ValidationError("Ссылка не может быть пустой")

    parsed_url = urlparse(value)

    if parsed_url.scheme not in ("http", "https"):
        raise serializers.ValidationError(
            "Ссылка должна начинаться с http:// или https://"
        )

    if parsed_url.netloc not in VALID_DOMAINS:
        raise serializers.ValidationError(
            "Неверная ссылка на видео. Добавьте ссылку на видео с YouTube"
        )