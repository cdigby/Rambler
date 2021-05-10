from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from RoutePlanner.models import Route

title = "Nice walk"
points = "[[100.0, 100.0], [30.0, 30.0]]"
description = "A very nice walk to go on with your friends"
length = 100.0
image = "image"
user = 1
tags = "scenic rural walk"

title2 = "Horrible walk"
description2 = "Don't go on this walk it's horrible"
user2 = 1
tags2 = "nasty ugly walk"

title3 = "Town run"
description3 = "I run this way to town every day"
user3 = 2
tags3 = "urban run exercise"

class FeedTestCase(TestCase):
    # Create some dummy routes and users
    def setUp(self):
        User.objects.create_user(username='bob', email='bob@bob.com', password='bob')
        User.objects.create_user(username='fred', email='fred@fred.com', password='fred')

        r1 = Route()
        r2 = Route()
        r3 = Route()

        r1.create_route(title, points, description, length, image, user, tags)
        r2.create_route(title2, points, description2, length, image, user2, tags2)
        r3.create_route(title3, points, description3, length, image, user3, tags3)

        r1.save()
        r2.save()
        r3.save()

    def test_show_latest(self):
        url = reverse('Feed:feed')
        response = self.client.get(url)
        first = response.context['routes'][0][0].title
        self.assertEqual(first, title3)
