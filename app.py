from flask import Flask, render_template, request, flash, send_file
import os
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import secrets
from utils import filter_products, handle_excel_xls, handle_excel_xlsx, remove_files_folder, save_file_new

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


@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    url = "https://xiaomicantho.vn/san-pham/page/1/"
    text_key = "content_site"
    results = crawl_website(url, text_key)
    return render_template('index.html', results=results, url=url, text_key=text_key)


@app.route('/upload', methods=['POST'])
def upload():
    remove_files_folder(UPLOAD_FOLDER)
    filestock_path = check_save_file('filestock')
    fileproduct_path = check_save_file('fileproduct')
    
    if filestock_path == None and fileproduct_path == None:
        flash(f'Không tìm thấy file "Stock hàng về ..."', 'error')
        flash(f'Không tìm thấy file "ProducInOutStockDetail"', 'error')
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
