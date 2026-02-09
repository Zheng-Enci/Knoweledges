# LeetCode 414. 第三大的数完全解析
## 从排序到三指针维护的算法进阶之路

**摘要**：深入解析寻找第三大数的四种解法（排序、有序集合、三指针无穷小/空值），从O(nlogn)到O(n)优化。涵盖生活化比喻、Python/Java双语言实现、复杂度对比、问题预警，适合小白到高级开发者。

---

## 📋 前置知识点

### 基础知识点（必须掌握）
- **数组排序**：将数组元素按大小排列，如 `[3,1,2]` 排序后为 `[1,2,3]`
- **变量赋值**：用变量存储值，如 `a=3, b=2, c=1` 存储第一、二、三大数
- **循环遍历**：逐个检查数组中的每个元素，如 `for num in nums`
- **条件判断**：根据条件决定执行哪个分支，如 `if num > first`

### 进阶知识点（建议了解）
- **时间复杂度**：衡量算法运行快慢的指标，如 O(n) 表示扫描 n 个元素
- **空间复杂度**：衡量算法占用内存的指标，如 O(1) 表示只占用固定内存
- **有序集合**：自动保持元素有序的数据结构，如 Python 的 `SortedList`、Java 的 `TreeSet`
- **指针维护**：用变量标记特定位置，通过比较更新位置

---

## 🎯 题目概述

### 问题描述
给你一个非空数组，返回此数组中**第三大的数**。如果不存在，则返回数组中最大的数。

### 示例说明

**示例 1：**
- 输入：`[3, 2, 1]`
- 输出：`1`
- 解释：排序后的数组是 `[1, 2, 3]`，第三大的数是 `1`

**示例 2：**
- 输入：`[1, 2]`
- 输出：`2`
- 解释：数组中只有两个不同的数 `[1, 2]`，第三大的数不存在，返回最大的数 `2`

**示例 3：**
- 输入：`[2, 2, 3, 1]`
- 输出：`1`
- 解释：去重后是 `[1, 2, 3]`，第三大的数是 `1`。注意，`2` 出现了两次，但在统计中只算一次

### 关键要点
1. **去重计数**：相同的数只算一次，如 `[2, 2, 3, 1]` 中 `2` 只算一个
2. **不足三个**：如果数组中不同数字少于 3 个，返回最大的数
3. **时间优化**：要求时间复杂度 O(n) 的解决方案

---

## 💡 算法思路：生活化比喻

### 核心思想
想象你在比赛中记录前三名的成绩：
- **方法一：排序后数**：先把所有成绩从高到低排序，然后从前往后数到第三个不同的成绩
- **方法二：小本子记录**：准备一个小本子，只记录前三名，每次有新成绩就更新本子
- **方法三：三张卡片（无穷小版）**：用三张卡片分别记录第一、二、三名的成绩，开始标记为"无穷小"
- **方法四：三张卡片（空值版）**：用三张卡片分别记录第一、二、三名的成绩，开始标记为"空"

### 问题本质
在数组中找出**去重后**第三大的数，如果不足三个不同的数，就返回最大的数。

---

## 🚀 方法一：排序 + 去重计数（力扣官方题解）

### 算法思路
先把数组从大到小排序，然后从头遍历，统计不同元素的个数。找到第三个不同的元素就返回。

### 生活化比喻
就像给学生成绩排名次：
1. 先把所有成绩按分数从高到低排序
2. 从第一个开始数，数到第三个不同的成绩
3. 如果数不到第三个，就返回第一名

### Python 代码实现

```python
from typing import List

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        """
        力扣官方题解：排序 + 去重计数（Python 版）
        作者：力扣官方题解
        链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
        来源：力扣（LeetCode）
        著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        """
        # 🔥 重要！排序从大到小
        nums.sort(reverse=True)
        
        # diff 统计不同元素的个数
        diff = 1
        
        # 从第二个元素开始遍历（因为第一个肯定是不同的）
        for i in range(1, len(nums)):
            # 如果当前元素和前一个元素不同
            if nums[i] != nums[i - 1]:
                diff += 1  # 不同元素个数 +1
                if diff == 3:  # 如果达到第三个不同元素
                    return nums[i]  # 直接返回这个元素
        
        # 如果找不到第三大的数，返回最大的数
        return nums[0]
```

