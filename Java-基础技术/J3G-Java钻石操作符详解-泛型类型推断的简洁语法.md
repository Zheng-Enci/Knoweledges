# Java 符号 `<>` 详解 📚

## 📖 概述

在 Java 编程语言中，符号 `<>` 是一个极其重要的语法元素，主要用于**泛型（Generics）**和**类型推断**。这个看似简单的符号，实际上承载着 Java 类型系统安全性的重要使命。

## 🎯 核心概念

### 1. 泛型（Generics）基础

泛型是 Java 5 引入的重要特性，它允许在类、接口和方法中定义类型参数，从而实现**类型安全**的代码复用。

#### 🔹 基本语法

```java
// 泛型类定义
public class Container<T> {
    private T content;
    
    public void setContent(T content) {
        this.content = content;
    }
    
    public T getContent() {
        return content;
    }
}
```

#### 🔹 使用示例

```java
// 创建不同类型的容器
Container<String> stringContainer = new Container<>();
Container<Integer> intContainer = new Container<>();
Container<Double> doubleContainer = new Container<>();

// 类型安全的使用
stringContainer.setContent("Hello World");
intContainer.setContent(42);
doubleContainer.setContent(3.14);

// 编译时类型检查
String text = stringContainer.getContent(); // ✅ 正确
// Integer number = stringContainer.getContent(); // ❌ 编译错误
```

### 2. 钻石操作符（Diamond Operator）

Java 7 引入了**钻石操作符** `<>`，它允许在创建泛型对象时省略类型参数，编译器会自动推断类型。

#### 🔹 传统写法 vs 钻石操作符

```java
// Java 7 之前的写法
List<String> list1 = new ArrayList<String>();
Map<String, Integer> map1 = new HashMap<String, Integer>();

// Java 7+ 钻石操作符写法
List<String> list2 = new ArrayList<>();
Map<String, Integer> map2 = new HashMap<>();
```

#### 🔹 实际应用场景

```java
import java.util.*;

public class DiamondOperatorExample {
    public static void main(String[] args) {
        // 集合框架中的钻石操作符
        List<String> names = new ArrayList<>();
        Set<Integer> numbers = new HashSet<>();
        Map<String, List<String>> groups = new HashMap<>();
        
        // 添加元素
        names.add("张三");
        names.add("李四");
        
        numbers.add(1);
        numbers.add(2);
        numbers.add(3);
        
        // 复杂泛型类型
        Map<String, Map<String, List<Integer>>> complexMap = new HashMap<>();
        
        System.out.println("姓名列表: " + names);
        System.out.println("数字集合: " + numbers);
    }
}
```

## 🚀 高级特性

### 1. 泛型方法

```java
public class GenericMethods {
    
    // 泛型方法定义
    public static <T> void printArray(T[] array) {
        for (T element : array) {
            System.out.print(element + " ");
        }
        System.out.println();
    }
    
    // 泛型方法调用
    public static void main(String[] args) {
        Integer[] intArray = {1, 2, 3, 4, 5};
        String[] stringArray = {"Hello", "World", "Java"};
        
        printArray(intArray);    // 输出: 1 2 3 4 5
        printArray(stringArray); // 输出: Hello World Java
    }
}
```

### 2. 有界泛型

有界泛型（Bounded Generics）是泛型的一个重要概念，它允许我们限制泛型类型参数的范围。通过使用 `extends` 关键字，我们可以指定类型参数必须是某个类的子类或实现某个接口。

#### 🔹 有界泛型的概念

- **上界（Upper Bound）**：使用 `extends` 关键字，限制类型参数必须是某个类的子类或实现某个接口
- **下界（Lower Bound）**：使用 `super` 关键字，限制类型参数必须是某个类的父类
- **多重边界**：可以同时指定多个上界，使用 `&` 连接

#### 🔹 语法格式

```java
// 上界泛型
<T extends ClassName>
<T extends InterfaceName>
<T extends ClassName & InterfaceName>

// 下界泛型
<? super ClassName>
```

#### 🔹 实际应用示例

```java
// 上界通配符
public class BoundedGenerics {
    
    // 数字类型上界
    public static <T extends Number> double sum(List<T> numbers) {
        double total = 0.0;
        for (T number : numbers) {
            total += number.doubleValue();
        }
        return total;
    }
    
    // 接口上界
    public static <T extends Comparable<T>> T findMax(T[] array) {
        if (array.length == 0) return null;
        
        T max = array[0];
        for (T element : array) {
            if (element.compareTo(max) > 0) {
                max = element;
            }
        }
        return max;
    }
    
    public static void main(String[] args) {
        List<Integer> integers = Arrays.asList(1, 2, 3, 4, 5);
        List<Double> doubles = Arrays.asList(1.1, 2.2, 3.3);
        
        System.out.println("整数和: " + sum(integers)); // 输出: 15.0
        System.out.println("浮点数和: " + sum(doubles)); // 输出: 6.6
        
        String[] words = {"apple", "banana", "cherry"};
        System.out.println("最大单词: " + findMax(words)); // 输出: cherry
    }
}
```

