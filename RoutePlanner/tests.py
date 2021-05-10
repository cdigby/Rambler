from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Route

title = "Title"
points = "[[100.0, 100.0], [30.0, 30.0]]"
description = "description"
length = 100.0
image = "image"
user = 1
tags = "scenic walk"

# Create your tests here.
class RouteTestCase(TestCase):

    def test_valid_route_save(self):
        failed = False
        route = Route()
        route.create_route(title, points, description, length, image, user, tags)
        try:
            route.save()
        except(ValidationError):
            failed = True
        self.assertFalse(failed, "Invalid Model")

    def test_invalid_title(self):
        new_title = ""
        route = Route()
        route.create_route(new_title, points, description, length, image, user, tags)
        with self.assertRaises(ValidationError):
            route.save()

    def test_invalid_points(self):
        new_points = ""
        route = Route()
        route.create_route(title, new_points, description, length, image, user, tags)
        with self.assertRaises(ValidationError):
            route.save()

    def test_invalid_description(self):
        new_desc = ""
        route = Route()
        route.create_route(title, points, new_desc, length, image, user, tags)
        with self.assertRaises(ValidationError):
            route.save()

    def test_invalid_length(self):
        new_length = "Invalid"
        route = Route()
        route.create_route(title, points, description, new_length, image, user, tags)
        with self.assertRaises(ValidationError):
            route.save()
        new_length = -30.0
        route.create_route(title, points, description, new_length, image, user, tags)
        with self.assertRaises(ValidationError):
            route.save()

    def test_invalid_image(self):
        new_image = ""
        route = Route()
        route.create_route(title, points, description, length, new_image, user, tags)
        with self.assertRaises(ValidationError):
            route.save()

    def test_data_retireval(self):
        route = Route()
        route.create_route(title, points, description, length, image, user, tags)
        route.save()
        retrieved_route = Route.objects.get(pk=1)
        self.assertEqual(retrieved_route.title, "Title")
        self.assertEqual(retrieved_route.description, "description")
        self.assertEqual(retrieved_route.points, "[[100.0, 100.0], [30.0, 30.0]]")
        self.assertEqual(retrieved_route.length, 100.0)
        self.assertEqual(retrieved_route.image, "image")
        self.assertEqual(retrieved_route.tags, "scenic walk")

