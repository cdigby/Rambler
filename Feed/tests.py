from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from RoutePlanner.models import Route
from .models import Like, Dislike
from urllib.parse import urlencode
import json

title = "Nice walk"
points = "[[100.0, 100.0], [30.0, 30.0]]"
description = "A very nice walk to go on with your friends"
length = 100.0
image = "image"
tags = "scenic rural walk"

title2 = "Horrible walk"
description2 = "Don't go on this walk it's horrible"
tags2 = "nasty urban walk"

title3 = "Town run"
description3 = "I run this way to town every day"
tags3 = "urban run exercise"

def qreverse(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url

class FeedTestCase(TestCase):
    def get_three(self, url):
        response = self.client.get(url)
        first = response.context['routes'][0][0]['title']
        second = response.context['routes'][0][1]['title']
        third = response.context['routes'][1][0]['title']
        return first, second, third

    def get_two(self, url):
        response = self.client.get(url)
        first = response.context['routes'][0][0]['title']
        second = response.context['routes'][0][1]['title']
        return first, second

    def get_one(self, url):
        response = self.client.get(url)
        first = response.context['routes'][0][0]['title']
        return first

    # Create some dummy routes and users
    def setUp(self):
        u1 = User.objects.create_user(username='bob', email='bob@bob.com', password='bob')
        u2 = User.objects.create_user(username='fred', email='fred@fred.com', password='fred')

        r1 = Route()
        r2 = Route()
        r3 = Route()

        r1.create_route(title, points, description, length, image, u1.id, tags)
        r2.create_route(title2, points, description2, length, image, u1.id, tags2)
        r3.create_route(title3, points, description3, length, image, u2.id, tags3)

        #Make ratings r2 > r1 > r3
        r2.rating = 1
        r1.rating = 0
        r3.rating = -1

        r1.save()
        r2.save()
        r3.save()

    def test_show_default(self):
        url = reverse('Feed:feed')
        f, s ,t = self.get_three(url)
        self.assertEqual(f, title3)
        self.assertEqual(s, title2)
        self.assertEqual(t, title)

    def test_show_new(self):
        url = qreverse('Feed:feed', get={'showall': 'new'})
        f, s ,t = self.get_three(url)
        self.assertEqual(f, title3)
        self.assertEqual(s, title2)
        self.assertEqual(t, title)

    def test_show_old(self):
        url = qreverse('Feed:feed', get={'showall': 'old'})
        f, s, t = self.get_three(url)
        self.assertEqual(f, title)
        self.assertEqual(s, title2)
        self.assertEqual(t, title3)

    def test_show_top(self):
        url = qreverse('Feed:feed', get={'showall': 'top'})
        f, s, t = self.get_three(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)
        self.assertEqual(t, title3)

    def test_search_routes_new(self):
        url = qreverse('Feed:feed', get={'query': 'walk', 'target': 'routes', 'sort': 'new'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)

    def test_search_routes_old(self):
        url = qreverse('Feed:feed', get={'query': 'walk', 'target': 'routes', 'sort': 'old'})
        f, s = self.get_two(url)
        self.assertEqual(f, title)
        self.assertEqual(s, title2)

    def test_search_routes_top(self):
        url = qreverse('Feed:feed', get={'query': 'walk', 'target': 'routes', 'sort': 'top'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)

    def test_search_tags_new(self):
        url = qreverse('Feed:feed', get={'query': 'urban', 'target': 'tags', 'sort': 'new'})
        f, s = self.get_two(url)
        self.assertEqual(f, title3)
        self.assertEqual(s, title2)

    def test_search_tags_old(self):
        url = qreverse('Feed:feed', get={'query': 'urban', 'target': 'tags', 'sort': 'old'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title3)

    def test_search_tags_top(self):
        url = qreverse('Feed:feed', get={'query': 'urban', 'target': 'tags', 'sort': 'top'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title3)

    def test_search_description_new(self):
        url = qreverse('Feed:feed', get={'query': 'walk', 'target': 'description', 'sort': 'new'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)

    def test_search_description_old(self):
        url = qreverse('Feed:feed', get={'query': 'walk', 'target': 'description', 'sort': 'old'})
        f, s = self.get_two(url)
        self.assertEqual(f, title)
        self.assertEqual(s, title2)

    def test_search_description_top(self):
        url = qreverse('Feed:feed', get={'query': 'walk', 'target': 'description', 'sort': 'top'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)

    def test_search_users_new(self):
        url = qreverse('Feed:feed', get={'query': 'bob', 'target': 'users', 'sort': 'new'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)

    def test_search_users_old(self):
        url = qreverse('Feed:feed', get={'query': 'bob', 'target': 'users', 'sort': 'old'})
        f, s = self.get_two(url)
        self.assertEqual(f, title)
        self.assertEqual(s, title2)

    def test_search_users_top(self):
        url = qreverse('Feed:feed', get={'query': 'bob', 'target': 'users', 'sort': 'top'})
        f, s = self.get_two(url)
        self.assertEqual(f, title2)
        self.assertEqual(s, title)

    def test_like(self):
        r = Route.objects.all()[0]
        self.client.login(username='fred', password='fred')
        response = self.client.post(reverse('Feed:feed'), {'function': 'LIKE', 'route': r.id}, xhr=True)
        data = json.loads(response.content)
        self.assertEquals(data['rating'], 1)

    def test_dislike(self):
        r = Route.objects.all()[0]
        self.client.login(username='fred', password='fred')
        response = self.client.post(reverse('Feed:feed'), {'function': 'DISLIKE', 'route': r.id}, xhr=True)
        data = json.loads(response.content)
        self.assertEquals(data['rating'], -1)



