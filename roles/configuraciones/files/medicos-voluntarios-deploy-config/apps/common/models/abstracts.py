"""
Abstracts models to use as base for other models
"""
from uuid import uuid4

from django.db import models


class UUIDModel(models.Model):
    """Model that has `uuid` field as primary key"""

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class TimeStampModel(models.Model):
    """Model that has 2 "audit" fields for the creation and last
    modification datetime"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditModel(models.Model):
    """Model that has 2 "audit" fields to track the user that created
     and/or modified an entry """

    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)

    class Meta:
        abstract = True
