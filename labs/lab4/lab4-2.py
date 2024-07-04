# 根据需求导库
from math import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation


# 定义算法的全局变量
POP_NUM = 50  # 初始种群数
GEN_LEN = 20  # 基因长度
CROSS_RATE = 0.7  # 交叉率
VARIATION_RATE = 0.01  # 变异率
EPOCH = 100  # 遗传轮数


# 初始化种群
def init_population():
    population = np.random.randint(2, size=(POP_NUM, GEN_LEN))  # 初始化种群列表
    population = population.tolist()
    return population

# 目标函数
def target_func(x, y):
    return x * np.cos(2 * np.pi * y) + y * np.sin(2 * np.pi * x)

# 基因解码
def decode(individual):
    x, y = 0, 0
    for i in range(0, GEN_LEN, 2):
        x += individual[i] * (2 ** (i // 2))
        y += individual[i] * (2 ** (i // 2))
    x = (x / (2 ** (GEN_LEN // 2) - 1)) * 4 - 2
    y = (y / (2 ** (GEN_LEN // 2) - 1)) * 4 - 2
    return x, y

# 从基因中得出值
def calc_val(individual):
    x, y = decode(individual)
    return target_func(x, y)

# 计算种群的适应度
def get_fitness(pop):
    fitness = []
    for individual in pop:  # 计算种群中每个个体的适应度
        # 适应度为值
        fitness.append(np.exp(calc_val(individual) / 10))
    return fitness

# 轮盘赌法选择
def choose(pop, fitness):
    # 先计算选择到的概率
    sm = np.sum(fitness)
    prob = [fitness[0] / sm]  # 选择概率
    for i in fitness[1:]:
        prob.append(prob[-1] + i / sm)
    # 根据上述概率进行选择
    nxt_pop = []  # 初始化下一代种群
    for _ in range(POP_NUM):
        p = np.random.random()
        for i in range(POP_NUM):  # 根据概率列表进行选择
            if p < prob[i]:
                nxt_pop.append(pop[i])
                break
    # 为了保证当前解不会比之前解差, 需要将之前解加到当前解中
    nxt_pop += pop
    nxt_pop.sort(key=lambda x : -calc_val(x))
    return nxt_pop[:POP_NUM]  # 返回保证种群数量为POP_NUM

# 交叉操作
def cross(pop):
    nxt_pop = []  # 初始化记录下一个种群
    for individual in pop:
        gen1 = individual.copy()  # 复制当前元素
        if np.random.random() < CROSS_RATE:  # 按照概率随机选择是否交叉
            gen2 = pop[np.random.randint(POP_NUM)].copy()  # 选择与之交叉的另一个父节点
            # 选择交叉的两点
            p1, p2 = np.random.choice(range(GEN_LEN), size=2, replace=True)
            p1, p2 = min(p1, p2), max(p1, p2) # 调整大小顺序
            # 进行交叉
            gen1[p1:p2] = gen2[p1:p2]
        nxt_pop.append(gen1)
    return nxt_pop

# 变异操作, 反转两点
def mutation(pop):
    nxt_pop = []  # 初始化记录下一个种群
    for individual in pop:
        ind2 = individual.copy()
        if np.random.random() < CROSS_RATE:
            p = np.random.randint(GEN_LEN)
            ind2[p] = 1 - ind2[p]
        nxt_pop.append(ind2)
    return nxt_pop

# 计算最大值
def calc_max_val(pop):
    max_val = 0
    max_xy = []
    for individual in pop:
        val = calc_val(individual)
        if val > max_val:
            max_val = val
            max_xy = decode(individual)
    return max_val, max_xy

# 画图初始化（显示中文）
# plt.rcParams['font.sans-serif']=['SimHei']

# 程序入口
if __name__ == '__main__':
    pop = init_population()  # 初始化种群
    max_val_change = []  # 记录每一个epoch对应的极大值
    for epoch in range(EPOCH):
        fitness = get_fitness(pop)  # 一个种群的适应度
        nxt_pop = choose(pop, fitness)  # 进行种群选择
        nxt_pop = cross(nxt_pop)  # 对种群进行交叉
        nxt_pop = mutation(nxt_pop)  # 对种群进行变异
        max_val = calc_max_val(nxt_pop)  # 计算种群的极大值
        pop = nxt_pop  # 更新到下一代
        max_val_change.append(max_val)
    # 极大值对应的x, y
    print(max_val)
    # 画出极大值变化曲线
    plt.plot([i for i in range(EPOCH)], [i[0] for i in max_val_change])
    plt.show()