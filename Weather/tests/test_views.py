from django.test import TestCase, Client
from django.urls import reverse
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.weather_url = reverse('Weather:weather-page')

    def test_page(self):
        response = self.client.get(self.weather_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weatherPage.html')