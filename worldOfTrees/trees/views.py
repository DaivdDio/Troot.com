from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.http import JsonResponse, HttpResponse
from datetime import date, datetime
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Q
import json
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet

from .models import Tree

def trees(request):
    tree_list = Tree.objects.prefetch_related("images")
    trees = tree_list

    search = request.GET.get("search", "")
    tree_type = request.GET.get("tree_type", "")
    status = request.GET.get("status", "")
    sort = request.GET.get("sort", "name_asc")
    
    # Get page number, but we'll handle reset logic differently
    page_number = request.GET.get("page", 1)
    
    # Apply filters first
    if search:
        trees = trees.filter(
            Q(common_name__icontains=search) |
            Q(scientific_name__icontains=search) |
            Q(family__icontains=search)
        )

    if tree_type:
        trees = trees.filter(tree_type=tree_type)

    if status:
        trees = trees.filter(conservation_status=status)

    # IMPORTANT: Always include ID in ordering to ensure consistency
    if sort == "name_asc":
        trees = trees.order_by("common_name", "id")  # Added id for tie-breaking
    elif sort == "name_desc":
        trees = trees.order_by("-common_name", "id")  # Added id for tie-breaking
    elif sort == "newest":
        trees = trees.order_by("-id", "-created_at")  # Added created_at for tie-breaking
    elif sort == "oldest":
        trees = trees.order_by("id", "created_at")  # Added created_at for tie-breaking
    else:
        trees = trees.order_by("common_name", "id")  # Default with tie-breaking

    # Paginate
    paginator = Paginator(trees, 12)
    page_obj = paginator.get_page(page_number)

    # AJAX requests
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Get current filter state for client-side tracking
        filter_state = {
            'search': search,
            'tree_type': tree_type,
            'status': status,
            'sort': sort,
            'page': int(page_number)
        }
        
        html = render_to_string(
            "trees/partials/tree_cards.html",
            {"trees": page_obj}
        )

        return JsonResponse({
            "html": html,
            "has_next": page_obj.has_next(),
            "current_page": int(page_number),
            "total_pages": paginator.num_pages,
            "filter_state": filter_state  # Send filter state to client
        })
    
    context = {
        "trees": page_obj,
        "search": search,
        "tree_type": tree_type,
        "status": status,
        "sort": sort,
    }

    return render(request, "trees/trees.html", context)


def upload_tree(request):
    if request.method == "POST":

        # ==========================
        # EXCEL IMPORT
        # ==========================
        excel_file = request.FILES.get("excel_file")

        if excel_file:

            try:
                df = pd.read_excel(excel_file)

                created = 0
                skipped = 0
                duplicates = []

                for _, row in df.iterrows():

                    scientific_name = str(row.get("scientific_name", "")).strip()

                    if not scientific_name:
                        continue  # skip empty rows

                    # duplicate check (case-insensitive safe)
                    exists = Tree.objects.filter(
                        scientific_name__iexact=scientific_name
                    ).exists()

                    if exists:
                        skipped += 1
                        duplicates.append(scientific_name)
                        continue

                    Tree.objects.create(
                        common_name=row.get("common_name"),
                        scientific_name=scientific_name,
                        family=row.get("family"),
                        tree_type=row.get("tree_type"),
                        native_region=row.get("native_region"),
                        conservation_status=row.get("conservation_status"),
                    )

                    created += 1

                return JsonResponse({
                    "success": True,
                    "imported": created,
                    "skipped": skipped,
                    "duplicates": duplicates,
                    "message": (
                        f"{created} trees imported, {skipped} duplicates skipped"
                        if created > 0 or skipped > 0
                        else "No valid rows found"
                    )
                })

            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": f"Excel import failed: {str(e)}"
                })


        # ==========================
        # SINGLE TREE CREATE
        # ==========================

        scientific_name = request.POST.get("scientific_name", "").strip()

        if Tree.objects.filter(scientific_name__iexact=scientific_name).exists():
            return JsonResponse({
                "success": False,
                "error": "Tree already exists."
            })

        tree = Tree.objects.create(
            common_name=request.POST.get("common_name"),
            scientific_name=scientific_name,
            family=request.POST.get("family"),
            tree_type=request.POST.get("tree_type"),
            native_region=request.POST.get("native_region"),
            conservation_status=request.POST.get("conservation_status"),
        )

        return JsonResponse({
            "success": True,
            "message": "Tree saved successfully.",
            "id": tree.id
        })

    return JsonResponse({"success": False})


