from flask import Flask, render_template, request
import csv
import os
from datetime import datetime

app = Flask(__name__)
ATTENDANCE_DIR = 'attendance_logs'  # Thư mục chứa các file điểm danh

@app.route('/', methods=['GET'])
def index():
    all_data = []
    headers = ["ID", "Name", "Time", "Status", "SourceFile"]
    search_name = request.args.get('name', '').strip().lower()
    date_filter = request.args.get('date', '')  # yyyy-mm-dd

    if os.path.exists(ATTENDANCE_DIR):
        for filename in sorted(os.listdir(ATTENDANCE_DIR)):
            if filename.endswith('.csv'):
                file_path = os.path.join(ATTENDANCE_DIR, filename)
                try:
                    with open(file_path, newline='', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        rows = list(reader)

                        if len(rows) > 1 and rows[0][:4] == ["ID", "Name", "Time", "Status"]:
                            for row in rows[1:]:
                                row.append(filename)  # Thêm tên file để biết nguồn
                                all_data.append(row)
                except Exception as e:
                    print(f"⚠️ Không thể đọc file {filename}: {e}")

    # Lọc theo tên
    if search_name:
        all_data = [row for row in all_data if search_name in row[1].lower()]

    # Lọc theo ngày
    if date_filter:
        filtered_data = []
        for row in all_data:
            try:
                row_date = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S").date()
                if str(row_date) == date_filter:
                    filtered_data.append(row)
            except Exception:
                continue
        all_data = filtered_data

    return render_template('index.html', headers=headers, data=all_data,
                           search_name=search_name, date_filter=date_filter)

if __name__ == '__main__':
    app.run(debug=True)
