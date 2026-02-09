# ☕ Java继承和多态详解

## 🎯 核心概念

**继承**：子类继承父类的属性和方法，实现代码重用  
**多态**：同一方法在不同对象上具有不同的表现形式

## 🏗️ 继承基础

### 基本语法
```java
public class 父类 {
    // 父类的属性和方法
}

public class 子类 extends 父类 {
    // 子类的属性和方法
}
```

### 继承特点
- **单继承**：Java只支持单继承，一个类只能有一个直接父类
- **代码重用**：子类自动获得父类的非私有成员
- **扩展性**：子类可以添加新的属性和方法

### 示例代码
```java
// 父类
public class Animal {
    protected String name;
    protected int age;
    
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void eat() {
        System.out.println(name + "在吃东西");
    }
    
    public void sleep() {
        System.out.println(name + "在睡觉");
    }
}

// 子类
public class Dog extends Animal {
    private String breed;  // 子类特有属性
    
    public Dog(String name, int age, String breed) {
        super(name, age);  // 调用父类构造函数
        this.breed = breed;
    }
    
    public void bark() {   // 子类特有方法
        System.out.println(name + "在汪汪叫");
    }
    
    @Override
    public void eat() {    // 重写父类方法
        System.out.println(name + "正在吃狗粮");
    }
}
```

## 🔧 super关键字

### 主要用途
1. **调用父类构造函数**：`super(参数)`
2. **访问父类成员**：`super.成员名`
3. **调用父类方法**：`super.方法名()`

### 使用示例
```java
public class Cat extends Animal {
    private String color;
    
    public Cat(String name, int age, String color) {
        super(name, age);  // 调用父类构造函数
        this.color = color;
    }
    
    @Override
    public void eat() {
        super.eat();  // 先调用父类方法
        System.out.println("然后舔爪子");
    }
    
    public void climb() {
        System.out.println(super.name + "在爬树");  // 访问父类成员
    }
}
```

## 🔄 方法重写

### 重写规则
- 方法名、参数列表、返回类型必须相同
- 访问权限不能比父类更严格
- 使用`@Override`注解（推荐）

### 重写示例
```java
public class Bird extends Animal {
    public Bird(String name, int age) {
        super(name, age);
    }
    
    @Override
    public void eat() {
        System.out.println(name + "在啄食");
    }
    
    public void fly() {
        System.out.println(name + "在飞翔");
    }
}
```

## 🎭 多态实现

### 向上转型
```java
public class PolymorphismDemo {
    public static void main(String[] args) {
        // 向上转型：父类引用指向子类对象
        Animal animal1 = new Dog("旺财", 3, "金毛");
        Animal animal2 = new Cat("咪咪", 2, "橘色");
        Animal animal3 = new Bird("小黄", 1);
        
        // 多态调用：同一方法，不同表现
        animal1.eat();  // 输出：旺财正在吃狗粮
        animal2.eat();  // 输出：咪咪在吃东西
        animal3.eat();  // 输出：小黄在啄食
        
        // 注意：只能调用父类中定义的方法
        // animal1.bark();  // 编译错误！
    }
}
```

### 向下转型
```java
public class DowncastDemo {
    public static void main(String[] args) {
        Animal animal = new Dog("旺财", 3, "金毛");
        
        // 向下转型：父类引用转为子类引用
        if (animal instanceof Dog) {
            Dog dog = (Dog) animal;
            dog.bark();  // 现在可以调用子类特有方法
        }
    }
}
```

## 🎯 实际应用示例

### 动物管理系统
```java
public class AnimalManager {
    private List<Animal> animals = new ArrayList<>();
    
    public void addAnimal(Animal animal) {
        animals.add(animal);
    }
    
    public void feedAll() {
        for (Animal animal : animals) {
            animal.eat();  // 多态调用
        }
    }
    
    public void showInfo() {
        for (Animal animal : animals) {
            System.out.println("姓名：" + animal.name + 
                             "，年龄：" + animal.age);
        }
    }
}

// 使用示例
public class Test {
    public static void main(String[] args) {
        AnimalManager manager = new AnimalManager();
        
        manager.addAnimal(new Dog("旺财", 3, "金毛"));
        manager.addAnimal(new Cat("咪咪", 2, "橘色"));
        manager.addAnimal(new Bird("小黄", 1));
        
        manager.feedAll();  // 多态体现
    }
}
```

## 🔄 现代Java特性

