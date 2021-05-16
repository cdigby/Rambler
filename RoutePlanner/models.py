from django.core.exceptions import ValidationError
from django.db import models
from Feed.models import Like, Dislike
from django.contrib.postgres.fields import ArrayField


def validate_presence(attribute):
    #print("Validating: ", attribute)
    if attribute == "":
        raise ValidationError("%(field) is empty",
                              params={'field': attribute},
                              )


def validate_int(attribute):
    return attribute.type == int


def validate_length(attribute):
    if type(attribute) != float:
        raise ValidationError("%(field) is not a float",
                              params={'field': attribute},
                              )
    if attribute < 0:
        raise ValidationError("%(field) is negative",
                              params={'field': attribute},
                              )


class Route(models.Model):
    title = models.CharField(max_length=50, default="", validators=[validate_presence])
    description = models.TextField(max_length=450, default="", validators=[validate_presence])
    points = models.TextField(default="", validators=[validate_presence])
    length = models.FloatField(default=0.0, validators=[validate_length])
    #Limit image url to 8192 characters, as that is the max the mapbox api will accept
    image = models.CharField(max_length=8192, default="")
    user = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    tags = ArrayField(models.CharField(max_length=50, blank=True))
    rating = models.IntegerField()

    def create_route(self, title, points, description, length, image, user, tags):
        self.title = title
        self.points = points
        self.description = description
        self.image = image
        self.length = length
        self.user = user
        self.tags = tags.lower().split()
        self.rating = 0
        #print(self.length)

    def printRoute(self):
        print(self.title, self.description, round(self.length, 2), self.points, self.image)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Route, self).save(*args, **kwargs)
        #print("Saved route: ", self.title, ", Desc: ", self.description, " with points: ", self.points)

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
