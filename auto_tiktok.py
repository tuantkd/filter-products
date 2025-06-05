import os
import sys
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

# ================= CẬP NHẬT CHO MÁY BẠN =================
# Đường dẫn tới file chromedriver.exe (hoặc chromedriver trên macOS/Linux)
CHROME_DRIVER_PATH = r"chromedriver.exe"

# Nếu muốn chạy với profile Chrome đã login sẵn, gán USER_DATA_DIR.
# Nếu không, đặt USER_DATA_DIR = None hoặc comment dòng dưới.
# Ví dụ Windows: r"C:\Users\YourName\AppData\Local\Google\Chrome\User Data"
# USER_DATA_DIR = r"C:\chrome-profile\tiktok-persistent"
USER_DATA_DIR = r"C:\chrome-profile\tiktok-nhanha1007"

# Đường dẫn TikTok đã login
TIKTOK_URL = "https://www.tiktok.com/"
TIKTOK_URL_EXPLORE = "https://www.tiktok.com/explore"
# =====================================================


def setup_driver(
    chrome_driver_path: str = CHROME_DRIVER_PATH,
    user_data_dir: str = USER_DATA_DIR,
    window_position: tuple[int, int] = (0, 0),
    window_size: tuple[int, int] = (1300, 850),
    device_scale_factor: float = 0.9,
) -> webdriver.Chrome:
    """
    Khởi tạo và trả về một instance của Chrome WebDriver với cấu hình tối ưu:
      - Sử dụng profile đã login (nếu user_data_dir không None và tồn tại).
      - Thiết lập DPI và tỉ lệ hiển thị để PyAutoGUI thao tác chính xác.
      - Cố định vị trí và kích thước cửa sổ.
      - Tắt thông báo.
    """
    options = Options()

    # Nếu thư mục profile tồn tại, thêm để Chrome load profile đã login
    if user_data_dir and os.path.isdir(user_data_dir):
        options.add_argument(f"--user-data-dir={user_data_dir}")

    # Thiết lập DPI scaling cho màn hình độ phân giải cao
    options.add_argument("--high-dpi-support=1")
    options.add_argument(f"--force-device-scale-factor={device_scale_factor}")

    # Cố định vị trí và kích thước cửa sổ để PyAutoGUI thao tác chính xác
    xpos, ypos = window_position
    width, height = window_size
    options.add_argument(f"--window-position={xpos},{ypos}")
    options.add_argument(f"--window-size={width},{height}")

    # Tắt popup/notification
    options.add_argument("--disable-notifications")

    # Khởi tạo ChromeDriver
    try:
        service = ChromeService(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print("❌ Lỗi khi khởi tạo ChromeDriver. Vui lòng kiểm tra:")
        print("   1) CHROME_DRIVER_PATH có đúng không?")
        print("   2) ChromeDriver có khớp với phiên bản Chrome đang dùng không?")
        print("   3) USER_DATA_DIR có tồn tại và hợp lệ không?")
        print("Chi tiết lỗi:", e)
        sys.exit(1)

    return driver


def like_button(driver):
    # ===========================
    # 1. Tìm tất cả nút "Thích" rồi click từng cái
    # ===========================
    try:
        like_spans = driver.find_elements(
            By.CSS_SELECTOR, "span[data-e2e='like-icon']"
        )  # like-icon
        browse_like_icon = driver.find_elements(
            By.CSS_SELECTOR, "span[data-e2e='browse-like-icon']"
        )  # browse-like-icon
        if not like_spans:
            like_spans = browse_like_icon

        print(f"🔍 Tìm thấy {len(like_spans)} nút Thích.")
        for idx, btn in enumerate(like_spans, start=1):
            try:
                # Lấy phần tử cha (button) từ span nếu cần
                parent_button = btn.find_element(By.XPATH, "./ancestor::button[1]")
                parent_button.click()
                print(f"  ✓ Đã click nút Thích thứ {idx}.")
                time.sleep(1)  # đợi TikTok ghi nhận
            except Exception as e:
                print(f"  ⚠ Lỗi khi click nút Thích thứ {idx}: {e}")
    except Exception as e:
        print(f"    ❌ Lỗi khi tìm/nhấn nút Like (Tym):", e)


def click_undefined_button(driver):
    """
    Tìm tất cả <span> có attribute data-e2e="undefined-icon", sau đó click vào nút <button> cha chứa nó.
    """
    try:
        # XPath tìm tất cả span có data-e2e="undefined-icon"
        span_elements = driver.find_elements(
            By.CSS_SELECTOR, "span[data-e2e='undefined-icon']"
        )  # undefined-icon
        print(f"🔍 Tìm thấy {len(span_elements)} nút thêm vào mục yêu thích")

        for idx, span in enumerate(span_elements, start=1):
            try:
                # Lấy nút button cha gần nhất
                button = span.find_element(By.XPATH, "./ancestor::button[1]")

                # Scroll button vào giữa màn hình
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                time.sleep(0.5)

                # Click button
                button.click()
                print(f"  ✓ Đã click button thứ {idx} nút mục yêu thích")
                time.sleep(1)
            except Exception as e:
                print(f"  ⚠ Lỗi khi click button thứ {idx}: {e}")
    except Exception as e:
        print(f"  ⚠ Lỗi khi tìm nút thêm vào mục yêu thích")


def click_all_follow_buttons(driver):
    """
    Tìm tất cả các nút Follow bên trong div có data-e2e="browse-follow"
    rồi click từng nút.
    """
    # Tìm tất cả các div chứa nút Follow theo attribute data-e2e
    try:
        follow_wrappers = driver.find_elements(
            By.CSS_SELECTOR, 'div[data-e2e="browse-follow"]'
        )
        print(f"🔍 Tìm thấy {len(follow_wrappers)} phần tử chứa nút Follow.")
        for idx, wrapper in enumerate(follow_wrappers, start=1):
            try:
                # Tìm button con bên trong wrapper
                follow_button = wrapper.find_element(By.TAG_NAME, "button")

                # Scroll button vào giữa màn hình để đảm bảo click chính xác
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", follow_button
                )
                time.sleep(0.5)

                # Click nút Follow
                follow_button.click()
                print(f"  ✓ Đã click nút Follow thứ {idx}.")
                time.sleep(1)  # Đợi trang xử lý click
            except Exception as e:
                print(f"  ⚠ Lỗi khi click nút Follow thứ {idx}: {e}")
    except Exception as e:
        print(f"  ⚠ Lỗi khi tìm nút theo dõi (Follow)")


