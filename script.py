import requests
import time
from bs4 import BeautifulSoup
import telegram_url

TELEGRAM_URL = telegram_url.api_uri

URL = 'https://compragamer.com/index.php?criterio=3070&x=0&y=0&seccion=3&nro_max=50'

has_product_flag = True

while True:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # este string dice la cantidad de productos de acuerdo a los query params de arriba
    has_products = soup.find_all("span", class_="sorting__info")
    has_products_string = str(has_products)
    # este array indica si se puede agregar al carrito (hay stock) o no
    has_stock = soup.find_all("button",class_="products-btns__btn products-btns__add")

    # si no hay 0 productos, o sea si hay productos
    if "1 - 0" not in has_products_string:
        # queremos una sola notif de si llego el producto
        if has_product_flag and not has_stock:
            print("Hay productos de la 3070 pero no hay stock")
            requests.get(TELEGRAM_URL + 'Atento maestro, parece que la 3070 ha arribado')
            has_product_flag = False
        elif has_stock:
            requests.get(TELEGRAM_URL + 'LLEGO LA 3070 PAPA HORA DE COMPRAR')
            print("LLEGO LA 3070 SUPREMA")
    # GET cada 120s
    time.sleep(120)