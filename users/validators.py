import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_phone_number(value):
    if not value:
        return value

    if value.startswith("8"):
        normalized = "+7" + value[1:]
    elif value.startswith("+7"):
        normalized = value
    else:
        raise ValidationError("Телефон должен начинаться с 8 или +7")

    if not re.match(r"^\+7\d{10}$", normalized):
        raise ValidationError("Телефон должен содержать 10 цифр после кода")

    return normalized


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
