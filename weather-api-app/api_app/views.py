from django.shortcuts import render
import requests
from .forms import CityForm
from .models import City
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def index(request):
    """Index View"""

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=300643401e394f710740603cbc8f63c4'
    icon_url = 'http://openweathermap.org/img/w/{}.png'
    # city = 'London'
    # detail_city_weather = requests.get(url.format(city)).json()
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('index'))

    cities = City.objects.all()
    hot_city = []
    warm_city = []
    cold_city = []
    """Appending each city data dict in the DB to either hold,warm, or cold city list"""
    for city in cities:
        # print(city.city_name)
        city_name = city.city_name
        detail_city_weather = requests.get(url.format(city_name)).json()
        temp = detail_city_weather['main']['temp']
        icon_img = icon_url.format(detail_city_weather['weather'][0]['icon'])
        city_data = {
            'city_name':city_name,
            'temp':temp,
            'humidity':str(detail_city_weather['main']['humidity'])+'%',
            'description':detail_city_weather['weather'][0]['description'],
            'icon':icon_img
        }
        if temp <= 40:
            cold_city.append(city_data)
        elif temp > 40 and temp <= 65:
            warm_city.append(city_data)
        else:
            hot_city.append(city_data)

    # print(temp)
    # print(warm_city_context)
    context = {'cold_city':cold_city, 'warm_city':warm_city, 'hot_city': hot_city, 'form':form}
    return render(request, 'api_app/index.html', context)
