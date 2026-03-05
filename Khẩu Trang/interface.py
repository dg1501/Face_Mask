import streamlit as st
import requests
import cv2
import numpy as np
from PIL import Image

# =========================
# Cấu hình giao diện
# =========================
st.set_page_config(page_title="Mask Detection System", layout="wide")
st.title("😷 Hệ thống Phát hiện Người Đeo Khẩu Trang")

st.sidebar.header("Cấu hình")
conf_threshold = st.sidebar.slider(
    "Ngưỡng tin cậy (Confidence)", 0.1, 1.0, 0.4
)

uploaded_file = st.file_uploader(
    "Chọn ảnh để kiểm tra...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ảnh gốc", width=400)

    if st.button("Bắt đầu nhận dạng"):

        uploaded_file.seek(0)
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        }

        with st.spinner("Đang xử lý..."):
            try:
                response = requests.post(
                    "http://localhost:8051/detect/",
                    files=files,
                    data={"conf": conf_threshold}
                )

                if response.status_code != 200:
                    st.error("Backend lỗi!")
                    st.stop()

                data = response.json()

                img_array = np.array(image)
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                mask_count = 0

                for det in data["detections"]:
                    x1, y1, x2, y2 = det["bbox"]
                    conf = det["confidence"]

                    mask_count += 1

                    label = f"Mask {conf:.2f}"

                    cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(
                        img_cv,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                    )

                result_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

                st.image(result_img, caption="Kết quả", width=600)

                st.success("Hoàn tất!")
                st.metric("😷 Số người đeo khẩu trang", mask_count)

                if mask_count == 0:
                    st.warning("Không phát hiện người đeo khẩu trang!")

            except Exception as e:
                st.error(f"Lỗi kết nối Backend: {e}")

# Chạy:
# streamlit run interface.py