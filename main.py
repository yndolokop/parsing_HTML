import pprint
import requests
from bs4 import BeautifulSoup
import re

'''
Будем парсить сайт www.film.ru на топ 30 лучших сериалов. Нам нужно русское и английское название, также 
дата выхода фильма и ссылка на сам фильм'''


url = 'https://www.film.ru/a-z/serials'

response = requests.get(url)  # запрос на сайт

soup = BeautifulSoup(response.text, 'html.parser')  # парсим весь сайт

print(soup.find('div', class_='film_list').find('a', class_='film_list_link').get('href'))  # ищем ссылку на фильм

link = url + soup.find('div', class_='film_list_block').find('a', class_='film_list_link').get('href')

name_ru = soup.find('div', class_='film_list').find('a', class_='film_list_link').find('strong').string  # название RU

name_en = soup.select("span[title]")  # название EN фильма. Они записано в теге span title. Поэтому используем .select()

films = soup.find_all('div', class_='film_list')  # найдем все div с карточками фильмов
print(len(films))

data = []  # будет добавлять спарсенные элементы

for film in films:
    link = url + film.find('a', class_='film_list_link').get('href')
    name_ru = film.find('a', class_='film_list_link').find('strong').text
    date = film.find('a', class_='film_list_link').find_all('span')[2].text
    name_en = film.select("span[title]")
    for name in name_en:
        n = re.findall('"([^"]*)"', str(name))  # обязательно переведем класс soup в строку
        data.append([name_ru, n, date, link])  # добавим в список
pprint.pprint(data)

