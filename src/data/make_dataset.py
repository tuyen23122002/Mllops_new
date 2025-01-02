import pandas as pd
from sklearn.model_selection import train_test_split
import os

def process_data():
    print("Processing data...")
    
    # Đảm bảo thư mục processed tồn tại
    os.makedirs("data/processed", exist_ok=True)
    
    # Tải dữ liệu
    train_df = pd.read_csv("data/raw/train.csv")
    test_df = pd.read_csv("data/raw/test.csv")
    
    # Tách dữ liệu huấn luyện và mục tiêu
    X = train_df.drop(columns=['SalePrice'])
    y = train_df['SalePrice']
    
    # Chia dữ liệu thành train và validation set
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # In ra một vài dòng để kiểm tra
    print(X_train.head(), X_val.head(), y_train.head(), y_val.head())
    
    # Lưu trữ dữ liệu đã xử lý vào thư mục processed
    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_val.to_csv("data/processed/X_val.csv", index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_val.to_csv("data/processed/y_val.csv", index=False)

    # Trả về dữ liệu đã xử lý
    return X_train, X_val, y_train, y_val

# Hàm main để gọi process_data khi tập tin được chạy trực tiếp
if __name__ == "__main__":
    process_data()
