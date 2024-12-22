from rest_framework import serializers
from .models import *
from customers.serializers import UserSerializer


class CarSerializer(serializers.ModelSerializer):
        class Meta:
                model = Car
                fields = '__all__'




class BookingSerializer(serializers.ModelSerializer):
        car_details = CarSerializer(source='car', read_only=True)
        car_make = serializers.SerializerMethodField()
        car_model = serializers.SerializerMethodField()
        user_details = UserSerializer(source='user', read_only=True)
        class Meta:
                model = Booking
                fields = ['id', 'start_date', 'end_date', 'total_price', 'status', 'car', 'car_details', 'user_details', 'car_make', 'car_model']

        def get_car_make(self, obj):
                return obj.car.make

        def get_car_model(self, obj):
                return obj.car.model

        def create(self, validated_data):
                car = validated_data.pop('car')
                #car_instance = Car.objects.get(id=car)
                booking = Booking.objects.create(car=car, **validated_data)
                return booking

        def update(self, instance, validated_data):
                car_data = validated_data.pop('car')
                car = Car.objects.get(id=car_data['id'])
                instance.car = car
                instance.start_date = validated_data.get('start_date', instance.start_date)
                instance.end_date = validated_data.get('end_date', instance.end_date)
                instance.status = validated_data.get('status', instance.status)
                instance.save()
                return instance


class PaymentSerializer(serializers.ModelSerializer):
        booking = BookingSerializer()
        class Meta:
                model = Payment
                fields = '__all__'