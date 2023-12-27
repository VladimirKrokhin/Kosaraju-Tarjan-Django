from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import DjangoModelPermissions
from algorythm import views


app_name = "algorythm"
urlpatterns = [
    # path("create/", views.create_graph, name="create"),
    path("index/", views.index_graphs, name='index-graphs'),
    path("index/<int:graph_id>/", views.index, name="index"),
    path('', views.ApiRoot.as_view(), name="api-root"),
]

urlpatterns += format_suffix_patterns([
    path('graphs/',
        views.GraphList.as_view(),
        name="graph-list"),
    path('graphs/<int:pk>/',
        views.GraphDetail.as_view(),
        name="graph-detail"),
    path('graphs/<int:graph_id>/nodes/',
        views.NodeListView.as_view(),
        name='node-list'),
    path('graphs/<int:graph_id>/nodes/<int:pk>/',
        views.NodeView.as_view(),
        name='node-detail'),
    path('graphs/<int:graph_id>/edges/',
        views.EdgeListView.as_view(),
        name='edge-list'),
    path('graphs/<int:graph_id>/edges/<int:pk>/',
        views.EdgeView.as_view(),
        name='edge-detail'),    
    path('graphs/<int:graph_id>/run-algorithm/', 
    views.RunAlgorithmView.as_view(),
    name='run-algorithm'),
    path('users/', 
        views.UserList.as_view(), 
        name="user-list"),
    path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name="user-detail")
])
