import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import predict_house_price  # Import hàm từ app.py

def test_predict_house_price():
    # Tạo dữ liệu giả định để kiểm thử
    input_data = {
        "OverallQual": 7,
        "YearBuilt": 1995,
        "YearRemodAdd": 2000,
        "TotalBsmtSF": 800,
        "GrLivArea": 1200,
        "FullBath": 2,
        "HalfBath": 1,
        "BedroomAbvGr": 3,
        "KitchenAbvGr": 1,
        "GarageArea": 500,
    }

    # Gọi hàm predict_house_price và kiểm tra kết quả
    result = predict_house_price(input_data)

    # Kiểm tra không phải None
    assert result is not None, "Kết quả không được là None"

    # Kiểm tra kết quả là chuỗi
    assert isinstance(result, str), "Kết quả phải là chuỗi (string)"
    
    # Loại bỏ ký hiệu '$' và ',' để kiểm tra chuyển đổi sang float
    try:
        numeric_value = float(result.replace("$", "").replace(",", ""))
    except ValueError:
        assert False, "Kết quả không thể chuyển đổi sang số thực (float)"
    
    # Kiểm tra giá trị phải lớn hơn 0
    assert numeric_value > 0, "Giá dự đoán phải lớn hơn 0"
