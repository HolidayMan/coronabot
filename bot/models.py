from django.db import models


class TgUser(models.Model):
    tg_id = models.IntegerField()
    first_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    send_orders = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return str(self.id)


class Order(models.Model):
    city = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone = models.CharField(max_length=256, blank=True)
    amount = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey("TgUser", on_delete=models.CASCADE, related_name="users")
    date_added = models.DateTimeField(auto_now_add=True)