#### 🔹 多重边界示例

```java
// 定义接口
interface Drawable {
    void draw();
}

interface Movable {
    void move();
}

// 定义类
class Shape {
    protected String name;
    
    public Shape(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}

class Circle extends Shape implements Drawable, Movable {
    public Circle(String name) {
        super(name);
    }
    
    @Override
    public void draw() {
        System.out.println("绘制圆形: " + name);
    }
    
    @Override
    public void move() {
        System.out.println("移动圆形: " + name);
    }
}

// 多重边界泛型方法
public class MultipleBoundsExample {
    
    // T 必须同时继承 Shape 类并实现 Drawable 和 Movable 接口
    public static <T extends Shape & Drawable & Movable> void processShape(T shape) {
        System.out.println("处理形状: " + shape.getName());
        shape.draw();
        shape.move();
    }
    
    public static void main(String[] args) {
        Circle circle = new Circle("我的圆形");
        processShape(circle);
        
        // 以下代码会编译错误，因为 String 不满足边界条件
        // processShape("test"); // ❌ 编译错误
    }
}
```

#### 🔹 有界泛型的优势

1. **类型安全**：确保传入的类型符合预期，避免类型转换错误
2. **方法调用**：可以调用边界类型的方法，如 `Number.doubleValue()`
3. **代码复用**：一套代码可以处理多种相关类型
4. **编译时检查**：在编译阶段就能发现类型不匹配的问题

#### 🔹 有界泛型 vs 无界泛型

```java
public class ComparisonExample {
    
    // 无界泛型 - 只能调用 Object 的方法
    public static <T> void processUnbounded(T item) {
        System.out.println(item.toString()); // 只能调用 Object 的方法
        // item.doubleValue(); // ❌ 编译错误，T 可能是任何类型
    }
    
    // 有界泛型 - 可以调用 Number 的方法
    public static <T extends Number> void processBounded(T item) {
        System.out.println(item.toString());
        System.out.println("数值: " + item.doubleValue()); // ✅ 可以调用 Number 的方法
        System.out.println("整数部分: " + item.intValue());
    }
    
    public static void main(String[] args) {
        Integer intValue = 42;
        Double doubleValue = 3.14;
        
        processUnbounded(intValue);    // 只能使用 Object 方法
        processBounded(intValue);      // 可以使用 Number 方法
        processBounded(doubleValue);   // 可以使用 Number 方法
        
        // processBounded("Hello"); // ❌ 编译错误，String 不是 Number 的子类
    }
}
```

### 3. 通配符（Wildcards）

```java
import java.util.*;

public class WildcardExample {
    
    // 无界通配符
    public static void printList(List<?> list) {
        for (Object obj : list) {
            System.out.println(obj);
        }
    }
    
    // 上界通配符
    public static void printNumbers(List<? extends Number> numbers) {
        for (Number num : numbers) {
            System.out.println(num.doubleValue());
        }
    }
    
    // 下界通配符
    public static void addNumbers(List<? super Integer> list) {
        list.add(1);
        list.add(2);
        list.add(3);
    }
    
    public static void main(String[] args) {
        List<String> strings = Arrays.asList("Hello", "World");
        List<Integer> integers = Arrays.asList(1, 2, 3);
        List<Number> numbers = new ArrayList<>();
        
        printList(strings);      // 可以打印任何类型的列表
        printNumbers(integers);  // 只能打印数字类型的列表
        addNumbers(numbers);     // 可以向数字列表添加整数
        
        System.out.println("数字列表: " + numbers);
    }
}
```

## 💡 最佳实践

### 1. 类型安全优先

```java
// ✅ 推荐：使用泛型确保类型安全
List<String> names = new ArrayList<>();
names.add("张三");
String name = names.get(0); // 无需强制类型转换

// ❌ 不推荐：使用原始类型
List rawList = new ArrayList();
rawList.add("张三");
String name = (String) rawList.get(0); // 需要强制类型转换，容易出错
```

### 2. 合理使用钻石操作符

```java
// ✅ 推荐：在明确类型的情况下使用钻石操作符
Map<String, List<Integer>> studentScores = new HashMap<>();

// ✅ 推荐：在方法返回时使用钻石操作符
public static <T> List<T> createList() {
    return new ArrayList<>();
}

// ❌ 不推荐：在类型不明确时使用钻石操作符
var list = new ArrayList<>(); // 类型推断为 ArrayList<Object>
```

### 3. 泛型与集合框架

