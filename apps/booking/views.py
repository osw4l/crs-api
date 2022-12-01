from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response

from .serializers import AvailabilitySerializer
from .models import Inventory, Hotel


class AvailabilityView(generics.GenericAPIView):
    serializer_class = AvailabilitySerializer

    @staticmethod
    def get_hotel(code: str):
        """
            Retrieve an hotel using the code
        """
        try:
            return Hotel.objects.get(code=code)
        except Hotel.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        """
        API endpoint for get the inventory of rooms in a given date range and hotel
        Args (GET method):
            'code' -> str: code_hotel (this is the hotel code)
            'checkin' -> date: 2022-12-01 (this is checkin date))
            'checkout' -> date: 2022-12-03 (this is checkout date))
        Returns:
            [json]: rooms
        You can see the full json request/response example going to 'http://localhost:6060'
        in swagger documentation.
        """
        code = kwargs.get('code')
        hotel = self.get_hotel(code=code)
        query = {
            'rate__room__hotel': hotel,
            'date__range': [
                kwargs.get('checkin'),
                kwargs.get('checkout')
            ],
        }
        qs = Inventory.objects.select_related('rate').filter(**query)
        serializer = AvailabilitySerializer(qs)
        return Response(serializer.data)

