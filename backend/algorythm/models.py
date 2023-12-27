from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Модель графа (как граф связан с пользователем)
class Graph(models.Model):
        id = models.BigAutoField(primary_key=True)
        name = models.CharField(verbose_name="Имя графа: ", max_length=80)
        owner = models.ForeignKey(User, related_name="graphs", on_delete=models.CASCADE)

        def __str__(self):
            return self.name


        class Meta:
            ordering = ['id']


        def get_adj_list(self):
            adj_list = {}
            nodes = self.nodes.all()
            
            for node in nodes:
                adj_list[node.id] = []
                parents = node.parents.all()
                for parent in parents:
                    adj_list[node.id].append(parent.id)

            return adj_list


        def get_node_ids(self):
            nodes = self.nodes.all()
            return [node.id for node in nodes]




            




# Вершина
class Node(models.Model):
        id = models.BigAutoField(primary_key=True)
        name = models.CharField(verbose_name="node's name", max_length=80)
        graph = models.ForeignKey(Graph, db_column="graph_id", related_name="nodes", on_delete=models.CASCADE)
        # поле foreign key для связи вершины с графом
        parents = models.ManyToManyField("self", related_name="children", symmetrical=False)

        def __str__(self):
                return self.name


