# J5B-@Entity注解详解-实体映射的核心基石

## 概述

`@Entity`注解是Java持久化API（JPA）中最核心的注解之一，用于将一个普通的Java类（POJO）声明为持久化实体。被`@Entity`注解标记的类，其实例将映射到数据库中的一张表，每个实例对应表中的一行数据。

## 基本语法

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface Entity {
    String name() default "";
}
```

## 基本用法

### 1. 最简单的实体类

```java
import javax.persistence.Entity;

@Entity
public class User {
    // 实体类定义
}
```

### 2. 指定实体名称

```java
@Entity(name = "UserEntity")
public class User {
    // 实体名称用于JPQL查询中引用
}
```

## @Entity注解的属性

### name属性

**作用**：指定实体的名称，用于JPQL查询中引用

**默认值**：空字符串（使用类名作为实体名）

**使用场景**：
- 需要在JPQL查询中使用不同的名称引用实体
- 避免类名与JPQL关键字冲突

**示例**：
```java
@Entity(name = "UserEntity")
public class User {
    @Id
    private Long id;
    private String username;
}

// 在JPQL查询中使用实体名称
@Query("SELECT u FROM UserEntity u WHERE u.username = :username")
User findByUsername(@Param("username") String username);
```

## 实体类的基本要求

### 1. 无参构造方法

**要求**：实体类必须提供一个公共或受保护的无参数构造方法

**原因**：
- JPA使用反射机制来实例化实体对象
- JPA提供者（如Hibernate）需要调用无参构造方法来创建对象实例
- 代理对象和懒加载功能也依赖于无参构造方法

**JPA规范要求**：
- 必须是`public`或`protected`访问级别
- 不能是`private`访问级别
- 如果类中有其他带参构造方法，必须显式定义无参构造方法

```java
@Entity
public class User {
    private Long id;
    private String username;
    
    // 必须有无参构造方法（public或protected）
    public User() {
    }
    
    // 可以有带参构造方法
    public User(String username) {
        this.username = username;
    }
}

// 也可以使用protected访问级别
@Entity
public class Product {
    private Long id;
    private String name;
    
    // protected访问级别也满足JPA要求
    protected Product() {
    }
    
    public Product(String name) {
        this.name = name;
    }
}
```

**常见错误**：
```java
// 错误：缺少无参构造方法
@Entity
public class User {
    private Long id;
    private String username;
    
    // 只有带参构造方法，没有无参构造方法
    public User(String username) {
        this.username = username;
    }
    // 编译错误：JPA无法实例化此实体
}

// 错误：无参构造方法是private
@Entity
public class User {
    private Long id;
    private String username;
    
    // 错误：private访问级别不满足JPA要求
    private User() {
    }
}
```

### 2. 主键标识

**要求**：每个实体类必须有一个被`@Id`注解标识的主键字段

```java
@Entity
public class User {
    @Id
    private Long id;  // 主键字段
    
    private String username;
}
```

### 3. 类的基本限制

**要求**：
- 实体类不能是`final`的
- 实体类不能包含`final`的方法
- 实体类不能是非静态的内部类

```java
// 正确示例
@Entity
public class User {
    // 实体类定义
}

// 错误示例
@Entity
public final class User {  // 错误：不能是final类
    public final void someMethod() {  // 错误：不能有final方法
    }
}

@Entity
public class OuterClass {
    @Entity
    public class InnerClass {  // 错误：不能是非静态内部类
    }
}
```

## 完整示例

### 基础实体类

```java
import javax.persistence.*;
import java.io.Serializable;
import java.time.LocalDateTime;

@Entity
@Table(name = "users")
public class User implements Serializable {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", nullable = false, length = 50)
    private String username;
    
    @Column(name = "email", unique = true, nullable = false)
    private String email;
    
    @Column(name = "password", nullable = false)
    private String password;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // 无参构造方法
    public User() {
    }
    
    // 带参构造方法
    public User(String username, String email, String password) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }
    
    // Getter和Setter方法
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public String getPassword() {
        return password;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    
    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
    
    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}
```

## 最佳实践

### 1. 命名规范

```java
// 推荐：使用有意义的实体名称
@Entity(name = "UserEntity")
public class User {
    // 实体定义
}

// 推荐：使用复数形式的表名
@Entity
@Table(name = "users")
public class User {
    // 实体定义
}
```

### 2. 字段访问策略

```java
@Entity
@Access(AccessType.FIELD)  // 字段访问策略
public class User {
    @Id
    private Long id;
    
    private String username;
    
    // 不需要getter/setter方法
}

@Entity
@Access(AccessType.PROPERTY)  // 属性访问策略
public class User {
    private Long id;
    private String username;
    
    @Id
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
}
```

### 3. 序列化支持

```java
@Entity
public class User implements Serializable {
    private static final long serialVersionUID = 1L;
    
    @Id
    private Long id;
    
    private String username;
    
    // 构造方法、getter和setter
}
```

## 常见问题

### 1. 注解位置混用

```java
// 错误：注解位置混用
@Entity
public class User {
    @Id
    private Long id;
    
    @Column(name = "username")
    public String getUsername() {  // 错误：字段上有注解，方法上也有注解
        return username;
    }
}

// 正确：统一使用字段注解
@Entity
public class User {
    @Id
    private Long id;
    
    @Column(name = "username")
    private String username;
    
    public String getUsername() {
        return username;
    }
}
```

### 2. 缺少无参构造方法

```java
// 错误：缺少无参构造方法
@Entity
public class User {
    @Id
    private Long id;
    
    private String username;
    
    public User(String username) {  // 只有带参构造方法
        this.username = username;
    }
    // 运行时错误：JPA无法实例化此实体
}

// 正确：提供无参构造方法
@Entity
public class User {
    @Id
    private Long id;
    
    private String username;
    
    public User() {  // 必须有无参构造方法
    }
    
    public User(String username) {
        this.username = username;
    }
}

// 也可以使用protected访问级别
@Entity
public class User {
    @Id
    private Long id;
    
    private String username;
    
    protected User() {  // protected也满足JPA要求
    }
    
    public User(String username) {
        this.username = username;
    }
}
```

### 3. 实体类设计问题

```java
// 错误：实体类过于复杂
@Entity
public class User {
    @Id
    private Long id;
    
    private String username;
    
    // 错误：在实体类中包含业务逻辑
    public void sendEmail() {
        // 业务逻辑
    }
    
    public void calculateAge() {
        // 业务逻辑
    }
}

// 正确：实体类只包含数据和基本方法
@Entity
public class User {
    @Id
    private Long id;
    
    private String username;
    private LocalDate birthDate;
    
    // 正确：只包含数据相关的方法
    public int getAge() {
        return Period.between(birthDate, LocalDate.now()).getYears();
    }
}
```

## 总结

`@Entity`注解是JPA中最基础的注解，用于将Java类标识为持久化实体。使用`@Entity`注解时需要注意：

- **基本要求**：无参构造方法、主键标识、类的基本限制
- **实体命名**：可以使用name属性指定实体名称
- **最佳实践**：遵循命名规范、选择合适的访问策略、支持序列化

在实际开发中，应该根据具体的业务需求来设计实体类，遵循JPA规范，并注意常见的问题和陷阱。

---

**厦门工学院人工智能创作坊 --郑恩赐**  
**2025-9-28**
