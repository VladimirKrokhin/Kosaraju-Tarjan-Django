from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'graphes', views.GraphViewSet)
router.register(r'nodes', views.NodeViewSet)

app_name = "algorythm"
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("<int:graph_id>/", views.index, name="index"),
    path("create/", views.create_graph, name="create")
]

urlpatterns += router.urls
