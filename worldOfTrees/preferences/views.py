from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from jobs.models import Job
from trees.models import Tree
from django.db.models import Q
from core.models import SiteStats
from django.db.models import Count
from trees.models import *
from trees.forms import *
from .forms import *
from django.contrib import messages
from accounts.models import BackupSchedule, BackupLog
from django.contrib.auth.models import User
import json



# Create your views here.
def tree_details(request, tree_id):

    tree = get_object_or_404(Tree, pk=tree_id)

    tree = get_object_or_404(Tree.objects.select_related(

    ), pk=tree_id)
    

    physical, _ = PhysicalCharacteristics.objects.get_or_create(
        tree=tree
    )

    habitat, _ = Habitat.objects.get_or_create(
        tree=tree
    )

    conditions, _ = GrowingConditions.objects.get_or_create(
        tree=tree
    )

    ecology, _ = EcologicalImportance.objects.get_or_create(
        tree=tree
    )

    uses, _ = TreeUses.objects.get_or_create(
        tree=tree
    )

    care, _ = CareGuide.objects.get_or_create(
        tree=tree
    )

    # Profile completion calculation

    completed = 0
    total = 8

    if physical.average_height_m:
        completed += 1

    if habitat.native_range:
        completed += 1

    if conditions.sunlight:
        completed += 1

    if ecology.ecosystem_role:
        completed += 1

    if uses.timber:
        completed += 1

    if care.planting_time:
        completed += 1

    if tree.threats.exists():
        completed += 1

    if tree.images.exists():
        completed += 1

    completion_percentage = int(
        (completed / total) * 100
    )

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        if form_type == "physical":

            form = PhysicalCharacteristicsForm(
                request.POST,
                instance=physical
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Physical characteristics saved successfully."
                )

        elif form_type == "habitat":

            form = HabitatForm(
                request.POST,
                instance=habitat
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Habitat information saved successfully."
                )

        elif form_type == "conditions":

            form = GrowingConditionsForm(
                request.POST,
                instance=conditions
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Growing conditions saved successfully."
                )

        elif form_type == "ecology":

            form = EcologicalImportanceForm(
                request.POST,
                instance=ecology
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Ecological information saved successfully."
                )

        elif form_type == "uses":

            form = TreeUsesForm(
                request.POST,
                instance=uses
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Tree uses saved successfully."
                )

        elif form_type == "care":

            form = CareGuideForm(
                request.POST,
                instance=care
            )

            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "Care guide saved successfully."
                )

        elif form_type == "threat":

            form = ThreatForm(request.POST)

            if form.is_valid():

                threat = form.save(commit=False)

                threat.tree = tree

                threat.save()

                messages.success(
                    request,
                    "Threat added successfully."
                )

        elif form_type == "image":

            form = TreeImageForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():

                image = form.save(
                    commit=False
                )

                image.tree = tree

                image.save()

                messages.success(
                    request,
                    "Image uploaded successfully."
                )
        else:
            messages.error(request, "Please correct the errors below.")

    physical_form = PhysicalCharacteristicsForm(
        instance=physical
    )

    habitat_form = HabitatForm(
        instance=habitat
    )

    conditions_form = GrowingConditionsForm(
        instance=conditions
    )

    ecology_form = EcologicalImportanceForm(
        instance=ecology
    )

    uses_form = TreeUsesForm(
        instance=uses
    )

    care_form = CareGuideForm(
        instance=care
    )

    threat_form = ThreatForm()
    threats = tree.threats.all()

    image_form = TreeImageForm()
    images = tree.images.all()

    context = {
        "tree": tree,

        "physical_form": physical_form,
        "habitat_form": habitat_form,
        "conditions_form": conditions_form,
        "ecology_form": ecology_form,
        "uses_form": uses_form,
        "care_form": care_form,

        "threat_form": threat_form,
        "threats": threats,
        "image_form": image_form,
        "images": images,
        "completion_percentage": completion_percentage,
    }

    return render(
        request,
        "preferences/tree_details.html",
        context
    )

