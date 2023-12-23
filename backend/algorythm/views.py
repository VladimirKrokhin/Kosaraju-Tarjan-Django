from .models import Graph

from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from algorythm.serializers import GraphSerializer, GraphDetailSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse




@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def graph_list(request, format=None):
    """
    Отображает список графов пользователя или создает новый граф.
    """

    user = request.user


    if request.method == "GET":
        try:
            graphs = Graph.objects.filter(user=user)
        except Graph.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GraphSerializer(graphs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GraphSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def graph_detail(request, pk, format=None):
    """
    Получает, обновляет или удаляет граф.
    """


    user = request.user
    try:
        graph = Graph.objects.get(pk=pk, user=user)
    except Graph.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = GraphDetailSerializer(graph)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GraphSerializer(graph, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        graph.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


    
@login_required
def index(request, graph_id):
    user = request.user
    graph = get_object_or_404(Graph, pk=graph_id)
    if (graph.user.id == user.id):
        context = {"graph_id":graph_id}
        return render(request, 'index.html', context)
    else:
        return HttpResponseForbidden('You do not have permission to access this graph')

# @login_required
# def create_graph(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         user = request.user
#         graph = Graph.create(name, user)

#         return redirect(f'/graph/{graph.id}')
#         # перенаправляем на страницу  созданного 

#     return render(request, "create_graph.html")



# class GraphViewSet(viewsets.ModelViewSet):
#     """
#     API эндпоинт который позволяет просматривать или редактировать граф.
#     """
#     queryset = Graph.objects.all()
#     serializer_class = GraphSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def list(self, request):
#         user = request.user  # Получаем текущего пользователя
#         graphs = Graph.objects.filter(user=user)  # Получаем все графы, принадлежащие этому пользователю
#         serializer = GraphSerializer(graphs, context = {'request': request}, many=True)  # Сериализуем полученные графы
#         return Response(serializer.data)