```java
import java.util.*;

public class CollectionGenerics {
    public static void main(String[] args) {
        // 现代 Java 集合使用方式
        List<String> fruits = new ArrayList<>();
        fruits.add("苹果");
        fruits.add("香蕉");
        fruits.add("橙子");
        
        Set<Integer> primeNumbers = new HashSet<>();
        primeNumbers.addAll(Arrays.asList(2, 3, 5, 7, 11));
        
        Map<String, Integer> wordCount = new HashMap<>();
        wordCount.put("Java", 1);
        wordCount.put("Python", 1);
        wordCount.put("C++", 1);
        
        // 使用 Stream API 进行函数式编程
        fruits.stream()
              .filter(fruit -> fruit.length() > 2)
              .forEach(System.out::println);
    }
}
```

## 🔧 常见问题与解决方案

### 1. 类型擦除问题

```java
// 问题：泛型在运行时会被擦除
public class TypeErasureExample {
    public static void main(String[] args) {
        List<String> stringList = new ArrayList<>();
        List<Integer> intList = new ArrayList<>();
        
        // 这两个列表在运行时类型相同
        System.out.println(stringList.getClass() == intList.getClass()); // 输出: true
        
        // 解决方案：使用 Class 对象保存类型信息
        Class<?> stringListClass = stringList.getClass();
        System.out.println("列表类型: " + stringListClass.getSimpleName()); // 输出: ArrayList
    }
}
```

### 2. 泛型数组限制

```java
// ❌ 不能直接创建泛型数组
// T[] array = new T[10]; // 编译错误

// ✅ 解决方案：使用 Object 数组然后转换
public class GenericArrayExample {
    @SuppressWarnings("unchecked")
    public static <T> T[] createArray(Class<T> clazz, int size) {
        return (T[]) java.lang.reflect.Array.newInstance(clazz, size);
    }
    
    public static void main(String[] args) {
        String[] stringArray = createArray(String.class, 5);
        stringArray[0] = "Hello";
        stringArray[1] = "World";
        
        System.out.println(Arrays.toString(stringArray));
    }
}
```

## 🎨 现代 Java 特性

### 1. Java 10+ 的 var 关键字

```java
import java.util.*;

public class ModernJavaFeatures {
    public static void main(String[] args) {
        // Java 10+ 局部变量类型推断
        var list = new ArrayList<String>();
        var map = new HashMap<String, Integer>();
        
        // 与钻石操作符结合使用
        var numbers = new ArrayList<>();
        numbers.add(1);
        numbers.add(2);
        numbers.add(3);
        
        // 注意：var 推断的类型可能与预期不同
        System.out.println("列表类型: " + numbers.getClass().getSimpleName());
    }
}
```

### 2. Java 14+ 的 Record 类型

```java
// Java 14+ 引入的 Record 类型
public record Person<T>(String name, T data) {
    // Record 自动生成构造函数、getter、equals、hashCode 和 toString
}

public class RecordWithGenerics {
    public static void main(String[] args) {
        Person<String> person1 = new Person<>("张三", "工程师");
        Person<Integer> person2 = new Person<>("李四", 25);
        
        System.out.println(person1); // 输出: Person[name=张三, data=工程师]
        System.out.println(person2); // 输出: Person[name=李四, data=25]
    }
}
```

## 📊 性能考虑

### 1. 泛型对性能的影响

```java
import java.util.*;

public class PerformanceComparison {
    public static void main(String[] args) {
        int iterations = 1_000_000;
        
        // 测试泛型集合性能
        long startTime = System.nanoTime();
        List<Integer> genericList = new ArrayList<>();
        for (int i = 0; i < iterations; i++) {
            genericList.add(i);
        }
        long genericTime = System.nanoTime() - startTime;
        
        // 测试原始类型集合性能
        startTime = System.nanoTime();
        List rawList = new ArrayList();
        for (int i = 0; i < iterations; i++) {
            rawList.add(i);
        }
        long rawTime = System.nanoTime() - startTime;
        
        System.out.println("泛型列表耗时: " + genericTime / 1_000_000 + " ms");
        System.out.println("原始列表耗时: " + rawTime / 1_000_000 + " ms");
        System.out.println("性能差异: " + ((double)(genericTime - rawTime) / rawTime * 100) + "%");
    }
}
```

## 🎯 总结

Java 符号 `<>` 是现代 Java 开发中不可或缺的重要元素：

### ✨ 主要优势

1. **类型安全**：编译时类型检查，减少运行时错误
2. **代码复用**：一套代码适用于多种数据类型
3. **性能优化**：避免不必要的类型转换
4. **代码可读性**：明确表达代码意图

### 🚀 使用建议

1. **优先使用泛型**：在集合和自定义类中广泛使用泛型
2. **善用钻石操作符**：在类型明确时使用 `<>` 简化代码
3. **注意类型擦除**：了解泛型在运行时的限制
4. **遵循最佳实践**：避免使用原始类型，优先使用有界泛型

通过深入理解和正确使用 Java 符号 `<>`，您可以编写更加安全、高效和可维护的 Java 代码！

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 10 月 2 日**
