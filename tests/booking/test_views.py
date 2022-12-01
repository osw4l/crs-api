from decimal import Decimal
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.booking.models import Hotel, Room, Rate, Inventory
from apps.booking.serializers import AvailabilitySerializer


class HotelAvailabilityTestView(TestCase):
    def setUp(self) -> None:
        self.start_date = datetime(2020, 3, 1)
        self.end_date = datetime(2020, 3, 2)
        self.hotel = Hotel.objects.create(code='co42', name='hotel')

    def get_url(self, code):
        return reverse('booking:availability', kwargs={
            'code': code,
            'checkin': self.start_date,
            'checkout': self.end_date
        })

    def test_availability_success(self):
        self.assertEqual(Hotel.objects.count(), 1)

        room = self.hotel.rooms.create(code='room_code_1', name='room 1')
        self.assertEqual(Room.objects.count(), 1)

        rate = Rate.objects.create(code='rate_code_1', room=room)
        self.assertEqual(Rate.objects.count(), 1)

        rate.inventory.create(date=self.start_date, price=Decimal(45.12), allotment=2)
        rate.inventory.create(date=self.end_date, price=Decimal(45.12), allotment=3)
        self.assertEqual(Inventory.objects.count(), 2)

        # set query like the view
        query = {
            'rate__room__hotel': self.hotel,
            'date__range': [
                self.start_date,
                self.end_date
            ],
        }
        qs = Inventory.objects.select_related('rate').filter(**query)
        serializer = AvailabilitySerializer(qs)

        response = self.client.get(self.get_url(code=self.hotel.code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_availability_empty_response(self):
        response = self.client.get(self.get_url(code=self.hotel.code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_availability_fail(self):
        response = self.client.get(self.get_url(code='wrong_code'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
