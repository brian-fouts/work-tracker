from django import forms

from worktracker.models.project import Project, ProjectMember


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]
