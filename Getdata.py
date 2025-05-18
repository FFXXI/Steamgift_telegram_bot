import requests
from bs4 import BeautifulSoup


from Getcookies import get_cookies


HEADERS={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}


def get_data(url, headers=HEADERS):
    r = requests.get(url, cookies=get_cookies(), headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


if __name__ == "__main__":
    pass
