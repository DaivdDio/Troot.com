from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path("backup-database/", views.backup_database, name="backup_database"),
    path("restore-database/", views.restore_database, name="restore_database"),
    path("backup-schedule/", views.save_backup_schedule, name="save_backup_schedule"),
]