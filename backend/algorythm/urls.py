from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import DjangoModelPermissions
from . import views


app_name = "algorythm"
urlpatterns = [
    path('graphs/', views.graph_list),
    path('graphs/<int:pk>/', views.graph_detail),
    # path("create/", views.create_graph, name="create"),
    path("index/<int:graph_id>/", views.index, name="index"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
