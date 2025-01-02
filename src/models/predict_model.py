import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

def predict_model():
    print("Loading model and predicting...")

    # Tải dữ liệu đã xử lý
    X_test = pd.read_csv("data/processed/X_val.csv")
    y_test = pd.read_csv("data/processed/y_val.csv")
    y_test = y_test.values.ravel()

    # Chỉ sử dụng các cột đã chọn trong phần huấn luyện
    selected_columns = [
        "OverallQual", "YearBuilt", "YearRemodAdd", "TotalBsmtSF", 
        "GrLivArea", "FullBath", "HalfBath", "BedroomAbvGr", 
        "KitchenAbvGr", "GarageArea"
    ]
    X_test = X_test[selected_columns]

    # Tải mô hình đã huấn luyện
    model = joblib.load("models/house_price_model.pkl")
    
    # Kiểm tra xem có cần encoder hay không
    try:
        ohe = joblib.load("models/encoder.pkl")  # Tải encoder nếu có
        categorical_cols = X_test.select_dtypes(include=["object"]).columns

        # Nếu có cột chuỗi, thực hiện mã hóa
        if len(categorical_cols) > 0:
            X_test_encoded = ohe.transform(X_test[categorical_cols])
            X_test_encoded_df = pd.DataFrame(X_test_encoded, columns=ohe.get_feature_names_out(categorical_cols))
            X_test = X_test.drop(categorical_cols, axis=1).join(X_test_encoded_df)
    except FileNotFoundError:
        print("Encoder not found. Skipping categorical encoding...")
        ohe = None

    # Dự đoán
    y_pred = model.predict(X_test)

    # Tính toán các chỉ số đánh giá
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    # In ra các chỉ số đánh giá
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"Mean Absolute Error (MAE): {mae}")

    # Lưu các chỉ số đánh giá vào file CSV
    metrics = pd.DataFrame({
        'RMSE': [rmse],
        'MAE': [mae]
    })
    metrics.to_csv("reports/metrics.csv", index=False)

    print("Predictions complete and metrics saved to 'reports/metrics.csv'")

if __name__ == "__main__":
    predict_model()
