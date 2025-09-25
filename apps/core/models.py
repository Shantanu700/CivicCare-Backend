from mailbox import Babyl
import uuid6
from cloudinary_storage.storage import MediaCloudinaryStorage


from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from apps.core.choices import UserRoleChoices, CompalaintsChoices
from apps.core.enums import Status
from apps.core.managers import DeleteStatusManager

from config.defaults import DEFAULT_ON_DELETE

# Create your models here.


class BaseModel(models.Model):
    BASE_MODEL_FIELDS = (
        "uuid",
        "status",
        "created_at",
        "updated_at",
    )

    uuid = models.UUIDField(default=uuid6.uuid6)
    status = models.IntegerField(default=Status.CREATED)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = DeleteStatusManager()

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    USER_MODEL_FIELDS = BaseModel.BASE_MODEL_FIELDS + (
        "is_superuser",
        "last_login",
        "is_staff",
        "is_active",
        "date_joined",
        "groups",
        "user_permissions",
    )

    first_name = None
    last_name = None
    username = None
    name = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(unique=True, blank=False, null=False)
    location = models.PointField(blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.USER,
    )
    upvoted_posts = models.ManyToManyField(
        "Complaints", related_name="upvoted_complaints", null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    REQUIRED_FIELDS = []


class DropDown(BaseModel):
    label = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self",
        DEFAULT_ON_DELETE,
        null=True,
        related_name="children",
    )

    def __str__(self):
        return self.label


class Complaints(BaseModel):
    user = models.ForeignKey(
        User, on_delete=DEFAULT_ON_DELETE, related_name="complaints"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", storage=MediaCloudinaryStorage)
    # address = models.CharField(max_length=500)
    location = models.PointField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=CompalaintsChoices, default=CompalaintsChoices.REGISTERED
    )
    # category = models.ForeignKey(
    #     DropDown,
    #     on_delete=DEFAULT_ON_DELETE,
    #     related_name="type",
    # )

    category = models.ForeignKey(
        DropDown,
        on_delete=DEFAULT_ON_DELETE,
        related_name="department",
    )
