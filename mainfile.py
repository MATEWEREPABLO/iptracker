#from flask import Flask, render_template, request, redirect, url_for
#import requests
#from bs4 import BeautifulSoup
#
#app = Flask(__name__)
#
#user_logged_in = False
#
#website1_data = []
#website2_data = []
#
#def scrape_website1():
#    url = "https://vtechmw.co/"
#    response = requests.get(url)
#
#    if response.status_code == 200:
#        soup = BeautifulSoup(response.text, 'html.parser')
#
#        product_elements = soup.find_all('div', class_='product-inner')
#
#        website1_data.clear()
#
#        for product in product_elements:
#            product_name_element = product.find('h2', class_='woocommerce-loop-product__title')
#            product_name = product_name_element.text.strip() if product_name_element else "Product name not found"
#
#            product_price_element = product.find('span', class_='woocommerce-Price-amount amount')
#            product_price = product_price_element.text.strip() if product_price_element else "Price not found"
#
#            website1_data.append({'Product Name': product_name, 'Product Price': product_price})
#
#    else:
#        print("Failed to retrieve data from the first website. Status code:", response.status_code)
#
#def scrape_website2():
#    url = "https://www.iconicmalawi.com/NewArrivalsProducts"
#    response = requests.get(url)
#
#    if response.status_code == 200:
#        soup = BeautifulSoup(response.text, 'html.parser')
#
#        product_elements = soup.find_all('div', class_='product-card')
#
#        website2_data.clear()
#
#        for product in product_elements:
#            product_name_element = product.find('p', class_='product-name mx-2')
#            product_name = product_name_element.text.strip() if product_name_element else "Product name not found"
#
#            product_price_element = product.find('p', class_='product-price mr-auto')
#            product_price = product_price_element.text.strip() if product_price_element else "Price not found"
#
#            website2_data.append({'Product Name': product_name, 'Product Price': product_price})
#
#    else:
#        print("Failed to retrieve data from the second website. Status code:", response.status_code)
#
#@app.route('/')
#def index():
#    if not user_logged_in:
#        return redirect(url_for('login'))
#    data_available = len(website1_data) > 0 or len(website2_data) > 0
#    return render_template('index.html', data_available=data_available)
#
#users = {
#    'user1': 'password1',
#    'user2': 'password2',
#    'user3': 'pass',
#}
#
#def is_valid_login(username, password):
#    return username in users and users[username] == password
#
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    global user_logged_in  
#    if request.method == 'POST':
#        username = request.form.get('username')
#        password = request.form.get('password')
#
#        if is_valid_login(username, password):
#            user_logged_in = True
#            return redirect(url_for('index'))
#        else:
#            return "Invalid login credentials. Please try again or sign up."
#
#    return render_template('login.html')
#
#def is_username_taken(username):
#    return username in users
#
#def add_user(username, password):
#    users[username] = password
#
#@app.route('/signup', methods=['GET', 'POST'])
#def signup():
#    global user_logged_in  
#    if request.method == 'POST':
#        username = request.form.get('username')
#        password = request.form.get('password')
#
#        if is_username_taken(username):
#            return "Username is already taken. Please choose a different one."
#        else:
#            add_user(username, password)
#
#            user_logged_in = True
#
#            return redirect(url_for('index'))
#
#    return render_template('signup.html')
#
#@app.route('/start_scraping', methods=['POST'])
#def start_scraping():
#    if user_logged_in:
#        scrape_website1()
#        scrape_website2()
#        return "Scraping process has been completed succefully ."
#    else:
#        return "Unauthorized. Please log in or sign up."
#
#@app.route('/show_data', methods=['GET'])
#def show_data():
#    if user_logged_in:
#        return render_template('data.html', website1_data=website1_data, website2_data=website2_data)
#    else:
#        return "Unauthorized. Please log in or sign up."
#
#@app.route('/compare_prices', methods=['GET'])
#def compare_prices():
#    if user_logged_in:
#        compared_data = []
#
#        for item1 in website1_data:
#            for item2 in website2_data:
#                if item1['Product Name'] == item2['Product Name']:
#                    compared_data.append({
#                        'Product Name': item1['Product Name'],
#                        'Website 1 Price': item1['Product Price'],
#                        'Website 2 Price': item2['Product Price']
#                    })
#
#        return render_template('compare.html', compared_data=compared_data)
#    else:
#        return "Unauthorized. Please log in or sign up."
#
#if __name__ == "__main__":
#    app.run(debug=True)
#