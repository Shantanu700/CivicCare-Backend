from django.db.models import IntegerChoices

class UserTaskChoices(IntegerChoices):
    PENDING = 1
    STARTED = 2
    RUNNING = 3
    COMPLETED = 4
    ERROR = 0
