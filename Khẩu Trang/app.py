# Import thư viện FastAPI để tạo API
from fastapi import FastAPI, UploadFile, File, Form

# Import YOLO từ thư viện ultralytics để dùng mô hình nhận diện
from ultralytics import YOLO

# Thư viện xử lý ảnh OpenCV
import cv2

# Thư viện xử lý mảng số học
import numpy as np

# Trả về dữ liệu dạng JSON khi có lỗi
from starlette.responses import JSONResponse


# =========================
# Khởi tạo FastAPI
# =========================

# Tạo một ứng dụng FastAPI với tên hiển thị là "Mask Detection API"
app = FastAPI(title="Mask Detection API")


# =========================
# Load model YOLO
# =========================

# Load mô hình YOLO đã huấn luyện từ file best.pt
model = YOLO("best.pt")


# In ra danh sách các lớp (classes) mà model nhận diện được
print("===== MODEL CLASSES =====")
print(model.names)

# In dòng phân cách
print("=========================")


# =========================
# API Detect Mask
# =========================

# Tạo API dạng POST tại đường dẫn /detect/
@app.post("/detect/")
async def detect(

    # Nhận file ảnh upload từ người dùng
    file: UploadFile = File(...),

    # Nhận tham số confidence từ frontend (mặc định = 0.4)
    conf: float = Form(0.4)
):

    try:

        # Đọc toàn bộ dữ liệu của file ảnh
        contents = await file.read()

        # Chuyển dữ liệu ảnh thành mảng numpy
        image = np.frombuffer(contents, np.uint8)

        # Decode ảnh từ dạng buffer sang ảnh OpenCV
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Kiểm tra nếu ảnh không đọc được
        if image is None:
            return JSONResponse(
                content={"error": "Không đọc được ảnh"},  # thông báo lỗi
                status_code=400,  # mã lỗi HTTP
            )

        # =========================
        # Chạy YOLO
        # =========================

        # Cho mô hình YOLO dự đoán trên ảnh với ngưỡng confidence
        results = model(image, conf=conf)

        # Danh sách lưu các đối tượng phát hiện được
        detections = []

        # Biến đếm số người đeo khẩu trang
        mask_count = 0


        # Duyệt qua kết quả dự đoán
        for r in results:

            # Duyệt qua từng bounding box trong kết quả
            for box in r.boxes:

                # Lấy tọa độ bounding box (x1,y1,x2,y2)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Lấy ID của class
                class_id = int(box.cls[0])

                # Lấy độ tin cậy (confidence)
                confidence = float(box.conf[0])

                # Lấy tên class từ model
                class_name = model.names[class_id]


                # Chỉ lấy những object có class là "mask"
                if class_name.lower() == "mask":

                    # Tăng số lượng người đeo khẩu trang
                    mask_count += 1

                    # Lưu thông tin detection
                    detections.append(
                        {
                            "confidence": confidence,  # độ tin cậy
                            "bbox": [x1, y1, x2, y2],  # tọa độ bounding box
                        }
                    )


        # Trả kết quả về frontend
        return {
            "mask_detected": mask_count,  # tổng số người đeo khẩu trang
            "detections": detections,     # danh sách các detection
        }


    # Nếu có lỗi xảy ra trong quá trình xử lý
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},  # thông báo lỗi
            status_code=500,            # mã lỗi server
        )


# =========================
# Lệnh chạy server
# =========================

# Chạy server bằng lệnh:
# uvicorn app:app --host 0.0.0.0 --port 8051