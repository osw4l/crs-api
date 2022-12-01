from django.contrib import admin
from .models import Hotel, Room, Rate, Inventory


class RoomStackedInline(admin.StackedInline):
    model = Room
    extra = 0


class BaseModelAdmin(admin.ModelAdmin):
    actions = [
        'restore'
    ]

    def restore(self, request, queryset):
        queryset.update(deleted=False)
        for item in queryset:
            item.restore()


@admin.register(Hotel)
class HotelAdmin(BaseModelAdmin):
    list_display = [
        'id',
        'name',
        'code',
        'deleted',
    ]
    inlines = (
        RoomStackedInline,
    )


@admin.register(Room)
class RoomAdmin(BaseModelAdmin):
    list_display = [
        'id',
        'hotel',
        'name',
        'code',
        'deleted'
    ]
    list_filter = [
        'hotel'
    ]


class InventoryStackedInline(admin.StackedInline):
    extra = 0
    model = Inventory


@admin.register(Rate)
class RateAdmin(BaseModelAdmin):
    list_display = [
        'id',
        'name',
        'code',
        'deleted',
    ]
    inlines = (
        InventoryStackedInline,
    )
