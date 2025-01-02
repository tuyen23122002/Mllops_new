import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import joblib
import pytest
import pandas as pd

# Tải mô hình đã huấn luyện
model = joblib.load("models/house_price_model.pkl")

# Dữ liệu thử nghiệm
test_data = {
    "OverallQual": [7],
    "YearBuilt": [2005],
    "YearRemodAdd": [2010],
    "TotalBsmtSF": [1000],
    "GrLivArea": [1500],
    "FullBath": [2],
    "HalfBath": [1],
    "BedroomAbvGr": [3],
    "KitchenAbvGr": [1],
    "GarageArea": [500],
}

def test_model_prediction():
    # Chuyển dữ liệu thử nghiệm thành DataFrame
    input_df = pd.DataFrame(test_data)
    
    # Dự đoán giá trị
    prediction = model.predict(input_df)
    
    # Kiểm tra rằng dự đoán có giá trị hợp lệ
    assert isinstance(prediction[0], (int, float)), "Dự đoán không phải là số hợp lệ"
    assert prediction[0] >= 0, "Giá trị dự đoán không hợp lệ (giá trị âm)"
