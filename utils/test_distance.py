import numpy as np
import matplotlib.pyplot as plt

# 1. 构造曲线点集：y = sin(x)
x_vals = np.linspace(0, 4 * np.pi, 500)
curve = np.column_stack((x_vals, np.sin(x_vals)))  # shape (500, 2)

# 2. 已知点
point = np.array([1.0, 1.5])

# 3. 计算每个曲线点到已知点的距离
distances = np.linalg.norm(curve - point, axis=1)

# 4. 找出最短距离点
min_index = np.argmin(distances)
closest_point = curve[min_index]
min_distance = distances[min_index]

# 5. 打印最近点和距离
print(f"最近点: ({closest_point[0]:.4f}, {closest_point[1]:.4f})")
print(f"最短距离: {min_distance:.4f}")

# 6. 可视化
plt.figure(figsize=(8, 5))
plt.plot(curve[:, 0], curve[:, 1], label='Curve (y = sin(x))')
plt.scatter(*point, color='blue', label='Known Point', zorder=5)
plt.scatter(*closest_point, color='red', label='Closest Point', zorder=5)
plt.plot([point[0], closest_point[0]], [point[1], closest_point[1]], 'k--', label='Shortest Distance')

plt.title('Closest Point on Curve to Given Point')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
