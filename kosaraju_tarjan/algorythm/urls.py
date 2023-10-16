from django.urls import path

from . import views

urlpatterns = [
    path("<int:graph_id>/", views.index,
          name="index"),
]