#https://chatgpt.com/c/672242e0-240c-800c-9966-ba9d229782d5
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 生成 600 個隨機點，並固定其位置
np.random.seed(42)
num_points = 600
mean = [0, 0]
cov = [[10, 0], [0, 10]]  # 方差為 10
x1, x2 = np.random.multivariate_normal(mean, cov, num_points).T

# 計算第三維度 x3 使用高斯函數
x3 = np.exp(-0.1 * (x1**2 + x2**2))

# 設定超平面參數的滑桿
slope_x = st.sidebar.slider("超平面 x1 方向斜率", -1.0, 1.0, 0.0, 0.1)
slope_y = st.sidebar.slider("超平面 x2 方向斜率", -1.0, 1.0, 0.0, 0.1)
intercept = st.sidebar.slider("超平面高度", -1.0, 1.0, 0.0, 0.1)

# 計算每個點與超平面的關係，並根據超平面的斜率和高度來決定點的顏色
plane_values = slope_x * x1 + slope_y * x2 + intercept
colors = np.where(x3 > plane_values, 'blue', 'red')  # 超平面以上為藍色，以下為紅色

# 繪製 3D 散點圖
fig = go.Figure()
fig.add_trace(go.Scatter3d(
    x=x1, y=x2, z=x3,
    mode='markers',
    marker=dict(size=5, color=colors),
    name="Data Points"
))

# 添加超平面
x1_range = np.linspace(min(x1), max(x1), 50)  # 使用與數據範圍一致的範圍
x2_range = np.linspace(min(x2), max(x2), 50)
X1, X2 = np.meshgrid(x1_range, x2_range)
Z = slope_x * X1 + slope_y * X2 + intercept  # 超平面的方程式

fig.add_trace(go.Surface(x=X1, y=X2, z=Z, colorscale='gray', opacity=0.5, showscale=False))

# 設定圖表參數
fig.update_layout(scene=dict(
    xaxis_title="x1", yaxis_title="x2", zaxis_title="x3",
    xaxis=dict(range=[min(x1), max(x1)]),
    yaxis=dict(range=[min(x2), max(x2)]),
    zaxis=dict(range=[min(x3), max(x3)])
))

# 顯示圖表
st.plotly_chart(fig, use_container_width=True)
