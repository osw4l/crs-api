from django.db import IntegrityError
from django.test import TestCase
from apps.booking.models import Hotel


class HotelTest(TestCase):

    def test_create_hotel_success(self):
        """
            This test creates a new Hotel
        """
        name = 'reus'
        code = 123
        hotel = Hotel.objects.create(
            name=name,
            code=code
        )
        self.assertEqual(Hotel.objects.count(), 1)
        self.assertEqual(hotel.name, name)
        self.assertEqual(hotel.code, code)

    def test_create_hotel_fail(self):
        """
            This test try to create a new Hotel
            we expect that fails, because we are sending
            the same code
        """
        Hotel.objects.create(name='reus', code='123')

        try:
            Hotel.objects.create(name='reus', code='123')
            self.fail()
        except IntegrityError as e:
            self.assertIsInstance(e, IntegrityError)

    def test_get_hotel_success(self):
        """
            This test gets a Hotel
        """
        hotel = Hotel.objects.create(name='reus', code='123')

        hotel_instance = Hotel.objects.get(code='123')
        self.assertIsNotNone(hotel_instance)
        self.assertEqual(hotel_instance.id, hotel.id)
        self.assertEqual(hotel_instance.code, hotel.code)
        self.assertEqual(Hotel.objects.count(), 1)

    def test_get_hotel_fail(self):
        """
            This test gets a Hotel fail
        """
        try:
            Hotel.objects.get(code='123x')
            self.fail()
        except Hotel.DoesNotExist as e:
            self.assertIsInstance(e, Hotel.DoesNotExist)

    def test_update_hotel_success(self):
        """
            This test updates a Hotel
        """
        hotel = Hotel.objects.create(name='reus', code='123')
        new_name = 'barcelona'
        hotel.name = 'barcelona'
        hotel.save(update_fields=['name'])

        hotel_instance = Hotel.objects.get(code='123')
        self.assertEqual(hotel_instance.name, new_name)

    def test_update_hotel_fail(self):
        """
            This test updates a Hotel fail
        """
        hotel_1 = Hotel.objects.create(name='reus', code='123')
        hotel_2 = Hotel.objects.create(name='barcelona', code='1234')

        try:
            hotel_2.code = hotel_1.code
            hotel_2.save(update_fields=['code'])
        except IntegrityError as e:
            self.assertIsInstance(e, IntegrityError)

    def test_delete_hotel_success(self):
        """
            This test delete a Hotel
        """
        hotel = Hotel.objects.create(name='reus', code='123')
        self.assertEqual(Hotel.objects.count(), 1)

        hotel_instance = Hotel.objects.get(code='123')
        self.assertEqual(hotel.id, hotel_instance.id)
        self.assertEqual(hotel.code, hotel_instance.code)

        hotel_instance.delete()
        self.assertEqual(Hotel.objects.filter(deleted=True).count(), 1)

    def test_delete_hotel_fail(self):
        """
            This test delete a Hotel fail
        """
        try:
            Hotel.objects.get(code='123').delete()
        except Hotel.DoesNotExist as e:
            self.assertIsInstance(e, Hotel.DoesNotExist)