def click_all_comment_like_icons(driver):
    """
    Tìm tất cả các div có attribute data-e2e="comment-like-icon" rồi click từng cái.
    """
    try:
        # Tìm tất cả phần tử div có data-e2e="comment-like-icon"
        like_icons = driver.find_elements(
            By.CSS_SELECTOR, 'div[data-e2e="comment-like-icon"]'
        )
        print(f"🔍 Tìm thấy {len(like_icons)} icon 'comment-like'.")

        for idx, icon in enumerate(like_icons, start=1):
            try:
                # CLick đến nút thích bình luận thứ 8 thì dừng lại
                if idx == 5:
                    break

                # Scroll icon vào giữa màn hình để chắc chắn nó hiển thị
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", icon
                )
                time.sleep(0.5)  # Đợi animation scroll

                # Click vào icon (div)
                icon.click()
                print(f"  ✓ Đã click icon 'comment-like' thứ {idx}.")
                time.sleep(1)  # Đợi trang ghi nhận click
            except Exception as e:
                print(f"  ⚠ Lỗi khi click icon thứ {idx}: {e}")
    except Exception as e:
        print(f"  ⚠ Lỗi khi tìm nút thích bình luận")


def press_arrow_down():
    # Thời gian đợi trước khi gửi phím (nếu cần)
    time.sleep(2.5)
    # -------------------------------------
    pyautogui.keyDown("down")  # Nhấn giữ
    pyautogui.keyDown("down")  # Nhấn giữ
    pyautogui.keyUp('down')   # Thả phím
    # -------------------------------------

    # -------------------------------------
    # pyautogui.keyDown('down') # Nhấn giữ
    # pyautogui.keyDown('down') # Nhấn giữ
    # time.sleep(0.2)            # Giữ key
    # pyautogui.keyUp('down')   # Thả phím

    # pyautogui.keyDown('down') # Nhấn giữ
    # pyautogui.keyDown('down') # Nhấn giữ
    # pyautogui.keyDown('down') # Nhấn giữ
    # time.sleep(0.2)           # Giữ key
    # pyautogui.keyUp('down')   # Thả phím
    # -------------------------------------


