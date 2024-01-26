from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
import threading
import secrets
import time

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

user_logged_in = False

user_logged_in_lock = threading.Lock()

website1_data = []
website2_data = []

scraping_active = False

def scrape_website1():
    url = "https://vtechmw.co/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_elements = soup.find_all('div', class_='product-inner')

        website1_data.clear()

        for product in product_elements:
            product_name_element = product.find('h2', class_='woocommerce-loop-product__title')
            product_name = product_name_element.text.strip() if product_name_element else "Product name not found"

            product_price_element = product.find('span', class_='woocommerce-Price-amount amount')
            product_price = product_price_element.text.strip() if product_price_element else "Price not found"
            
            product_link_element = product.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
            product_link = product_link_element.get('href') if product_link_element else "Link not found"

            website1_data.append({
    'Product Name': product_name,
    'Product Price': product_price,
    'Product Link': product_link,})


    else:
        print("Failed to retrieve data from the first website. Status code:", response.status_code)

def scrape_website2():
    url = "https://www.iconicmalawi.com/NewArrivalsProducts"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_elements = soup.find_all('div', class_='product-card')

        website2_data.clear()

        for product in product_elements:
            product_name_element = product.find('p', class_='product-name mx-2')
            product_name = product_name_element.text.strip() if product_name_element else "Product name not found"

            product_price_element = product.find('p', class_='product-price mr-auto')
            product_price = product_price_element.text.strip() if product_price_element else "Price not found"
            
            product_link_element = product.find('a', class_='product-link')
            product_link = product_link_element.get('href') if product_link_element else "Product link not found"

            website2_data.append({
    'Product Name': product_name,
    'Product Price': product_price,
    'Product Link': product_link,})

    else:
        print("Failed to retrieve data from the second website. Status code:", response.status_code)
        
def parse_price(price_str):
    try:
     
        return float(price_str.replace('mwk', '').replace(',', '').strip())
    except ValueError:
       
        return None


def initiate_scraping():
    global scraping_active
    global website1_data
    global website2_data

    previous_website1_data = website1_data.copy()  
    previous_website2_data = website2_data.copy()

    scraping_active = True
    scrape_website1()
    scrape_website2()
    scraping_active = False

    
    website1_changes = compare_prices(previous_website1_data, website1_data)
    website2_changes = compare_prices(previous_website2_data, website2_data)

   
    update_price_template(website1_changes, website2_changes)

def compare_prices(previous_data, current_data):
    changes = []

    for prev_item in previous_data:
        for curr_item in current_data:
            if prev_item['Product Name'] == curr_item['Product Name']:
                prev_price = parse_price(prev_item['Product Price'])
                curr_price = parse_price(curr_item['Product Price'])

                if prev_price is not None and curr_price is not None and prev_price != curr_price:
                   
                    changes.append({
                        'Product Name': curr_item['Product Name'],
                        'Previous Price': prev_item['Product Price'],
                        'Current Price': curr_item['Product Price']
                    })

    return changes

def update_price_template(website1_changes, website2_changes):
    global website1_price_changes
    global website2_price_changes

    website1_price_changes = website1_changes
    website2_price_changes = website2_changes





@app.route('/')
def index():
    global user_logged_in
    global scraping_active
    global website1_data
    global website2_data

    if not user_logged_in:
        return redirect(url_for('login'))

    while scraping_active:
        time.sleep(1)

    data_available = len(website1_data) > 0 or len(website2_data) > 0
    return render_template('index.html', data_available=data_available)

users = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'pass',
}

def is_valid_login(username, password):
    return username in users and users[username] == password

def is_username_taken(username):
    return username in users

def add_user(username, password):
    users[username] = password

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_logged_in
    global user_logged_in_lock

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if is_valid_login(username, password):
            time.sleep(3)

            with user_logged_in_lock:
                user_logged_in = True

            scraping_thread = threading.Thread(target=initiate_scraping)
            scraping_thread.start()

            return redirect(url_for('index'))
        else:
            return "Invalid login credentials. Please try again or sign up."

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global user_logged_in
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if is_username_taken(username):
            return "Username is already taken. Please choose a different one."
        else:
            add_user(username, password)

            user_logged_in = True

            return redirect(url_for('index'))
        

    return render_template('signup.html')


from flask import jsonify

from flask import render_template

@app.route('/get_prices', methods=['POST'])
def get_prices():
    global scraping_active
    scraping_active = True
    scrape_website1()
    scrape_website2()
    scraping_active = False


    initiate_scraping()

    return render_template('price.html', website1_changes=website1_price_changes, website2_changes=website2_price_changes)



@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/show_data', methods=['GET'])
def show_data():
    if user_logged_in:
        search_query = request.args.get('search', '').strip().lower()
        filtered_website1_data = [item for item in website1_data if search_query in item['Product Name'].lower()]
        filtered_website2_data = [item for item in website2_data if search_query in item['Product Name'].lower()]
        return render_template('data.html', website1_data=filtered_website1_data, website2_data=filtered_website2_data)
    else:
        return "Unauthorized. Please log in or sign up."

@app.route('/logout', methods=['POST'])
def logout():
    global user_logged_in
    user_logged_in = False
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
