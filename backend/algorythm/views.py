from algorythm.models import Graph
from algorythm.serializers import GraphSerializer, GraphDetailSerializer, UserSerializer
from algorythm.permissions import IsOwnerOrReadOnly

from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404



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
    serializer_class = GraphDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)





class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    
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