def preferences(request):

    section = request.GET.get("section", "general")
    stats, created = SiteStats.objects.get_or_create(pk=1)

    context = {
        "section": section,
        "tree_count": Tree.objects.count(),
        "job_count": Job.objects.count(),
        "visit_count": stats.total_visits,
    }

    # ------------------------------------------------------------
    # Backup Scheduler
    # ------------------------------------------------------------

    days = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

    schedule, created = BackupSchedule.objects.get_or_create(
        id=1,
        defaults={
            "enabled": False,
            "interval": "daily",
            "days": "",
        }
    )

    context["days"] = days
    context["schedule"] = schedule
    context["schedule_days"] = (
        schedule.days.split(",")
        if schedule.days
        else []
    )

    context["saved"] = request.GET.get("saved")

    # ------------------------------------------------------------
    # Jobs Section
    # ------------------------------------------------------------

    if section == "jobs":

        action = request.GET.get("action")
        context["action"] = action

        edit_id = request.GET.get("edit")
        context["edit_id"] = edit_id

        if edit_id:
            context["edit_job"] = Job.objects.filter(id=edit_id).first()

        search = request.GET.get("search", "")

        job_list = Job.objects.all().order_by("-id")

        if search:
            job_list = job_list.filter(
                Q(title__icontains=search) |
                Q(sector__icontains=search)
            )

        paginator = Paginator(job_list, 6)

        page_number = request.GET.get("page")
        jobs = paginator.get_page(page_number)

        context["jobs"] = jobs
        context["search"] = search

    # ------------------------------------------------------------
    # Trees Section
    # ------------------------------------------------------------

    if section == "trees":

        search = request.GET.get("search", "")
        edit_id = request.GET.get("edit")
        action = request.GET.get("action")
        view_mode = request.GET.get("view", "list")

        tree_list = Tree.objects.all()

        if search:
            tree_list = tree_list.filter(
                Q(common_name__icontains=search) |
                Q(scientific_name__icontains=search) |
                Q(family__icontains=search)
            )

        per_page = 9 if view_mode == "grid" else 6

        paginator = Paginator(tree_list, per_page)

        page_number = request.GET.get("page")
        trees = paginator.get_page(page_number)

        context["trees"] = trees
        context["search"] = search
        context["action"] = action
        context["view_mode"] = view_mode

        if edit_id:
            context["edit_tree"] = (
                Tree.objects.filter(id=edit_id).first()
            )

    if section == "users":

        if not request.user.is_superuser:
            return redirect("preferences")

        search = request.GET.get("search", "")

        users = User.objects.filter(
            is_superuser=False
        ).order_by("username")

        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )

        context["users"] = users
        context["search"] = search

    # ------------------------------------------------------------
    # Dashboard Charts
    # ------------------------------------------------------------

    tree_type_data = (
        Tree.objects.values("tree_type")
        .annotate(total=Count("id"))
    )

    conservation_data = (
        Tree.objects.values("conservation_status")
        .annotate(total=Count("id"))
    )

    context["tree_type_labels"] = json.dumps(
        [item["tree_type"].title() for item in tree_type_data]
    )

    context["tree_type_counts"] = json.dumps(
        [item["total"] for item in tree_type_data]
    )

    context["conservation_labels"] = json.dumps(
        [item["conservation_status"] for item in conservation_data]
    )

    context["conservation_counts"] = json.dumps(
        [item["total"] for item in conservation_data]
    )

    # ------------------------------------------------------------
    # Backup Logs
    # ------------------------------------------------------------

    context["backup_logs"] = (
        BackupLog.objects
        .order_by("-created_at")[:10]
    )

    # ------------------------------------------------------------

    return render(
        request,
        "preferences/preferences.html",
        context
    )

def delete_tree_image(request, image_id):

    image = get_object_or_404(
        TreeImage,
        pk=image_id
    )

    tree_id = image.tree.id

    image.delete()

    messages.success(
        request,
        "Image deleted successfully."
    )

    return redirect(
        "tree_details",
        tree_id=tree_id
    )

def edit_threat(request, threat_id):

    threat = get_object_or_404(
        Threat,
        pk=threat_id
    )

    if request.method == "POST":

        form = ThreatForm(
            request.POST,
            instance=threat
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Threat updated successfully."
            )

            return redirect(
                "tree_details",
                tree_id=threat.tree.id
            )

    else:

        form = ThreatForm(
            instance=threat
        )

    return render(
        request,
        "preferences/edit_threat.html",
        {
            "form": form,
            "threat": threat
        }
    )

def ajax_upload_image(request, tree_id):

    tree = get_object_or_404(
        Tree,
        pk=tree_id
    )

    if request.method == "POST":

        form = TreeImageForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            image = form.save(commit=False)

            image.tree = tree

            image.save()

            return JsonResponse({
                "success": True,
                "image_url": image.image.url,
                "caption": image.caption,
                "image_type": image.get_image_type_display(),
            })

        return JsonResponse({
            "success": False,
            "errors": form.errors
        })

    return JsonResponse({
        "success": False
    })

