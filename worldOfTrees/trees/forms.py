from django import forms
from .models import Threat
from trees.models import *

class ThreatForm(forms.ModelForm):

    class Meta:
        model = Threat

        exclude = ["tree"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "threat_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
        }

class TreeImageForm(forms.ModelForm):

    class Meta:
        model = TreeImage

        exclude = ["tree"]

        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "caption": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "image_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }