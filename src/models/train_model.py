import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import joblib
from math import sqrt
from sklearn.preprocessing import OneHotEncoder
import mlflow
import mlflow.sklearn

def train_model():
    print("Training model...")

    # Đảm bảo thư mục models và reports tồn tại
    os.makedirs("models", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Cài đặt URI cho MLflow để kết nối với DagsHub
    mlflow.set_tracking_uri("https://dagshub.com/ngocnamk3er/house-prices.mlflow")  # Thay URL này bằng URL của repository của bạn trên DagsHub

    # Tải dữ liệu đã xử lý
    X_train = pd.read_csv("data/processed/X_train.csv")
    y_train = pd.read_csv("data/processed/y_train.csv")
    y_train = y_train.values.ravel()

    # Chỉ sử dụng các cột mà bạn muốn huấn luyện
    selected_columns = [
        "OverallQual", "YearBuilt", "YearRemodAdd", "TotalBsmtSF", 
        "GrLivArea", "FullBath", "HalfBath", "BedroomAbvGr", 
        "KitchenAbvGr", "GarageArea"
    ]
    X_train = X_train[selected_columns]

    # Kiểm tra xem có cột chuỗi nào cần mã hóa không
    categorical_cols = X_train.select_dtypes(include=["object"]).columns
    if len(categorical_cols) > 0:
        # Tạo OneHotEncoder cho các cột chuỗi
        ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        X_train_encoded = ohe.fit_transform(X_train[categorical_cols])

        # Chuyển đổi mã hóa thành DataFrame và kết hợp lại với dữ liệu huấn luyện
        X_train_encoded_df = pd.DataFrame(X_train_encoded, columns=ohe.get_feature_names_out(categorical_cols))
        X_train = X_train.drop(categorical_cols, axis=1).join(X_train_encoded_df)
    else:
        ohe = None  # Không cần encoder nếu không có cột chuỗi

    # Kết nối DagsHub để theo dõi
    with mlflow.start_run() as run:
        # Ghi lại các tham số mô hình
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)

        # Huấn luyện mô hình Random Forest
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Dự đoán trên tập huấn luyện
        y_pred = model.predict(X_train)

        # Tính toán các chỉ số đánh giá
        rmse = sqrt(mean_squared_error(y_train, y_pred))
        mae = mean_absolute_error(y_train, y_pred)

        # In ra các chỉ số đánh giá
        print(f"Root Mean Squared Error (RMSE): {rmse}")
        print(f"Mean Absolute Error (MAE): {mae}")

        # Ghi lại các chỉ số đánh giá vào MLflow
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)

        # Lưu mô hình vào DagsHub (MLflow sẽ tự động lưu vào repository)
        mlflow.sklearn.log_model(model, "model")

        # Lưu encoder nếu cần vào DagsHub
        if ohe:
            mlflow.sklearn.log_model(ohe, "encoder")

        # Lưu mô hình vào thư mục cục bộ
        joblib.dump(model, "models/house_price_model.pkl")
        if ohe:
            joblib.dump(ohe, "models/encoder.pkl")

        # Lưu các chỉ số đánh giá vào file CSV
        metrics = pd.DataFrame({
            'RMSE': [rmse],
            'MAE': [mae]
        })
        metrics.to_csv("reports/training_metrics.csv", index=False)

        print("Model training complete and saved to 'models/house_price_model.pkl'")
        print("Training metrics saved to 'reports/training_metrics.csv'")

# Hàm main để gọi train_model khi tập tin được chạy trực tiếp
if __name__ == "__main__":
    train_model()
