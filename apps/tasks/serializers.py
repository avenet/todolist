from rest_framework import serializers

from .models import Task


class TaskCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description')


class TaskListSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
        fields = ('id', 'name', 'status')


class TaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status',
                  'created', 'updated')
