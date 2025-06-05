import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ================= CẬP NHẬT CHO MÁY BẠN =================
CHROME_DRIVER_PATH = r"chromedriver.exe"
# Nếu bạn muốn chạy với profile đã login sẵn, giữ dòng USER_DATA_DIR.
# Nếu không cần, hoặc muốn Chrome khởi "fresh", comment dòng dưới đi.
USER_DATA_DIR = r"C:\chrome-profile\fb-persistent"
# =====================================================


def setup_driver():
    options = webdriver.ChromeOptions()
    # --- nếu bạn đã login Facebook trong một Chrome profile riêng ---
    options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    # Ép Chrome hiển thị ở tỉ lệ 90%
    options.add_argument("--high-dpi-support=1")
    options.add_argument("--force-device-scale-factor=0.9")
    # Cố định vị trí/kích thước cửa sổ để PyAutoGUI gõ chính xác
    options.add_argument("--window-position=0,0")
    options.add_argument("--window-size=1300,850")
    # Tắt thông báo Facebook
    options.add_argument("--disable-notifications")
    service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def close_modal_comment(driver):
    # ================== 3. CUỘN XUỐNG LOAD BÀI MỚI ==================
    print("[INFO] Cuộn xuống để load thêm bài.")
    driver.execute_script("window.scrollBy(0, 900);")
    time.sleep(1)

    # Sau khi comment xong, tìm nút Đóng và click
    try:
        # Nút Đóng có aria-label="Đóng", nên ta đợi nó xuất hiện và có thể click
        close_btns = driver.find_elements(
            By.XPATH,
            "//div[@aria-label='Đóng' and @role='button']",
        )
        print(f"    ✅ Đã tìm được {len(close_btns)} nút Đóng")
    except Exception as e:
        print(f"    ❌ Không tìm thấy được nút Đóng: {e}")

    if len(close_btns) > 0:
        for idx, btn in enumerate(close_btns, start=1):
            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    btn,
                )
                time.sleep(0.3)
                btn.click()
                print(f"    ✅ Đã click nút Đóng để tắt popup bình luận {idx}")
                time.sleep(0.5)
            except Exception as e:
                print(f"    ❌ Lỗi xử lý click nút Đóng: {e}")


def like_button(driver):
    try:
        # Lấy danh sách tất cả <div aria-label='Thích'> đang hiển thị
        like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
        print(f"    ✅ Tìm được {len(like_buttons)} nút Thích trong viewport.")
    except Exception as e:
        print(f"    ❌ Không tìm được nút Thích trong viewport: {e}")

    for idx, btn in enumerate(like_buttons, start=1):
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", btn
            )
            time.sleep(0.3)
            btn.click()
            print(f"  {idx}. ✅ Đã click Thích")
            time.sleep(0.5)
        except Exception as e:
            print(f"  {idx}. ❌ Lỗi khi click Thích: {e}")


def comment_box(driver):
    try:
        # Lấy danh sách tất cả <div aria-label='Bình luận dưới tên'> đang hiển thị
        comment_boxs = driver.find_elements(
            By.XPATH,
            "//div[@contenteditable='true' and contains(@aria-label, 'Bình luận dưới tên')]",
        )
        print(f"    ✅ Đã tìm thấy {len(comment_boxs)} ô comment")
    except Exception as e:
        print(f"    ❌ Không tìm được ô nhập bình luận: {e}")

    for idx, comment in enumerate(comment_boxs, start=1):
        try:
            # --- Đưa ô nhập vào giữa viewport để Selenium click chính xác ---
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                comment,
            )

            # --- Click để focus vào ô nhập và gõ chữ ---
            comment.click()
            time.sleep(0.5)  # chờ focus thực sự vào ô

            # --- Xóa nội dung cũ (nếu có) và gõ mới ---
            # Thông thường <div contenteditable> đã trống, nhưng nếu có sẵn <p><br> hoặc text cũ, ta có thể clear:
            comment.clear()
            print(f"  {idx}. ✅ Đã clear ô comment cũ")

            # --- Dùng send_keys để gõ nội dung mới ---
            comment.send_keys("Xin chào!!!")
            print(f"  {idx}. ✅ Đã nhập nội dung text")
            time.sleep(0.3)

            # --- Nhấn Enter để gửi bình luận ---
            comment.send_keys(Keys.ENTER)
            time.sleep(4)

            break
        except Exception as e:
            print(f"    ❌ Không tìm thấy ô comment: {e}")


def comment_button(driver):
    try:
        # Lấy lại danh sách mỗi lần vì DOM có thể thay đổi sau khi đã click Thích
        comment_buttons = driver.find_elements(
            By.XPATH, "//div[@aria-label='Viết bình luận']"
        )
        print(f"   ✅ Tìm được {len(comment_buttons)} nút Bình luận trong viewport.")
    except Exception as e:
        print(f"   ❌ Lỗi không tìm thấy nút Bình luận: {e}")

    for idx, btn in enumerate(comment_buttons, start=1):
        try:
            # --- Scroll sao cho nút nằm giữa màn hình ---
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", btn
            )
            time.sleep(0.3)
            btn.click()
            print(f"  {idx}. ✅ Đã click Bình luận nút")
            time.sleep(0.5)

            # --- Gọi hàm bình luận nhập ô textbox ---
            comment_box(driver)

            # --- Gọi hàm đóng popup bình luận ---
            close_modal_comment(driver)

            break
        except Exception as e:
            print(f"  {idx}. ❌ Lỗi khi xử lý nút Bình luận: {e}")


def main_loop():
    driver = setup_driver()
    # Mở Facebook và chờ Feed load
    driver.get("https://www.facebook.com/?filter=all&sk=h_chr")
    print("[INFO] Đã vào News Feed.")

    try:
        while True:
            # --- Gọi hàm đóng popup bình luận ---
            close_modal_comment(driver)

            # ================== 1. NHẤP TẤT CẢ CÁC NÚT "Thích" ==================
            # Lấy danh sách tất cả <div aria-label='Thích'> đang hiển thị
            like_button(driver)

            # ================== 2. NHẤP TẤT CẢ CÁC NÚT "Bình luận" ==================
            comment_button(driver)

            # --- Gọi hàm đóng popup bình luận ---
            close_modal_comment(driver)
    except KeyboardInterrupt:
        print("\n[INFO] Người dùng đã dừng chương trình.")
    finally:
        driver.quit()
        print("[INFO] Đóng trình duyệt xong, kết thúc.")


if __name__ == "__main__":
    main_loop()