### 1. 接口默认方法 (Java 8+)
```java
// 现代接口：支持默认方法
public interface Flyable {
    void fly();  // 抽象方法
    
    // 默认方法：提供默认实现
    default void takeOff() {
        System.out.println("准备起飞");
    }
    
    // 静态方法：接口级别的工具方法
    static void showInfo() {
        System.out.println("这是一个飞行接口");
    }
}

public class Bird implements Flyable {
    @Override
    public void fly() {
        System.out.println("鸟儿在飞翔");
    }
    
    // 可以选择重写默认方法
    @Override
    public void takeOff() {
        System.out.println("鸟儿拍打翅膀准备起飞");
    }
}
```

### 2. 密封类 (Java 17+)
```java
// 密封类：限制哪些类可以继承
public sealed class Shape 
    permits Circle, Rectangle, Triangle {
    
    public abstract double area();
}

// 只有被允许的类才能继承
public final class Circle extends Shape {
    private final double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public final class Rectangle extends Shape {
    private final double width, height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double area() {
        return width * height;
    }
}

public final class Triangle extends Shape {
    private final double base, height;
    
    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }
    
    @Override
    public double area() {
        return 0.5 * base * height;
    }
}

// 编译错误：Pentagon不在permits列表中
// public class Pentagon extends Shape { }  // 编译错误！
```

### 3. 记录类 (Java 14+)
```java
// 记录类：简化数据类定义
public record Point(int x, int y) {
    // 自动生成构造函数、getter、equals、hashCode、toString
    
    // 可以添加自定义方法
    public double distanceFromOrigin() {
        return Math.sqrt(x * x + y * y);
    }
}

// 使用示例
Point p1 = new Point(3, 4);
Point p2 = new Point(3, 4);
System.out.println(p1.equals(p2));  // true
System.out.println(p1.distanceFromOrigin());  // 5.0
```

## ⚡ 性能考虑

### 1. 多态性能开销
```java
public class PerformanceComparison {
    public static void main(String[] args) {
        int iterations = 10_000_000;
        
        // 直接调用：最快
        Dog dog = new Dog("旺财", 3, "金毛");
        long start1 = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            dog.eat();  // 直接调用，无开销
        }
        long end1 = System.nanoTime();
        
        // 多态调用：有虚方法表查找开销
        Animal animal = dog;
        long start2 = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            animal.eat();  // 虚方法调用，有开销
        }
        long end2 = System.nanoTime();
        
        System.out.println("直接调用耗时：" + (end1 - start1) / 1_000_000 + "ms");
        System.out.println("多态调用耗时：" + (end2 - start2) / 1_000_000 + "ms");
    }
}
```

### 2. 性能优化建议
```java
// ✅ 优化：避免频繁的类型检查
import java.util.*;
import java.util.stream.Collectors;

public class OptimizedProcessor {
    public void processAnimals(List<Animal> animals) {
        // 按类型分组，减少instanceof检查
        Map<Class<?>, List<Animal>> grouped = animals.stream()
            .collect(Collectors.groupingBy(Animal::getClass));
        
        // 分别处理每种类型
        if (grouped.containsKey(Dog.class)) {
            grouped.get(Dog.class).forEach(this::processDog);
        }
        if (grouped.containsKey(Cat.class)) {
            grouped.get(Cat.class).forEach(this::processCat);
        }
    }
    
    private void processDog(Animal animal) {
        Dog dog = (Dog) animal;  // 安全转换
        // 处理狗的逻辑
    }
    
    private void processCat(Animal animal) {
        Cat cat = (Cat) animal;  // 安全转换
        // 处理猫的逻辑
    }
}
```

## 🏗️ 设计原则

### 1. 组合优于继承
```java
// ❌ 问题：使用继承
public class Car extends Engine {
    // 汽车不是引擎，这是错误的设计
}

// ✅ 解决：使用组合
public class Car {
    private Engine engine;  // 组合关系
    private Wheel[] wheels;
    
    public Car(Engine engine, Wheel[] wheels) {
        this.engine = engine;
        this.wheels = wheels;
    }
    
    public void start() {
        engine.start();  // 委托给引擎
    }
}
```

### 2. 里氏替换原则
```java
// ✅ 正确：子类可以替换父类
public class Bird extends Animal {
    @Override
    public void eat() {
        System.out.println("鸟儿啄食");
    }
    
    // 子类可以扩展功能
    public void fly() {
        System.out.println("鸟儿飞翔");
    }
}

// 使用：任何需要Animal的地方都可以用Bird替换
public void feedAnimal(Animal animal) {
    animal.eat();  // Bird对象可以正常工作
}
```

## 💡 最佳实践

### 1. 合理使用继承
- 确保"is-a"关系：子类应该是父类的一种
- 避免过深的继承层次（建议不超过3-4层）
- 优先使用组合而非继承
- 遵循里氏替换原则

