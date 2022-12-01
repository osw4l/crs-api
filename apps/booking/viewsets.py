from rest_framework.decorators import action
from .decorators import action_paginated
from .serializers import (
    HotelSerializer,
    RoomSerializer,
    RateSerializer,
    InventorySerializer
)
from .models import (
    Hotel,
    Room,
    Rate,
    Inventory
)
from .utils import CrudModelViewSet


class HotelViewSet(CrudModelViewSet):
    """
    API endpoint for creating, list, update and delete hotels
    This endpoint allows just the create operation.
    Args (POST method):
        'name' -> str: hotel x (this is the name)
        'code' -> str: hot3l (this is the code)
    Returns:
        [json]: id, code, name
    You can see the full json request/response example going to 'http://localhost:6060'
    in swagger documentation.
    """
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all().only('name', 'code')
    lookup_field = 'code'

    @action_paginated
    @action(detail=True,
            methods=['GET'],
            custom_serializer_class=RoomSerializer)
    def rooms(self, request, code=None):
        """
        API endpoint action for get the rooms of an hotel
        in swagger documentation.
        args (GET method):
        'code' -> str: 'hot3l' (hotel code)
        Returns:
        [json]: id, name, code, rate
        """
        return Room.objects.filter(hotel=self.get_object())


class RoomViewSet(CrudModelViewSet):
    """
    API endpoint for creating, list, update and delete rooms

    Args (POST method):
        'name' -> str: hotel x (this is the name)
        'code' -> str: hot3l (this is the code)
    Returns:
        [json]: id, code, name, rate
    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class RateViewSet(CrudModelViewSet):
    """
    API endpoint for creating, list, update and delete hotels
    This endpoint allows just the create operation.
    Args (POST method):
        'name' -> str: rate name x (this is the name)
        'code' -> str: rat3 (this is the code)
        'room' -> int: 1 (this is the room id)
    Returns:
        [json]: id, code, name, room
    You can see the full json request/response example going to 'http://localhost:6060'
    in swagger documentation.
    """
    serializer_class = RateSerializer
    queryset = Rate.objects.all()

    @action_paginated
    @action(detail=True,
            methods=['GET'],
            custom_serializer_class=InventorySerializer)
    def inventory(self, request, pk=None):
        """
        API endpoint action for get the inventory of a rate
        in swagger documentation.
        args (GET method):
        'pk' -> int: 1 (rate id)
        Returns:
        [json]: id, rate, price, date, allotment
        """
        return Inventory.objects.filter(rate=self.get_object())


class InventoryViewSet(CrudModelViewSet):
    """
    API endpoint for creating, list, update and delete hotels
    This endpoint allows just the create operation.
    Args (POST method):
        'rate' -> int: 1 (this is the rate_id)
        'price'-> float: 45.12 (this is the price)
        'date' -> str: 2022-12-01 (this is the date)
    Returns:
        [json]: id, code, name, room
    You can see the full json request/response example going to 'http://localhost:6060'
    in swagger documentation.
    """
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

