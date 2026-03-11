# Import thư viện Streamlit để tạo giao diện web
import streamlit as st

# Thư viện gửi request HTTP để gọi API backend
import requests

# Thư viện xử lý ảnh OpenCV
import cv2

# Thư viện xử lý mảng số
import numpy as np

# Thư viện xử lý ảnh PIL
from PIL import Image


# =========================
# Cấu hình giao diện
# =========================

# Thiết lập cấu hình trang Streamlit
st.set_page_config(
    page_title="Mask Detection System",  # tiêu đề tab trình duyệt
    layout="wide"                        # giao diện rộng toàn màn hình
)

# Tiêu đề chính của hệ thống
st.title("😷 Hệ thống Phát hiện Người Đeo Khẩu Trang")


# =========================
# Sidebar cấu hình
# =========================

# Tạo tiêu đề phần sidebar
st.sidebar.header("Cấu hình")

# Thanh trượt để chọn ngưỡng confidence
conf_threshold = st.sidebar.slider(
    "Ngưỡng tin cậy (Confidence)",  # tên slider
    0.1,                            # giá trị nhỏ nhất
    1.0,                            # giá trị lớn nhất
    0.4                             # giá trị mặc định
)


# =========================
# Upload ảnh
# =========================

# Tạo nút upload ảnh
uploaded_file = st.file_uploader(
    "Chọn ảnh để kiểm tra...",   # nội dung hiển thị
    type=["jpg", "jpeg", "png"]  # chỉ cho phép các định dạng ảnh
)


# Nếu người dùng đã upload ảnh
if uploaded_file is not None:

    # Mở ảnh bằng thư viện PIL
    image = Image.open(uploaded_file)

    # Hiển thị ảnh gốc lên giao diện
    st.image(
        image,
        caption="Ảnh gốc",
        width=400
    )


    # =========================
    # Nút bắt đầu nhận dạng
    # =========================

    # Khi người dùng bấm nút
    if st.button("Bắt đầu nhận dạng"):

        # Đưa con trỏ file về đầu để đọc lại
        uploaded_file.seek(0)

        # Chuẩn bị dữ liệu gửi sang API
        files = {
            "file": (
                uploaded_file.name,  # tên file
                uploaded_file,       # dữ liệu file
                uploaded_file.type   # kiểu file
            )
        }


        # Hiển thị biểu tượng loading
        with st.spinner("Đang xử lý..."):

            try:

                # =========================
                # Gửi request đến API
                # =========================

                response = requests.post(
                    "http://localhost:8051/detect/",  # địa chỉ API backend
                    files=files,                      # gửi file ảnh
                    data={"conf": conf_threshold}     # gửi ngưỡng confidence
                )


                # Nếu backend trả về lỗi
                if response.status_code != 200:

                    # Hiển thị lỗi trên giao diện
                    st.error("Backend lỗi!")

                    # Dừng chương trình
                    st.stop()


                # Chuyển kết quả JSON thành dictionary
                data = response.json()


                # =========================
                # Xử lý ảnh để vẽ bounding box
                # =========================

                # Chuyển ảnh PIL sang numpy array
                img_array = np.array(image)

                # Chuyển màu RGB sang BGR cho OpenCV
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                # Biến đếm số người đeo khẩu trang
                mask_count = 0


                # Duyệt qua từng detection trả về từ API
                for det in data["detections"]:

                    # Lấy tọa độ bounding box
                    x1, y1, x2, y2 = det["bbox"]

                    # Lấy độ tin cậy
                    conf = det["confidence"]

                    # Tăng số lượng mask
                    mask_count += 1

                    # Tạo nhãn hiển thị
                    label = f"Mask {conf:.2f}"


                    # Vẽ khung chữ nhật quanh đối tượng
                    cv2.rectangle(
                        img_cv,
                        (x1, y1),     # góc trên trái
                        (x2, y2),     # góc dưới phải
                        (0, 255, 0),  # màu xanh
                        3             # độ dày khung
                    )


                    # Vẽ chữ lên ảnh
                    cv2.putText(
                        img_cv,
                        label,                     # nội dung chữ
                        (x1, y1 - 10),             # vị trí chữ
                        cv2.FONT_HERSHEY_SIMPLEX,  # font chữ
                        0.8,                       # kích thước chữ
                        (0, 255, 0),               # màu chữ
                        2                          # độ dày chữ
                    )


                # =========================
                # Hiển thị kết quả
                # =========================

                # Chuyển ảnh từ BGR về RGB để hiển thị
                result_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

                # Hiển thị ảnh kết quả
                st.image(
                    result_img,
                    caption="Kết quả",
                    width=600
                )


                # Hiển thị thông báo hoàn tất
                st.success("Hoàn tất!")

                # Hiển thị số lượng người đeo khẩu trang
                st.metric(
                    "😷 Số người đeo khẩu trang",
                    mask_count
                )


                # Nếu không phát hiện khẩu trang
                if mask_count == 0:
                    st.warning(
                        "Không phát hiện người đeo khẩu trang!"
                    )


            # Nếu lỗi kết nối backend
            except Exception as e:

                # Hiển thị lỗi
                st.error(f"Lỗi kết nối Backend: {e}")


# =========================
# Lệnh chạy chương trình
# =========================

# Chạy giao diện bằng lệnh:
# streamlit run interface.py