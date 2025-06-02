import os
import sys
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= CẬP NHẬT CHO MÁY BẠN =================
# Đường dẫn tới file chromedriver.exe (hoặc chromedriver trên macOS/Linux)
CHROME_DRIVER_PATH = r"chromedriver.exe"

# Nếu muốn chạy với profile Chrome đã login sẵn, gán USER_DATA_DIR.
# Nếu không, đặt USER_DATA_DIR = None hoặc comment dòng dưới.
# Ví dụ Windows: r"C:\Users\YourName\AppData\Local\Google\Chrome\User Data"
USER_DATA_DIR = r"C:\chrome-profile\tiktok-persistent"

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

        # comment_like_icon = driver.find_elements(
        #     By.CSS_SELECTOR, "div[data-e2e='comment-like-icon']"
        # )  # comment-like-icon
        # if comment_like_icon:
        #     like_spans.extend(comment_like_icon)

        if not like_spans:
            like_spans = browse_like_icon

        print(f"🔍 Tìm thấy {len(like_spans)} nút Thích.")
        for idx, btn in enumerate(like_spans, start=1):
            try:
                # Lấy phần tử cha (button) từ span nếu cần
                parent_button = btn.find_element(By.XPATH, "./ancestor::button[1]")
                parent_button.click()
                print(f"  ✓ Đã click nút Thích thứ {idx}.")
                time.sleep(0.5)  # đợi TikTok ghi nhận
            except Exception as e:
                print(f"  ⚠ Lỗi khi click nút Thích thứ {idx}: {e}")
    except Exception as e:
        print(f"    ❌ Lỗi khi tìm/nhấn nút Like (Tym):", e)


def next_button(driver, wait):
    # ===========================
    # Tìm tất cả nút "Chuyển tiếp video" rồi click từng cái
    # ===========================
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.action-item"))
        )
        # Tìm tất cả các nút "Next" bằng cách locate <svg> có path giống chuyển video
        next_buttons = driver.find_elements(
            By.XPATH,
            '//svg[path[@d="m24 27.76 13.17-13.17a1 1 0 0 1 1.42 0l2.82 2.82a1 1 0 0 1 0 1.42L25.06 35.18a1.5 1.5 0 0 1-2.12 0L6.59 18.83a1 1 0 0 1 0-1.42L9.4 14.6a1 1 0 0 1 1.42 0L24 27.76Z"]]',
        )
        print(f"🔍 Tìm thấy {len(next_buttons)} nút Chuyển tiếp video.")
        for idx, btn in enumerate(next_buttons, start=1):
            try:
                # Click vào button đầu tiên trong danh sách (chuyển sang video kế)
                btn.click()
                print(f"  → Đã click nút Next thứ {idx}.")
                time.sleep(1)  # đợi video mới load
            except Exception as e:
                print(f"  ⚠ Lỗi khi click nút Next thứ {idx}: {e}")
    except Exception as e:
        print("    ❌ Lỗi khi tìm/nhấn nút Next (Chuyển video):", e)


def press_arrow_down():
    # Thời gian đợi trước khi gửi phím (nếu cần)
    time.sleep(2.5)
    # -------------------------------------
    pyautogui.keyDown("down")  # Nhấn giữ
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


def main():
    # Khởi động WebDriver với cấu hình tối ưu
    driver = setup_driver()

    # Mở rộng cửa sổ trình duyệt để PyAutoGUI click chính xác
    driver.maximize_window()

    # Điều hướng tới TikTok
    driver.get(TIKTOK_URL_EXPLORE)

    # Đợi tạm 3s để đảm bảo JS, CSS, video, popup load xong
    time.sleep(3)

    print("▶ Bắt đầu vòng lặp tự động Like + Next. Nhấn Ctrl+C để dừng.")
    try:
        # Vòng lặp vô hạn: Like rồi Next liên tục
        while True:
            # ========== Tìm và click nút "Like" (Tym) ==========
            like_button(driver)

            # ========== Tìm và click nút "Next" (Chuyển video) ==========
            # next_button(driver, wait)
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
