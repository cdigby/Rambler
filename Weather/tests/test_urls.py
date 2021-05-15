from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Weather.views import weather

class TestUrls(SimpleTestCase):

    def test_weather_page_working(self):
        url = reverse('weather-page')
        self.assertEquals(resolve(url).func, weather)