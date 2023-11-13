from django.shortcuts import render, redirect
from .models import Node

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

        graph = Node.objects.create(id=id, name=name, user=user)

        return redirect("graph_detail", pk=graph.pk)
    # перенаправляем на страницу деталей созданного графа

    return render(request, "algorythm/create.graph.html")
