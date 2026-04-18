name = "Alice"
score = 95.5

# 常规方式：需要手动写变量名
print(f"name={name}, score={score}")
# 输出：name=Alice, score=95.5

# 使用 = 说明符：自动显示变量名
print(f"{name=}, {score=}")
# 输出：name='Alice', score=95.5

# 表达式也可以用
x = 10
print(f"{x * 2 = }")
# 输出：x * 2 = 20