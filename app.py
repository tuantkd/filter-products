from flask import Flask, render_template, request, flash
import os
import time
import requests
import secrets
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
from utils import filter_products, handle_excel_xls, handle_excel_xlsx, remove_files_folder, save_file_new
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
app.secret_key = secrets.token_hex(16)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def check_save_file(input_name):
    file = request.files[input_name]
    if file.filename == '':
        return None
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path


def crawl_website(url, parent_class):
    try:
        # Fetch HTML content from the URL
        response = requests.get(url)
        if response.status_code == 200:
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the parent element with the specified class
            parent_element = soup.find('div', class_=parent_class)

            # Find all 'a' tags within the parent
            if parent_element:
                links = parent_element.find_all('a', href=True)

                # Extract text, href, and other attributes from each 'a' tag
                results = []
                for link in links:
                    text = link.get_text(strip=True)
                    href = link['href']
                    # Add more attributes as needed
                    results.append({'text': text, 'href': href})

                return results
            else:
                return None
        else:
            return None
    except Exception as e:
        return str(e)

def login_facebook(username, password, driver):
    driver.maximize_window()
    
    # Open Facebook
    driver.get("https://www.facebook.com")
    
    # Log in
    time.sleep(2)  # Wait for the page to load
    email_element = driver.find_element(By.ID, "email")
    email_element.send_keys(username)
    password_element = driver.find_element(By.ID, "pass")
    password_element.send_keys(password)
    password_element.send_keys(Keys.RETURN)

    # Wait for login to complete
    time.sleep(3)
    
def scroll_like_posts(driver, posts_number, minutes):
    # Time end processing
    current_time_plus = datetime.now() + timedelta(minutes = int(minutes))
    current_time_plus_str = current_time_plus.strftime('%Y-%m-%d %H:%M')
        
    # Scroll and like posts
    for _ in range(int(posts_number)):  
        # Adjust the range for the number of scrolls/likes
        like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
        for index, button in enumerate(like_buttons):
            print(index, button)
            if index <= 1:
                try:
                    button.click()
                    time.sleep(2)  # Wait a bit between likes to mimic human behavior
                except Exception as e:
                    print(f"An error occurred: {e}")

        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new posts to load
        
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(time_now, current_time_plus_str)
        if time_now == current_time_plus_str:
            # Close the browser
            driver.quit()
            break
        else:
            continue

    
@app.route('/auto-like')
def autolike():
    return render_template('autolike.html')

@app.route('/autolike', methods=['GET', 'POST'])
def auto():
    if request.method == 'POST':
        # Get data from form
        username = request.form['username']
        password = request.form['password']
        posts_number = request.form['posts']
        minutes = request.form['minutes']

        # Set up WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        service = Service('chromedriver.exe')  # Replace with the path to your WebDriver

        driver = webdriver.Chrome(service=service, options=chrome_options)
        login_facebook(username, password, driver)
        scroll_like_posts(driver, posts_number, minutes)
    
    flash('Kết thúc quá trình Auto Liked Facebook', 'error')
    return render_template('autolike.html')


@app.route('/upload', methods=['POST'])
def upload():
    remove_files_folder(UPLOAD_FOLDER)
    filestock_path = check_save_file('filestock')
    fileproduct_path = check_save_file('fileproduct')
    
    if filestock_path == None and fileproduct_path == None:
        flash('Không tìm thấy file "Stock hàng về ..."', 'error')
        flash('Không tìm thấy file "ProducInOutStockDetail"', 'error')
        return render_template('index.html')
    else: 
        data_stocks = handle_excel_xlsx(filestock_path)
        data_products = handle_excel_xls(fileproduct_path)
        product_filtered = filter_products(data_stocks, data_products)
        save_file_new(product_filtered['product_filters'])
    return render_template('products.html', products=product_filtered)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
