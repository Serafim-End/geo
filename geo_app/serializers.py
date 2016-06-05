# coding: utf-8

from django.contrib.auth.models import Group, User
from rest_framework import serializers

from models import Scenario, Action, Device


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'is_superuser', 'scenario_set', 'device_set')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'latitude', 'longitude')


class ActionSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True)

    class Meta:
        model = Action
        fields = ('name', 'status', 'devices')

    def create(self, validated_data):
        a = Action.objects.create(
            name=validated_data['name'],
            status=validated_data['status']
        )

        return a


class ScenarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scenario
        fields = ('name', 'latitude', 'longitude', 'distance', 'action_set')