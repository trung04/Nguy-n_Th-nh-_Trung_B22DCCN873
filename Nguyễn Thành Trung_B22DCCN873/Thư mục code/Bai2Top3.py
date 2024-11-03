import pandas as pd
import numpy as np
df = pd.read_csv("result.csv", header=[0, 1]) 

print("Tìm top 3 cầu thủ có điểm cao nhất và thấp nhất ở mỗi chỉsố.")
# Khởi tạo dictionary để lưu kết quả
top_and_bottom = {}

# Duyệt qua từng cột của DataFrame để tìm top và bottom 3 cầu thủ
for col in df.columns:
    # Kiểm tra nếu cột là kiểu số
    if pd.api.types.is_numeric_dtype(df[col]):
        top_players = df.nlargest(3, col)  # Top 3 cầu thủ có điểm cao nhất
        bottom_players = df.nsmallest(3, col)  # Top 3 cầu thủ có điểm thấp nhất
        top_and_bottom[col] = {
            'top_3': top_players,
            'bottom_3': bottom_players
        }
# print(top_and_bottom)
for col, results in top_and_bottom.items():
    print(f"\nChỉ số: {col}")
    print("Top 3 cầu thủ cao nhất:")
    #in ra thông tin cầu thủ
    print(results['top_3'][[('Info', 'Player'), ('Info', 'Age'), ('Info', 'Team'), ('Info', 'Nation')]])  # Hiển thị tên cầu thủ và điểm số
    print("Top 3 cầu thủ thấp nhất:")
    print(results['bottom_3'][[('Info', 'Player'), ('Info', 'Age'), ('Info', 'Team'), ('Info', 'Nation')]])




