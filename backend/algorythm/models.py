from django.db import models
from django.contrib.auth.models import User
from pyvis.network import Network
from django.conf import settings

# import json

# Create your models here.


# Модель графа (как граф связан с пользователем)
class Graph(models.Model):
        id = models.BigAutoField(primary_key=True)
        name = models.CharField(verbose_name="graph's =  name", max_length=80)
        user = models.ForeignKey(User, on_delete=models.CASCADE)



        # def get_json(self):
        #         # Создать граф с помощью PyVis
        #         network = Network()

        #         # Получить вершины графа с помощью Django ORM выбирая по graph_id
        #         nodes = Node.objects.filter(graph_id=self.id)

        #         # Добавить вершины в PyVis граф
        #         for node in nodes:
        #             network.add_node(n_id = node.id, label = node.name)

        #         # Добавить ребра PyVis графу
        #         for node in nodes:
        #             for parent in node.parents.all():
        #                 network.add_edge(parent.id, node.id)

        #         # Получаем данные о PyVis графе в формате, который можно преобразовать в JSON
        #         graph_data = network.get_adj_list()
                
        #         graph_json = json.dump(graph_data)

        #         return  graph_json


        def add_node(self, name):
            return Node.create(name, self)


        def __str__(self):
            return self.name


        class Meta:
            ordering = ['id']



# Вершина
class Node(models.Model):
        id = models.BigAutoField(primary_key=True)
        name = models.CharField(verbose_name="node's name", max_length=80)
        graph = models.ForeignKey(Graph, db_column="graph_id", on_delete=models.CASCADE)
        # поле foreign key для связи вершины с графом
        parents = models.ManyToManyField("self", related_name="children", symmetrical=False)

        def __str__(self):
                return self.name


        def create(self, name, graph):
            """
            Создает и возвращает новую "Node" сущность основываясь на валидированных данных
            """
            return Node.objects.create(name = name, graph = graph)


        def update(self, instance, name, parents):
            """
            Изменяет и возвращает существующую "Node" сущность основываясь на валидированных данных.
            """
            instance.name = name
            instance.parents = parents
            instance.save()
            return instance
