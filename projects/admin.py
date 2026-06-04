from django.contrib import admin
from django.utils.html import format_html

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "owner_info",
        "status",
        "created_at",
        "participants_count",
    )

    list_display_links = ("id", "name")

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    )

    readonly_fields = ("created_at",)

    raw_id_fields = ("owner",)

    filter_horizontal = ("participants",)

    fieldsets = (
        ("Основная информация", {
         "fields": ("name", "description", "github_url")}),
        ("Статус", {"fields": ("status",)}),
        ("Участники", {"fields": ("owner", "participants")}),
        ("Даты", {"fields": ("created_at",)}),
    )

    @admin.display(description="Автор", ordering="owner__email")
    def owner_info(self, obj):
        if obj.owner:
            return format_html(
                '<a href="/admin/users/user/{}/">{}</a>',
                obj.owner.id,
                obj.owner.get_full_name(),
            )
        return "-"

    @admin.display(description="Участников")
    def participants_count(self, obj):
        return obj.participants.count()

    actions = ["make_open", "make_closed"]

    @admin.action(description="Открыть выбранные проекты")
    def make_open(self, request, queryset):
        updated = queryset.update(status="open")
        self.message_user(request, f"Открыто {updated} проектов.")

    @admin.action(description="Закрыть выбранные проекты")
    def make_closed(self, request, queryset):
        updated = queryset.update(status="closed")
        self.message_user(request, f"Закрыто {updated} проектов.")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("owner")
            .prefetch_related("participants")
        )
