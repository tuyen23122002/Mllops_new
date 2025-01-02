import streamlit as st
import joblib
import pandas as pd

# Tải mô hình
model = joblib.load("models/house_price_model.pkl")
required_features = model.feature_names_in_  # Lấy các trường cần thiết từ mô hình

def predict_house_price(fields):
    # Lấy các trường phù hợp với mô hình
    input_data = {key: [value] for key, value in fields.items() if key in required_features}
    
    # Kiểm tra xem có đủ các trường cần thiết hay không
    missing_features = set(required_features) - set(input_data.keys())
    if missing_features:
        return f"Thiếu các trường cần thiết: {', '.join(missing_features)}"
    
    # Chuyển dữ liệu thành DataFrame
    input_df = pd.DataFrame(input_data)
    
    # Dự đoán giá
    prediction = model.predict(input_df)
    return f"${prediction[0]:,.2f}"

# Streamlit UI
st.title("House Price Prediction")
st.write("Nhập thông tin của ngôi nhà để dự đoán giá bán.")

# Xây dựng form nhập liệu
with st.form(key="house_price_form"):
    st.header("Thông tin ngôi nhà")
    
    # Các trường nhập liệu (lọc dựa trên các trường cần thiết)
    fields = {
        "OverallQual": st.number_input("Overall Quality (1-10)", min_value=1, max_value=10, value=5),
        "YearBuilt": st.number_input("Year Built", min_value=1800, max_value=2024, value=2000),
        "YearRemodAdd": st.number_input("Year Remodeled", min_value=1800, max_value=2024, value=2005),
        "TotalBsmtSF": st.number_input("Total Basement Area (sq ft)", min_value=0, value=800),
        "GrLivArea": st.number_input("Above Grade Living Area (sq ft)", min_value=0, value=1200),
        "FullBath": st.number_input("Full Bathrooms", min_value=0, max_value=10, value=2),
        "HalfBath": st.number_input("Half Bathrooms", min_value=0, max_value=10, value=1),
        "BedroomAbvGr": st.number_input("Bedrooms Above Grade", min_value=0, max_value=10, value=3),
        "KitchenAbvGr": st.number_input("Kitchens Above Grade", min_value=0, max_value=10, value=1),
        "GarageArea": st.number_input("Garage Area (sq ft)", min_value=0, value=500),
    }
    
    # Nút submit
    submit_button = st.form_submit_button(label="Dự đoán giá nhà")

# Xử lý khi người dùng nhấn nút "Dự đoán giá nhà"
if submit_button:
    # Gọi hàm dự đoán
    prediction_result = predict_house_price(fields)
    st.write(f"**Giá nhà dự đoán:** {prediction_result}")
