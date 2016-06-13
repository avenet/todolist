from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from django.test import TestCase

from rest_framework import fields
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import force_authenticate, APIRequestFactory

from .admin import TaskAdmin
from .models import Task
from .serializers import TaskCreateSerializer, TaskDetailSerializer, TaskListSerializer
from .views import TaskList, TaskDetail, TaskSolve

User = get_user_model()


class TasksURLsTestCase(TestCase):
    """
    Task urls testcases
    """
    def test_task_list_url_uses_obtain_task_list_view(self):
        """
        Test that the task list url resolves to the correct
        view function.
        """
        task_list = resolve('/api/v1/tasks/')
        task_list_func_name = str(task_list.func).split()[1]
        self.assertEqual(task_list_func_name, "TaskList")

    def test_task_detail_url_uses_obtain_task_detail_view(self):
        """
        Test that the task detail url resolves to the correct
        view function.
        """
        task_detail = resolve('/api/v1/tasks/1/')
        task_detail_func_name = str(task_detail.func).split()[1]
        self.assertEqual(task_detail_func_name, "TaskDetail")

    def test_task_solve_url_uses_obtain_task_solve_view(self):
        """
        Test that the task solve url resolves to the correct
        view function.
        """
        task_solve = resolve('/api/v1/tasks/1/solve/')
        task_solve_func_name = str(task_solve.func).split()[1]
        self.assertEqual(task_solve_func_name, "TaskSolve")


class TaskModelTestCase(TestCase):
    """
    Task model tests
    """
    def setUp(self):
        self.task_name = "Do a guitar solo"
        self.task_description = "Just rock all over the place, blah blah blah"
        self.task_status = Task.SOLVED

        self.task_owner = User.objects.create(username='hendrix')

        guitar_solo_task = Task.objects.create(
            name=self.task_name,
            status=self.task_status,
            owner=self.task_owner,
            description=self.task_description)

        self.clean_closet_task = Task.objects.create(
            name="Clean out the closet",
            owner=self.task_owner)

        self.task_id = guitar_solo_task.pk

    def test_task_str_matches_task_name(self):
        """
        Tests that the task string representation is exactly the task name
        """
        task_name = 'Clean the dust'
        clean_dust_tag = Task(name=task_name)
        self.assertEqual(str(clean_dust_tag), task_name)

    def test_task_name_is_saved(self):
        """
        Tests that once saved the task name is the one who was saved
        """
        task = Task.objects.get(pk=self.task_id)
        self.assertEqual(task.name, self.task_name)

    def test_task_description_is_saved(self):
        """
        Tests that once saved the task description is the one who was saved
        """
        task = Task.objects.get(pk=self.task_id)
        self.assertEqual(task.description, self.task_description)

    def test_task_status_is_saved(self):
        """
        Tests that once saved the task status is the one who was saved
        """
        task = Task.objects.get(pk=self.task_id)
        self.assertEqual(task.status, self.task_status)

    def test_task_owner_is_saved(self):
        """
        Tests that once saved the task owner is the one who was saved
        """
        task = Task.objects.get(pk=self.task_id)
        self.assertEqual(task.owner, self.task_owner)

    def test_task_default_status_is_pending(self):
        """
        Tests that when tasks are saved without specifying the status,
        its saved status is pending
        """
        clean_out_closet_task = Task.objects.get(pk=self.clean_closet_task.pk)
        self.assertEqual(clean_out_closet_task.status, Task.PENDING)

    def test_task_default_description_is_the_empty_string(self):
        """
        Tests that when tasks are saved without specifying the description,
        its saved description is the empty string
        """
        clean_out_closet_task = Task.objects.get(pk=self.clean_closet_task.pk)
        self.assertEqual(clean_out_closet_task.description, "")

    def test_task_created_date_is_set(self):
        """
        Tests that when tasks are saved its created date is saved
        """
        clean_out_closet_task = Task.objects.get(pk=self.clean_closet_task.pk)
        self.assertIsNotNone(clean_out_closet_task.created)

    def test_task_updated_date_is_set(self):
        """
        Tests that when tasks are saved its updated date is saved
        """
        clean_out_closet_task = Task.objects.get(pk=self.clean_closet_task.pk)
        self.assertIsNotNone(clean_out_closet_task.created)


