from rest_framework import serializers
from urllib.parse import urlparse

VALID_DOMAINS = ('youtube.com',)


def validate_video_link(value: str) -> None:
    parsed_url = urlparse(value)

    if not all([
        parsed_url.scheme == 'https',
        parsed_url.netloc not in VALID_DOMAINS,
    ]):
        raise serializers.ValidationError("Неверная ссылка на видео")