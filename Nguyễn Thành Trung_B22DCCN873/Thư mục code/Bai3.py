import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from IPython.display import clear_output
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans



#hàm lấy random k điểm 
def random_centroids(data, k):
    centroids = []
    for i in range(k):
        centroid = data.apply(lambda x: float(x.sample()))
        centroids.append(centroid)
    return pd.concat(centroids, axis=1)

#lấy nhãn mỗi khoảng 
def get_labels(data, centroids):
    #tính khoảng cách
    distances = centroids.apply(lambda x: np.sqrt(((data - x) ** 2).sum(axis=1)))
    return distances.idxmin(axis=1)

#lấy mới lại k điểm cho mỗi khoảng
def new_centroids(data, labels, k):
    centroids = data.groupby(labels).apply(lambda x: np.exp(np.log(x).mean())).T
    return centroids

#hiển thị vẽ hình phân cụm các vùng dữ liệu trên mặt 2D
def plot_clusters(data, labels, centroids, iteration):
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data)
    centroids_2d = pca.transform(centroids.T)
    clear_output(wait=True)
    plt.title(f'Iteration {iteration}')
    plt.scatter(x=data_2d[:,0], y=data_2d[:,1], c=labels)
    plt.scatter(x=centroids_2d[:,0], y=centroids_2d[:,1],)
    # plt.savefig(f'iteration{iteration}.png')  # Lưu hình ảnh

    plt.show()
# hàm để lấy số k  centroid
def takeCentroids(data):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)
    inertia = []
    K = range(1, 10)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)
    # Vẽ đồ thị Elbow
    plt.plot(K, inertia, 'bx-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method For Optimal k')
    plt.show()


players = pd.read_csv("result.csv", header=[0, 1])
players.columns = ['_'.join(filter(None, col)).strip() for col in players.columns]
#các chỉ số để đánh giá 
features = ["Info_Age","Playing Time_MP","Playing Time_Min","Performance_G-PK","Performance_Ast"]
players=players.dropna(subset=features)
data = players[features].copy()
#chuẩn dữ liệu về từ khoảng 1 đến 11
data = ((data - data.min()) / (data.max() - data.min())) * 10 +1

#thuật toán elbow để lấy centroid

takeCentroids(data)




# Chạy thuật toán
max_iterations = 100
centroid_count = 4
centroids = random_centroids(data, centroid_count)
print(centroids)
old_centroids = pd.DataFrame()
iteration = 1
#ap dụng K-means
while iteration < max_iterations and not centroids.equals(old_centroids):
    old_centroids = centroids
    labels = get_labels(data, centroids)
    centroids = new_centroids(data, labels, centroid_count)
    plot_clusters(data, labels, centroids, iteration)
    iteration += 1

print(players[labels == 0][["Info_Player"] + features].head())
print(players[labels == 1][["Info_Player"] + features].head())
print(players[labels == 2][["Info_Player"] + features].head())
print(players[labels == 3][["Info_Player"] + features].head())






