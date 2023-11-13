from django.urls import path

from . import views


app_name = "algorythm"
urlpatterns = [
    path("<int:graph_id>/", views.index,
          name="index"),
    path("create/", views.create_graph, name="create")
]