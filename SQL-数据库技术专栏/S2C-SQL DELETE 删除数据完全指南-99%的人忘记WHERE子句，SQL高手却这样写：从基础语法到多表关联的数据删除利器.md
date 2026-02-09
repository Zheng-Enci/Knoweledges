# S2C-SQL DELETE 删除数据完全指南-99%的人忘记WHERE子句，SQL高手却这样写：从基础语法到多表关联的数据删除利器

## 📝 摘要

99% 的人执行 DELETE 时忘记 WHERE 子句，导致全表数据被误删？SQL 高手却掌握 WHERE 条件、标记删除、数据归档等技巧，数据删除精准安全。本文档用生活化比喻解析 SQL DELETE 删除数据，从基础语法到性能优化，帮你掌握数据删除核心技能，避免数据灾难。

---

> **面试场景**：
> 
> **面试官**：请你说说 SQL DELETE 语句的基本用法？
> 
> **求职者 A（错误回答）**：DELETE 就是删除数据，直接写 `DELETE FROM table` 就行了。
> 
> **面试官**：如果表里有 10000 条数据，你这样写会怎样？
> 
> **求职者 A**：呃...应该只会删除一条吧？
> 
> **面试官**：❌ 错误！这样会删除所有 10000 条数据！这就是为什么 99% 的人会犯的错误。
> 
> **求职者 B（正确回答）**：DELETE 语句用于删除表中已存在的记录。基本语法是 `DELETE FROM table_name WHERE condition`。**WHERE 子句非常重要**，它指定哪些记录需要删除。如果省略 WHERE 子句，所有记录都会被删除，这可能导致数据灾难。
> 
> **面试官**：✅ 正确！看来你掌握了 DELETE 的核心要点。
> 
> 通过这个面试场景，我们可以看到，掌握 DELETE 语句的关键在于理解 WHERE 子句的重要性，以及如何正确使用各种删除技巧。让我们一起来深入学习 SQL DELETE 语句，从基础语法到性能优化，掌握数据删除的核心技能。

## 📑 目录

