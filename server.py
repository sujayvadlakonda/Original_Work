from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
import Config
from requests_html import HTMLSession


app = Flask(__name__)
CORS(app)
app.secret_key = 'shushmans'

prepsportswear_categories = {
    # The Category Title: The Category ID
    'T-Shirts': '30',
    # 'Sweatshirts': '305',
    # 'Hats': '684',
    # 'Men': '29',
    # 'Women': '11',
    # 'Youth': '89',
    # 'Top Sellers': '183'
}

jostens_categories = {
    # The Category Title: The Category ID
    'T-Shirts': 't-shirts',
    # 'Sweatshirts': 'sweatshirts',
    # 'Hats': 'hats',
    # 'Men': 'mens',
    # 'Women': 'womens',
    # 'Youth': 'kids',
    # 'Top Sellers': 'products'
}

data = {
    'T-Shirts': [],
    'Sweatshirts': [],
    'Hats': [],
    'Men': [],
    'Women': [],
    'Youth': [],
    'Top Sellers': []
}

for category_title, category_id in jostens_categories.items():
    category_url = 'https://schoolstore.jostens.com/school/texas/frisco/reedy-high-school/' + category_id
    category_session = HTMLSession()
    category_response = category_session.get(category_url)
    links = category_response.html.absolute_links

    for link in links:
        # if this link leads to a product
        if '/product' in link:
            product_session = HTMLSession()
            product_response = product_session.get(link)
            product_response.html.render()

            product_title = product_response.html.find('a[href=' + link[39:] + ']', first=True).text
            product_price = product_response.html.find('div.btdzn-add-to-cart-price', first=True).text
            product_img_src = product_response.find('img.btdzn-link-img', first=True).attrs['src']
            print(product_title)
            data[category_title].append({'title': product_title,
                                         'price': product_price,
                                         'img_src': product_img_src,
                                         'url': link})

# Right now this iterates only through prepsportswear.com
# In the future, this should be adapted to function for multiple sites

for category_title, category_id in prepsportswear_categories.items():
    category_url = 'https://www.prepsportswear.com/school/us/Texas/Frisco/Rick-Reedy-High-School-Lions/productlist?schoolid=3208016&category=' + category_id
    category_session = HTMLSession()
    category_response = category_session.get(category_url)
    links = category_response.html.absolute_links

    for link in links:
        if 'https://www.prepsportswear.com/product' in link:
            product_session = HTMLSession()
            product_response = product_session.get(link)
            product_response.html.render()
            product_title = product_response.html.find('h2', first=True).text
            product_price = product_response.html.find('span.priceContent', first=True).text
            product_img_src = product_response.html.find('img.productImage-Front', first=True).attrs['src']

            data[category_title].append({'title': product_title,
                                         'price': product_price,
                                         'img_src': product_img_src,
                                         'url': link})


@app.route('/')
def index():
    return "<h5>" + data.__repr__() + "</h5>"


@app.route('/test')
def test():
    json = {'hello': 'world'}
    return jsonify(json)


app.run(debug=Config.DEBUG)
