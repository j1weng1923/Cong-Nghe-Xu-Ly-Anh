## Điểm danh bằng khuôn mặt sử dụng YOLOv8m-face

Hệ thống điểm danh tự động dựa trên nhận dạng khuôn mặt sử dụng mô hình YOLOv8m-face, một phiên bản YOLOv8 được tối ưu riêng cho nhận diện khuôn mặt với độ chính xác và tốc độ cao.

### Các bước chính:

1. **Phát hiện khuôn mặt (Face Detection):**  
   Sử dụng mô hình YOLOv8m-face để phát hiện vị trí khuôn mặt trong video hoặc hình ảnh đầu vào theo thời gian thực.

2. **Trích xuất đặc trưng khuôn mặt (Feature Extraction):**  
   Áp dụng các thuật toán embedding để chuyển khuôn mặt phát hiện thành vector đặc trưng số hóa.

3. **So sánh và nhận dạng (Face Recognition):**  
   So sánh vector đặc trưng với cơ sở dữ liệu khuôn mặt đã đăng ký để xác định danh tính.

4. **Điểm danh tự động:**  
   Khi khuôn mặt được nhận dạng thành công, hệ thống ghi lại thời gian và danh sách điểm danh, giúp quản lý attendance chính xác, nhanh chóng.

### Công nghệ và thư viện:

- YOLOv8m-face: Mô hình phát hiện khuôn mặt nhẹ, hiệu quả.
- OpenCV: Xử lý video và hình ảnh.
- DeepFace / Facenet: Trích xuất embedding khuôn mặt.
- Python: Ngôn ngữ lập trình chính.

### Ưu điểm:

- Xác thực nhanh, chính xác trong môi trường thực tế.
- Hoạt động tốt trong điều kiện ánh sáng và góc nhìn đa dạng.
- Hỗ trợ xử lý nhiều khuôn mặt cùng lúc.

