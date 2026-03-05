from fastapi import FastAPI, UploadFile, File, Form
from ultralytics import YOLO
import cv2
import numpy as np
from starlette.responses import JSONResponse

# =========================
# Khởi tạo FastAPI
# =========================
app = FastAPI(title="Mask Detection API")

# =========================
# Load model YOLO
# =========================
model = YOLO("best.pt")

print("===== MODEL CLASSES =====")
print(model.names)
print("=========================")


# =========================
# API Detect Mask
# =========================
@app.post("/detect/")
async def detect(
    file: UploadFile = File(...),
    conf: float = Form(0.4)  # nhận confidence từ frontend
):

    try:
        contents = await file.read()
        image = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if image is None:
            return JSONResponse(
                content={"error": "Không đọc được ảnh"},
                status_code=400,
            )

        # =========================
        # Chạy YOLO
        # =========================
        results = model(image, conf=conf)

        detections = []
        mask_count = 0

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = model.names[class_id]

                # Chỉ lấy class mask
                if class_name.lower() == "mask":
                    mask_count += 1
                    detections.append(
                        {
                            "confidence": confidence,
                            "bbox": [x1, y1, x2, y2],
                        }
                    )

        return {
            "mask_detected": mask_count,
            "detections": detections,
        }

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
        )

# Chạy:
# uvicorn app:app --host 0.0.0.0 --port 8051