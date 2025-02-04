from django.contrib import admin
from django import forms

from .models import (
    ProjectGroup,
    Project,
    ProjectObjective,
    Condition,
    ProjectObjectiveCondition,
    LevelCommitment,
    QI,
)


class LevelCommitmentInline(admin.TabularInline):
    model = LevelCommitment
    max_num = 0
    can_delete = False
    readonly_fields = ["objective", "work_cycle", "level"]
    classes = ["collapse"]


# ---- ProjectAdmin

from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory


class CustomInlineFormSet(BaseInlineFormSet):
    pass
    # should define how we call inlineformset_factory here, using


class ProjectObjectiveConditionInlineForm(forms.ModelForm):
    pass


class ProjectObjectiveConditionInline(admin.TabularInline):
    model = ProjectObjectiveCondition
    can_delete = False
    readonly_fields = ["condition"]
    exclude = ["condition", "objective", "level"]
    template = "admin/edit_inline/custominline.html"
    form = ProjectObjectiveConditionInlineForm
    formset = inlineformset_factory(
        Project,
        ProjectObjectiveCondition,
        fields=["done"],
        can_delete=False,
        extra=0,
        max_num=0,
    )

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


class ProjectObjectiveInline(admin.TabularInline):
    model = ProjectObjective
    inlines = [ProjectObjectiveConditionInline]
    max_num = 0
    can_delete = False
    readonly_fields = ["name", "status"]
    exclude = ["if_not_started", "objective"]


@admin.register(ProjectObjective)
class ProjectObjectiveAdmin(admin.ModelAdmin):
    # inlines = [LevelCommitmentInline]
    readonly_fields = ["project", "objective", "status"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("if_not_started", "status"),
                    ("project", "objective"),
                ),
            },
        ),
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        print(request, object_id, extra_context)
        extra_context = extra_context or {}
        extra_context["test"] = "success!"
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [LevelCommitmentInline, ProjectObjectiveConditionInline]
    list_display = ["name", "owner", "driver", "last_review", "last_review_status"]
    change_form_template = "admin/project_change_form.html"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("name", "group"),
                    ("owner", "driver"),
                    ("last_review", "last_review_status"),
                )
            },
        ),
    )


admin.site.register(ProjectGroup)
admin.site.register(QI)
admin.site.register(ProjectObjectiveCondition)
