from django.db import models


class BookingModelQuerySet(models.QuerySet):
    """
    Queryset to filter all non-deleted objects
    and deleted also if the developer wants
    """
    def all(self):
        return self.filter(deleted=False)

    def deleted(self):
        return self.filter(deleted=True)


class BookingModelManager(models.Manager):
    """
    Manager to override the all method to return non-deleted objects
    and deleted also if the developer wants
    """
    def get_queryset(self):
        return BookingModelQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def deleted(self):
        return self.get_queryset().deleted()

