from algorythm.models import Graph, Node
from django.contrib.auth.models import User
from rest_framework import serializers



class GraphSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Graph
        fields = ['url', 'id', 'user_id']




class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['url', 'id', 'name', 'graph_id', 'parents']




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
