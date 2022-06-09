from django.db import models

class Gift(models.Model):
    class Gifttype(models.TextChoices):
        HOLIDAY = "HOLIDAY", "Holiday"
        ANNIVERSARY = "ANNIVERSARY", "Anniversary"
        BIRTHDAY = "BIRTHDAY", "Birthday"

    name = models.CharField(max_length=200)
    event = models.CharField(choices=Gifttype.choices, max_length=30)
    date_assigned = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.IntegerField(STATUS, default=0)

    def __str__(self):
        return self.name