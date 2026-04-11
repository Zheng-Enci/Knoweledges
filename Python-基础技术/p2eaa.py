# 嵌套字典
company = {
    "部门A": {"员工数": 10, "预算": 50000},
    "部门B": {"员工数": 15, "预算": 80000}
}

# 遍历外层字典的所有键值对
print("=== 遍历所有部门及其信息 ===")
for dept, info in company.items():
    print(f"部门: {dept}")
    for key, value in info.items():
        print(f"  {key}: {value}")
# 输出:
# 部门: 部门A
#   员工数: 10
#   预算: 50000
# 部门: 部门B
#   员工数: 15
#   预算: 80000

# 遍历所有值（嵌套字典的值）
print("\n=== 遍历所有详细信息 ===")
for dept, info in company.items():
    for value in info.values():
        print(value)
# 输出: 10, 50000, 15, 80000

# 使用字典推导式创建新嵌套字典
doubled = {dept: {k: v * 2 for k, v in info.items()} for dept, info in company.items()}
print(doubled)
# 输出: {'部门A': {'员工数': 20, '预算': 100000}, '部门B': {'员工数': 30, '预算': 160000}}

# 统计所有部门的总预算
total_budget = sum(info["预算"] for info in company.values())
print(f"总预算: {total_budget}")  # 输出: 总预算: 130000

# 找出员工数最多的部门
max_staff_dept = max(company.items(), key=lambda x: x[1]["员工数"])
print(f"员工最多的部门: {max_staff_dept[0]}")  # 输出: 员工最多的部门: 部门B