### Java 代码实现

```java
class Solution {
    /**
     * 力扣官方题解：排序 + 去重计数（Java 版）
     * 作者：力扣官方题解
     * 链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
     * 来源：力扣（LeetCode）
     * 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
     */
    public int thirdMax(int[] nums) {
        // 🔥 重要！排序
        Arrays.sort(nums);
        reverse(nums);
        
        for (int i = 1, diff = 1; i < nums.length; ++i) {
            if (nums[i] != nums[i - 1] && ++diff == 3) { // 此时 nums[i] 就是第三大的数
                return nums[i];
            }
        }
        return nums[0];
    }

    public void reverse(int[] nums) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int temp = nums[left];
            nums[left] = nums[right];
            nums[right] = temp;
            left++;
            right--;
        }
    }
}
```

### 逐行代码解释

**Python 版**：
```python
nums.sort(reverse=True)  # 从大到小排序：[3,2,1] → [3,2,1]
diff = 1                 # diff 统计不同元素的个数，至少有一个
for i in range(1, len(nums)):  # 从第二个元素开始遍历
    if nums[i] != nums[i - 1]:  # 如果当前元素和前一个不同
        diff += 1         # 不同元素个数 +1
        if diff == 3:     # 如果达到第三个不同元素
            return nums[i]  # 返回这个元素
return nums[0]           # 找不到第三大的数，返回最大值
```

**Java 版**：
```java
Arrays.sort(nums);       // 先排序（从小到大）
reverse(nums);            // 反转变为从大到小
for (int i = 1, diff = 1; i < nums.length; ++i) {  // 从第二个开始遍历，diff=1
    if (nums[i] != nums[i - 1] && ++diff == 3) { // 不同且计数达到3
        return nums[i];   // 返回第三大的数
    }
}
return nums[0];          // 找不到，返回最大值
```

### 复杂度分析
- **时间复杂度**：O(n log n)，排序需要 O(n log n) 时间，遍历需要 O(n) 时间
- **空间复杂度**：O(log n)，排序算法在排序过程中需要 O(log n) 的递归栈空间（辅助空间）

---

## 🚀 方法二：有序集合维护（力扣官方题解）

### 算法思路
用一个有序集合自动保持前三大数。每遇到一个新数就插入集合，如果集合超过 3 个元素就删除最小的。

### 生活化比喻
准备一个小本子记录前三名成绩：
1. 遇到新成绩就写上去
2. 如果本子上有超过 3 个成绩，就删除最差的
3. 最后如果本子上有 3 个成绩，最差的就是第三大；否则返回最好的

### Python 代码实现

```python
from typing import List
from sortedcontainers import SortedList

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        """
        力扣官方题解：有序集合维护（Python 版）
        作者：力扣官方题解
        链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
        来源：力扣（LeetCode）
        著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        """
        # 🔥 重要！有序集合自动保持元素有序
        s = SortedList()
        
        for num in nums:
            # 如果数字不在集合中，就添加进去
            if num not in s:
                s.add(num)
                # 如果集合超过 3 个元素，删除最小的
                if len(s) > 3:
                    s.pop(0)  # 删除最小的元素
        
        # 如果集合有 3 个元素，最小的就是第三大
        # 否则返回最大的
        return s[0] if len(s) == 3 else s[-1]
```

### Java 代码实现