def edit_tree(request, tree_id):
    tree = get_object_or_404(Tree, id=tree_id)

    if request.method == "POST":
        try:
            tree.common_name = request.POST.get("common_name", "")
            tree.scientific_name = request.POST.get("scientific_name", "")
            tree.family = request.POST.get("family", "")
            tree.tree_type = request.POST.get("tree_type", "")
            tree.native_region = request.POST.get("native_region", "")
            tree.conservation_status = request.POST.get("conservation_status", "")

            tree.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=400)

    return JsonResponse({"success": False}, status=405)


def delete_trees(request):
    if request.method == "POST":

        data = json.loads(request.body)

        ids = data.get("ids", [])

        deleted, _ = Tree.objects.filter(id__in=ids).delete()

        return JsonResponse({
            "success": True,
            "deleted": deleted
        })

    return JsonResponse({
        "success": False
    })

def download_tree_template(request):

    df = pd.DataFrame([
        {
            "common_name": "Mango",
            "scientific_name": "Mangifera indica",
            "family": "Anacardiaceae",
            "tree_type": "evergreen",
            "native_region": "South Asia",
            "conservation_status": "LC",
        }
    ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    #from datetime import date
    timestamp = datetime.now().strftime("%d-%b-%Y_%H-%M")

    response["Content-Disposition"] = (
        f'attachment; filename="tree_import_template_{timestamp}.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Trees")

    return response

def tree_profile(request, tree_id):

    tree = get_object_or_404(
        Tree,
        pk=tree_id
    )

    featured_image = tree.images.first()

    context = {
        "tree": tree,
        "featured_image": featured_image,
    }

    return render(
        request,
        "trees/tree_profile.html",
        context
    )

def tree_qr(request, tree_id):

    tree = get_object_or_404(
        Tree,
        pk=tree_id
    )

    url = request.build_absolute_uri(
        reverse(
            "trees:tree_profile",
            args=[tree.id]
        )
    )

    qr = qrcode.make(url)

    buffer = BytesIO()

    qr.save(buffer, format="PNG")

    return HttpResponse(
        buffer.getvalue(),
        content_type="image/png"
    )

def tree_pdf(request, tree_id):

    tree = get_object_or_404(
        Tree,
        pk=tree_id
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="Troot.com-{tree.common_name}.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    content = []

    # Title

    content.append(
        Paragraph(
            tree.common_name,
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            tree.scientific_name,
            styles["Italic"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # Overview

    content.append(
        Paragraph(
            "<b>Overview</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Family: {tree.family}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Tree Type: {tree.get_tree_type_display()}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Conservation Status: {tree.get_conservation_status_display()}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    if hasattr(tree, "physical"):

        content.append(
            Paragraph(
                "Physical Characteristics",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                f"Average Height: {tree.physical.average_height_m or 'N/A'} m",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                f"Growth Rate: {tree.physical.get_growth_rate_display()}",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                tree.physical.leaf_description or "",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 12)
        )
        
    if hasattr(tree, "habitat"):

        content.append(
            Paragraph(
                "Habitat",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                tree.habitat.native_range or "",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                tree.habitat.preferred_climate or "",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

    if hasattr(tree, "uses"):

        content.append(
            Paragraph(
                "Uses",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                tree.uses.timber or "",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                tree.uses.medicinal or "",
                styles["BodyText"]
            )
        )

        content.append(
            Paragraph(
                tree.uses.landscaping or "",
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

    if tree.threats.exists():

        content.append(
            Paragraph(
                "Threats",
                styles["Heading2"]
            )
        )

        for threat in tree.threats.all():

            content.append(
                Paragraph(
                    f"• {threat.name} ({threat.get_threat_type_display()})",
                    styles["BodyText"]
                )
            )

        content.append(
            Spacer(1, 12)
        )

    doc.build(content)

    return response
    
    