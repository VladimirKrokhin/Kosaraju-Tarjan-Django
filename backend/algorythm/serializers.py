from .models import Graph, Node
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action



class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']



class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = ['id', 'name']

    

class GraphDetailSerializer(serializers.ModelSerializer):
    nodes = NodeSerializer(many=True, read_only=True, source='node_set')
    edges = serializers.SerializerMethodField()

    class Meta:
        model = Graph
        fields = ['id', 'name', 'nodes', 'edges']

    def get_edges(self, obj):
        edges = {}
        for node in obj.node_set.all():
            incident_nodes = list(node.parents.all().values_list('id', flat=True))
            edges[node.id] = incident_nodes
        return edges

