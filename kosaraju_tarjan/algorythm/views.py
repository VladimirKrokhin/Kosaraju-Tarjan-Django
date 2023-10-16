from django.shortcuts import render

# Create your views here.

def index(request, graph_id):
    return render(request, "index.html",
                   context={"graph_id" : graph_id})