class TaskAdminTestCase(TestCase):
    """
    Task admin tests
    """
    def test_task_admin_list_filter_fields(self):
        """
        Tests that task admin list_filter contains the right fields
        """
        self.assertEqual(TaskAdmin.list_filter,
                         ['status', 'created', 'updated', 'owner'])

    def test_task_admin_search_fields(self):
        """
        Tests that the task admin search_fields contains the right fields
        """
        self.assertEqual(TaskAdmin.search_fields,
                         ['name', 'description', 'owner'])

    def test_task_admin_list_display(self):
        """
        Tests that the task admin list_display contains the right fields
        """
        self.assertEqual(TaskAdmin.list_display,
                         ['status', 'owner'])


class TaskCreateSerializerTestCase(TestCase):
    """
    TaskCreateSerializer tests
    """
    def test_task_create_serializer_fields(self):
        """
        Tests that the task create serializer contains the right fields on the Meta clas.
        """
        self.assertEqual(TaskCreateSerializer.Meta.fields, ('id', 'name', 'description'))

    def test_task_create_serializer_model(self):
        """
        Tests that the task create serializer contains the right model on the Meta class.
        """
        self.assertEqual(TaskCreateSerializer.Meta.model, Task)


class TaskListSerializerTestCase(TestCase):
    """
    TaskListSerializer tests
    """
    def test_task_list_serializer_fields(self):
        """
        Tests that the task list serializer contains the right fields on the Meta class.
        """
        self.assertEqual(TaskListSerializer.Meta.fields, ('id', 'name', 'status'))

    def test_task_list_serializer_model(self):
        """
        Tests that the task list serializer contains the right model on the Meta class.
        """
        self.assertEqual(TaskListSerializer.Meta.model, Task)

    def test_task_list_serializer_status_field(self):
        """
        Tests that the task list serializer contains a valid status field.
        """
        status_field = TaskListSerializer().get_fields()['status']
        self.assertEqual(status_field.source, 'get_status_display')
        self.assertEqual(type(status_field), fields.CharField)


class TaskDetailSerializerTestCase(TestCase):
    """
    TaskDetailSerializer tests
    """
    def test_task_detail_serializer_fields(self):
        """
        Tests that the task detail serializer contains the right fields on the Meta class.
        """
        self.assertEqual(TaskDetailSerializer.Meta.fields, ('id', 'name', 'description',
                                                            'status', 'created', 'updated'))

    def test_task_detail_serializer_model(self):
        """
        Tests that the task detail serializer contains the right model on the Meta class.
        """
        self.assertEqual(TaskDetailSerializer.Meta.model, Task)

    def test_task_detail_serializer_status_field(self):
        """
        Tests that the task list serializer contains a valid status field.
        """
        status_field = TaskDetailSerializer().get_fields()['status']
        self.assertEqual(status_field.source, 'get_status_display')
        self.assertEqual(type(status_field), fields.CharField)


