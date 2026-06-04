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

    if "github.com" not in value:
        raise ValidationError("Ссылка должна вести на GitHub")

    return value
