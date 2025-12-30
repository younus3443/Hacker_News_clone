from django.urls import path
from . import views

app_name = "comments"
urlpatterns = [
    path('item/<int:id>/', views.item_detail, name='item'),
    path('item/<int:submission_id>/comment/', views.add_comment, name='add_comment'),
    path("comments/", views.show_comments, name="show_comments"),
    path("<int:pk>/edit/", views.edit_comment, name="edit_comment"),
    path("<int:pk>/delete/", views.delete_comment, name="delete_comment"),

]