class TaskListTestCase(TestCase):
    """
    TaskList view tests
    """
    def setUp(self):
        self.user = User.objects.create(username="master")
        self.tasks = [
            Task.objects.create(name='One', owner=self.user),
            Task.objects.create(name='Two', owner=self.user),
            Task.objects.create(name='Three', owner=self.user),
        ]

    def test_task_list_authentication_classes(self):
        """
        Tests that the authentication_classes attribute on the TaskList view contains
        the right classes
        """
        self.assertEqual(TaskList.authentication_classes, (TokenAuthentication,))

    def test_task_list_permission_classes(self):
        """
        Tests that the permission_classes attribute on the TaskList view contains
        the right classes
        """
        self.assertEqual(TaskList.permission_classes, (IsAuthenticated,))

    def test_get_task_list_without_authentication(self):
        """
        Tests that when getting a task list and no user is authenticated,
        the api returns a 401 error
        """
        factory = APIRequestFactory()
        request = factory.get('/api/v1/tasks', format='json')
        task_list_view = TaskList.as_view()
        response = task_list_view(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'],
                         'Authentication credentials were not provided.')

    def test_get_task_list_returns_json_list(self):
        """
        Tests that when the user is authenticated, the api returns a 200 error
        and gets the task count for that user
        """
        factory = APIRequestFactory()
        request = factory.get('/api/v1/tasks', format='json')
        task_list_view = TaskList.as_view()

        force_authenticate(request, user=self.user)

        response = task_list_view(request)

        self.assertEqual(response.status_code, 200)

        user_tasks_count = Task.objects.filter(owner=self.user).count()

        self.assertEqual(len(response.data), user_tasks_count)

    def test_get_task_list_contains_valid_fields(self):
        """
        Tests that when a valid user is authenticated, all of the returned
        tasks contain the correct fields
        """
        factory = APIRequestFactory()
        request = factory.get('/api/v1/tasks', format='json')
        task_list_view = TaskList.as_view()

        force_authenticate(request, user=self.user)

        response = task_list_view(request)

        response_fields = ['id', 'name', 'status']

        for item in response.data:
            for response_field in response_fields:
                self.assertEqual(response_field in item, True)

    def test_create_task(self):
        """
        Tests that when no user is authenticated and we are creating a task,
        the api returns a 201 created status code.
        """
        factory = APIRequestFactory()

        request = factory.post('/api/v1/tasks', {
            'name': 'Hello',
            'description': 'world',
        }, format='json')

        task_list_view = TaskList.as_view()

        force_authenticate(request, user=self.user)

        response = task_list_view(request)

        self.assertEqual(response.status_code, 201)
        response_fields = ['description', 'name', 'id']

        for response_field in response_fields:
            self.assertEqual(response_field in response.data, True)

    def test_create_task_owner(self):
        """
        Tests that once the task is created the owner is
        the authenticated user
        """
        factory = APIRequestFactory()

        request = factory.post('/api/v1/tasks', {
            'name': 'Hello',
            'description': 'world',
        }, format='json')

        task_list_view = TaskList.as_view()

        force_authenticate(request, user=self.user)

        response = task_list_view(request)

        self.assertEqual(response.status_code, 201)

        created_task = Task.objects.get(pk=response.data['id'])

        self.assertEqual(created_task.owner, self.user)

    def test_create_with_invalid_name(self):
        """
        Tests that trying to create a task with no name
        returns a 400 status code and a validation message
        """
        factory = APIRequestFactory()

        request = factory.post('/api/v1/tasks', {
            'name': '',
            'description': 'world',
        }, format='json')

        task_list_view = TaskList.as_view()

        force_authenticate(request, user=self.user)

        response = task_list_view(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'],
                         ['This field may not be blank.'])

    def test_create_task_fields(self):
        """
        Tests that when creating a task via API it contains
        the fields as passed on the POST mechanism.
        """
        factory = APIRequestFactory()

        task_name = 'Task'
        task_description = 'world'

        request = factory.post('/api/v1/tasks', {
            'name': task_name,
            'description': task_description,
        }, format='json')

        task_list_view = TaskList.as_view()

        force_authenticate(request, user=self.user)

        response = task_list_view(request)

        self.assertEqual(response.status_code, 201)

        new_task = Task.objects.order_by('-pk').first()

        self.assertEqual(new_task.name, task_name)
        self.assertEqual(new_task.description, task_description)
        self.assertIsNotNone(new_task.created)
        self.assertIsNotNone(new_task.updated)
        self.assertEqual(new_task.status, Task.PENDING)
