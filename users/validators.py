import re

from core.validators import validate_github_url
from django.core.exceptions import ValidationError


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
