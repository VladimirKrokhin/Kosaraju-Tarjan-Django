from algorythm.models import Graph, Node
from django.contrib.auth.models import User
from rest_framework import serializers



class GraphSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Graph
        fields = ['url', 'id', 'name', 'user']
        extra_kwargs = {
            'url': {'view_name': 'index', 'lookup_field': 'name'},
            'users': {'lookup_field': 'username'}
        }



class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ['url', 'id', 'name', 'graph', 'parents']
        extra_kwargs = {
            'url': {'view_name': 'index', 'lookup_field': 'name'},
            'graph': {'lookup_field': 'id'},
            'parents': {'lookup_field': 'parents'},
            'users': {'lookup_field': 'username'}
        }



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
        extra_kwargs = {
            'url': {'view_name': 'index', 'lookup_field': 'username'}
            }
