from django.urls import path

from projects.views import (
    CompleteProjectView,
    CreateProjectView,
    FavoriteProjectsView,
    ProjectDetailsView,
    ProjectListView,
    ProjectUpdateView,
    ToggleFavoriteView,
    ToggleParticipateView,
)

app_name = "projects"

urlpatterns = [
    path("list/", ProjectListView.as_view(), name="project_list"),
    path("favorites/", FavoriteProjectsView.as_view(), name="favorite_projects"),
    path("create-project/", CreateProjectView.as_view(), name="create_project"),
    path("<int:pk>/", ProjectDetailsView.as_view(), name="detail"),
    path("<int:pk>/edit/", ProjectUpdateView.as_view(), name="edit_project"),
    path("<int:pk>/complete/", CompleteProjectView.as_view(),
         name="complete_project"),
    path(
        "<int:pk>/toggle-favorite/",
        ToggleFavoriteView.as_view(),
        name="toggle_favorite",
    ),
    path(
        "<int:pk>/toggle-participate/",
        ToggleParticipateView.as_view(),
        name="toggle_participate",
    ),
]
