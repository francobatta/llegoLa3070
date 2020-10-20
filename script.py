import requests
import time
from bs4 import BeautifulSoup
import telegram_url

TELEGRAM_URL = telegram_url.api_uri

URL = 'https://compragamer.com/index.php?criterio=3070&x=0&y=0&seccion=3&nro_max=50'
page = requests.get(URL)

has_product_flag = True

while True:
    soup = BeautifulSoup(page.content, 'html.parser')

    has_products = soup.find_all("span", class_="sorting__info")
    has_products_string = str(has_products)
    has_stock = soup.find_all("button",class_="products-btns__btn products-btns__add")

    if "1 - 0" not in has_products_string:
        if has_product_flag and not has_stock:
            print("Hay productos de la 3070 pero no hay stock")
            requests.get(TELEGRAM_URL + 'Atento maestro, parece que la 3070 ha arribado')
            has_product_flag = False
        elif has_stock:
            requests.get(TELEGRAM_URL + 'LLEGO LA 3070 PAPA HORA DE COMPRAR')
            print("LLEGO LA 3070 SUPREMA")
    time.sleep(3)