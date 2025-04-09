from django.db import models

class Data(models.Model):
    TIME_SLOTS = [
        ("08:00", "08:00"),
        ("13:00", "13:00"),
        ("17:00", "17:00"),
    ] # créneau horaire
 
    date = models.DateField(auto_now_add=False)
    time_slot = models.CharField(max_length=5, choices=TIME_SLOTS)  # Ajout du créneau horaire
    temperature = models.FloatField()
    humidity = models.FloatField()
    egg_count = models.IntegerField()
    chicken_count = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.time_slot} - {self.temperature}°C, {self.humidity}% - {self.egg_count} œufs - {self.chicken_count} poules"
