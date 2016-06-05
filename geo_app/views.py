# coding: utf-8

import math
import json
import logging

from django.contrib.auth.models import Group, User
from rest_framework import viewsets, permissions, views, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from oauth2_provider.ext.rest_framework import (TokenHasReadWriteScope,
                                                TokenHasScope)

from models import Action, Scenario, Device
from serializers import (UserSerializer, GroupSerializer, ScenarioSerializer,
                         ActionSerializer, DeviceSerializer)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @detail_route(methods=['post'])
    def set_distances(self, request, pk=None):
        u = self.get_object()
        distances = json.loads(request.POST['distances'])
        for device, dist in zip(u.device_set.all(), distances):
            device.distance = float(dist)
            device.save()

        return Response({'password': 'set'}, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_distances(self, request, pk=None):
        u = self.get_object()
        return Response([d.distance for d in u.device_set.all()],
                        status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_active_scenarios(self, request, pk=None):
        u = self.get_object()

        scenario_distances = {}
        scenarios = []
        for s in Scenario.objects.all():
            devices = u.device_set.all()

            u_distances = [d.distance for d in u.device_set.all()]
            s_distances = [self.__distance(
                (s.latitude, s.longitude), (d.latitude, d.longitude)
            ) for d in devices]

            scenario_distances[str(s.id)] = s_distances

            if self.__square_distance(u_distances, s_distances) < s.distance:
                scenarios.append(s.id)

        return Response(json.dumps(scenarios), status.HTTP_200_OK)

    @staticmethod
    def __square_distance(d, s):
        return sum([(i - j) ** 2 for i, j in zip(d, s)])

    @staticmethod
    def __distance(origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371000

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))

        return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ActionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ScenarioViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
