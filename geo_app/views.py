# coding: utf-8

import json

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


class BeaconDistance(views.APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def post(self, request, format=None):
        scenarios = Scenario.objects.all()










