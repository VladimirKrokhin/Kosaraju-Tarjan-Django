from django.shortcuts import render, redirect
from .models import Node, Graph
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import NodeSerializer, GraphSerializer, UserSerializer
from django.contrib.auth.models import User

# Create your views here.

def index(request, graph_id):
    context = {"graph_id": graph_id}
    return render(request, "algorythm/index.html",
                   context=context)

def create_graph(request):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        user = request.user

        return redirect("graph_detail", pk=graph.create(id = id, name = name, user = user))
    # перенаправляем на страницу деталей созданного графа

    return render(request, "algorythm/create.graph.html")

class GraphViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows graphs to be viewed or edited.
    """
    queryset = Graph.objects.all().order_by('id')
    serializer_class = GraphSerializer
    permission_classes = [permissions.IsAuthenticated]

class NodeViewSet(viewsets.ModelViewSet):
    """
    API endpint that allows nodes to be viewed or edited
    """

    # TODO: Переделай, чтобы отображал вершины конкретного графа
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # TODO: Сделай отображение только для конкретных пользователей

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
