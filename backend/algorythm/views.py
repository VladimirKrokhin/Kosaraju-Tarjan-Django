from algorythm.models import Graph
from algorythm.serializers import GraphSerializer, GraphDetailSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404


class GraphList(APIView):
        """
        Отображает список графов пользователя или созает новый граф.
        """

        @authentication_classes([SessionAuthentication, BasicAuthentication])
        @permission_classes([IsAuthenticated])
        def get(self, request, format=None):
            user = request.user
            graphs = Graph.objects.filter(user=user)
            
            if not graphs:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = GraphSerializer(graphs, many=True)
            return Response(serializer.data)


        @authentication_classes([SessionAuthentication, BasicAuthentication])
        @permission_classes([IsAuthenticated])
        def post(self, request, format=None):
            serializer = GraphSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class GraphDetail(APIView):
    """
    Получает, обновляет или удаляет экземпляр графа.
    """

    def get_object(self, pk, user):
        try:
            return Graph.objects.get(pk=pk, user=user)
        except Snippet.DoesNotExist:
            raise Http404

    
    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, pk, format=None):
        graph = self.get_object(pk=pk, user=request.user)
        serializer = GraphDetailSerializer(graph)
        return Response(serializer.data)


    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def put(self, request, pk, format=None):
        graph = self.get_object(pk=pk, user=request.user)
        serializer = GraphDetailSerializer(graph, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @authentication_classes([SessionAuthentication, BasicAuthentication])
    @permission_classes([IsAuthenticated])
    def delete(self, request, pk, format=None):
        graph = self.get_object(pk, user=request.user)
        graph.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    
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

        return redirect(f'/index/{graph.id}')
        # перенаправляем на страницу  созданного 

    return render(request, "create_graph.html")



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