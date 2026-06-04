from django.urls import path

from users.views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserChangePasswordView,
    UserDetailView,
    UserEditView,
    UsersListView,
)

app_name = "users"

urlpatterns = [
    path("list/", UsersListView.as_view(), name="list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit-profile/", UserEditView.as_view(), name="edit_profile"),
    path("change-password/", UserChangePasswordView.as_view(),
         name="change_password"),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
]
