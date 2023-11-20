from django.test import TestCase
from algorythm.models import Graph, Node


# Create your tests here.


class GraphTestCase(TestCase):
  def setUp(self):
    Graph.objects.create(id=1, user_id=1)
    n1 = Node.objects.create(id=1, name="Amsterdam", graph_id=1)
    n2 = Node.objects.create(id=2, name="Boston", graph_id=1)
    n3 = Node.objects.create(id=3, name="Clinton", graph_id=1)
    n4 = Node.objects.create(id=4, name="Detroit", graph_id=1)
    n5 = Node.objects.create(id=5, name="Ekaterinburg", graph_id=1)


  def test_edges_creation(self):
    n2.parents.add(n1)
    n3.parents.add(n1)
    n4.parents.add(n1)
    n5.parents.add(n5)

  
