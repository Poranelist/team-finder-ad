from urllib.parse import urlparse

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_github_url(value):
    if not value:
        return value

    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError("Введите корректный URL")

    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    if domain != "github.com":
        raise ValidationError("Ссылка должна вести на GitHub")

    return value
