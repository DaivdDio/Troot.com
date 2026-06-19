from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from .models import BackupSchedule, BackupLog
from datetime import time as dt_time
from datetime import datetime
import subprocess
import json
import os
import tempfile

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('login')  # or wherever your page is

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('login')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return redirect('login')

def superuser_only(user):
    return user.is_superuser


@user_passes_test(superuser_only)
def backup_database(request):

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"db_backup_{timestamp}.json"

    fd, file_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            call_command("dumpdata", indent=2, stdout=f)

        # 🔥 LOG SUCCESS
        BackupLog.objects.create(
            status="success",
            filename=filename,
            message="Manual backup completed successfully"
        )

        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/json")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

    except Exception as e:

        # 🔥 LOG FAILURE
        BackupLog.objects.create(
            status="failed",
            filename=filename,
            message=str(e)
        )

        return HttpResponse(f"Backup failed: {str(e)}", status=500)

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@user_passes_test(lambda u: u.is_superuser)
def restore_database(request):

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    file = request.FILES.get("backup_file")

    if not file:
        return HttpResponse("No file uploaded", status=400)

    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)

    try:
        with open(temp_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        call_command("loaddata", temp_path)

        return HttpResponse("Database restored successfully!")

    except Exception as e:
        return HttpResponse(f"Restore failed: {str(e)}", status=500)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@user_passes_test(lambda u: u.is_superuser)
def save_backup_schedule(request):

    if request.method == "POST":

        enabled = request.POST.get("enabled") == "on"
        interval = request.POST.get("interval")
        time_value = request.POST.get("time")

        days = request.POST.getlist("days")
        days_str = ",".join(days)

        schedule, created = BackupSchedule.objects.get_or_create(id=1)

        schedule.enabled = enabled
        schedule.interval = interval
        schedule.time = time_value or None
        schedule.days = days_str
        schedule.save()

        # 🔥 send success flag
        return redirect("/preferences/?section=security&saved=schedule")