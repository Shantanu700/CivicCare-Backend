from django.db import models
from jsonschema_specifications import REGISTRY


class UserRoleChoices(models.TextChoices):
    USER = "USER", "User"
    MUNICIPAL = "MUNICIPAL", "Municipal"
    FIELD_WORKER = "FIELD_WORKER", "Field Worker"
    CONTRACTOR = "CONTRACTOR", "Contractor"


class CompalaintsChoices(models.TextChoices):
    REGISTERED = "Registered", "REGISTERED"
    APPROOVED = "Approoved", "APPROOVED"
    PENDING = "Pending", "PENDING"
    COMPLETED = "Completed", "COMPLETED"
    DELETED = "Deleted", "DELETED"
