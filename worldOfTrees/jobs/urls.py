from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_job, name='upload_job'),
    path('', views.job_list, name='job_list'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('edit-job/<int:id>/', views.edit_job, name='edit_job'),
]