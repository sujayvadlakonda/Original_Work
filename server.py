from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import Config
import requests


app = Flask(__name__)
CORS(app)
app.secret_key = 'shushmans'


prepsportswear_categories = {
    # The Category Title: The Category ID
    'T-Shirts': '30',
    'Sweatshirts': '305',
    'Hats': '684',
    'Applique': '1717',
    'Men\'s': '29',
    'Women\'s': '11',
    'Youth': '89',
    'Top Sellers': '183'
}

data = {}

#Consider moving method to a Util file
def url_to_soup(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


# Right now this iterates only through prepsportswear.com
# In the future, this should be adapted to function for multiple sites

for category_title, category_id in prepsportswear_categories.items():
    category_url = 'https://www.prepsportswear.com/school/us/Texas/Frisco/Rick-Reedy-High-School-Lions/productlist?schoolid=3208016&category=' + category_id
    category_soup = url_to_soup(category_url)
    data[category_title] = []

    for product in category_soup.find_all('a'):
        href = product.get('href')
        if href[0:8] == '/product':
            product_soup = url_to_soup('https://www.prepsportswear.com' + href)
            product_title = product_soup.find('h2').text
            product_price = product_soup.find('span', {'class': 'priceContent'}).text
            # Notably, the image is missing from the information being WebScraped
            # This is an essential part of the original work and should be completed
            data[category_title].append({'title': product_title, 'price': product_price})


@app.route('/')
def index():
    # mainly used for testing
    print(data)
    return data.__repr__()


@app.route('/test')
def test():
    json = {'hello': 'world'}
    return jsonify(json)


app.run(debug=Config.DEBUG)

# {
#     'hats': [
#         {'product_title': 'a', 'product_price': '39', 'type': 'hat'},
#         {'product_title': 'b', 'product_price': '79', 'type': 'hat'},
#         {'product_title': 'c', 'product_price': '29', 'type', 'hat'}
#     ],
#     'shirts': [
#         {'product_title': 'a', 'product_price': '39', 'type': 'hat'},
#         {'product_title': 'b', 'product_price': '79', 'type': 'hat'},
#         {'product_title': 'c', 'product_price': '29', 'type', 'hat'}
#     ]
# }
