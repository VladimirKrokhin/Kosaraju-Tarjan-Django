from algorythm.models import Graph, Node
from algorythm.serializers import GraphSerializer, UserSerializer, NodeSerializer, EdgeSerializer
from algorythm.permissions import IsOwnerOrReadOnly, IsGraphOwner
from algorythm.kosarajus_algorythm import kosaraju_algo
from algorythm.tarjans_algorythm import tarjan_algo


from rest_framework import generics, permissions, renderers, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, get_object_or_404



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'graphs': reverse('graph-list', request=request, format=format)
    })




class GraphList(generics.ListCreateAPIView):
    """
    Отображает список графов пользователя или созает новый граф.
    """
    queryset =  Graph.objects.all()
    serializer_class = GraphSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class GraphDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Получает, обновляет или удаляет экземпляр графа.
    """

    queryset =  Graph.objects.all()
    serializer_class = GraphSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
     serializer.save(owner=self.request.user)



class NodeView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Node.objects.all()        
        serializer_class = NodeSerializer
        permission_classes = [IsGraphOwner]

  



class NodeListView(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsGraphOwner]

    def perform_create(self, serializer):
        graph_id = self.kwargs['graph_id']  # Извлекаем 'graph_id' из URL параметров
        context = serializer.context
        context['graph_id'] = graph_id  # Передаем 'graph_id' в контекст сериализатора
        serializer.save()





class EdgeView(generics.RetrieveUpdateAPIView):
    queryset = Node.objects.all()
    serializer_class = EdgeSerializer
    permission_classes = [IsGraphOwner]


class EdgeListView(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = EdgeSerializer
    permission_classes = [IsGraphOwner]





class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class RunAlgorithmView(generics.GenericAPIView):
    def post(self, request,graph_id):
        algorithm_type = request.query_params.get('algorithm_type')
        print(algorithm_type)
        if algorithm_type == "kosaraju" or algorithm_type == "tarjan":
            graph = Graph.objects.get(pk=graph_id)
            node_list = graph.get_node_ids()
            adj_list = graph.get_adj_list()
            if algorithm_type == 'kosaraju':
                result_array = kosaraju_algo(adj_list, node_list)
            elif algorithm_type == "tarjan":
                result_array = tarjan_algo(adj_list, node_list)
        else:
            return Response("Неправильный тип алгоритма", status=status.HTTP_400_BAD_REQUEST)
        return Response(result_array, status=status.HTTP_200_OK)


    
@login_required
def index(request, graph_id):
    user = request.user
    graph = get_object_or_404(Graph, pk=graph_id)
    if (graph.owner == user):
        context = {"graph_id":graph_id}
        return render(request, 'index.html', context)
    else:
        return HttpResponseForbidden('You do not have permission to access this graph')



# @login_required
# def create_graph(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         owner = request.user
#         graph = Graph.create(name, owner)

#         return redirect(f'/index/{graph.id}')
#         # перенаправляем на страницу  созданного 

#     return render(request, "create_graph.html")


