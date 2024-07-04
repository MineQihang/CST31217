# 根据需求导库
from math import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation


# 定义算法的全局变量
POP_NUM = 50  # 初始种群数
CROSS_RATE = 0.1  # 交叉率
VARIATION_RATE = 0.1  # 变异率
EPOCH = 100  # 迭代轮数

# 直接计算直线距离
def calc_dis(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 计算一条路径的长度
def calc_path_dis(individual):
    sum = 0
    for i in range(1, n):
        sum += disMatrix[individual[i]][individual[i-1]]  # (0, 1) ... (n-1, n)
    sum += disMatrix[individual[n-1]][individual[0]]  # (n, 0)
    return sum

# TODO: 初始化种群
def init_population():
    population = list()  # 初始化种群列表
    return population

# TODO: 计算种群的适应度
def get_fitness(pop):
    fitness = []
    return fitness

# TODO: 轮盘赌法选择
def choose(pop, fitness):
    return pop

# TODO: 交叉操作
def cross(pop):
    return pop

# TODO: 变异操作, 反转两点
def mutation(pop):
    return pop

# 计算最短距离
def calc_min_dis(pop):
    min_dis = 0x3f3f3f3f
    pth = list()
    for individual in pop:
        dis = calc_path_dis(individual)
        if dis < min_dis:  # 更新最短距离和相应的路径
            min_dis = dis
            pth = individual
    return min_dis, pth

# 读入数据并进行数据预处理
df = pd.read_csv('cities.csv', encoding='gb2312')
n = df.shape[0]  # 城市的数量
disMatrix = np.zeros((n, n))  # 两城市间的距离矩阵
for i in range(n):
    for j in range(n):
        disMatrix[i][j] = calc_dis((df['latitude'][i], df['longitude'][i]), (df['latitude'][j], df['longitude'][j]))

# 画图初始化（显示中文）
plt.rcParams['font.sans-serif']=['SimHei']

# 程序入口
if __name__ == '__main__':
    pop = init_population()  # 初始化种群
    min_dis_change = []  # 记录每一个epoch对应的最短距离和路径
    for epoch in range(EPOCH):
        fitness = get_fitness(pop)  # 一个种群的适应度
        nxt_pop = choose(pop, fitness)  # 进行种群选择
        nxt_pop = cross(nxt_pop)  # 对种群进行交叉
        nxt_pop = mutation(nxt_pop)  # 对种群进行变异
        min_dis = calc_min_dis(nxt_pop)  # 计算种群的最短距离和路径
        pop = nxt_pop  # 更新到下一代
        min_dis_change.append(min_dis)  # 存储记录
    min_pth = min_dis_change[-1][1]
    print(f"最短路径为: {', '.join(map(lambda x : df['city'][x], min_pth))}.\n路径长度为: {min_dis_change[-1][0]:.2f}")
    # 最短路径长度变化曲线
    plt.plot([x[0] for x in min_dis_change])
    plt.show()
    plt.clf()
    # 可视化路径
    plt.scatter(df['latitude'], df['longitude'])
    for i in range(n):
        plt.annotate(df['city'][i], xy = (df['latitude'][i], df['longitude'][i]))
    plt.plot([df['latitude'][x] for x in min_pth + [min_pth[0]]], [df['longitude'][x] for x in min_pth + [min_pth[0]]])
    plt.show()
    # 动态可视化
    fig, ax = plt.subplots()
    ax.scatter(df['latitude'], df['longitude'])
    for i in range(n):
        ax.annotate(df['city'][i], xy = (df['latitude'][i], df['longitude'][i]))
    x = []
    y = []
    line, = ax.plot(x, y)
    def update(num):
        pth = min_dis_change[num][1]
        x = [df['latitude'][t] for t in pth + [pth[0]]]
        y = [df['longitude'][t] for t in pth + [pth[0]]]
        line.set_data(x, y)
        ax.set_title(f"第{num}代, 路径长度为{min_dis_change[num][0]:.2f}")
        return line,
    ani = animation.FuncAnimation(fig, update, frames=range(EPOCH), interval=100, blit=False)
    plt.show()