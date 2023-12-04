from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Модель графа (как граф связан с пользователем)
class Graph(models.Model):
        id = models.BigAutoField(primary_key=True)
        name = models.CharField(verbose_name="graph's =  name", max_length=80)
        user = models.ForeignKey(User, on_delete=models.CASCADE)

        def create(self, name, user):
            """
            Создает и возвращает новую "Graph" сущность основываясь на валидированных данных.
            """
            return Graph.objects.create(name = name, user = user)

        def update(self, instance, name):
            """
            Изменяет и возвращает существующую "Graph" сущность основываясь на валидированных данных.
            """
            instance.name = name
            instance.save()
            return instance

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
