from django.core.exceptions import ValidationError
from django.db import models


def validate_presence(attribute):
    print("Validating: ", attribute)
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
    image = models.CharField(max_length=2048, default="")

    def create_route(self, title, points, description, length, image):
        self.title = title
        self.points = points
        self.description = description
        self.image = image
        self.length = length
        print(self.length)

    def printRoute(self):
        print(self.title, self.description, round(self.length, 2), self.points, self.image)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Route, self).save(*args, **kwargs)
        print("Saved route: ", self.title, ", Desc: ", self.description, " with points: ", self.points)
