import uuid
from django.db import models


class AbstractDateCreatedRecordable(models.Model):
    date_created = models.DateTimeField("Date Created", auto_now_add=True)

    class Meta:
        abstract = True


class AbstractDateUpdatedRecordable(models.Model):
    date_updated = models.DateTimeField("Date Updated", auto_now=True)

    class Meta:
        abstract = True


class AbstractSoftDeleteable(models.Model):
    date_deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return self.date_deleted is not None


class AbstractTimestampable(AbstractDateCreatedRecordable, AbstractDateUpdatedRecordable):
    class Meta:
        abstract = True


class AbstractUUIDable(models.Model):
    uuid = models.UUIDField("UUID", default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        abstract = True


class AbstractPrimaryUUIDable(models.Model):
    id = models.UUIDField("ID", default=uuid.uuid4,
                          editable=False, primary_key=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class AbstractCategory(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class AbstractAddress(models.Model):
    street = models.CharField("Street", max_length=256)
    district = models.CharField(
        "District", max_length=256, null=True, blank=True)
    city = models.CharField("City", max_length=256, null=True, blank=True)
    province = models.CharField(
        "Province", max_length=256, null=True, blank=True)
    zip_code = models.CharField(
        "Zip Code", max_length=32, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        candidate_fields = (self.street, self.district,
                            self.city, self.province, self.zip_code)

        included_fields = (
            field for field in candidate_fields if field is not None and field is not "")

        return ", ".join(included_fields)
