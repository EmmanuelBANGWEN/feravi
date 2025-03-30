from django.db import models

class Data(models.Model):
    date = models.DateField(auto_now_add=False)
    temperature = models.FloatField()
    humidity = models.FloatField()
    egg_count = models.IntegerField()
    chicken_count = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.temperature}°C, {self.humidity}% - {self.egg_count} œufs - {self.chicken_count} poules "


