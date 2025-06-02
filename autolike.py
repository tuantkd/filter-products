from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time

# Replace 'your_email' and 'your_password' with your Facebook credentials
username = input("Mời nhập Tài khoản Facebook: ")
password = input("Mời nhập Mật khẩu Facebook: ")
posts_number = input("Mời nhập số lượng bài viết cần Like: ")
minutes = input("Nhập số phút auto like: ")

# Set up WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
service = Service("chromedriver.exe")  # Replace with the path to your WebDriver

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

# Time end processing
current_time_plus = datetime.now() + timedelta(minutes=int(minutes))
current_time_plus_str = current_time_plus.strftime("%Y-%m-%d %H:%M")

# Scroll and like posts
for _ in range(int(posts_number)):  # Adjust the range for the number of scrolls/likes
    buttons = driver.find_elements(
        By.CLASS_NAME,
        "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz x5ve5x3",
    )
    like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
    if len(like_buttons) > 0:
        try:
            like_buttons[0].click()
            time.sleep(2)  # Wait a bit between likes to mimic human behavior
        except Exception as e:
            print(f"An error occurred: {e}")

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new posts to load

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if time_now == current_time_plus_str:
        # Close the browser
        driver.quit()
    else:
        continue
