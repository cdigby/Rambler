from django.db import models

# Create your models here.
class Route(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField
    points = []

    def create_route(self, title, points):
        self.title = title
        self.points = points

    def save(self, *args, **kwargs):
        #super(Route, self).save(*args, **kwargs)
        print("Saved route: ", self.title, ", Desc: ", self.description, " with points: ", self.points)