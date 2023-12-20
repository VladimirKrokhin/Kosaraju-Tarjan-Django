from django.shortcuts import render, redirect, get_object_or_404
from .models import Node, Graph
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import NodeSerializer, GraphSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseForbidden


# Create your views here.

@login_required
def index(request, graph_id):
    user = request.user
    graph = get_object_or_404(Graph, pk=graph_id)
    if (graph.user.id == user.id):
        context = {"graph_id":graph_id}
        return render(request, 'index.html', context)
    else:
        return HttpResponseForbidden('You do not have permission to access this graph')

@login_required
def create_graph(request):
    if request.method == "POST":
        name = request.POST["name"]
        user = request.user
        graph = Graph.create(name, user)

        return redirect(f'/graph/{graph.id}')
        # перенаправляем на страницу  созданного 

    return render(request, "create_graph.html")



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
