from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView

from core.constants import USERS_PER_PAGE
from users.forms import ChangePasswordForm, LoginForm, ProfileEditForm, RegisterForm
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
        context = super().get_context_data(**kwargs)
        context["active_filter"] = self.request.GET.get("filter")
        return context


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("projects:project_list")
        return render(request, "users/register.html", {"form": form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("projects:project_list")
        return render(request, "users/login.html", {"form": form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("projects:project_list")


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user_obj"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse_lazy("users:detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/change_password.html"
    form_class = ChangePasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("users:detail", kwargs={"pk": self.request.user.pk})


def register_user(request):
    return RegisterView.as_view()(request)


def login_user(request):
    return LoginView.as_view()(request)


def logout_user(request):
    return LogoutView.as_view()(request)
