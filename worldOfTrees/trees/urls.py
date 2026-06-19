from django.urls import path
from . import views

app_name = "trees"

urlpatterns = [
    path("", views.trees, name="trees"),
    path("upload/", views.upload_tree, name="upload_tree"),
    path("edit/<int:tree_id>/", views.edit_tree, name="edit_tree"),
    #path("delete/<int:tree_id>/", views.delete_tree, name="delete_tree"),
    # NEW
    path("download-template/", views.download_tree_template, name="download_tree_template"),
    path("delete-multiple/",views.delete_trees,name="delete_trees"),
    path("profile/<int:tree_id>/", views.tree_profile, name="tree_profile"),
    path("profile/<int:tree_id>/qr/", views.tree_qr, name="tree_qr"),
    path("profile/<int:tree_id>/pdf/", views.tree_pdf, name="tree_pdf"),
]