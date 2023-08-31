import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # auto_id = models.PositiveIntegerField(db_index=True, unique=True)
    created_by = models.ForeignKey(
        "users.User", blank=True, null=True, related_name="creator_%(class)s_objects", on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(
        'users.User', blank=True, null=True, related_name="updator_%(class)s_objects", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['created_at']