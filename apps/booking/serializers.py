from rest_framework import serializers
from .documents import RateDocument
from .models import Hotel, Room, Rate, Inventory


class HotelSerializer(serializers.ModelSerializer):
    """
    Model serializer for Hotel
    """
    class Meta:
        model = Hotel
        fields = (
            'id',
            'code',
            'name'
        )


class RateSerializer(serializers.ModelSerializer):
    """
    Model serializer for Rate
    """
    class Meta:
        model = Rate
        fields = (
            'id',
            'name',
            'code',
            'room'
        )


class RoomSerializer(serializers.ModelSerializer):
    """
    Model serializer for Room
    """
    rate = RateSerializer(read_only=True)

    class Meta:
        model = Room
        fields = (
            'id',
            'name',
            'code',
            'hotel',
            'rate'
        )
        extra_kwargs = {
            'hotel': {
                'write_only': True
            }
        }


class InventorySerializer(serializers.ModelSerializer):
    """
    Model serializer for Inventory
    """
    class Meta:
        model = Inventory
        fields = (
            'id',
            'rate',
            'price',
            'date',
            'allotment'
        )


class ProcessBaseSerializer(serializers.Serializer):
    """
        Serializer to create custom structures with custom keys
        Is it necessary to overwrite the original behavior of to_representation()
        to create our custom structures
    """

    def update(self, instance, validated_data):  # pragma: no cover
        pass

    def create(self, validated_data):  # pragma: no cover
        pass

    def process_data(self, instance):
        """
            It process and clean the data added in
            a given instance
            :param instance: this attribute contains the data
            :return: returns the data processed
        """
        raise NotImplementedError('`process_data()` must be implemented.')

    def to_representation(self, instance):
        """
            It process and clean the data added in
            a given instance
            :param instance: this attribute contains the data
            :return: returns the data processed
        """
        return self.process_data(instance)


class RateInventorySerializer(ProcessBaseSerializer):
    """
        Serializer to get the inventory, allotment and price by date
    """

    def process_data(self, instance):
        """
            Process the data that comes from a queryset
            :param instance: contains the list with the data that we need to process
            :return: returns the rates in dict
        """
        result = {
            'rates': []
        }
        for rate in instance:
            self.rate_processor(
                rates=result.get('rates'),
                rate=rate
            )
        return result

    def rate_processor(self, rates, rate):
        """
            It takes each rate and it creates a new rate clean
            :param rate: contains a rate dict
            :param rates: contains the list of rates
            :return: returns noting
        """
        if not rates:
            self.rate_processor_add_first(rates, rate)
        else:
            self.rate_processor_add(rates, rate)

    def rate_processor_add_first(self, rates, rate):
        """
            It creates a rate element processed for first time in the rates
            :param rate: contains a rate dict
            :param rates: contains the list of rates
            :return: returns noting
        """
        rate_element = {
            rate.code: {
                'total_price': rate.price,
                'breakdown': [
                    self.get_breakdown(rate)
                ]
            }
        }
        rates.append(rate_element)

    def rate_processor_add(self, rates, rate):
        """
            It adds a new rate element inside rates adding a new breakdown
            and also changes the value of total_price
            :param rate: contains a rate dict
            :param rates: contains the list of rates
            :return: returns noting
        """
        slot = rates[0][rate.code]
        slot['total_price'] += rate.price
        breakdown = self.get_breakdown(rate)
        slot['breakdown'].append(breakdown)

    @staticmethod
    def get_breakdown(rate):
        """
            It takes the date, price and allotment of one rate
            :param rate: contains the rate
            :return: returns a breakdown in dict
        """
        return {
            rate.date: {
                "price": rate.price,
                "allotment": rate.allotment
            }
        }


class RoomInventorySerializer(ProcessBaseSerializer):
    """
        Serializer to get the rates of each room
    """

    def process_data(self, instance):
        """
            Process the data that comes from a queryset
            :param instance: contains the instance with the data that we need to process
            :return: returns the rates serialized
        """
        room_code = list(instance)[0]
        rates = instance.get(room_code)
        rates_serializer = RateInventorySerializer(rates)
        return {
            room_code: rates_serializer.data
        }


class AvailabilitySerializer(serializers.Serializer):
    """
        Serializer to get the rooms with it's rates, prices and breakdowns
    """
    rooms = serializers.SerializerMethodField()

    def get_rooms(self, queryset):
        """
            Gets the room with its rates, prices and more
            :param queryset: this attribute contains the queryset
            :return: returns the rooms serialized
        """
        if not queryset:
            return {}
        result = self.process_data(queryset)
        room_serializer = RoomInventorySerializer(result)
        return room_serializer.data

    @staticmethod
    def process_data(queryset):
        """
            Process the data that comes from a queryset
            :param queryset: this attribute contains the queryset
            :return: returns a dict that contains each room with it's rates
        """
        result = {}

        for item in queryset:
            rate = RateDocument.get(id=item.rate_id)
            room_code = rate.room.code
            item.rate.price = item.price
            item.rate.allotment = item.allotment
            item.rate.date = str(item.date)
            if room_code not in result.keys():
                result[room_code] = [item.rate]
            else:
                result[room_code].append(item.rate)
        return result

    def to_representation(self, instance):
        """
            Change the form of the data, when records were found or not
            :param instance: this attribute contains the result of all the linked process
            :return: the data such as we expected in the requirements
        """
        if not instance:
            representation = {}
        else:
            representation = super().to_representation(instance)
        return representation