```java
class Solution {
    /**
     * 力扣官方题解：有序集合维护（Java 版）
     * 作者：力扣官方题解
     * 链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
     * 来源：力扣（LeetCode）
     * 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
     */
    public int thirdMax(int[] nums) {
        // 🔥 重要！TreeSet 自动保持元素有序
        TreeSet<Integer> s = new TreeSet<Integer>();
        
        for (int num : nums) {
            s.add(num);
            if (s.size() > 3) {
                s.remove(s.first());  // 删除最小的元素
            }
        }
        
        // 如果集合有 3 个元素，最小的就是第三大
        // 否则返回最大的
        return s.size() == 3 ? s.first() : s.last();
    }
}
```

### 复杂度分析
- **时间复杂度**：O(n)，每个元素最多插入和删除一次
- **空间复杂度**：O(1)，集合最多存储 3 个元素

---

## 🚀 方法三：一次遍历 + 三指针（无穷小版）

### 算法思路
用三个变量 a、b、c 维护前三大的数。初始化为负无穷，遍历数组时，根据新数的位置更新这三个变量。

### 生活化比喻
用三张卡片记录前三名成绩，开始标记为"负无穷"：
1. 遇到新成绩，比较它和卡片上的成绩
2. 如果新成绩更好，就替换对应的卡片
3. 最后看第三张卡片，如果有成绩就是第三大，否则返回第一张卡片

### Python 代码实现

```python
from typing import List

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        """
        力扣官方题解：一次遍历 + 三指针维护（Python 版 - 无穷小初始化）
        作者：力扣官方题解
        链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
        来源：力扣（LeetCode）
        著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        """
        # 🔥 重要！初始化为负无穷（比任何数都小）
        a, b, c = float('-inf'), float('-inf'), float('-inf')
        
        for num in nums:
            # 如果当前数字是前三大的任何一个，跳过（去重）
            if num in (a, b, c):
                continue
            
            # 情况1：num 比第一大还大
            if num > a:
                a, b, c = num, a, b  # 整体右移
            # 情况2：num 在第一和第二之间
            elif num > b:
                b, c = num, b        # 更新第二和第三
            # 情况3：num 在第二和第三之间
            elif num > c:
                c = num              # 只更新第三
        
        # 如果 c 是负无穷，说明没有第三大的数，返回 a
        # 否则返回 c
        return c if c != float('-inf') else a
```

### Java 代码实现

```java
class Solution {
    /**
     * 力扣官方题解：一次遍历 + 三指针维护（Java 版 - 无穷小初始化）
     * 作者：力扣官方题解
     * 链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
     * 来源：力扣（LeetCode）
     * 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
     */
    public int thirdMax(int[] nums) {
        // 🔥 重要！初始化为负无穷
        long a = Long.MIN_VALUE, b = Long.MIN_VALUE, c = Long.MIN_VALUE;
        
        for (long num : nums) {
            if (num > a) {
                c = b;
                b = a;
                a = num;
            } else if (a > num && num > b) {
                c = b;
                b = num;
            } else if (b > num && num > c) {
                c = num;
            }
        }
        
        // 如果 c 是负无穷，说明没有第三大的数，返回 a
        // 否则返回 c
        return c == Long.MIN_VALUE ? (int) a : (int) c;
    }
}
```

### 复杂度分析
- **时间复杂度**：O(n)，只需要遍历一次数组
- **空间复杂度**：O(1)，只使用了三个变量

---

## 🚀 方法四：一次遍历 + 三指针（空值版）

### 算法思路
用三个变量 a、b、c 维护前三大的数。初始化为空值（None/Integer），遍历数组时，根据新数的位置更新这三个变量。

### 生活化比喻
用三张卡片记录前三名成绩，开始标记为"空"：
1. 遇到新成绩，比较它和卡片上的成绩
2. 如果新成绩更好，就替换对应的卡片
3. 最后看第三张卡片，如果有成绩就是第三大，否则返回第一张卡片

### Python 代码实现

