import requests
import pygame

coords = [52.299427, 54.898788] # Альметьевск
spns = [0.005, 0.005]

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": ','.join(coords),
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('Not founded')

res_j = response.json()
toponym = res_j["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

coords_toponym = toponym["Point"]["pos"]




pygame.init()
size = (800, 800)
screen = pygame.display.set_mod(size)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                pass

    map_params = {
        "ll": ",".join(coords_toponym.split(' ')),
        "spn": ','.join(spns),
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    photo = 'p.png'
    with open(photo, 'wb') as f:
        f.write(response.content)

    image = pygame.image.load(photo).convert()

    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))
    pygame.display.flip()
pygame.quit()
