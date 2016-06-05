from django.contrib import admin


from django.contrib.auth.models import User, Group
from models import Scenario, Action, Device

# Register your models here.
admin.site.register(Scenario)
admin.site.register(Action)
admin.site.register(Device)
