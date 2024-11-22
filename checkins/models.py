from django.contrib.auth.models import User
from django.db import models

class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 = very poor, 5 = excellent
    sleep_hours = models.FloatField()
    stress_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
