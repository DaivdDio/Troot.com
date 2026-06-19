from django import forms
from trees.models import *


class PhysicalCharacteristicsForm(forms.ModelForm):

    class Meta:
        model = PhysicalCharacteristics
        exclude = ["tree"]

        widgets = {
            "average_height_m": forms.NumberInput(attrs={"class": "form-control"}),
            "canopy_spread_m": forms.NumberInput(attrs={"class": "form-control"}),
            "trunk_diameter_cm": forms.NumberInput(attrs={"class": "form-control"}),
            "growth_rate": forms.Select(attrs={"class": "form-select"}),
            "lifespan_years": forms.NumberInput(attrs={"class": "form-control"}),
            "leaf_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "bark_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "flower_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "fruit_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class HabitatForm(forms.ModelForm):

    class Meta:
        model = Habitat
        exclude = ["tree"]

        widgets = {
            "native_range": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "introduced_regions": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "preferred_climate": forms.TextInput(attrs={"class": "form-control"}),
            "hardiness_zone": forms.TextInput(attrs={"class": "form-control"}),
            "elevation_min_m": forms.NumberInput(attrs={"class": "form-control"}),
            "elevation_max_m": forms.NumberInput(attrs={"class": "form-control"}),
        }

class GrowingConditionsForm(forms.ModelForm):

    class Meta:
        model = GrowingConditions
        exclude = ["tree"]

        widgets = {
            "sunlight": forms.TextInput(attrs={"class": "form-control"}),
            "soil_type": forms.TextInput(attrs={"class": "form-control"}),
            "soil_ph": forms.TextInput(attrs={"class": "form-control"}),
            "water_requirements": forms.TextInput(attrs={"class": "form-control"}),
            "drought_tolerance": forms.TextInput(attrs={"class": "form-control"}),
            "frost_tolerance": forms.TextInput(attrs={"class": "form-control"}),
        }

class EcologicalImportanceForm(forms.ModelForm):

    class Meta:
        model = EcologicalImportance
        exclude = ["tree"]

        widgets = {
            "carbon_sequestration": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "wildlife_supported": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "pollinators_attracted": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "soil_benefits": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "ecosystem_role": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class TreeUsesForm(forms.ModelForm):

    class Meta:
        model = TreeUses
        exclude = ["tree"]

        widgets = {
            "timber": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "landscaping": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "medicinal": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "cultural": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "food": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class CareGuideForm(forms.ModelForm):

    class Meta:
        model = CareGuide
        exclude = ["tree"]

        widgets = {
            "pruning_requirements": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "fertilization": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "watering_schedule": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "planting_time": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

