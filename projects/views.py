from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.constants import PROJECTS_PER_PAGE
from projects.forms import ProjectForm
from projects.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        return Project.objects.filter(status="open").order_by("-created_at")


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    paginate_by = PROJECTS_PER_PAGE

    def get_queryset(self):
        return self.request.user.favorites.all().order_by("-created_at")


class ProjectDetailsView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"
    pk_url_kwarg = "pk"


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        project.participants.add(self.request.user)
        return redirect("projects:detail", pk=project.pk)

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        context["project"] = self.get_object()
        return context

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            return redirect("projects:detail", pk=project.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.pk})


class CompleteProjectView(LoginRequiredMixin, View):

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        if project.owner != request.user:
            return JsonResponse({"status": "error", "message": "Forbidden"}, status=403)

        if project.status == "open":
            project.status = "closed"
            project.save()
            return JsonResponse({"status": "ok", "project_status": "closed"})

        return JsonResponse(
            {"status": "error", "message": "Project already closed"}, status=400
        )


class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        if project in request.user.favorites.all():
            request.user.favorites.remove(project)
            favorited = False
        else:
            request.user.favorites.add(project)
            favorited = True

        return JsonResponse({"status": "ok", "favorited": favorited})


class ToggleParticipateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        if request.user in project.participants.all():
            project.participants.remove(request.user)
            participated = False
        else:
            project.participants.add(request.user)
            participated = True

        return JsonResponse({"status": "ok", "participated": participated})
