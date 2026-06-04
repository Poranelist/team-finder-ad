from django import forms

from projects.models import Project
from projects.validators import validate_github_url


class ProjectForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False,
        validators=[validate_github_url],
        widget=forms.URLInput(attrs={"placeholder": "https://github.com/..."})
    )

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Название проекта"}),
            "description": forms.Textarea(attrs={"rows": 5, "placeholder": "Описание проекта"}),
            "status": forms.Select(),
        }