import requests
from bs4 import BeautifulSoup
import pymongo


def scrape_products():

    URL = "https://www.amazon.in/s?bbn=976419031&rh=n%3A976419031%2Cp_89%3Arealme&dc&qid=1624216249&rnid=3837712031&ref=lp_976420031_nr_p_89_3"

    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})

    markup = requests.get(URL, headers=HEADERS).text

    soup = BeautifulSoup(markup, 'html.parser')

    products = []
    i = 1

    for item in soup.select('div.a-spacing-none.a-section'):

        product = {}
        try:
            product['name'] = item.select_one(
                'span.a-text-normal.a-color-base.a-size-base-plus').get_text()

            price = item.select_one('span.a-price-whole').get_text()
            price = price.replace(',', '')
            product['price'] = int(price)

            rating = item.select_one('span.a-icon-alt').get_text()
            product['rating'] = float(list(rating.split(" "))[0])

            reviews = item.select_one('span.a-size-base').get_text()
            reviews = reviews.replace(',', '')
            product['reviews'] = int(reviews)

            product['id'] = i
            i = i + 1

        except:
            continue

        products.append(product)

    return products


# for i in products:
#     print(i)

# print(len(products))

# print(soup.select_one('a.s-pagination-button.s-pagination-item'))

products = scrape_products()

# for i in products:
#     print(i)
# print(len(products))

client = pymongo.MongoClient()
realme = client.realme.products_product

realme.insert_many(products)
print(f'Inserted {len(products)} products')
