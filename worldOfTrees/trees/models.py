from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class Tree(models.Model):

    TREE_TYPES = [
        ("deciduous", "Deciduous"),
        ("evergreen", "Evergreen"),
        ("conifer", "Conifer"),
    ]

    CONSERVATION_STATUS = [
        ("LC", "Least Concern"),
        ("NT", "Near Threatened"),
        ("VU", "Vulnerable"),
        ("EN", "Endangered"),
        ("CR", "Critically Endangered"),
    ]

    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=255, unique=True)
    family = models.CharField(max_length=200)

    tree_type = models.CharField(
        max_length=50,
        choices=TREE_TYPES
    )

    native_region = models.CharField(max_length=255)

    conservation_status = models.CharField(
        max_length=2,
        choices=CONSERVATION_STATUS,
        default="LC"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["common_name"]

    def __str__(self):
        return self.common_name


class PhysicalCharacteristics(models.Model):

    GROWTH_RATES = [
        ("slow", "Slow"),
        ("moderate", "Moderate"),
        ("fast", "Fast"),
    ]

    tree = models.OneToOneField(
        Tree,
        on_delete=models.CASCADE,
        related_name="physical"
    )

    average_height_m = models.FloatField(null=True, blank=True)
    canopy_spread_m = models.FloatField(null=True, blank=True)
    trunk_diameter_cm = models.FloatField(null=True, blank=True)

    growth_rate = models.CharField(
        max_length=20,
        choices=GROWTH_RATES,
        blank=True
    )

    lifespan_years = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    leaf_description = models.TextField(blank=True)
    bark_description = models.TextField(blank=True)
    flower_description = models.TextField(blank=True)
    fruit_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tree.common_name} Characteristics"


class Habitat(models.Model):

    tree = models.OneToOneField(
        Tree,
        on_delete=models.CASCADE,
        related_name="habitat"
    )

    native_range = models.TextField(blank=True)
    introduced_regions = models.TextField(blank=True)

    preferred_climate = models.CharField(
        max_length=200,
        blank=True
    )

    hardiness_zone = models.CharField(
        max_length=100,
        blank=True
    )

    elevation_min_m = models.IntegerField(
        null=True,
        blank=True
    )

    elevation_max_m = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tree.common_name} Habitat"


class GrowingConditions(models.Model):

    tree = models.OneToOneField(
        Tree,
        on_delete=models.CASCADE,
        related_name="growing_conditions"
    )

    sunlight = models.CharField(
        max_length=100,
        blank=True
    )

    soil_type = models.CharField(
        max_length=200,
        blank=True
    )

    soil_ph = models.CharField(
        max_length=100,
        blank=True
    )

    water_requirements = models.CharField(
        max_length=100,
        blank=True
    )

    drought_tolerance = models.CharField(
        max_length=100,
        blank=True
    )

    frost_tolerance = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"{self.tree.common_name} Growing Conditions"


class EcologicalImportance(models.Model):

    tree = models.OneToOneField(
        Tree,
        on_delete=models.CASCADE,
        related_name="ecology"
    )

    carbon_sequestration = models.TextField(blank=True)
    wildlife_supported = models.TextField(blank=True)
    pollinators_attracted = models.TextField(blank=True)
    soil_benefits = models.TextField(blank=True)
    ecosystem_role = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tree.common_name} Ecology"


class TreeUses(models.Model):

    tree = models.OneToOneField(
        Tree,
        on_delete=models.CASCADE,
        related_name="uses"
    )

    timber = models.TextField(blank=True)
    landscaping = models.TextField(blank=True)
    medicinal = models.TextField(blank=True)
    cultural = models.TextField(blank=True)
    food = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tree.common_name} Uses"


class Threat(models.Model):

    THREAT_TYPES = [
        ("disease", "Disease"),
        ("pest", "Pest"),
        ("environmental", "Environmental"),
    ]

    tree = models.ForeignKey(
        Tree,
        on_delete=models.CASCADE,
        related_name="threats"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    threat_type = models.CharField(
        max_length=20,
        choices=THREAT_TYPES
    )

    def __str__(self):
        return f"{self.name} ({self.get_threat_type_display()})"


class CareGuide(models.Model):

    tree = models.OneToOneField(
        Tree,
        on_delete=models.CASCADE,
        related_name="care"
    )

    pruning_requirements = models.TextField(blank=True)
    fertilization = models.TextField(blank=True)
    watering_schedule = models.TextField(blank=True)
    planting_time = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tree.common_name} Care Guide"


class TreeImage(models.Model):

    IMAGE_TYPES = [
        ("general", "General"),
        ("leaf", "Leaf"),
        ("bark", "Bark"),
        ("flower", "Flower"),
        ("fruit", "Fruit"),
    ]

    tree = models.ForeignKey(
        Tree,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="trees/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPES,
        default="general"
    )

    def save(self, *args, **kwargs):

        if self.image:

            img = Image.open(self.image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output = BytesIO()

            img.save(
                output,
                format="WEBP",
                quality=85
            )

            output.seek(0)

            filename = os.path.splitext(
                self.image.name
            )[0]

            self.image = ContentFile(
                output.read(),
                name=f"{filename}.webp"
            )

        super().save(*args, **kwargs)