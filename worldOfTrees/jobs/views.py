from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.core.files.base import ContentFile
from django.http import JsonResponse
from io import BytesIO
from PIL import Image
import os


# ---------------------------
# IMAGE → WEBP CONVERSION
# ---------------------------
def convert_to_webp(image_file):
    image = Image.open(image_file)

    # Convert RGBA / palette images to RGB
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    output = BytesIO()

    image.save(output, format='WEBP', quality=85)
    output.seek(0)

    file_name = os.path.splitext(image_file.name)[0] + '.webp'

    return ContentFile(output.read(), name=file_name)


# ---------------------------
# TEXTAREA → JSON LIST
# ---------------------------
def to_list(value):
    if not value:
        return []
    return [item.strip() for item in value.split('\n') if item.strip()]


# ---------------------------
# UPLOAD JOB
# ---------------------------
def upload_job(request):
    if request.method == 'POST':
        title = request.POST.get('job-title')
        sector = request.POST.get('job-sector')
        description = request.POST.get('job-description')
        image = request.FILES.get('job-image')

        if not title:
            return JsonResponse({
                'success': False,
                'error': 'Title is required'
            })

        webp_image = convert_to_webp(image) if image else None

        job = Job.objects.create(
            title=title,
            sector=sector,
            description=description,
            image=webp_image
        )

        return JsonResponse({
            'success': True,
            'id': job.id,
            'title': job.title,
            'sector': job.sector
        })

    return JsonResponse({'success': False})


# ---------------------------
# JOB LIST (PAGINATION)
# ---------------------------
def job_list(request):
    jobs = Job.objects.all()

    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'jobs/list.html', {'jobs': jobs})


# ---------------------------
# DELETE JOB
# ---------------------------
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        job.delete()

        return JsonResponse({
            'success': True,
            'job_id': job_id
        })

    return JsonResponse({
        'success': False
    })


# ---------------------------
# EDIT JOB
# ---------------------------
def edit_job(request, id):
    job = get_object_or_404(Job, id=id)

    if request.method == 'POST':
        job.title = request.POST.get('job-title')
        job.sector = request.POST.get('job-sector')
        job.description = request.POST.get('job-description')

        image = request.FILES.get('job-image')
        if image:
            job.image = convert_to_webp(image)

        job.study = to_list(request.POST.get('job-study'))
        job.responsibilities = to_list(request.POST.get('job-responsibilities'))
        job.where_they_work = to_list(request.POST.get('job-where-they-work'))
        job.skills_required = to_list(request.POST.get('job-skills'))
        job.importance_of_work = to_list(request.POST.get('job-importance'))
        job.how_troot_supports = to_list(request.POST.get('job-supports'))

        job.save()

        return JsonResponse({
            'success': True
        })

    return JsonResponse({
        'success': False
    })