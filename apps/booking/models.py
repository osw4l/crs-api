from django.db import models

from apps.booking.managers import BookingModelManager


class BaseModel(models.Model):
    deleted = models.BooleanField(default=False, editable=False)
    objects = BookingModelManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # logical erase, non-physical
        self.deleted = True
        self.save(update_fields=['deleted'])

    def restore(self):
        pass


class BaseHotelItem(BaseModel):
    name = models.CharField(
        max_length=20
    )
    code = models.CharField(
        max_length=20,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Hotel(BaseHotelItem):
    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'

    def delete(self, using=None, keep_parents=False):
        super().delete()
        self.set_status_related_objects(deleted=True)

    def restore(self):
        self.set_status_related_objects(deleted=False)

    def set_status_related_objects(self, deleted: bool):
        # method to disable or enable all related records
        self.rooms.all().update(**{'deleted': deleted})
        Rate.objects.filter(room__hotel=self).update(**{'deleted': deleted})
        Inventory.objects.filter(rate__room__hotel=self).update(**{'deleted': deleted})


class Room(BaseHotelItem):
    hotel = models.ForeignKey(
        'booking.Hotel',
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f'{self.hotel} - {self.name} - {self.code}'


class Rate(BaseHotelItem):
    room = models.OneToOneField(
        'booking.Room',
        on_delete=models.CASCADE,
        related_name='rate'
    )


class Inventory(BaseModel):
    rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        related_name='inventory',
        db_index=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = models.DateField(db_index=True)
    allotment = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        unique_together = [
            'rate',
            'date',
            'deleted'
        ]
