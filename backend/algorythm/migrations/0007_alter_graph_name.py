# Generated by Django 5.0.2 on 2024-02-15 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algorythm', '0006_alter_node_graph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Имя графа: '),
        ),
    ]