- [🎯 前置知识点](#-前置知识点)
- [🔍 什么是 DELETE？](#-什么是-delete)
- [❓ 问题描述](#-问题描述)
- [🎯 问题考察点](#-问题考察点)
- [⚡ 快速上手](#-快速上手)
- [🏗️ DELETE 基本语法](#️-delete-基本语法)
- [📊 单表删除](#-单表删除)
- [🔍 DELETE 与 WHERE 子句](#-delete-与-where-子句)
- [🔗 DELETE 与子查询](#-delete-与子查询)
- [🔀 DELETE 与 JOIN](#-delete-与-join)
- [🌐 不同数据库语法差异](#-不同数据库语法差异)
- [⚠️ 注意事项和警告](#️-注意事项和警告)
- [🚀 性能优化](#-性能优化)
- [🆚 对比示例](#-对比示例)
- [🐛 常见错误与修正](#-常见错误与修正)
- [💼 实战应用案例](#-实战应用案例)
- [📚 总结](#-总结)

---

## 🎯 前置知识点

### 基础知识点（必须掌握）

- **数据库表结构**：理解表、字段、记录的概念
- **数据类型**：了解常见数据类型（整数、字符串、日期等）
- **SQL 基础语法**：理解 SQL 语句的基本结构
- **WHERE 子句**：掌握 WHERE 条件筛选的基本用法（参见 [S1D-SQL WHERE 条件筛选完全指南](./S1D-SQL%20WHERE%20条件筛选完全指南-99%25的人只会用等于和大于，SQL高手却这样写：从基础运算符到复杂条件的数据过滤利器.md)）

### 进阶知识点（建议了解）

- **约束（constraint）**：了解主键（primary key）、外键（foreign key）、唯一性约束（unique constraint）的作用
- **子查询（subquery）**：了解子查询的基本概念和使用方法
- **多表关联（JOIN）**：了解表与表之间的关联关系
- **事务（transaction）**：了解事务的基本概念，理解 COMMIT 和 ROLLBACK 的作用

### 学习建议

- **小白（零基础）**：先理解表的基本概念，掌握 DELETE 的基本语法，重点理解 WHERE 子句的重要性
- **初级（刚入门不久）**：学会使用 DELETE 删除单条记录和多条记录，掌握 WHERE 条件的使用
- **中级（入门一段时间）**：掌握 DELETE 与子查询、多表关联删除、标记删除等高级技巧
- **高级（资深开发者）**：理解 DELETE 的性能优化、事务处理、数据归档等高级特性

---

## 🔍 什么是 DELETE？

### 核心概念

**DELETE（删除）** 是 SQL 中用于删除表中已存在记录的语句。

**生活化比喻**：DELETE 就像从图书馆的书籍登记册（表）中删除某条记录。比如某本书已经丢失，需要从登记册中删除这条记录。DELETE 不会删除表结构，只会删除表中的数据记录。

让我们来理解一下 DELETE 语句的本质：它是对表中数据的删除操作，而不是对表结构的修改。

### 为什么需要 DELETE？

#### ❌ 不使用 DELETE 会怎样？

**问题场景**：学生表中某个学生已经退学，需要删除他的记录

**不使用 DELETE**：
- 无法删除已存在的数据
- 只能手动修改表结构（繁琐且容易出错）
- 无法批量删除多条记录
- 无法根据条件选择性删除

#### ✅ 使用 DELETE 的解决方案

```sql
-- 删除学生表中 id 为 1 的学生的记录
DELETE FROM students 
WHERE id = 1;
```

**优势**：
- ✅ 可以直接删除已存在的数据
- ✅ 操作简单，一条语句即可完成
- ✅ 可以批量删除多条记录
- ✅ 可以根据条件选择性删除
- ✅ 可以配合事务进行回滚操作

---

## ❓ 问题描述

### 真实场景

想象一下这样的场景：你在一家电商公司工作，负责维护订单表。某天，产品经理告诉你："我们需要删除所有已取消且超过 30 天的订单记录。"

**新手做法**：
- 先查询所有符合条件的订单
- 一条一条手动删除每条记录
- 或者写一个循环，逐条删除

**问题**：
- 效率低下，如果符合条件的订单有 10000 个，需要执行 10000 次删除操作
- 容易出错，可能漏掉某些订单
- 代码复杂，需要写循环逻辑
- **最危险的是**：如果忘记添加 WHERE 条件，会删除所有订单数据！

**SQL 高手做法**：
```sql
-- 一条 DELETE 语句搞定
DELETE FROM orders 
WHERE status = 'CANCELLED' 
  AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

**优势**：
- ✅ 一条语句完成所有删除
- ✅ 效率高，数据库自动优化执行
- ✅ 不会漏掉任何符合条件的记录
- ✅ 代码简洁，易于维护
- ✅ 可以先用 SELECT 测试，确认无误后再执行 DELETE

### 核心痛点

1. **忘记 WHERE 子句**：99% 的人在执行 DELETE 时忘记添加 WHERE 条件，导致全表数据被误删
2. **不知道如何批量删除**：面对大量数据需要删除时，不知道如何高效处理
3. **多表关联删除困难**：需要根据其他表的数据来删除当前表时，不知道如何写 SQL
4. **性能问题**：删除大量数据时，不知道如何优化性能
5. **数据恢复困难**：误删数据后，不知道如何恢复

---

## 🎯 问题考察点

通过本文档的学习，你将掌握以下核心知识点：

### 基础能力 🔥 Must

1. **DELETE 基本语法**：掌握 DELETE 语句的基本结构和语法规则
2. **WHERE 子句使用**：理解 WHERE 子句的重要性，掌握条件筛选的写法
3. **单表删除**：学会删除单条记录、多条记录，以及删除前检查的方法

### 进阶能力 ⭐ Should

4. **子查询删除**：学会使用子查询来删除数据，理解 EXISTS 条件的重要性
5. **多表关联删除**：掌握 MySQL、SQL Server 等不同数据库的多表关联删除语法
6. **标记删除**：理解标记删除 vs 物理删除的区别，掌握标记删除的最佳实践

### 高级能力 💡 Could

7. **性能优化**：了解 DELETE vs TRUNCATE、数据归档、分批删除、行锁优化等性能优化技巧
8. **不同数据库差异**：了解 MySQL、Oracle、SQL Server、PostgreSQL 等数据库的语法差异
9. **实战应用**：掌握各种实际业务场景下的 DELETE 应用技巧

---

## ⚡ 快速上手 🔥 Must

让我们通过一个最简单的例子来快速了解 DELETE 语句的使用方法。通过这个例子，我们可以快速理解 DELETE 语句的基本用法。

### 最简单的 DELETE 示例

假设我们有一个学生表 `students`，现在需要删除 id 为 1 的学生的记录。

```sql
-- 删除学生表中 id 为 1 的学生的记录
DELETE FROM students 
WHERE id = 1;
```

**逐行代码解释**：

```sql
-- DELETE FROM 作用：指定要删除数据的表
DELETE FROM students 

-- WHERE 作用：指定删除条件，只删除 id 为 1 的记录
WHERE id = 1;
```

**执行结果**：
- 如果 id 为 1 的记录存在，则删除该记录
- 如果 id 为 1 的记录不存在，则不删除任何记录（不会报错）

**重要提醒**：⚠️ **WHERE 子句非常重要！** 如果省略 WHERE 子句，会删除表中的所有记录！详细说明请参见 [DELETE 与 WHERE 子句](#-delete-与-where-子句) 章节。

---

## 🏗️ DELETE 基本语法 🔥 Must

### 基本语法结构

**标准语法**：
```sql
DELETE FROM table_name 
WHERE condition;
```

**语法说明**：
- `DELETE FROM`：删除命令关键字
- `table_name`：要删除数据的表名
- `WHERE condition`：删除条件，用于指定哪些数据要删除（**可选，但强烈建议使用**）

### 参数说明

| 参数 | 说明 | 是否必需 |
|------|------|---------|
| `table_name` | 要删除数据的表名 | ✅ 必需 |
| `WHERE condition` | 删除条件 | ⚠️ 可选，但强烈建议使用 |

### 重要提醒

⚠️ **WHERE 子句的重要性**和**删除前检查**的详细说明，请参见 [DELETE 与 WHERE 子句](#-delete-与-where-子句) 章节。

---

## 📊 单表删除 🔥 Must

### 删除单条记录

**语法**：
```sql
DELETE FROM table_name 
WHERE condition;
```

**示例 1：删除指定 ID 的记录**
```sql
-- 删除学生表中 id 为 1 的学生的记录
DELETE FROM students 
WHERE id = 1;
```

**示例 2：删除指定姓名的记录**
```sql
-- 删除学生表中姓名为"张三"的学生的记录
DELETE FROM students 
WHERE name = '张三';
```

**示例 3：删除指定条件的记录**
```sql
-- 删除学生表中成绩小于 60 分的学生的记录
DELETE FROM students 
WHERE score < 60;
```

### 删除多条记录

**语法**：与删除单条记录相同，WHERE 条件匹配多条记录即可

**示例 1：删除符合条件的多条记录**
```sql
-- 删除学生表中成绩小于 60 分的所有学生的记录
DELETE FROM students 
WHERE score < 60;
```

**示例 2：使用 IN 删除多条记录**
```sql
-- 删除学生表中 id 为 1、2、3 的学生的记录
DELETE FROM students 
WHERE id IN (1, 2, 3);
```

**示例 3：使用 BETWEEN 删除范围内的记录**
```sql
-- 删除学生表中 id 在 1 到 100 之间的学生的记录
DELETE FROM students 
WHERE id BETWEEN 1 AND 100;
```

### 删除所有记录

**语法**：
```sql
DELETE FROM table_name;
```

**示例**：
```sql
-- 删除学生表中的所有记录
DELETE FROM students;
```

**重要提醒**：
- ⚠️ **这会删除表中的所有记录！**
- ⚠️ **表结构、属性和索引将保持不变**
- ⚠️ **如果要删除所有记录，建议使用 TRUNCATE TABLE（性能更好）**

**TRUNCATE vs DELETE**：
- `TRUNCATE TABLE` 比 `DELETE` 更快
- `TRUNCATE TABLE` 使用较少的系统和事务日志资源
- `TRUNCATE TABLE` 不能回滚（某些数据库）

---

## 🔍 DELETE 与 WHERE 子句 🔥 Must

### WHERE 子句的重要性

**WHERE 子句是 DELETE 语句的核心**，它决定了哪些记录会被删除。我们来深入理解一下 WHERE 子句的重要性。

**重要原则**：
- ✅ **始终使用 WHERE 子句**：除非你真的想删除所有记录
- ✅ **删除前检查**：先用 SELECT 测试 WHERE 条件
- ✅ **条件要精确**：确保 WHERE 条件准确匹配要删除的记录

### 使用单个条件

**示例 1：使用等于条件**
```sql
-- 删除 id 为 1 的记录
DELETE FROM students 
WHERE id = 1;
```

**示例 2：使用大于条件**
```sql
-- 删除 id 大于 100 的记录
DELETE FROM students 
WHERE id > 100;
```

**示例 3：使用 LIKE 条件**
```sql
-- 删除姓名以"张"开头的记录
DELETE FROM students 
WHERE name LIKE '张%';
```

### 使用多个条件

**示例 1：使用 AND 连接多个条件**
```sql
-- 删除成绩小于 60 分且年龄大于 20 岁的学生的记录
DELETE FROM students 
WHERE score < 60 AND age > 20;
```

**示例 2：使用 OR 连接多个条件**
```sql
-- 删除成绩小于 60 分或年龄大于 25 岁的学生的记录
DELETE FROM students 
WHERE score < 60 OR age > 25;
```

**示例 3：使用 NOT 条件**
```sql
-- 删除成绩不小于 60 分的学生的记录
DELETE FROM students 
WHERE NOT score < 60;
```

### 使用 NULL 条件

**示例 1：删除 NULL 值**
```sql
-- 删除 email 为 NULL 的记录
DELETE FROM students 
WHERE email IS NULL;
```

**示例 2：删除非 NULL 值**
```sql
-- 删除 email 不为 NULL 的记录
DELETE FROM students 
WHERE email IS NOT NULL;
```

### 删除前检查的最佳实践

**建议流程**：

1. **第一步：先用 SELECT 查看会删除哪些记录**
```sql
-- 查看要删除的记录
SELECT * FROM students WHERE score < 60;
```

2. **第二步：确认记录数量和内容**
```sql
-- 查看要删除的记录数量
SELECT COUNT(*) FROM students WHERE score < 60;
```

3. **第三步：确认无误后，再执行 DELETE**
```sql
-- 执行删除
DELETE FROM students WHERE score < 60;
```

---

## 🔗 DELETE 与子查询 ⭐ Should

### 基于子查询删除

让我们来看看如何使用子查询来删除数据。通过子查询，我们可以根据其他表的数据来决定要删除哪些记录。

**语法**：
```sql
DELETE FROM table_name 
WHERE column_name IN (SELECT column_name FROM other_table WHERE condition);
```

**示例 1：基于另一个表的数据删除**
```sql
-- 删除销售人员的配额历史记录，这些销售人员的年度销售额超过 2500000
DELETE FROM Sales.SalesPersonQuotaHistory   
WHERE BusinessEntityID IN   
    (SELECT BusinessEntityID   
     FROM Sales.SalesPerson   
     WHERE SalesYTD > 2500000.00);
```

**示例 2：使用 EXISTS 条件删除**
```sql
-- 删除存在关联订单的客户记录
DELETE FROM customers 
WHERE EXISTS (
    SELECT 1 
    FROM orders 
    WHERE orders.customer_id = customers.id
);
```

### 使用 EXISTS 的优势

**EXISTS vs IN**：
- `EXISTS` 通常比 `IN` 性能更好
- `EXISTS` 在找到第一个匹配项后就会停止搜索
- `IN` 需要先执行子查询，然后进行匹配

**示例：使用 EXISTS 优化删除**
```sql
-- 使用 EXISTS 删除存在关联订单的客户记录
DELETE FROM customers 
WHERE EXISTS (
    SELECT 1 
    FROM orders 
    WHERE orders.customer_id = customers.id
      AND orders.status = 'CANCELLED'
);
```

---

## 🔀 DELETE 与 JOIN ⭐ Should

### MySQL 多表关联删除

**语法**：
```sql
DELETE t1 FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.id
WHERE condition;
```

**示例 1：使用 INNER JOIN 删除**
```sql
-- 删除销售人员的配额历史记录，这些销售人员的年度销售额超过 4500000
DELETE sq
FROM Sales.SalesPersonQuotaHistory sq
     INNER JOIN Sales.SalesPerson sp ON sq.BusinessEntityID = sp.BusinessEntityID
WHERE sp.SalesYTD > 4500000.00;
```

**示例 2：使用 LEFT JOIN 删除**
```sql
-- 删除没有关联订单的客户记录
DELETE c
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

### SQL Server 多表关联删除

**语法 1：使用 FROM 子句**
```sql
DELETE FROM table1
FROM table1
INNER JOIN table2 ON table1.id = table2.id
WHERE condition;
```

**语法 2：使用 DELETE 别名**
```sql
DELETE t1
FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.id
WHERE condition;
```

**示例**：
```sql
-- 删除销售人员的配额历史记录
DELETE FROM Sales.SalesPersonQuotaHistory
FROM Sales.SalesPersonQuotaHistory AS spqh
INNER JOIN Sales.SalesPerson AS sp
ON spqh.BusinessEntityID = sp.BusinessEntityID
WHERE sp.SalesYTD > 2500000.00;
```

---

## 🌐 不同数据库语法差异 💡 Could

### MySQL

**特点**：
- 支持使用 `LIMIT` 限制删除的行数
- 可以通过设置 `sql_safe_updates` 强制要求 WHERE 条件
- DELETE 语句会返回删除的行数

**安全模式设置**：
```sql
-- 开启安全更新模式，强制要求 WHERE 条件
SET sql_safe_updates = 1;
```

**使用 LIMIT 删除**：
```sql
-- 删除前 100 条符合条件的记录
DELETE FROM students 
WHERE score < 60
LIMIT 100;
```

**返回结果示例**：
```sql
-- 删除 id=1 的记录
mysql> DELETE FROM students WHERE id=1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

-- 删除 id=999 的记录（不存在）
mysql> DELETE FROM students WHERE id=999;
Query OK, 0 rows affected (0.00 sec)
Rows matched: 0  Changed: 0  Warnings: 0
```

### SQL Server

**特点**：
- 支持使用 `TOP` 限制删除的行数
- 支持使用 `OUTPUT` 子句返回删除的行
- 支持使用 CTE（公用表表达式）
- 支持使用游标进行定位删除

**TOP 语法**：
```sql
DELETE TOP (20) FROM table_name WHERE condition;
```

**OUTPUT 语法**：
```sql
DELETE FROM table_name
OUTPUT DELETED.*
WHERE condition;
```

**示例：使用 OUTPUT 返回删除的行**
```sql
-- 删除并返回删除的行
DELETE Sales.ShoppingCartItem  
OUTPUT DELETED.*   
WHERE ShoppingCartID = 20621;
```

### Oracle

**特点**：
- 支持使用 `ROWNUM` 限制删除的行数
- 语法相对标准

**示例**：
```sql
DELETE FROM table_name
WHERE ROWNUM <= 100;
```

### PostgreSQL

**特点**：
- 语法相对标准
- 支持 `RETURNING` 子句返回删除的行

**RETURNING 语法**：
```sql
DELETE FROM table_name
WHERE condition
RETURNING *;
```

**示例**：
```sql
-- 删除并返回删除的行
DELETE FROM students
WHERE score < 60
RETURNING *;
```

---

## ⚠️ 注意事项和警告

### WHERE 子句的重要性

⚠️ **重要警告**：在删除记录时要格外小心！因为您不能重来！

**核心要点**：
- 如果省略 WHERE 子句，所有的记录都将被删除！
- 执行没有 WHERE 子句的 DELETE 要慎重，再慎重！

**详细说明和最佳实践**，请参见 [DELETE 与 WHERE 子句](#-delete-与-where-子句) 章节。

### 删除前检查

**建议**：始终建议从 SELECT 语句开始，然后再删除任何内容，以确保定位的是正确的记录。

**详细检查方法和最佳实践**，请参见 [DELETE 与 WHERE 子句](#-delete-与-where-子句) 章节中的"删除前检查的最佳实践"小节。

### 外键约束的影响

**说明**：
- 大多数数据库系统都支持外键约束，因此当删除表中的一行时，外键表中的行也会自动删除（如果设置了 CASCADE）
- 从逻辑上讲，如果不引用员工，就不能存在依赖关系。换句话说，当删除员工信息时，他/她的家属也必须要删除

**示例**：
```sql
-- 删除员工及其相关依赖
DELETE
FROM employees
WHERE employee_id = 199;

DELETE
FROM dependents
WHERE employee_id = 199;
```

**注意**：
- 如果表之间存在外键关系，删除主表记录时可能会影响从表记录
- 需要根据外键约束的配置（CASCADE、SET NULL 等）来处理

### 事务处理

**使用事务确保数据一致性**：
```sql
-- 开始事务
START TRANSACTION;

-- 执行删除操作
DELETE FROM students 
WHERE score < 80;

-- 检查删除结果
SELECT COUNT(*) FROM students WHERE score >= 80;

-- 如果结果正确，提交事务
COMMIT;

-- 如果结果不正确，回滚事务
-- ROLLBACK;
```

**优势**：
- ✅ 确保数据一致性
- ✅ 可以回滚错误的删除
- ✅ 保证原子性操作

### 回滚操作

**说明**：
- 由于 DELETE 语句是 DML 操作，它可以在语句中执行时回滚
- 如果您意外删除记录或需要重复该过程，可以使用 ROLLBACK 命令

**示例**：
```sql
START TRANSACTION;
DELETE FROM students WHERE score < 60;
-- 如果需要，可以回滚删除
ROLLBACK;
```

**说明**：
- ROLLBACK 命令将撤销 DELETE 语句所做的更改，有效地恢复在事务期间删除的记录

### 无匹配记录的处理

**说明**：
- 如果 WHERE 条件没有匹配到任何记录，DELETE 语句不会报错，也不会有任何记录被删除

**示例**：
```sql
-- 删除 id 为 999 的记录（假设不存在）
DELETE FROM students 
WHERE id = 999;
```

**执行结果**：
- 不会报错
- 不会删除任何记录
- MySQL 会返回 `Rows matched: 0  Changed: 0`

**建议**：
- 如果需要确认是否有记录被删除，可以检查 DELETE 语句的返回结果

### 触发器的影响

**说明**：
- DELETE 语句可能会因为违反触发器或尝试删除另一个表中具有 FOREIGN KEY 约束的数据引用的行而失败
- 如果 DELETE 删除多行，并且任何被删除的行违反触发器或约束，则语句被取消，返回错误，并且不删除任何行

### 错误处理

**使用 TRY...CATCH 处理错误（SQL Server）**：
```sql
BEGIN TRY
    DELETE FROM table_name WHERE condition;
END TRY
BEGIN CATCH
    -- 错误处理逻辑
    SELECT ERROR_MESSAGE();
END CATCH;
```

---

## 🚀 性能优化 💡 Could

### DELETE vs TRUNCATE

我们来对比一下 DELETE 和 TRUNCATE 的区别，这对于性能优化非常重要。

**区别说明**：

1. **对于删除整个表的所有数据时，DELETE 并不会释放表所占用的空间**
2. **如果用户确定是删除整表的所有数据，那么使用 TRUNCATE TABLE 速度更快**

**示例**：
```sql
-- 删除所有部门信息:使用 DELETE
DELETE FROM table_name;

-- 删除所有部门信息:使用 TRUNCATE
TRUNCATE TABLE table_name;
```

**TRUNCATE TABLE 的优势**：
- ✅ TRUNCATE TABLE 比 DELETE 更快
- ✅ TRUNCATE TABLE 使用较少的系统和事务日志资源
- ✅ TRUNCATE TABLE 有限制，例如，表不能参与复制

**最佳实践**：
- 要删除表中的所有行，请使用 TRUNCATE TABLE
- TRUNCATE TABLE 比 DELETE 更快，并且使用较少的系统和事务日志资源

### 标记删除 vs 物理删除

让我们来理解一下标记删除和物理删除的区别。这是实际开发中非常重要的最佳实践。

**问题**：
- 通过从 InnoDB 存储空间分布，DELETE 对性能的影响可以看到，DELETE 物理删除既不能释放磁盘空间，而且会产生大量的碎片，导致索引频繁分裂，影响 SQL 执行计划的稳定性
- 同时在碎片回收时，会耗用大量的 CPU，磁盘空间，影响表上正常的 DML 操作

**解决方案**：
- 在业务代码层面，应该做逻辑标记删除，避免物理删除

**实现方式**：
- 在 MySQL 数据库建模规范中有 4 个公共字段，基本上每个表必须有的，同时在 create_time 列要创建索引

**字段定义**：
```sql
`id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',
`is_deleted` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否逻辑删除：0：未删除，1：已删除',
`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
```

**使用方式**：
```sql
-- 有了删除标记，业务接口的 DELETE 操作就可以转换为 UPDATE
UPDATE user SET is_deleted = 1 WHERE user_id = 1213;

-- 查询的时候需要带上 is_deleted 过滤
SELECT id, age, phone FROM user WHERE is_deleted = 0 AND name LIKE 'lyn12%';
```

### 数据归档方式

**通用数据归档方法**：

**步骤 1：创建归档表**
```sql
CREATE TABLE `ota_order_bak` (
  -- 表结构定义
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (to_days(create_time)) ( 
  PARTITION p201808 VALUES LESS THAN (to_days('2018-09-01')), 
  -- 更多分区...
);
```

**步骤 2：插入原表中无效的数据**
```sql
CREATE TABLE tbl_p201808 AS 
SELECT * FROM ota_order 
WHERE create_time BETWEEN '2018-08-01 00:00:00' AND '2018-08-31 23:59:59';
```

**步骤 3：跟归档表分区做分区交换**
```sql
ALTER TABLE ota_order_bak EXCHANGE PARTITION p201808 WITH TABLE tbl_p201808;
```

**步骤 4：删除原表中已经归档的数据**
```sql
DELETE FROM ota_order 
WHERE create_time BETWEEN '2018-08-01 00:00:00' AND '2018-08-31 23:59:59' 
LIMIT 3000;
```

**优势**：
- 这样原表和归档表都是按月的分区表，只需要创建一个中间普通表，在业务低峰期做两次分区交换，既可以删除无效数据，又能回收空间，而且没有空间碎片，不会影响表上的索引及 SQL 的执行计划

### 分批删除

**当需要删除大量数据时，可以分批进行删除，避免一次性删除过多数据影响性能**

**方式 1：使用 LIMIT 分批删除（MySQL）**
```sql
-- 每次只删除 1000 条
DELETE FROM students 
WHERE score < 80
LIMIT 1000;
```

**方式 2：使用循环分批删除**
```sql
-- 第一次删除 id 1-1000
DELETE FROM students 
WHERE score < 80 AND id BETWEEN 1 AND 1000;

-- 第二次删除 id 1001-2000
DELETE FROM students 
WHERE score < 80 AND id BETWEEN 1001 AND 2000;
```

**优势**：
- ✅ 减少锁表时间
- ✅ 降低对数据库性能的影响
- ✅ 可以随时中断和恢复

### 行锁优化

**在 MySQL 中，当执行 `DELETE xxxx WHERE topic_id = xxx` 时，MySQL 会对 topic_id 索引加行锁**

**问题场景**：
- 在高并发场景下，如果多个操作在同一个事务中，行锁的持有时间会延长
- 可以通过调整操作顺序来降低行锁的持有粒度

**优化示例**：

原逻辑（性能较差）：
```sql
START TRANSACTION;
-- 第一步：DELETE（加行锁）
DELETE FROM topics WHERE topic_id = 1;
-- 第二步：INSERT（行锁一直持有，直到事务结束）
INSERT INTO results (topic_id, result) VALUES (1, 'AC');
COMMIT;
```

优化后（性能更好）：
```sql
START TRANSACTION;
-- 第一步：INSERT（不加行锁或加锁时间短）
INSERT INTO results (topic_id, result) VALUES (1, 'AC');
-- 第二步：DELETE（行锁持有时间短）
DELETE FROM topics WHERE topic_id = 1;
COMMIT;
```

### 索引的使用

**对于 DELETE 语句中涉及的列，确保相应的列上建有索引，以提高检索速度**

**注意事项**：
- WHERE 条件中的字段应该有索引
- 但索引也会影响 DELETE 的性能（需要更新索引）
- 需要权衡查询速度和删除速度

### 大数据删除的注意事项

**大数据删除要注意**：
- ✅ **索引**：确保 WHERE 条件字段有索引
- ✅ **分批删除**：避免一次性删除过多数据
- ✅ **事务**：使用事务确保数据一致性

**重要提醒**：
- ⚠️ 如果删除条件不精准，可能导致大面积锁表，影响其他业务

---

## 🆚 对比示例 ⭐ Should

### 不使用 DELETE vs 使用 DELETE

**场景**：需要删除学生表中成绩小于 60 分的所有记录

**❌ 不使用 DELETE（手动删除）**：
- 需要先查询所有符合条件的记录
- 然后逐条手动删除
- 效率低下，容易出错

**✅ 使用 DELETE（一条语句搞定）**：
```sql
-- 一条 DELETE 语句完成所有删除
DELETE FROM students 
WHERE score < 60;
```

**优势**：
- ✅ 操作简单，一条语句即可完成
- ✅ 效率高，数据库自动优化执行
- ✅ 不会漏掉任何符合条件的记录
- ✅ 代码简洁，易于维护

### 错误写法 vs 正确写法

**❌ 错误写法 1：忘记 WHERE 子句**
```sql
-- 危险！这会删除所有记录
DELETE FROM students;
```

**✅ 正确写法 1：始终使用 WHERE 子句**
```sql
-- 正确：指定删除条件
DELETE FROM students 
WHERE id = 1;
```

**❌ 错误写法 2：删除前不检查**
```sql
-- 危险！可能删除错误的记录
DELETE FROM students 
WHERE score < 60;
```

**✅ 正确写法 2：删除前先检查**
```sql
-- 第一步：先查询要删除的记录
SELECT * FROM students WHERE score < 60;

-- 第二步：确认无误后，再执行删除
DELETE FROM students 
WHERE score < 60;
```

**❌ 错误写法 3：不使用事务**
```sql
-- 危险！如果删除出错，无法回滚
DELETE FROM students 
WHERE score < 60;
```

**✅ 正确写法 3：使用事务确保安全**
```sql
-- 开始事务
START TRANSACTION;

-- 执行删除操作
DELETE FROM students 
WHERE score < 60;

-- 检查删除结果
SELECT COUNT(*) FROM students WHERE score >= 60;

-- 如果结果正确，提交事务
COMMIT;

-- 如果结果不正确，回滚事务
-- ROLLBACK;
```

### 物理删除 vs 标记删除

**❌ 物理删除（不推荐）**：
```sql
-- 直接删除记录
DELETE FROM user WHERE user_id = 1213;
```

**问题**：
- ❌ 无法恢复数据
- ❌ 会产生大量碎片
- ❌ 影响性能

**✅ 标记删除（推荐）**：
```sql
-- 使用标记删除
UPDATE user SET is_deleted = 1 WHERE user_id = 1213;

-- 查询时过滤已删除的记录
SELECT * FROM user WHERE is_deleted = 0;
```

**优势**：
- ✅ 可以恢复数据
- ✅ 不会产生碎片
- ✅ 性能更好

---

## 🐛 常见错误与修正 🔥 Must

### 错误 1：忘记 WHERE 子句

**错误现象**：
```sql
-- ❌ 危险！这会删除所有记录
DELETE FROM students;
```

**问题分析**：
- 这是最常见的错误，99% 的人会犯这个错误
- 如果省略 WHERE 子句，所有记录都将被删除

**修正方法和预防措施**，请参见 [DELETE 与 WHERE 子句](#-delete-与-where-子句) 章节。

### 错误 2：删除前不检查

**错误现象**：
```sql
-- ❌ 危险！可能删除错误的记录
DELETE FROM students 
WHERE score < 60;
```

**问题分析**：
- 没有先查询要删除的记录，直接执行删除
- 可能删除错误的记录，无法恢复

**修正方法和预防措施**，请参见 [DELETE 与 WHERE 子句](#-delete-与-where-子句) 章节中的"删除前检查的最佳实践"小节。

### 错误 3：条件不精确

**错误现象**：
```sql
-- ❌ 危险！可能删除错误的记录
DELETE FROM students 
WHERE name = '张';
```

**问题分析**：
- 条件不精确，可能匹配到多条记录
- 如果只想删除一条记录，应该使用唯一标识（如 id）

**修正方法**：
```sql
-- ✅ 正确：使用唯一标识删除
DELETE FROM students 
WHERE id = 1;

-- ✅ 或者：使用更精确的条件
DELETE FROM students 
WHERE name = '张三' AND id = 1;
```

**预防措施**：
- 尽量使用唯一标识（如主键）删除
- 如果使用非唯一字段，确保条件足够精确
- 删除前先查询，确认匹配的记录数量

### 错误 4：不使用事务

**错误现象**：
```sql
-- ❌ 危险！如果删除出错，无法回滚
DELETE FROM students 
WHERE score < 60;
```

**问题分析**：
- 没有使用事务，如果删除出错，无法回滚
- 对于重要的数据删除操作，应该使用事务

**修正方法**：
```sql
-- ✅ 正确：使用事务确保安全
START TRANSACTION;

-- 执行删除操作
DELETE FROM students 
WHERE score < 60;

-- 检查删除结果
SELECT COUNT(*) FROM students WHERE score >= 60;

-- 如果结果正确，提交事务
COMMIT;

-- 如果结果不正确，回滚事务
-- ROLLBACK;
```

**预防措施**：
- 对于重要的数据删除操作，始终使用事务
- 删除后检查结果，确认无误后再提交
- 如果结果不正确，立即回滚

### 错误 5：性能问题

**错误现象**：
```sql
-- ❌ 性能问题：一次性删除大量数据
DELETE FROM students 
WHERE score < 60;
-- 如果符合条件的记录有 100 万条，这会很慢
```

**问题分析**：
- 一次性删除大量数据，会导致锁表时间过长
- 影响其他业务的正常执行

**修正方法**：
```sql
-- ✅ 正确：分批删除
-- 每次只删除 1000 条
DELETE FROM students 
WHERE score < 60
LIMIT 1000;

-- 重复执行，直到删除完成
```

**预防措施**：
- 对于大量数据的删除，使用分批删除
- 在业务低峰期执行删除操作
- 监控删除进度，确保不影响其他业务

---

## 💼 实战应用案例 ⭐ Should

### 案例 1：删除过期订单

**场景**：删除所有已取消且超过 30 天的订单记录

**解决方案**：
```sql
-- 第一步：先查询要删除的记录
SELECT * FROM orders 
WHERE status = 'CANCELLED' 
  AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- 第二步：确认无误后，执行删除
DELETE FROM orders 
WHERE status = 'CANCELLED' 
  AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

**优化建议**：
- 如果订单数量很大，建议分批删除
- 在业务低峰期执行删除操作
- 使用事务确保数据一致性

### 案例 2：删除无效用户

**场景**：删除所有注册但从未登录的用户记录

**解决方案**：
```sql
-- 使用子查询删除
DELETE FROM users 
WHERE id NOT IN (
    SELECT DISTINCT user_id 
    FROM login_logs
);
```

**或者使用 EXISTS**：
```sql
-- 使用 EXISTS 删除（性能更好）
DELETE FROM users 
WHERE NOT EXISTS (
    SELECT 1 
    FROM login_logs 
    WHERE login_logs.user_id = users.id
);
```

### 案例 3：删除重复数据

**场景**：删除学生表中的重复记录（保留 id 最小的记录）

**解决方案**：
```sql
-- 使用子查询删除重复记录
DELETE FROM students 
WHERE id NOT IN (
    SELECT MIN(id) 
    FROM students 
    GROUP BY name, email
);
```

**或者使用窗口函数（SQL Server）**：
```sql
-- 使用 CTE 和 ROW_NUMBER() 删除重复记录
WITH CTE AS (
    SELECT *, 
           ROW_NUMBER() OVER(PARTITION BY name, email ORDER BY id) AS Row_Num
    FROM students
)
DELETE FROM CTE
WHERE Row_Num > 1;
```

### 案例 4：多表关联删除

**场景**：删除所有没有订单的客户记录

**解决方案（MySQL）**：
```sql
-- 使用 LEFT JOIN 删除
DELETE c
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

**解决方案（SQL Server）**：
```sql
-- 使用子查询删除
DELETE FROM customers 
WHERE id NOT IN (
    SELECT DISTINCT customer_id 
    FROM orders
);
```

### 案例 5：标记删除实现

**场景**：实现软删除（标记删除），而不是物理删除

**解决方案**：
```sql
-- 第一步：在表中添加 is_deleted 字段
ALTER TABLE users 
ADD COLUMN is_deleted TINYINT(1) NOT NULL DEFAULT 0 
COMMENT '是否删除：0-未删除，1-已删除';

-- 第二步：删除操作改为更新操作
UPDATE users 
SET is_deleted = 1 
WHERE id = 1;

-- 第三步：查询时过滤已删除的记录
SELECT * FROM users 
WHERE is_deleted = 0;
```

**优势**：
- ✅ 可以恢复数据
- ✅ 不会产生碎片
- ✅ 性能更好
- ✅ 可以记录删除时间

---

## 📚 总结

通过本文档的学习，我们掌握了 SQL DELETE 语句的核心技能。让我们来总结一下关键要点：

### 核心要点回顾

1. **WHERE 子句的重要性**：⚠️ 这是 DELETE 语句最核心的要点，99% 的人会忘记 WHERE 子句，导致全表数据被误删
2. **删除前检查**：✅ 始终建议从 SELECT 语句开始，然后再删除任何内容，以确保定位的是正确的记录
3. **标记删除 vs 物理删除**：✅ 在业务代码层面，应该做逻辑标记删除，避免物理删除
4. **性能优化**：✅ 对于大量数据的删除，使用分批删除、数据归档等方式优化性能
5. **事务处理**：✅ 对于重要的数据删除操作，始终使用事务，确保数据一致性

### 最佳实践总结

1. **始终使用 WHERE 子句**：执行没有 WHERE 子句的 DELETE 要慎重，再慎重
2. **删除前检查**：先用 SELECT 测试 WHERE 条件，确认无误后再执行 DELETE
3. **使用标记删除**：在业务代码层面，应该做逻辑标记删除，避免物理删除
4. **数据归档**：为了实现数据归档需求，可以用采用 MySQL 分区表特性来实现
5. **权限控制**：控制业务账号权限，只授予必要的 DML 权限，不授予 DELETE 权限
6. **性能优化**：
   - 使用索引提高查询速度
   - 分批删除大量数据
   - 使用事务确保数据一致性
   - 调整操作顺序降低行锁持有粒度

### 写在最后

💪 **掌握 DELETE 语句的关键在于理解 WHERE 子句的重要性，以及如何正确使用各种删除技巧。** 通过本文档的学习，相信你已经掌握了 SQL DELETE 语句的核心技能。在实际工作中，记住：**删除数据要谨慎，WHERE 子句不能忘！**

🚀 **让我们一起成为 SQL 高手，掌握数据删除的核心技能，避免数据灾难！**

---

**作者**：郑恩赐  
**机构**：厦门工学院人工智能创作坊  
**日期**：2025 年 01 月 27 日

