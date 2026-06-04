from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import exceptions
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.constants import (PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN,
                            PROJECTS_PER_PAGE)
from projects.forms import ProjectForm
from projects.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        return Project.objects.filter(status=PROJECT_STATUS_OPEN)


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        return self.request.user.favorites.all()


class ProjectDetailsView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"
    pk_url_kwarg = "project_id"


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, is_edit=False)

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        project.participants.add(self.request.user)
        return redirect("projects:detail", project_id=project.pk)

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"project_id": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    pk_url_kwarg = "project_id"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs, is_edit=True, project=self.get_object()
        )

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            return redirect("projects:detail", project_id=project.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"project_id": self.object.pk})


class CompleteProjectView(LoginRequiredMixin, View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if project.owner != request.user:
            return JsonResponse(
                {"status": "error", "message": "Forbidden"},
                status=exceptions.PermissionDenied.status_code,
            )

        if project.status == PROJECT_STATUS_OPEN:
            project.status = PROJECT_STATUS_CLOSED
            project.save()
            return JsonResponse(
                {"status": "ok", "project_status": PROJECT_STATUS_CLOSED}
            )

        return JsonResponse(
            {"status": "error", "message": "Project already closed"},
            status=exceptions.BadRequest.status_code,
        )


class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if request.user.favorites.filter(pk=project.pk).exists():
            request.user.favorites.remove(project)
            favorited = False
        else:
            request.user.favorites.add(project)
            favorited = True

        return JsonResponse({"status": "ok", "favorited": favorited})


class ToggleParticipateView(LoginRequiredMixin, View):

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if project.participants.filter(pk=request.user.pk).exists():
            project.participants.remove(request.user)
            participated = False
        else:
            project.participants.add(request.user)
            participated = True

        return JsonResponse({"status": "ok", "participated": participated})