```python
from typing import List

class Solution:
    def thirdMax(self, nums: List[int]) -> int:
        """
        力扣官方题解：一次遍历 + 三指针维护（Python 版 - 空值初始化）
        作者：力扣官方题解
        链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
        来源：力扣（LeetCode）
        著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        """
        # 🔥 重要！初始化为空值
        a = b = c = None
        
        for num in nums:
            if a is None or num > a:
                a, b, c = num, a, b
            elif a > num and (b is None or num > b):
                b, c = num, b
            elif b is not None and b > num and (c is None or num > c):
                c = num
        
        # 如果 c 是空值，说明没有第三大的数，返回 a
        # 否则返回 c
        return a if c is None else c
```

### Java 代码实现

```java
class Solution {
    /**
     * 力扣官方题解：一次遍历 + 三指针维护（Java 版 - 空值初始化）
     * 作者：力扣官方题解
     * 链接：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
     * 来源：力扣（LeetCode）
     * 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
     */
    public int thirdMax(int[] nums) {
        // 🔥 重要！初始化为空值
        Integer a = null, b = null, c = null;
        
        for (int num : nums) {
            if (a == null || num > a) {
                c = b;
                b = a;
                a = num;
            } else if (a > num && (b == null || num > b)) {
                c = b;
                b = num;
            } else if (b != null && b > num && (c == null || num > c)) {
                c = num;
            }
        }
        
        // 如果 c 是空值，说明没有第三大的数，返回 a
        // 否则返回 c
        return c == null ? a : c;
    }
}
```

### 复杂度分析
- **时间复杂度**：O(n)，只需要遍历一次数组
- **空间复杂度**：O(1)，只使用了三个变量

---

## 📊 四种方法对比分析

### 时间复杂度对比表格

| 方法 | 时间复杂度 | 空间复杂度 | 优势 | 劣势 |
|------|-----------|-----------|------|------|
| 方法一：排序 | O(n log n) | O(log n) | 思路简单直观 | 性能较差 |
| 方法二：有序集合 | O(n) | O(1) | 代码简洁 | 需要外部库 |
| 方法三：三指针（无穷小） | O(n) | O(1) | 性能最优，不依赖库 | 需要避免整数溢出 |
| 方法四：三指针（空值） | O(n) | O(1) | 性能最优，不依赖库，无需考虑溢出 | 逻辑稍微复杂 |

### 推荐使用场景
- **面试场景**：推荐方法三或方法四，展示对时间和空间复杂度的理解
- **日常开发**：使用方法二，代码简洁易维护
- **学习理解**：按顺序学习，从简单到高级

---

## ⚠️ 常见问题预警

### 问题一：去重逻辑缺失

**错误做法**（不推荐）：
```python
def thirdMax(self, nums: List[int]) -> int:
    nums.sort(reverse=True)
    return nums[2] if len(nums) >= 3 else nums[0]  # ❌ 没去重
```

**错误原因**：对于 `[2, 2, 3, 1]`，排序后是 `[3,2,2,1]`，直接取 `nums[2]=2` 是错误的

**正确做法**（推荐）：
```python
def thirdMax(self, nums: List[int]) -> int:
    nums.sort(reverse=True)
    diff = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            diff += 1
            if diff == 3:
                return nums[i]
    return nums[0]
```

### 问题二：边界条件处理

**错误做法**（不推荐）：
```python
def thirdMax(self, nums: List[int]) -> int:
    a, b, c = float('-inf'), float('-inf'), float('-inf')
    for num in nums:
        if num > a:
            a, b, c = num, a, b
        elif num > b:  # ❌ 没检查是否已经在a,b,c中
            b, c = num, b
        elif num > c:
            c = num
    return c
```

**错误原因**：对于 `[2, 2, 3]`，重复的 `2` 会被重复处理

**正确做法**（推荐）：
```python
def thirdMax(self, nums: List[int]) -> int:
    a, b, c = float('-inf'), float('-inf'), float('-inf')
    for num in nums:
        if num in (a, b, c):  # ✅ 去重检查
            continue
        if num > a:
            a, b, c = num, a, b
        elif num > b:
            b, c = num, b
        elif num > c:
            c = num
    return c if c != float('-inf') else a  # ✅ 边界检查
```

