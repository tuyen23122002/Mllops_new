# Sử dụng python:3.12-slim làm base image
FROM python:3.12-slim

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements.txt vào thư mục /app trong container
# COPY requirements.txt /app/
COPY requirements_build.txt /app/

# Cài đặt các thư viện cần thiết từ requirements.txt
RUN pip install --no-cache-dir -r /app/requirements_build.txt

# Copy chỉ thư mục models và tệp app.py vào container
COPY models /app/models
COPY app.py /app/

# Tải mô hình từ DVC remote (chỉ tải mô hình)
# Expose cổng 8501 cho Streamlit
EXPOSE 8501

# Chạy ứng dụng Streamlit
CMD ["streamlit", "run", "app.py"]
