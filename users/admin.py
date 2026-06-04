from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):

    list_display = (
        "id",
        "email",
        "name",
        "surname",
        "phone",
        "avatar_preview",
        "is_active",
        "is_staff",
    )

    list_display_links = ("id", "email")

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "email",
        "name",
        "surname",
        "phone",
    )

    ordering = ("-id",)

    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "surname",
                    "avatar",
                    "phone",
                    "github_url",
                    "about",
                )
            },
        ),
        (
            _("Favorites"),
            {
                "fields": ("favorites",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "surname",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    filter_horizontal = ("favorites", "groups", "user_permissions")

    @admin.display(description="Avatar")
    def avatar_preview(self, obj):
        if obj.avatar and obj.avatar.name != "avatars/default.png":
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%;" />',
                obj.avatar.url,
            )
        return "-"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("favorites")
