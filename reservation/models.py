from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=256)
    room_places = models.IntegerField(default=0)
    project_available = models.BooleanField(default=False)

class Reservation(models.Model):
    data = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField()

class Meta:
    unique_together = ('data', 'room_id',)