from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskCreateSerializer, TaskListSerializer, \
    TaskDetailSerializer


class TaskList(APIView):
    """
    List all tasks, or create a new one.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user_tasks = Task.objects.filter(owner=request.user)
        serializer = TaskListSerializer(user_tasks, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    Retrieve, update or delete a task instance.
    """
    queryset = Task.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = TaskDetailSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        try:
            Task.objects.get(pk=pk, owner=request.user)
        except:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        return self.retrieve(request, *args, **kwargs)


class TaskSolve(APIView):
    """
    Solves a task when called via PUT
    """
    authentication_classes = (TokenAuthentication,)

    def put(self, request, pk, format=None):
        user = request.user
        task = get_object_or_404(Task, pk=pk, owner=user)

        if task.status == Task.SOLVED:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        task.status = Task.SOLVED
        task.save(update_fields=['status'])

        serializer = TaskDetailSerializer(task, context={
            'request': request,
        })

        return Response(serializer.data)
