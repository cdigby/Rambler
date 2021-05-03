from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
'''
class Route(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    points = models.TextField()
    user = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    tags = ArrayField(models.CharField(max_length=50, blank=True))
    rating = models.IntegerField()

    def get_likes(self):
        try:
            #print (Like.objects.filter(pk=3))
            return Like.objects.filter(route=self.id).count()
        except models.ObjectDoesNotExist:
            return 0

    def get_dislikes(self):
        try:
            return Dislike.objects.filter(route=self.id).count()
        except models.ObjectDoesNotExist:
            return 0

    def get_rating(self):
        return self.get_likes() - self.get_dislikes()

    def update_rating(self):
        self.rating = self.get_rating()
        self.save()

    def create_route(self, title, desc, points, user, tags):
        self.title = title
        self.description = desc
        self.points = points
        self.user = user
        self.tags = tags.lower().split()
        self.rating = 0

    def save(self, *args, **kwargs):
        super(Route, self).save(*args, **kwargs)
'''

class Like(models.Model):
    user = models.IntegerField()
    route = models.IntegerField()

    def create_like(self, route, user):
        self.route = route
        self.user = user

    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)


class Dislike(models.Model):
    user = models.IntegerField()
    route = models.IntegerField()

    def create_dislike(self, route, user):
        self.route = route
        self.user = user

    def save(self, *args, **kwargs):
        super(Dislike, self).save(*args, **kwargs)

