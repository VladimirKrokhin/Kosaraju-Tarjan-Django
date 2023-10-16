from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Вершина
class Node(models.Model):
        id = models.BigAutoField(
                primary_key=True)
        name = models.CharField(
                verbose_name="node's name",
                max_length=80)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        # поле foreign key для связи с пользователем
        parents = models.ManyToManyField(
                "self",
                related_name="children",
                symmetrical=False)
        
        def __str__(self):
                return self.name
