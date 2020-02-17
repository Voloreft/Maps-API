import requests
import pygame

coords = '52.299427,54.898788' # Альметьевск

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": coords,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('Not founded')

res_j = response.json()
toponym = res_j["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

coords_toponym = toponym["Point"]["pos"]

pygame.init()

screen = pygame.display.set_mod()
