from algorythm.models import Graph, Node
from algorythm.serializers import GraphSerializer, UserSerializer, NodeSerializer, EdgeSerializer, RunAlgorithmSerializer
from algorythm.permissions import IsOwnerOrReadOnly, IsGraphOwner
from algorythm.kosarajus_algorythm import kosaraju_algo
from algorythm.tarjans_algorythm import tarjan_algo
from algorythm.forms import RegistrationForm, LoginForm, GraphForm

from rest_framework import generics, permissions, renderers, mixins, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect



class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'users': reverse('algorythm:user-list', request=request),
            'graphs': reverse('algorythm:graph-list', request=request),
        })



class GraphList(generics.ListCreateAPIView):
    """
    Отображает список графов пользователя или созает новый граф.
    """

    serializer_class = GraphSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Graph.objects.filter(owner=user)


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
    serializer_class = NodeSerializer
    permission_classes = [IsGraphOwner]

    def get_queryset(self):
        graph_id = self.kwargs['graph_id']  # Извлекаем 'graph_id' из URL параметров
        return Node.objects.filter(graph_id=graph_id)

    


class NodeListView(generics.ListCreateAPIView):
    serializer_class = NodeSerializer
    permission_classes = [IsGraphOwner]

    def get_queryset(self):
        graph_id = self.kwargs['graph_id']
        return Node.objects.filter(graph_id=graph_id)

    def perform_create(self, serializer):
        graph_id = self.kwargs['graph_id']
        serializer.save(graph_id=graph_id)


class EdgeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EdgeSerializer
    permission_classes = [IsGraphOwner]

    def get_queryset(self):
        graph_id = self.kwargs['graph_id']  # Извлекаем 'graph_id' из URL параметров
        return Node.objects.filter(graph_id=graph_id)


class EdgeListView(generics.ListCreateAPIView):
    serializer_class = EdgeSerializer
    permission_classes = [IsGraphOwner]

    def get_queryset(self):
        graph_id = self.kwargs['graph_id']  # Извлекаем 'graph_id' из URL параметров
        return Node.objects.filter(graph_id=graph_id)

    def perform_create(self, serializer):
        graph_id = self.kwargs['graph_id']
        serializer.save(graph_id=graph_id)





class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class RunAlgorithmView(APIView):
    serializer_class = RunAlgorithmSerializer

    def post(self, request, graph_id):
        serializer = RunAlgorithmSerializer(data={'graph_id': graph_id, 'algorithm_type': request.query_params.get('algorithm_type')})
        if serializer.is_valid():
            result_array = serializer.retrieve(serializer.validated_data)
            return Response(result_array, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index_graphs(request):
    if request.method == "POST":
        form = GraphForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            owner = request.user
            graph = Graph(name=name, owner=owner)
            graph.save()
            messages.success(request, "Граф успешно создан!")
            return redirect('algorythm:index-graphs')
    else:
        form = GraphForm()
    return render(request, 'graph_list.html', {'form': form})
    
@login_required
def index(request, graph_id):
    user = request.user
    graph = get_object_or_404(Graph, pk=graph_id)
    if (graph.owner == user):
        context = {"graph_id":graph_id}
        return render(request, 'index.html', context)
    else:
        return HttpResponseForbidden('You do not have permission to access this graph')






def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '') 
                if next_url: 
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('algorythm:index-graphs')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

   
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})