from django.contrib import admin
from .models import (
    Tree,
    PhysicalCharacteristics,
    Habitat,
    GrowingConditions,
    EcologicalImportance,
    TreeUses,
    Threat,
    CareGuide,
    TreeImage,
)

class PhysicalCharacteristicsInline(admin.StackedInline):
    model = PhysicalCharacteristics
    extra = 0


class HabitatInline(admin.StackedInline):
    model = Habitat
    extra = 0


class GrowingConditionsInline(admin.StackedInline):
    model = GrowingConditions
    extra = 0


class EcologicalImportanceInline(admin.StackedInline):
    model = EcologicalImportance
    extra = 0


class TreeUsesInline(admin.StackedInline):
    model = TreeUses
    extra = 0


class CareGuideInline(admin.StackedInline):
    model = CareGuide
    extra = 0

class ThreatInline(admin.TabularInline):
    model = Threat
    extra = 1


class TreeImageInline(admin.TabularInline):
    model = TreeImage
    extra = 1


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = (
        "common_name",
        "scientific_name",
        "family",
        "tree_type",
    )

    search_fields = (
        "common_name",
        "scientific_name",
        "family",
    )

    inlines = [
        PhysicalCharacteristicsInline,
        HabitatInline,
        GrowingConditionsInline,
        EcologicalImportanceInline,
        TreeUsesInline,
        CareGuideInline,
        ThreatInline,
        TreeImageInline,
    ]