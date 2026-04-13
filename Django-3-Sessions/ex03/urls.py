from django.urls import path

from . import views

urlpatterns = [
    path("tips/<int:tip_id>/upvote/", views.upvote_tip, name="tip_upvote"),
    path("tips/<int:tip_id>/downvote/", views.downvote_tip, name="tip_downvote"),
    path("tips/<int:tip_id>/delete/", views.delete_tip, name="tip_delete"),
]
