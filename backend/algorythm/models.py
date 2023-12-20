from django.db import models
from django.contrib.auth.models import User
from pyvis.network import Network
from django.conf import settings

# Create your models here.


# Модель графа (как граф связан с пользователем)
class Graph(models.Model):
        id = models.BigAutoField(primary_key=True)
        name = models.CharField(verbose_name="graph's =  name", max_length=80)
        user = models.ForeignKey(User, on_delete=models.CASCADE)

        @classmethod
        def create(cls, name, user):
            """
            Создает и возвращает новую "Graph" сущность основываясь на валидированных данных.
            """
            graph = cls.objects.create(name=name, user=user)
            graph.generate_html()
            return graph
            

        def update(self, instance, name):
            """
            Изменяет и возвращает существующую "Graph" сущность основываясь на валидированных данных.
            """
            instance.name = name
            instance.save()
            return instance

        def generate_html(self):
                # Create graph in PyVis

                network = Network(height="750px", width="50%", directed=True, heading = f"#{self.id} {self.name}",bgcolor="#F6F2FF", font_color="#222222", filter_menu=True, cdn_resources = "remote")
                network.barnes_hut()
                #network.barnes_hut(gravity=-80000, central_gravity=8, spring_length=250, spring_strength=0.001, damping=0.09, overlap=0)
                network.inherit_edge_colors(status=True)
                network.toggle_stabilization(status=True)
                # network.set_options("""
                # var options = {
                #     "configure": {
                #         "enabled": true,
                #         "filter": "physics",
                #         "container": "undefined",
                #         "showButton": true
                #     },

                #     "physics": {
                #         "barnesHut": {
                #             "gravitationalConstant": -80000,
                #             "centralGravity": 3.0,
                #             "springLength": 250,
                #             "springConstant": 0.001
                #         },
                #         "minVelocity": 0.75
                #     }
                # }
                # """)

                # Fetch nodes from Django ORM by graph_id
                nodes = Node.objects.filter(graph_id=self.id)

                # Add nodes from Django ORM to PyVis graph
                for node in nodes:
                    network.add_node(n_id = node.id, label = node.name, title = "", color = "#7D47B6")

                # Add edges to PyVis graph
                for node in nodes:
                    for parent in node.parents.all():
                        network.add_edge(parent.id, node.id, color = "#202A25")

                # Add title to nodes (neighbors)
                for node in network.nodes:
                    node["title"] += " Соединено с:\n" + "\n".join(network.get_node(neighbor)["label"] for neighbor in network.neighbors(node["id"]))

                network.show_buttons(filter_=["nodes", "edges", "physics"])

                network.save_graph(str(settings.BASE_DIR)+f'/algorythm/templates/algorythm/graphes/pvis_graph{self.id}.html')

        def add_node(self, name):
            return Node.create(name, self)


        def __str__(self):
            return self.name



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
