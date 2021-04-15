from django.db import models

def validate_presence(attribute):
    print("Validating: ", attribute)
    if attribute != "":
        return True
    else:
        return False

def validate_int(attribute):
    return (attribute.type == int)

class Route(models.Model):
    title = models.CharField(max_length=50, default="", validators=[validate_presence])
    description = models.TextField(max_length=450, default="", validators=[validate_presence])
    points = models.TextField(default="", validators=[validate_presence])
    rating = models.IntegerField()


    def create_route(self, title, points):
        self.title = title
        self.points = points

    def save(self, *args, **kwargs):
        super(Route, self).save(*args, **kwargs)
        print("Saved route: ", self.title, ", Desc: ", self.description, " with points: ", self.points)
