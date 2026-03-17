## Link Youtube: https://youtu.be/kw5MJN73IrM

---- 

# 📌 FACE MASK DETECTION SYSTEM

Hệ thống phát hiện người đeo khẩu trang sử dụng YOLOv8 – FastAPI – Streamlit

---

## 1️⃣ Giới thiệu

Dự án gồm:

* **Backend**: `app.py` (FastAPI – xử lý ảnh và chạy model YOLO)
* **Frontend**: `interface.py` (Streamlit – giao diện người dùng)
* **Model**: `best.pt` (mô hình YOLO đã huấn luyện)

Frontend gửi ảnh lên Backend → Backend chạy YOLO → trả kết quả → Frontend hiển thị ảnh đã detect.

---

## 2️⃣ Yêu cầu hệ thống

* Windows 10 hoặc Windows 11
* Python 3.9 – 3.11
* pip

Kiểm tra Python đã cài:

```bash
python --version
```

---

## 3️⃣ Cài đặt môi trường

### 🔹 Bước 1: Tạo môi trường ảo (khuyến nghị)

Mở Command Prompt tại thư mục project:

```bash
python -m venv venv
```

Kích hoạt môi trường:

```bash
venv\Scripts\activate
```

Nếu thành công sẽ thấy `(venv)` phía trước dòng lệnh.

---

### 🔹 Bước 2: Cài đặt các thư viện cần thiết

Cài từng thư viện:

```bash
pip install fastapi
pip install uvicorn
pip install ultralytics
pip install streamlit
pip install requests
pip install opencv-python
pip install numpy
pip install pillow
pip install python-multipart
```

Hoặc cài một lần:

```bash
pip install fastapi uvicorn ultralytics streamlit requests opencv-python numpy pillow python-multipart
```

---

## 4️⃣ Cấu trúc thư mục

```
project/
│
├── app.py
├── interface.py
├── best.pt
```

Lưu ý: `best.pt` phải cùng thư mục với `app.py`.

---

## 5️⃣ Chạy Backend (FastAPI)

Mở Command Prompt tại thư mục chứa `app.py`, chạy:

```bash
uvicorn app:app --host 0.0.0.0 --port 8051
```

Nếu thành công sẽ hiển thị:

```
Uvicorn running on http://0.0.0.0:8051
```

Backend đang hoạt động tại:

```
http://localhost:8051
```

⚠ Không được tắt cửa sổ này khi đang chạy hệ thống.

---

## 6️⃣ Chạy Frontend (Streamlit)

Mở Command Prompt mới (giữ backend đang chạy) và chạy or chạy trược tiếp trên cửa sổ terminal của pycham:

```bash
streamlit run interface.py
```

Sau khi chạy, trình duyệt sẽ tự mở tại:

```
http://localhost:8501
```

---

## 7️⃣ Cách sử dụng hệ thống

1. Chạy backend trước.
2. Chạy frontend.
3. Upload ảnh.
4. Chọn ngưỡng tin cậy (Confidence).
5. Nhấn **Bắt đầu nhận dạng**.
6. Hệ thống hiển thị:

   * Ảnh đã detect
   * Số người đeo khẩu trang
   * Confidence của từng đối tượng

---

## 8️⃣ Lỗi thường gặp và cách xử lý

### 🔹 Không kết nối được Backend

* Kiểm tra backend đã chạy chưa.
* Kiểm tra đúng port `8051`.

### 🔹 Lỗi không tìm thấy model

* Đảm bảo file `best.pt` nằm cùng thư mục với `app.py`.

### 🔹 Port bị chiếm

Đổi port backend:

```bash
uvicorn app:app --port 8000
```

Sau đó sửa trong `interface.py`:

```
http://localhost:8000/detect/
```

---

## 9️⃣ Ghi chú

* Backend phải chạy trước frontend.
* Hệ thống hiện hỗ trợ phát hiện trên ảnh tĩnh.
* Có thể mở rộng để xử lý video hoặc camera realtime trong tương lai.

---

## 👨‍💻 Thông tin đề tài

Hệ thống phát hiện người đeo khẩu trang trong ảnh sử dụng YOLOv8
Triển khai bằng FastAPI và Streamlit trên Windows.