### 2. 方法重写注意事项
- 始终使用`@Override`注解
- 保持重写方法的行为一致性
- 不要改变方法的核心逻辑
- 考虑使用`@Deprecated`标记过时方法

### 3. 多态使用技巧
- 使用父类引用提高代码灵活性
- 合理使用`instanceof`进行类型检查
- 避免频繁的向下转型
- 考虑性能影响，在热点代码中谨慎使用

### 4. 现代Java最佳实践
- 优先使用接口而非抽象类
- 利用接口默认方法减少重复代码
- 使用密封类限制继承层次
- 考虑使用记录类简化数据类

## ⚠️ 继承和多态的缺点与注意事项

### 1. 继承的缺点

#### 继承层次过深问题
```java
// ❌ 问题：继承层次过深，难以维护
class Animal { }
class Mammal extends Animal { }
class Carnivore extends Mammal { }
class Feline extends Carnivore { }
class DomesticCat extends Feline { }
class PersianCat extends DomesticCat { }
// 继续下去... 维护困难！
```

#### 紧耦合问题
```java
// ❌ 问题：子类与父类紧耦合
public class Rectangle {
    protected int width, height;
    
    public void setWidth(int width) {
        this.width = width;
    }
    
    public void setHeight(int height) {
        this.height = height;
    }
}

// 正方形继承矩形会导致问题
public class Square extends Rectangle {
    @Override
    public void setWidth(int width) {
        super.setWidth(width);
        super.setHeight(width);  // 强制保持正方形
    }
    
    @Override
    public void setHeight(int height) {
        super.setHeight(height);
        super.setWidth(height);  // 强制保持正方形
    }
}
// 问题：违反了里氏替换原则！
```

### 2. 多态的缺点

#### 性能开销
```java
// ⚠️ 注意：多态调用有性能开销
public class PerformanceTest {
    public static void main(String[] args) {
        Animal[] animals = new Animal[1000000];
        
        // 初始化数组，避免NullPointerException
        for (int i = 0; i < animals.length; i++) {
            if (i % 3 == 0) {
                animals[i] = new Dog("Dog" + i, 3, "金毛");
            } else if (i % 3 == 1) {
                animals[i] = new Cat("Cat" + i, 2, "橘色");
            } else {
                animals[i] = new Bird("Bird" + i, 1);
            }
        }
        
        // 多态调用：每次都需要查找虚方法表
        long start = System.currentTimeMillis();
        for (Animal animal : animals) {
            animal.eat();  // 虚方法调用，有开销
        }
        long end = System.currentTimeMillis();
        System.out.println("多态调用耗时：" + (end - start) + "ms");
    }
}
```

#### 调试困难
```java
// ⚠️ 问题：多态使调试变得复杂
public class DebugExample {
    public static void processAnimal(Animal animal) {
        // 调试时难以确定实际调用的是哪个类的方法
        animal.eat();  // 需要运行时才能确定具体实现
    }
}
```

### 3. 常见错误

#### 重写错误
```java
// ❌ 错误：参数列表不同
public void eat(String food) { }

// ❌ 错误：返回类型不兼容
public String eat() { return ""; }

// ✅ 正确
@Override
public void eat() { }
```

#### 转型错误
```java
Animal animal = new Dog("旺财", 3, "金毛");

// ❌ 错误：直接强制转换
Cat cat = (Cat) animal;  // 运行时异常！

// ✅ 正确：先检查类型
if (animal instanceof Cat) {
    Cat cat = (Cat) animal;
}
```

## 📚 总结

### 继承和多态的价值
- **继承**：实现代码重用，建立清晰的类层次结构
- **多态**：提供灵活性和可扩展性，支持运行时动态绑定

### 关键要点
1. **合理使用**：继承要遵循"is-a"关系，避免过深层次
2. **性能考虑**：多态有虚方法调用开销，在性能敏感场景需谨慎
3. **现代特性**：利用接口默认方法、密封类、记录类等新特性
4. **设计原则**：优先使用组合，遵循里氏替换原则

### 学习路径建议
1. **基础阶段**：掌握基本语法和概念
2. **实践阶段**：完成实际项目，体验优缺点
3. **进阶阶段**：学习现代Java特性和设计模式
4. **优化阶段**：关注性能优化和最佳实践

---

**📝 学习建议：** 
- 多动手实践，创建不同的继承层次
- 完成一个完整的动物管理系统项目
- 学习现代Java特性，跟上技术发展
- 关注性能影响，培养优化意识
- 理解设计原则，写出更好的代码

---

**厦门工学院人工智能创作坊 --郑恩赐**  
**2025-9-27**
