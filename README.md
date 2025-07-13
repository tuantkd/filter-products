# Filter-products and Auto Like Facebook
Link download Chromedriver: https://googlechromelabs.github.io/chrome-for-testing/
```
python -m venv venv
.\venv\Scripts\activate --> for Windows
python -m pip install -r requirements.txt
flask run
```

---

# Hướng dẫn chi tiết để tạo và sử dụng Chrome profile độc lập cho Facebook, kèm theo những lưu ý quan trọng về bảo mật:

### **Các bước thực hiện:**
1. **Tạo thư mục profile**  
   Tạo thư mục mới (ví dụ: `C:\chrome-profile\fb-persistent`) bằng cách:
   - Mở File Explorer
   - Truy cập ổ `C:\`
   - Tạo thư mục `chrome-profile` → Mở nó → Tạo tiếp thư mục con `fb-persistent`

2. **Chạy Chrome với profile riêng**  
   Mở Command Prompt/PowerShell và chạy lệnh:
   ```
   CMD:
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\chrome-profile\fb-persistent"

   Powershell:
   & "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\chrome-profile\tiktok-nhanha1007"
   ```
   *(Lưu ý: Đảm bảo đường dẫn Chrome đúng với phiên bản bạn cài đặt)*

3. **Đăng nhập Facebook**  
   - Chrome sẽ mở ra với **profile trống** (không dữ liệu cũ)
   - Truy cập [facebook.com](https://facebook.com) → Đăng nhập tài khoản
   - Duyệt như bình thường

4. **Đóng Chrome và lưu session**  
   Sau khi đóng Chrome, toàn bộ dữ liệu (session, cookies, cache) sẽ được lưu vào:
   ```
   C:\chrome-profile\fb-persistent
   ```

---

### **Cách sử dụng lại profile:**
- Mỗi lần cần truy cập Facebook bằng profile này, chỉ cần chạy lại lệnh trên
- Session sẽ được giữ nguyên kể cả khi update Chrome hoặc khởi động lại máy

---

### **Tạo Shortcut tiện dụng (khuyến nghị):**
1. Chuột phải lên Desktop → New → Shortcut
2. Dán nội dung sau vào ô location:
   ```cmd
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\chrome-profile\fb-persistent" --profile-directory="FB-Session"
   ```
3. Đặt tên: `Facebook Profile` → Finish
4. (Tùy chọn) Chuột phải shortcut → Properties → Change Icon → Chọn icon Facebook

---

### ⚠️ **Cảnh báo bảo mật QUAN TRỌNG:**
1. **Ai truy cập được thư mục `fb-persistent` có thể chiếm quyền tài khoản FB của bạn**  
   → Cần bảo vệ thư mục bằng:
   - **Mã hóa thư mục** (BitLocker hoặc VeraCrypt)
   - **Đặt quyền truy cập** (Chuột phải thư mục → Properties → Security → Chỉ cho phép user hiện tại)

2. **Không chia sẻ/sao chép thư mục profile** sang máy khác vì:
   - Facebook tự động phát hiện đăng nhập bất thường → Khóa tài khoản
   - Nguy cơ lộ session nếu máy khác không an toàn

3. **Luôn sử dụng mật khẩu máy tính**  
   Đảm bảo máy tính có password login để ngăn người khác truy cập profile Chrome.

---

### **Tại sao nên dùng cách này?**
| Ưu điểm | Nhược điểm |
|---------|------------|
| ☑️ Tách biệt hoàn toàn với profile Chrome chính | ❌ Chiếm dung lượng ổ cứng (~100-500MB) |
| ☑️ Tránh lẫn lộn cookies với tài khoản khác | ❌ Phải dùng shortcut/lệnh để khởi động |
| ☑️ Dễ sao lưu/xóa session (chỉ cần xóa thư mục) | ❌ Không đồng bộ dữ liệu với Google Account |

---

### **Nâng cao: Tạo batch file tự động**
Tạo file `open-fb.bat` với nội dung:
```batch
@echo off
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\chrome-profile\fb-persistent" --new-window "https://facebook.com"
```
→ Nhấp đúp để mở Chrome thẳng đến Facebook với profile riêng.

---