### 问题三：初始化值选择不当

**错误做法**（不推荐）：
```python
a, b, c = -1, -1, -1  # ❌ 如果所有数都小于-1就出错
```

**正确做法**（推荐）：
```python
a, b, c = float('-inf'), float('-inf'), float('-inf')  # ✅ 负无穷
# 或者
a = b = c = None  # ✅ 空值版本
```


---

## 💡 最佳实践总结

### 算法选择原则
1. **面试场景**：优先使用方法三或方法四，展示优化思维
2. **日常开发**：可以使用方法二，代码更简洁
3. **性能要求**：明确 O(n log n) 和 O(n) 的区别

### 代码质量保证
1. **去重逻辑**：用 `num in (a, b, c)` 判断重复
2. **边界处理**：检查第三大是否存在
3. **初始化**：使用 `float('-inf')` 或 `None` 确保比任何数都小/空

### 常见错误规避
1. **忘记去重**：相同数字只统计一次
2. **边界处理**：数组不足 3 个不同数字时返回最大
3. **初始化错误**：不要使用固定的最小值

---

## 🔚 总结

### 核心要点
- **四种解法**：排序 O(n log n)、有序集合 O(n)、三指针（无穷小/空值）O(n)
- **核心思想**：去重后找第三大的数
- **优化思路**：从排序到有序集合到指针维护的进阶

### 学习价值
- **理解复杂度优化**：从 O(n log n) 到 O(n) 的性能提升
- **掌握指针维护**：用变量维护状态的核心思想
- **实践边界处理**：去重、边界条件等细节处理

### 鼓励语句
加油，未来的算法高手！掌握这道题后，你会对"维护前 K 大"类问题有更深的理解。继续刷题，算法水平会越来越强！

---

## 📚 参考资料与学习建议

### 官方资源
- **力扣（LeetCode）官方题解**：https://leetcode.cn/problems/third-maximum-number/solutions/1032401/di-san-da-de-shu-by-leetcode-solution-h3sp/
  - 提供官方解法、复杂度分析、边界条件处理
- **力扣（LeetCode）题解区**：https://leetcode.cn/problems/third-maximum-number/solutions/
  - 查看官方和社区的其他解法思路和代码分享

### 相关题目推荐
1. **215. 数组中的第K个最大元素** - 练习快速选择算法
2. **347. 前 K 个高频元素** - 练习 Top K 问题
3. **703. 数据流中的第 K 大元素** - 练习动态维护 Top K
4. **删除排序数组中的重复项** - 练习去重技巧
5. **数组中的第 K 个最大元素 II** - 进阶练习

### 学习建议
**方法一：排序 + 去重计数**
- **适用人群**：初学者
- **学习重点**：掌握 `sort()` 方法、理解去重逻辑、练习遍历数组统计
- **实践建议**：先用纸笔模拟排序后的去重过程，再写代码

**方法二：有序集合维护**
- **适用人群**：有一定基础的开发者
- **学习重点**：学习 `SortedList` / `TreeSet` 的使用、理解自动排序和去重特性
- **实践建议**：练习集合的插入、删除、容量限制操作

**方法三：三指针维护（无穷小）**
- **适用人群**：中级开发者
- **学习重点**：理解指针概念、多指针使用场景、维护多个最大值
- **实践建议**：练习处理边界情况（数组长度 < 3）

**方法四：三指针维护（空值）**
- **适用人群**：中级开发者
- **学习重点**：理解 `None` / `null` 的比较规则、掌握初始化技巧
- **实践建议**：与无穷小版本对比，理解两种初始化方式的优劣

### 进阶练习
1. **实现第 K 大的数**：修改代码，实现通用的"第 K 大的数"算法
2. **用其他语言实现**：尝试用 C++、JavaScript 等语言实现相同算法
3. **性能测试**：对不同方法进行性能对比测试，理解复杂度差异

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025年10月29日**
