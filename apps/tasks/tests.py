from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Task

User = get_user_model()


class TaskModelTests(TestCase):
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
