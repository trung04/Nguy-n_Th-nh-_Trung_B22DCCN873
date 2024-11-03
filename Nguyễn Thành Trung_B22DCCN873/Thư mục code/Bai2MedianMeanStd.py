import pandas as pd
import numpy as np
df = pd.read_csv("result.csv", header=[0, 1]) 
#Tìm trung vị của mỗi chỉ số. Tìm trung bình và độ lệch chuẩn của mỗi chỉsố cho các cầu thủ trong toàn
# giải và của mỗi đội. Ghi kết quả ra file results2.csv
print(" trung vị của mỗi chỉ số. Tìm trung bình và độ lệch chuẩn của mỗi chỉ số trong toàn giải và của mỗi đội")
df1=df
df1.columns = ['_'.join(filter(None, col)).strip() for col in df.columns]
total_scores = df.select_dtypes(include='number')
total_scores['Team'] = df['Info_Team']
#tính theo mỗi đội
total_scores=total_scores.groupby('Team').agg(['median','mean','std'])
#làm lại tên cột cho giống mẫu
total_scores.columns = ['_'.join(col).strip() for col in total_scores.columns]
total_scores.reset_index()
#tính toàn giải
all_stats = df.select_dtypes(include='number').agg(['median', 'mean', 'std'])
all_row = []
for col in all_stats.columns:
    all_row.append(all_stats[col]['median'])
    all_row.append(all_stats[col]['mean'])
    all_row.append(all_stats[col]['std'])
#thêm kết quả của toàn giải vào
total_scores.loc['All'] = all_row
#cho kết quả toàn giải lên đầu
total_scores = total_scores.sort_index(ascending=True)
print(total_scores)
total_scores.to_csv('result2.csv')
print("Đã xuất Excel result2 thành công")


