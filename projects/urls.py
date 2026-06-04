from django.urls import path

from projects.views import (CompleteProjectView, CreateProjectView,
                            FavoriteProjectsView, ProjectDetailsView,
                            ProjectListView, ProjectUpdateView,
                            ToggleFavoriteView, ToggleParticipateView)

app_name = "projects"

urlpatterns = [
    path("list/", ProjectListView.as_view(), name="project_list"),
    path("favorites/", FavoriteProjectsView.as_view(), name="favorite_projects"),
    path("create-project/", CreateProjectView.as_view(), name="create_project"),
    path("<int:project_id>/", ProjectDetailsView.as_view(), name="detail"),
    path("<int:project_id>/edit/", ProjectUpdateView.as_view(), name="edit_project"),
    path(
        "<int:project_id>/complete/",
        CompleteProjectView.as_view(),
        name="complete_project",
    ),
    path(
        "<int:project_id>/toggle-favorite/",
        ToggleFavoriteView.as_view(),
        name="toggle_favorite",
    ),
    path(
        "<int:project_id>/toggle-participate/",
        ToggleParticipateView.as_view(),
        name="toggle_participate",
    ),
]
