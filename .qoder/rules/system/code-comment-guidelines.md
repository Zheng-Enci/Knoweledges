---
trigger: model_decision
description: 所有语言的代码注释与类型注释规范强制要求
---
# 代码注释规范

## 概述
本规则定义了所有项目的代码注释标准。**所有函数级别的代码必须将注释写在函数签名行的上方。** 重点以 Python 为主，其他语言遵循类似约定。

## 通用原则

### 1. 类型注释（强制）
- **所有参数和返回值必须有显式的 type annotation** — 所有支持类型标注的语言都不能例外
- **Python**：在所有函数签名上使用原生 type hints（`str`, `int`, `float`, `list[T]`, `dict[K,V]`, `Optional[T]`, `Union[T,U]` 等）
- **TypeScript/JavaScript**：所有函数参数和返回类型使用 TypeScript type annotations
- **Java**：使用泛型（generic types）和正确的返回类型
- **C/C++**：使用正确的类型声明
- **类型模糊的变量**（如初始化为 `None` 或 `{}`）也必须显式标注类型

### 2. 强制注释
- **公共 API**：所有 public 方法、函数和类必须有 doc comments
- **复杂逻辑**：任何超出标准流程的算法复杂度必须加以解释
- **安全性**：涉及安全的关键代码必须说明为什么以及如何应用安全措施
- **性能**：有性能影响的代码必须解释其设计理由

### 3. 注释位置 — 仅限函数级
- **注释必须写在函数/方法签名行的上方，而不是下方**
- **Python 中**，docstring（三重引号字符串）写在 `def` 行的**上方**——而不是放在函数体内
- **其他语言中**，块注释（`/** */`）或行注释（`//`）直接放在函数签名上方

### 4. 注释风格
- Python 代码使用 **NumPy Style**（主要关注点 — 详见下方示例）
- JavaScript/TypeScript 代码使用 **JSDoc** 格式
- Java 代码使用 **Google Style**
- C/C++ 代码使用 **Doxygen**

---

## Python 注释（主要关注点）

> Python 是本项目的首要语言。所有 Python 函数级注释必须遵循以下模式。

### 函数文档 — Docstring 在 `def` 上方

```python
"""
Calculates attendance percentage for a student.

This function implements the project's attendance calculation
standard as defined in the attendance policy document.

Args:
    student_id: Unique identifier for the student

Returns:
    float: Attendance percentage (0-100)

Raises:
    ValueError: If student_id is empty or invalid
"""
def calculate_attendance_rate(student_id: str) -> float:
    # Implementation
    pass
```

> **Python 关键规则**：docstring（`"""..."""` 三重引号字符串）必须直接放在 `def` 行的**上方**。不要把它放在函数体内——虽然传统惯例是那样，但本项目明确要求 docstring 写在函数签名上方。

> **Type Annotation 规则**：每个参数（`student_id: str`）和返回值（`-> float`）都必须有显式的 type hint。绝不能省略。

### 替代方案 — 行注释在 `def` 上方

```python
# 根据项目标准验证和规范化学生姓名
# 返回 (名, 姓) 元组，首尾空白已被去除
def normalize_student_name(raw_name: str) -> tuple[str, str]:
    # 实现
    pass
```

> **Type Annotation 规则**：即使是简单函数，type hints 也是强制的。`raw_name: str` 和 `-> tuple[str, str]` 清晰地表明了期望的类型。

### 类文档 — Docstring 在 `class` 上方

```python
"""
Contactless Attendance System — Student Processor（无接触考勤系统 — 学生处理器）。

此类处理学生数据，包括规范化、验证和持久化。遵循项目的安全与
隐私指南，处理 PII（个人身份信息）。
"""
class StudentProcessor:
    # 实现
    pass
```

> **Type Annotation 规则**：class attributes 和 `__init__` 参数也必须包含 type annotations。使用 `dataclass` 或显式字段类型标注。

### 模块级文档

```python
"""
Contactless Attendance System Module（无接触考勤系统模块）。

本模块提供无接触考勤追踪的核心功能，遵循项目的安全与隐私标准。
"""
```

### 复杂/算法逻辑 — 行内注释

```python
# 使用二分查找按日期定位考勤记录，因为数据是按时间排序的
def find_attendance_record(records: list[dict], date: str) -> dict | None:
    left, right = 0, len(records) - 1
    while left <= right:
        mid = (left + right) // 2
        if records[mid]["date"] == date:
            return records[mid]
        elif records[mid]["date"] < date:
            left = mid + 1  # 搜索右半区
        else:
            right = mid - 1  # 搜索左半区
    return None

# TODO: 考勤记录超过 10,000 条时迁移到数据库查询
# FIXME: 处理跨地区学生的时区差异
# NOTE: 性能优化 — 缓存经常访问的日期结果
```

> **Type Annotation 规则**：使用泛型容器类型（`list[dict]`, `dict | None`），而不是裸 `list` 或 `dict`。这能为读者提供精确的数据结构信息。

---

## JavaScript/TypeScript 注释

### 函数文档 — 注释在函数上方

 **JSDoc 示例**：
```typescript
/**
 * 根据项目特定模式验证用户输入。
 *
 * @param email - 用户的邮箱地址
 * @param age - 用户的年龄（岁）
 * @returns 输入有效返回 true，否则返回 false
 * @throws ValidationError 输入格式不正确时抛出
 *
 * @example
 * validateUserInput("user@example.com", 25); // returns true
 */
function validateUserInput(email: string, age: number): boolean {
  // 实现
}
```

