from ultralytics import YOLO
import cv2
import os
import pandas as pd
import re
from datetime import datetime
from deepface import DeepFace
import numpy as np

# Tạo thư mục lưu file điểm danh
ATTENDANCE_DIR = "attendance_logs"
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Tạo tên file mới theo thời gian hiện tại
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
ATTENDANCE_FILE = os.path.join(ATTENDANCE_DIR, f"Attendance_{current_time}.csv")

# Tạo file CSV mới với cấu trúc đúng
df = pd.DataFrame(columns=["ID", "Name", "Time", "Status"])
df.to_csv(ATTENDANCE_FILE, index=False)
print(f"✅ Tạo mới file điểm danh: {ATTENDANCE_FILE}")

# Load YOLOv8 face detection model
model = YOLO("yolov8m-face.pt")  # Đảm bảo bạn có file model này

# Load database ảnh mẫu
DB_PATH = "faces"
if not os.path.exists(DB_PATH) or len(os.listdir(DB_PATH)) == 0:
    print("❌ Thư mục 'faces/' chưa có ảnh mẫu. Vui lòng thêm ảnh vào để điểm danh!")
    exit()

print("[INFO] Đang tải ảnh mẫu và tính embedding...")

db_embeddings = []
db_labels = []

for file in os.listdir(DB_PATH):
    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(DB_PATH, file)
        try:
            embedding = DeepFace.represent(img_path=img_path, model_name="Facenet512", enforce_detection=True)[0]["embedding"]
            db_embeddings.append(embedding)
            filename = os.path.splitext(file)[0]
            match = re.match(r'^(\d+)_([A-Za-z]+)', filename)
            if match:
                student_id = match.group(1)
                name = match.group(2)
            else:
                student_id = "UNKNOWN"
                name = filename
            db_labels.append((student_id, name))
        except Exception as e:
            print(f"Lỗi khi xử lý ảnh mẫu {file}: {e}")

db_embeddings = np.array(db_embeddings)
print(f"[INFO] Đã load {len(db_embeddings)} ảnh mẫu.")

# Hàm nhận diện khuôn mặt
def recognize_face(embedding, db_embeddings, db_labels, threshold=0.4):
    from numpy.linalg import norm
    def cosine_similarity(a, b):
        return np.dot(a, b) / (norm(a) * norm(b))

    sims = [cosine_similarity(embedding, e) for e in db_embeddings]
    best_idx = np.argmax(sims)
    best_score = sims[best_idx]
    if best_score > (1 - threshold):
        return db_labels[best_idx]
    else:
        return None, None

last_recognized = {}

cap = cv2.VideoCapture(0)
print("\n[INFO] Hệ thống điểm danh khuôn mặt đang chạy...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Không thể truy cập camera.")
        break

    frame = cv2.resize(frame, (640, 480))

    results = model(frame)[0]
    boxes = results.boxes.xyxy.cpu().numpy()

    for box in boxes:
        xmin, ymin, xmax, ymax = map(int, box)
        face_img = frame[ymin:ymax, xmin:xmax]

        try:
            rep = DeepFace.represent(face_img, model_name="Facenet512", enforce_detection=False)[0]["embedding"]
            student_id, name = recognize_face(rep, db_embeddings, db_labels)
            if student_id is None:
                student_id = "UNKNOWN"
                name = "UNKNOWN"
        except Exception as e:
            student_id, name = "UNKNOWN", "UNKNOWN"

        if student_id != "UNKNOWN":
            now = datetime.now()
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")

            last_time = last_recognized.get(student_id)
            if not last_time or (now - last_time).total_seconds() > 30:
                past = df[df["ID"] == student_id]
                status = "Check-in" if past.empty or past.iloc[-1]["Status"] == "Check-out" else "Check-out"

                df.loc[len(df)] = [student_id, name, time_str, status]
                df.to_csv(ATTENDANCE_FILE, index=False)
                last_recognized[student_id] = now

                print(f"[+] {student_id} - {name} {status} lúc {time_str}")

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(frame, f"{student_id} - {name}", (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Face Attendance System - YOLOv8", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n[INFO] Thoát chương trình.")
        break

cap.release()
cv2.destroyAllWindows()
