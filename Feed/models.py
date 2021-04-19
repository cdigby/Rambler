from django.db import models


# Create your models here.
class Route(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    points = models.TextField()

    def get_likes(self):
        try:
            #print (Like.objects.filter(pk=3))
            return Like.objects.filter(route=self.id).count()
        except models.ObjectDoesNotExist:
            return 0;

    def get_dislikes(self):
        try:
            return Dislike.objects.filter(route=self.id).count()
        except models.ObjectDoesNotExist:
            return 0;

    def get_rating(self):

        return self.get_likes() - self.get_dislikes()

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

    def create_like(self, route, user):
        self.route = route
        self.user = user

    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)
        print("Saved like, Route", self.route, ", User: ", self.user)


class Dislike(models.Model):
    user = models.IntegerField()
    route = models.IntegerField()

    def create_dislike(self, route, user):
        self.route = route
        self.user = user

    def save(self, *args, **kwargs):
        super(Dislike, self).save(*args, **kwargs)
        print("Saved dislike, Route", self.route, ", User: ", self.user)

