import requests
import time
import sys
import re
import json
from requests import RequestException
from random import randint

from Getcookies import get_cookies
from Getdata import get_data, HEADERS


COOKIES = get_cookies()
print("Читаем файл cookies.txt", "*" * 22, sep="\n", end="\n \n")

points=None

# filter_url = {
#             'All': "search?page=%d",
#             'Wishlist': "search?page=%d&type=wishlist",
#             'Recommended': "search?page=%d&type=recommended",
#             'Copies': "search?page=%d&copy_min=2",
#             'DLC': "search?page=%d&dlc=true",
#             'New': "search?page=%d&type=new"
#         }

def get_page():
    global xsrf_token, points

    try:
        soup = get_data("https://www.steamgifts.com")

        xsrf_token = soup.find("input", {"name": "xsrf_token"})["value"]
        points = int(soup.find("span", {"class": "nav__points"}).text)
        print(f"У вас {points} очков.")

    except RequestException:
        print("Нет соединения с сайтом.")
        print("Ждем 2 минуты до соединения...")
        time.sleep(120)
        get_page()
    except TypeError:
        print("Непорядок с куки ((.")
        time.sleep(20)
        sys.exit(0)

games=[]
def get_games():
    global pages
    max_pages=int(input("Введите количество читаемых страниц: "))
    n = 1
    while n <= max_pages:
        soup = get_data('https://www.steamgifts.com/giveaways/search?page=' + str(n))
        lists = soup.find_all("div", class_="giveaway__row-outer-wrap")
        print(f"Читаем страницу {n}")

        for list in lists:
            # price=list.find("span", class_="giveaway__heading__thin", text=re.compile("P")).text  # находим цену игры с помощью re
            len_copies = str(list.find_all("span", class_="giveaway__heading__thin")[0].text).replace("(","").replace(")","").replace(",","") # находим количество копий игры, вырезаем () и ",", приводим к str


            if re.findall("Copies", len_copies): # Проверяем есть ли слово Copies
                len_copies=int(len_copies.replace("Copies",""))  # Если True вырезаем "Copies" и приводим к int
            else:
                len_copies = int(1)  # Если False приводим к 1
            if not list.find("div",{"class":"giveaway__row-inner-wrap is-faded"}):
                games.append({
                    "titles": list.find("a", {"class":"giveaway__heading__name"}).text,  # находим название игры
                    "price": int(list.find_all("span", {"class": "giveaway__heading__thin"})[-1].text.replace("(", "").replace(")","").replace("P", "")), # находим цену игры, удаляем(p),приводим к int
                    "len_copies": len_copies, # количество копий игры
                    "game_id": list.find('a', {'class': 'giveaway__heading__name'})['href'].split('/')[2] # Получаем Game_id
                    })
        time.sleep(randint(3, 5))
        n +=1


def entry_gifts():
    global points
    print(f"У вас {points} очков ")
    min_copies = int(input("Введите минимальное количество копий: "))
    min_price = int(input("Введите минимальную цену: "))
    while points > 6 and bool(games):
        if games[0].get("len_copies") >= min_copies and games[0].get("price") >= min_price and points - games[0].get("price") >=0:
            print(f"Осталось: {points}")
            payload = {'xsrf_token': xsrf_token, 'do': 'entry_insert', 'code': games[0].pop("game_id")}
            entry = requests.post('https://www.steamgifts.com/ajax.php', data=payload, cookies=COOKIES, headers=HEADERS)
            json_data = json.loads(entry.text)
            points=int(json_data.get("points"))

            if json_data['type'] == 'success':
                print(f'> Бот получил игру: {games[0].get("titles")} за :{games[0].get("price")}p  Количество копий :{games[0].get("len_copies")}')
                del games[0]
                time.sleep(randint(3,7))
            else:
                print("Что-то пошло не так")
        else:
            del games[0]

    else:
        print(f"<<< Не хватает очков, осталось: {points} или игр, осталось: {len(games)} >>>")
        while True:
            reboot_ = input("Хотите повторить [y/n]: ")
            if reboot_.lower() in ["y","д","да"]:
                get_page()
                get_games()
                entry_gifts()
            elif reboot_.lower() in ["n","н","нет","т"]:
                print("Выходим...")
                time.sleep(3)
                sys.exit(0)
            else:
                print("Введите правильное значение Y или N.")
                continue

if __name__ == '__main__':
    get_page()
    get_games()
    entry_gifts()
