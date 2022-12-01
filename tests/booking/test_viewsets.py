from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.booking.models import Hotel, Room


class HotelViewSetTest(APITestCase):

    def test_create_success(self):
        data = {'code': 'h0t31', 'name': 'hotel'}

        url = reverse('booking:hotel-list')
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('code'), data.get('code'))
        self.assertEqual(Hotel.objects.count(), 1)

    def test_create_fail(self):
        url = reverse('booking:hotel-list')
        data = {'code': 'h0t31', 'name': 'hotel'}

        Hotel.objects.create(**data)

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Hotel.objects.count(), 1)

    def test_list_success(self):
        data = {'code': 'h0t31', 'name': 'hotel'}
        hotel = Hotel.objects.create(**data)
        self.assertEqual(Hotel.objects.count(), 1)

        url = reverse('booking:hotel-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0].get('code'), hotel.code)

    def test_retrieve_success(self):
        data = {'code': 'h0t31', 'name': 'hotel'}
        hotel = Hotel.objects.create(**data)
        self.assertEqual(Hotel.objects.count(), 1)

        url = reverse('booking:hotel-detail', kwargs={'code': hotel.code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), hotel.code)

    def test_retrieve_fail(self):
        url = reverse('booking:hotel-detail', kwargs={'code': 'random_code'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_success(self):
        hotel = Hotel.objects.create(**{'code': 'h0t31', 'name': 'hotel'})

        url = reverse('booking:hotel-detail', kwargs={'code': hotel.code})
        data = {'code': 'new_code', 'name': 'new_name'}

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), data.get('code'))

    def test_update_fail(self):
        hotel_1 = Hotel.objects.create(**{'code': 'h0t31', 'name': 'hotel 1'})
        hotel_2 = Hotel.objects.create(**{'code': 'h0t32', 'name': 'hotel 1'})

        url = reverse('booking:hotel-detail', kwargs={'code': hotel_1.code})
        data = {'code': hotel_2.code}

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        hotel = Hotel.objects.get(code=hotel_1.code)
        self.assertEqual(hotel.code, hotel_1.code)

    def test_delete_success(self):
        hotel = Hotel.objects.create(**{'code': 'h0t31', 'name': 'hotel'})

        url = reverse('booking:hotel-detail', kwargs={'code': hotel.code})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hotel.objects.filter(deleted=True).count(), 1)

    def test_delete_fail(self):
        url = reverse('booking:hotel-detail', kwargs={'code': 'random_code'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_rooms_success(self):
        hotel = Hotel.objects.create(**{'code': 'h0t31', 'name': 'hotel'})
        hotel.rooms.create(**{'code': 'r00m', 'name': 'room'})
        self.assertEqual(Room.objects.count(), 1)

        url = reverse('booking:hotel-rooms', kwargs={'code': hotel.code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0].get('code'), hotel.rooms.first().code)

    def test_rooms_fail(self):
        url = reverse('booking:hotel-rooms', kwargs={'code': 'random_code'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

