import matplotlib.pyplot as plt
from collections import deque

CAPACITY = (8, 5, 3)  # A, B, C 瓶的容量

def is_goal(state):
    a, b, c = state
    return (a == 4 and b == 4) or (a == 4 and c == 4) or (b == 4 and c == 4)

def pour(state, from_idx, to_idx):
    state = list(state)
    from_cap = CAPACITY[from_idx]
    to_cap = CAPACITY[to_idx]
    amount = min(state[from_idx], to_cap - state[to_idx])
    state[from_idx] -= amount
    state[to_idx] += amount
    return tuple(state)

def solve():
    visited = set()
    queue = deque()
    path = {}

    initial = (8, 0, 0)
    queue.append(initial)
    visited.add(initial)
    path[initial] = None

    while queue:
        current = queue.popleft()
        if is_goal(current):
            steps = []
            while current:
                steps.append(current)
                current = path[current]
            steps.reverse()
            return steps

        for i in range(3):
            for j in range(3):
                if i != j:
                    next_state = pour(current, i, j)
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append(next_state)
                        path[next_state] = current
    return None

def plot_steps(steps):
    fig, axes = plt.subplots(len(steps), 1, figsize=(6, len(steps) * 2))
    if len(steps) == 1:
        axes = [axes]  # 单步情况处理

    for i, state in enumerate(steps):
        ax = axes[i]
        labels = ['A (8kg)', 'B (5kg)', 'C (3kg)']
        colors = ['#1f77b4', '#2ca02c', '#ff7f0e']
        values = state
        max_heights = CAPACITY

        ax.bar(labels, values, color=colors)
        ax.set_ylim(0, max(CAPACITY) + 1)
        ax.set_title(f"Step {i}: A={values[0]}kg, B={values[1]}kg, C={values[2]}kg")
        ax.set_ylabel("kg")

        # 显示瓶子当前油量数值
        for j, val in enumerate(values):
            ax.text(j, val + 0.1, f'{val}kg', ha='center')

    plt.tight_layout()
    plt.show()

# 执行
steps = solve()
if steps:
    print("找到方案，总步骤数：", len(steps) - 1)
    for i, state in enumerate(steps):
        print(f"步骤{i}: A={state[0]}kg, B={state[1]}kg, C={state[2]}kg")
    plot_steps(steps)
else:
    print("未能找到解决方案")
