from django import forms
from django.core.exceptions import ValidationError

from projects.models import Project
from projects.validators import validate_github_url


class ProjectForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False, validators=[validate_github_url])

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Название проекта"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Описание проекта",
                }
            ),
            "github_url": forms.URLInput(
                attrs={"class": "form-control",
                       "placeholder": "https://github.com/..."}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Название проекта",
            "description": "Описание",
            "github_url": "Ссылка на GitHub",
            "status": "Статус",
        }
