from django.urls import path
from . import views

urlpatterns = [
    path("", views.preferences, name="preferences"),
    path("tree/<int:tree_id>/", views.tree_details, name="tree_details"),
    path("tree/image/delete/<int:image_id>/", views.delete_tree_image, name="delete_tree_image"),
    path("tree/threat/edit/<int:threat_id>/", views.edit_threat, name="edit_threat"),
    path("tree/<int:tree_id>/upload-image/", views.ajax_upload_image, name="ajax_upload_image"),
    
]