from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Task(models.Model):
    """
    Represents an user's task
    """
    PENDING = 1
    SOLVED = 2

    TASK_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (SOLVED, 'Solved'),
    )

    name = models.CharField(
        max_length=60,
        help_text="Up to 60 characters for a "
                  "short name for the task"
    )

    description = models.TextField(
        help_text="A text which describes further details "
                  "on what should be done with the task",
        blank=True,
        default="",
    )

    status = models.IntegerField(
        choices=TASK_STATUS_CHOICES,
        default=PENDING
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='The date when this task was created'
    )

    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='The date when this task was last updated'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text="The user who created this task",
    )

    def __str__(self):
        return self.name