def type_comment_with_pyautogui_and_post(driver, comment_text="Great video!"):
    """
    1. Tìm ô nhập comment (div contenteditable).
    2. Click vào để focus, dùng pyautogui gõ comment_text.
    3. Chờ nút Đăng chuyển từ aria-disabled="true" sang "false".
    4. Click nút Đăng để gửi.
    """
    try:
        # 1. Tìm ô nhập comment (contenteditable div)
        editable_divs = driver.find_elements(
            By.CSS_SELECTOR, 'div[contenteditable="true"][role="textbox"]'
        )
        if not editable_divs:
            print("❌ Không tìm thấy ô nhập comment.")
        input_div = editable_divs[0]

        # Scroll đến input_div và click để focus
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", input_div
        )
        time.sleep(0.5)
        input_div.click()
        time.sleep(0.5)  # đợi focus ổn định

        #------------------------------
        # 2. Xóa nội dung cũ (nếu có)
        input_div.send_keys(Keys.CONTROL, 'a')  # Ctrl+A chọn tất cả (macOS dùng Keys.COMMAND)
        time.sleep(0.1)
        input_div.send_keys(Keys.BACKSPACE)     # Xóa

        # 3. Gửi comment mới bằng send_keys
        input_div.send_keys(comment_text)
        time.sleep(0.5)
        #------------------------------
        #------------------------------
        # 2. Xóa nội dung cũ (nếu có)
        input_div.send_keys(Keys.CONTROL, 'a')  # Ctrl+A chọn tất cả (macOS dùng Keys.COMMAND)
        time.sleep(0.1)
        input_div.send_keys(Keys.BACKSPACE)     # Xóa

        # 3. Gửi comment mới bằng send_keys
        input_div.send_keys(comment_text)
        time.sleep(0.5)
        #------------------------------

        # 3. Tìm nút Đăng
        post_buttons = driver.find_elements(
            By.CSS_SELECTOR, "div[data-e2e='comment-post']"
        )
        if not post_buttons:
            print("❌ Không tìm thấy nút Đăng.")
        post_button = post_buttons[0]

        # 4. Chờ nút Đăng enabled (aria-disabled="false")
        timeout = 5  # giây
        poll_interval = 0.5
        elapsed = 0
        while elapsed < timeout:
            aria_disabled = post_button.get_attribute("aria-disabled")
            if aria_disabled == "false":
                # Scroll và click nút Đăng
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", post_button
                )
                time.sleep(0.3)
                post_button.click()
                print("✓ Đã gửi bình luận.")
            time.sleep(poll_interval)
            elapsed += poll_interval
        print("⚠ Nút Đăng không được bật trong thời gian chờ.")
    except Exception as e:
        print("    ❌ Lỗi khi tìm/nhấn nút Next (Chuyển video):", e)


def main():
    # Khởi động WebDriver với cấu hình tối ưu
    driver = setup_driver()

    # Mở rộng cửa sổ trình duyệt để PyAutoGUI click chính xác
    driver.maximize_window()

    # Điều hướng tới TikTok
    driver.get(TIKTOK_URL_EXPLORE)

    # Đợi tạm 5s để đảm bảo JS, CSS, video, popup load xong
    time.sleep(5)

    print("▶ Bắt đầu vòng lặp tự động Like + Next. Nhấn Ctrl+C để dừng.")
    try:
        # Vòng lặp vô hạn: Like rồi Next liên tục
        while True:
            # ========== Dùng pyautogui xử lý phím mũi tên xuống để chyển tiếp video ==========
            press_arrow_down()

            # ========== Tìm và click nút "Follow" (Theo dõi)==========
            click_all_follow_buttons(driver)

            # ========== Tìm và click nút "Like" (Tym) ==========
            like_button(driver)

            # ========== Tìm và click nút "Undefined" (Mục yêu thích) ==========
            click_undefined_button(driver)

            # ========== Tìm và nhập text nhấn nút gửi bình luận ==========
            type_comment_with_pyautogui_and_post(driver)

            # ========== Tìm và click nút "Comment Like" (Tym) ==========
            click_all_comment_like_icons(driver)

            # ========== Dùng pyautogui xử lý phím mũi tên xuống để chyển tiếp video ==========
            press_arrow_down()
    except KeyboardInterrupt:
        # Khi người dùng nhấn Ctrl+C, sẽ bắt vào đây để dọn dẹp
        print("\n■ Nhận lệnh dừng từ người dùng, chương trình sẽ đóng trình duyệt.")
    finally:
        # Đảm bảo driver.quit() luôn được gọi dù có lỗi hay không
        driver.quit()
        print("■ Trình duyệt đã đóng. Kết thúc chương trình.")


if __name__ == "__main__":
    main()
