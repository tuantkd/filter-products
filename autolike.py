from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, datetime

# Replace 'your_email' and 'your_password' with your Facebook credentials
username = input("Mời nhập Tài khoản Facebook: ")
password = input("Mời nhập Mật khẩu Facebook: ")

# Set up WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
service = Service('chromedriver.exe')  # Replace with the path to your WebDriver

driver = webdriver.Chrome(service=service, options=chrome_options)
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
time.sleep(5)

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Scroll and like posts
for _ in range(2):  # Adjust the range for the number of scrolls/likes
    like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
    for button in like_buttons:
        try:
            button.click()
            time.sleep(2)  # Wait a bit between likes to mimic human behavior
        except Exception as e:
            print(f"An error occurred: {e}")

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new posts to load

# Close the browser
driver.quit()
