from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import DjangoModelPermissions
from algorythm import views


app_name = "algorythm"
urlpatterns = [
    path('graphs/', views.GraphList.as_view()),
    path('graphs/<int:pk>/', views.GraphDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    # path("create/", views.create_graph, name="create"),
    path("index/<int:graph_id>/", views.index, name="index"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
