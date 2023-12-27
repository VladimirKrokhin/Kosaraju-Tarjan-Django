from algorythm.models import Graph, Node
from algorythm.kosarajus_algorythm import kosaraju_algo
from algorythm.tarjans_algorythm import tarjan_algo


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError



class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']

    def create(self, validated_data):
        if 'graph_id' in validated_data:
            graph_id = validated_data['graph_id']  # Получаем graph_id из контекста
            graph = Graph.objects.get(pk=graph_id)  # Получаем объект текущего графа
            node = Node.objects.create(graph=graph, **validated_data)  # Создаем вершину с указанным графом
            return node
        else:
            # Обработка ситуации, когда 'graph_id' отсутствует в контексте
            raise serializers.ValidationError("Не указан 'graph_id' в контексте при создании вершины.")





class EdgeSerializer(serializers.Serializer):
    source_node_id = serializers.PrimaryKeyRelatedField(source='id', queryset=Node.objects.all())
    target_node_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def to_internal_value(self, data):
        source_node_id = data['source_node_id']
        target_node_ids = data['target_node_ids']

        return {
            'source_node_id': source_node_id,
            'target_node_ids': target_node_ids
        }

    def to_representation(self, instance):
        target_node_ids = list(instance.children.all().values_list('id', flat=True))
        return {str(instance.id): target_node_ids}

    
    def get_target_node_ids(self, instance):
        return list(instance.children.all().values_list('id', flat=True))



    def create(self, validated_data):
        source_node_id = validated_data.get('source_node_id')
        target_node_ids = validated_data.get('target_node_ids')

        source_node = Node.objects.get(id=source_node_id)
        target_node_ids_list = []

        for target_id in target_node_ids:
            target_node = Node.objects.get(id=target_id)
            source_node.children.add(target_node)
            target_node_ids_list.append(target_id)

        return source_node


    def update(self, instance, validated_data):
        source_node_id = validated_data.get('source_node_id')
        target_node_ids = validated_data.get('target_node_ids')


        instance.source_node_id = source_node_id
        
        source_node = Node.objects.get(id=source_node_id)
        source_node.children.clear()
        for target_id in target_node_ids:
            target_node = Node.objects.get(id=target_id)
            source_node.children.add(target_node)

        instance.save()

        return instance

                
    def validate(self, data):
        source_node_id = data.get('source_node_id')
        target_node_ids = data.get('target_node_ids')

        if not Node.objects.filter(id=source_node_id).exists():
            raise ValidationError("Исходный узел не существует")
        

        if not isinstance(target_node_ids, list):
            raise serializers.ValidationError("target_node_ids должен быть списком")
        
        
        for target_id in target_node_ids:
            if not Node.objects.filter(id=target_id).exists():
                raise ValidationError(f"Node with id {target_id} does not exist")
                if not isinstance(target_id, int):
                    raise serializers.ValidationError("Каждый элемент в списке должен быть целым числом")

        return data



class RunAlgorithmSerializer(serializers.Serializer):
    graph_id = serializers.IntegerField()
    algorithm_type = serializers.CharField()

    def validate_algorithm_type(self, value):
        if value not in ['kosaraju', 'tarjan']:
            raise serializers.ValidationError("Неправильный тип алгоритма")
        return value

    def retrieve(self, validated_data):
        graph = Graph.objects.get(pk=validated_data['graph_id'])
        node_list = graph.get_node_ids()
        adj_list = graph.get_adj_list()
        if validated_data["algorithm_type"] == 'kosaraju':
            result_array = kosaraju_algo(adj_list, node_list)
        elif validated_data["algorithm_type"] == "tarjan":
            result_array = tarjan_algo(adj_list, node_list)
        return result_array


class GraphSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    
    class Meta:
        model = Graph
        fields = ['id', 'name', 'owner']

    

class UserSerializer(serializers.ModelSerializer):
    graphs = serializers.PrimaryKeyRelatedField(many=True, queryset=Graph.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'graphs']