### 行内注释
```typescript
// 根据项目标准公式计算百分比
const percentage = (value / maxValue) * 100;

// TODO: 性能关键场景下改用缓存数据
// FIXME: 生产环境中处理 null 情况
// NOTE: 此处使用项目特定的编码方式
```

---

## Java 注释

### 方法文档 — 注释在方法上方

```java
/**
 * 从数据库中检索学生记录。
 *
 * 此方法实现了项目特定的缓存策略，
 * 平均减少 30% 的数据库负载。
 *
 * @param studentId 学生的唯一标识符
 * @return 匹配条件的 Student 对象列表
 * @throws DatabaseConnectionException 连接失败时抛出
 */
public List<Student> getStudents(String studentId) {
    // 实现
}
```

### 类文档

```java
/**
 * 无接触考勤系统的人脸识别处理器。
 *
 * 此类实现了项目的安全标准：
 * - 仅使用本地处理（无云端传输）
 * - 实现项目特定的加密
 * - 遵循项目的隐私指南
 */
public class FaceProcessor {
    // 实现
}
```

---

## C/C++ 注释

### 函数文档 — 注释在函数上方

```cpp
/**
 * 使用项目特定阈值初始化 IP 监控器。
 *
 * @param port 要监控的网络端口
 * @param threshold 以毫秒为单位的丢包阈值
 * @return 成功返回 0，初始化失败返回 -1
 */
int initializeIPMonitor(int port, int threshold);
```

### 行内注释
```cpp
// 在传输前对数据应用项目特定的加密
encryptData(payload);

// 按照项目内存管理指南缓存结果
std::shared_ptr<Data> cachedResult = processData();
```

---

## 注释质量标准

### 不要注释代码在做什么
```typescript
// 差 — 从代码本身就能看出来
let x = 5; // 把 x 设为 5

// 好 — 解释 WHY，而不是 what
// 使用常量 5 因为它代表项目的最大重试次数
const MAX_RETRIES = 5;
```

### Type Annotations — 绝不能省略

```python
# 差 — 缺少 type annotations
# 使用项目特定公式计算学生分数
# 并检查是否达到最低及格线
def compute_score(name, scores, threshold):  # name, scores, threshold 分别是什么类型？
    pass

# 差 — 不完整的 type annotations（裸类型，没有泛型）
def compute_score(name: str, scores: list, threshold: float) -> bool:
    pass  # list 里是什么？不清楚。

# 好 — 完整的 type annotations 加上泛型容器
"""
计算学生的加权分数并检查是否达到阈值。

Args:
    student_name: 学生的全名
    score_records: 各次评分记录列表（每个 0-100）
    pass_threshold: 通过所需的最低分数

Returns:
    bool: 加权分数 >= 阈值返回 True，否则返回 False
"""
def compute_score(
    student_name: str,
    score_records: list[float],
    pass_threshold: float,
) -> bool:
    # 实现
    pass
```

```python
# 差 — 变量没有 type annotation（类型不明确）
result = None  # result 将来会是什么类型？

# 差 — 复杂类型隐藏在裸 dict 后面
config = {}  # dict 的 key 和 value 分别是什么？

# 好 — 变量有显式的 type annotation
result: str | None = None
config: dict[str, int] = {}
```

### 注释在函数签名上方 — 不要写在行内或下方

```python
# 差 — 注释在函数体内（在 def 行下方）
def parse_student(data: dict) -> Student:
    """将字典解析为 Student 对象。"""
    # 实现
    pass

# 同样差 — 变量缺少 type annotation
parsed = None

# 好 — 注释在 def 行上方，type hints 完整
"""
将字典解析为 Student 对象。

Args:
    data: 原始学生数据字典

Returns:
    Student: 解析后的 Student 实例
"""
def parse_student(data: dict[str, Any]) -> Student:
    # 实现
    pass

parsed: Student | None = None
```

```typescript
// 差 — 行内注释跟在函数签名后面
function computeScore(input: number): number { // 计算最终分数
}

// 好 — 注释在函数上方
// 通过项目加权公式计算最终分数
function computeScore(input: number): number {
}
```

### 简洁但完整
```typescript
// 差
// 这个函数做了很多事情并返回一些东西

// 好
// 汇总学生成绩并应用项目的评分公式
function aggregateScores(): number
```

---

## 项目特定要求

### 安全注释
- 记录所有安全措施
- 说明为什么使用某些库或方法
- 用安全标记标注敏感操作

### 性能注释
- 记录性能关键部分
- 解释优化选择
- 标记应用了缓存或懒加载的位置

### API 文档
- 记录所有公共接口
- 包含使用示例
- 说明错误条件

---

## 代码审查清单

审查代码时，请验证：
- [ ] 所有公共 API 都有文档说明
- [ ] 所有函数级注释都放在函数签名上方
- [ ] Python docstring 写在 `def` 上方，而不是函数体内
- [ ] **所有函数参数都有显式的 type annotation**
- [ ] **所有函数返回值都有显式的 type annotation**
- [ ] **类型模糊的变量（None, {}, []）有 type annotation**
- [ ] **泛型使用完整的容器规格（list[str]，而不是裸 list）**
- [ ] 注释使用了该语言正确的格式
- [ ] 注释使用一般现在时
- [ ] 注释不重复代码已经在做的事情
- [ ] TODO/FIXME 注释是可执行的
- [ ] 安全措施已记录
- [ ] 性能考量已注明

---

## 执行

本规则适用于：
- 项目中编写的所有新代码
- 对现有代码的所有修改
- Pull requests 必须通过注释质量检查
