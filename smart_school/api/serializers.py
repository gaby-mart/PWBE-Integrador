from rest_framework import serializers
from django import forms
from .models import User, Laboratory, Microcontroller, MicrocontrollerModel, MeasurementUnit, SensorModel, Sensor, SensorReading


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
            'first_name',
            'last_name',
            'ni', 
            'photo',
            'is_superuser',
            'is_staff',
            'password'
        ]
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password:
            instance.set_password(password)
        instance.save()
        return instance  

class LaboratorySerializer(serializers.ModelSerializer):
    model = Laboratory
    field = '__all__'

class MicrocontrollerModelSerializer(serializers.ModelSerializer):
    model = MicrocontrollerModel
    field = '__all__'

class MicrocontrollerSerializer(serializers.ModelSerializer):
    model = Microcontroller
    field = '__all__'

class MeasuredUnitSerializer(serializers.ModelSerializer):
    model = MeasurementUnit
    field = '__all__'

class SensorModelSerializer(serializers.ModelSerializer):
    model = SensorModel
    field = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    model = Sensor
    field = '__all__'

class SensorReadingSerializer(serializers.ModelSerializer):
    model = SensorReading
    field = '__all__'