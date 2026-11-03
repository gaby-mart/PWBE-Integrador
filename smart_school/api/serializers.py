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
    class Meta:
        model = Laboratory
        fields = '__all__'

class MicrocontrollerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicrocontrollerModel
        fields = '__all__'

class MicrocontrollerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microcontroller
        fields = '__all__'

class MeasuredUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = '__all__'

class SensorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorModel
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['sr_id', 'sr_measured_value', 'sr_measured_at', 'sr_sen']
        read_only_fields = ['sr_id', 'sr_measured_at']

    def validate(self, data):
        sensor = data.get('sr_sen')
        
        if sensor and not sensor.sen_is_active:
            raise serializers.ValidationError(
                {"sr_sen": "Não é permitido registrar leituras para um sensor inativo."}
            )
            
        if sensor and sensor.sen_connected_to and not sensor.sen_connected_to.mc_is_active:
            raise serializers.ValidationError(
                {"sr_sen": "Não é permitido registrar leituras. O microcontrolador associado a este sensor está inativo."}
            )
            
        return data