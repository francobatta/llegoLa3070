import requests
import time
from bs4 import BeautifulSoup
import telegram_url
import asyncio

TELEGRAM_URL = telegram_url.api_uri

URL = 'https://compragamer.com/index.php?criterio=3070&x=0&y=0&seccion=3&nro_max=50'

def getUrl(item):
    return 'https://compragamer.com/index.php?criterio='+item+'&x=0&y=0&seccion=3&nro_max=50'

async def check(url,value):
    has_product_flag = True
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, requests.get, url)
    page = await future
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
            requests.get(TELEGRAM_URL + 'Atento maestro, parece que la '+value+' ha arribado')
            print('Hay productos de la'+ value +' pero no hay stock')
            has_product_flag = False
        elif has_stock:
            requests.get(TELEGRAM_URL + 'LLEGO LA '+value+' PAPA HORA DE COMPRAR')
            print('LLEGO LA '+value+' SUPREMA')


products = ["580","3070","3080"]

async def main():
    values = await asyncio.gather(*[check(getUrl(i),i) for i in products])

while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    time.sleep(120)