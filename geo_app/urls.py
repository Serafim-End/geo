# coding: utf-8

from django.conf.urls import url, include

from rest_framework import routers

import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('actions', views.ActionViewSet)
router.register('scenarios', views.ScenarioViewSet)
router.register('devices', views.DeviceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
