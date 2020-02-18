from django.contrib import admin
from .models import *


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_id", "first_name", "username", "send_orders", "date_joined")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "city", "address", "phone", "date_added")