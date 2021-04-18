from django.db import models

# Create your models here.
class Route(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    points = models.TextField()

    def get_likes(self):
        return len(Like.objects.get(pk=self.id).all)

    def create_route(self, title, desc, points):
        self.title = title
        self.description = desc
        self.points = points

    def save(self, *args, **kwargs):
        super(Route, self).save(*args, **kwargs)
        print("Saved route: ", self.title, ", Desc: ", self.description, " with points: ", self.points)

class Like(models.Model):
    user = models.IntegerField()
    route = models.IntegerField()

class Dislike(models.Model):
    user = models.IntegerField()
    route = models.IntegerField()
