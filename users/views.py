from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.constants import USERS_PER_PAGE
from users.forms import LoginForm, ProfileEditForm, RegisterForm
from users.models import User


class UsersListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = USERS_PER_PAGE

    def get_queryset(self):
        users = User.objects.filter(is_active=True)
        active_filter = self.request.GET.get("filter")

        if self.request.user.is_authenticated and active_filter:

            if active_filter == "owners-of-favorite-projects":
                favorite_projects = self.request.user.favorites.all()
                users = User.objects.filter(
                    owned_projects__in=favorite_projects
                ).distinct()

            elif active_filter == "owners-of-participating-projects":
                my_projects = self.request.user.participated_projects.all()
                users = User.objects.filter(
                    owned_projects__in=my_projects).distinct()

            elif active_filter == "interested-in-my-projects":
                my_projects = self.request.user.owned_projects.all()
                users = User.objects.filter(
                    favorites__in=my_projects).distinct()

            elif active_filter == "participants-of-my-projects":
                my_projects = self.request.user.owned_projects.all()
                users = User.objects.filter(
                    participated_projects__in=my_projects
                ).distinct()

        return users

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, active_filter=self.request.GET.get("filter"))


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("projects:project_list")


class LoginView(CreateView):
    form_class = LoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect("projects:project_list")


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user_obj"
    pk_url_kwarg = "user_id"

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"
    pk_url_kwarg = "user_id"

    def get_success_url(self):
        return reverse("users:detail", kwargs={"user_id": self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/change_password.html"
    success_url = reverse("users:detail", kwargs={"user_id": None})

    def get_success_url(self):
        return reverse("users:detail", kwargs={"user_id": self.request.user.pk})
