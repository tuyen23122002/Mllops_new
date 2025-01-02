import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import pytest
import pandas as pd
from src.data.make_dataset import process_data

def test_process_data():
    # Gọi hàm process_data để tạo dữ liệu
    X_train, X_val, y_train, y_val = process_data()
    
    # Kiểm tra xem dữ liệu đã được xử lý có phải là DataFrame không
    assert isinstance(X_train, pd.DataFrame), "X_train không phải là DataFrame"
    assert isinstance(X_val, pd.DataFrame), "X_val không phải là DataFrame"
    assert isinstance(y_train, pd.Series), "y_train không phải là Series"
    assert isinstance(y_val, pd.Series), "y_val không phải là Series"
    
    # Kiểm tra dữ liệu không rỗng
    assert len(X_train) > 0, "X_train rỗng"
    assert len(X_val) > 0, "X_val rỗng"
    assert len(y_train) > 0, "y_train rỗng"
    assert len(y_val) > 0, "y_val rỗng"
