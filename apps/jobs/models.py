from django.db import models

from apps.core.models import BaseModel, User
from apps.jobs.choices import UserTaskChoices

from config.defaults import DEFAULT_ON_DELETE


class UserTask(BaseModel):
    user = models.ForeignKey(User, on_delete=DEFAULT_ON_DELETE, related_name="tasks")
    name = models.CharField(max_length=255)
    function = models.CharField(max_length=255)
    args = models.JSONField(blank=True, default=list)
    kwargs = models.JSONField(blank=True, default=dict)
    status = models.IntegerField(
       choices=UserTaskChoices, 
       default=UserTaskChoices.PENDING,
   )
    progress = models.PositiveIntegerField(default=0)
    result = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    queue = models.CharField(max_length=50, default="default", blank=True)
    priority = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)