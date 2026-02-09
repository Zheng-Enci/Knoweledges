# @ResponseStatus 注解详解

## 📋 概述

`@ResponseStatus` 是 Spring 框架提供的一个核心注解，用于在处理 HTTP 请求时设置响应的状态码和原因短语。它可以应用于控制器方法或异常类上，让开发者能够更精确地控制 API 的响应状态。

## 🎯 主要特性

- ✅ 支持在方法上直接设置响应状态码
- ✅ 支持在异常类上定义默认状态码
- ✅ 提供原因短语的自定义设置
- ✅ 与全局异常处理器完美集成
- ✅ 简化 RESTful API 的状态管理

## 🔧 注解属性

| 属性 | 类型 | 说明 | 必需 |
|------|------|------|------|
| `value` / `code` | `HttpStatus` | HTTP 状态码枚举值 | ✅ |
| `reason` | `String` | 状态码的原因短语 | ❌ |

## 💡 使用方式

### 1. 在控制器方法上使用

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public User getUser(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public User createUser(@RequestBody User user) {
        return userService.save(user);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.deleteById(id);
    }
}
```

### 2. 在异常类上使用

```java
@ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "用户不存在")
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "请求参数无效")
public class InvalidRequestException extends RuntimeException {
    public InvalidRequestException(String message) {
        super(message);
    }
}
```

### 3. 在全局异常处理器中使用

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(DataIntegrityViolationException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleDataIntegrityViolation(DataIntegrityViolationException ex) {
        return new ErrorResponse("CONFLICT", "数据完整性冲突", ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidationException(MethodArgumentNotValidException ex) {
        return new ErrorResponse("VALIDATION_ERROR", "参数验证失败", ex.getMessage());
    }
}
```

## 🚀 实际应用场景

### 场景 1：RESTful API 设计

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    @GetMapping
    @ResponseStatus(HttpStatus.OK)
    public List<Product> getAllProducts() {
        return productService.findAll();
    }

    @GetMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public Product getProduct(@PathVariable Long id) {
        Product product = productService.findById(id);
        if (product == null) {
            throw new ProductNotFoundException("产品不存在");
        }
        return product;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Product createProduct(@Valid @RequestBody Product product) {
        return productService.save(product);
    }

    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public Product updateProduct(@PathVariable Long id, @Valid @RequestBody Product product) {
        return productService.update(id, product);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteProduct(@PathVariable Long id) {
        productService.deleteById(id);
    }
}
```

### 场景 2：自定义业务异常

```java
// 业务异常定义
@ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "订单不存在")
public class OrderNotFoundException extends RuntimeException {
    public OrderNotFoundException(String orderId) {
        super("订单 " + orderId + " 不存在");
    }
}

@ResponseStatus(value = HttpStatus.FORBIDDEN, reason = "权限不足")
public class InsufficientPermissionException extends RuntimeException {
    public InsufficientPermissionException(String message) {
        super(message);
    }
}

// 控制器使用
@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @GetMapping("/{orderId}")
    public Order getOrder(@PathVariable String orderId, 
                         @RequestHeader("Authorization") String token) {
        // 权限检查
        if (!hasPermission(token)) {
            throw new InsufficientPermissionException("用户权限不足");
        }
        
        // 订单查找
        Order order = orderService.findByOrderId(orderId);
        if (order == null) {
            throw new OrderNotFoundException(orderId);
        }
        
        return order;
    }
}
```

## ⚠️ 注意事项

### 1. reason 属性的限制

```java
// ❌ 不推荐：使用 reason 属性会清空响应体
@ResponseStatus(value = HttpStatus.BAD_REQUEST, reason = "参数错误")
public class BadRequestException extends RuntimeException {
    // 这种方式会调用 response.sendError()，清空响应体
}

// ✅ 推荐：不使用 reason，在异常处理器中处理
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) {
        super(message);
    }
}

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BadRequestException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleBadRequest(BadRequestException ex) {
        return new ErrorResponse("BAD_REQUEST", "请求参数错误", ex.getMessage());
    }
}
```

### 2. 与 ResponseEntity 的区别

```java
// 使用 @ResponseStatus（简单场景）
@GetMapping("/simple")
@ResponseStatus(HttpStatus.OK)
public String getSimpleData() {
    return "简单数据";
}

// 使用 ResponseEntity（复杂场景）
@GetMapping("/complex")
public ResponseEntity<ApiResponse<String>> getComplexData() {
    ApiResponse<String> response = new ApiResponse<>();
    response.setData("复杂数据");
    response.setTimestamp(LocalDateTime.now());
    
    return ResponseEntity.ok()
            .header("Custom-Header", "value")
            .body(response);
}
```

### 3. 状态码优先级

```java
@RestController
public class PriorityController {

    @GetMapping("/priority")
    @ResponseStatus(HttpStatus.OK)  // 方法级别的状态码
    public ResponseEntity<String> getData() {
        // ResponseEntity 的状态码会覆盖 @ResponseStatus
        return ResponseEntity.status(HttpStatus.CREATED)
                .body("数据创建成功");
    }
}
```

## 🔍 最佳实践

### 1. 统一异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ValidationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(ValidationException ex) {
        return ErrorResponse.builder()
                .code("VALIDATION_ERROR")
                .message("参数验证失败")
                .details(ex.getErrors())
                .timestamp(LocalDateTime.now())
                .build();
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return ErrorResponse.builder()
                .code("RESOURCE_NOT_FOUND")
                .message("资源不存在")
                .details(ex.getMessage())
                .timestamp(LocalDateTime.now())
                .build();
    }
}
```

### 2. 状态码枚举使用

```java
public enum ApiStatus {
    SUCCESS(HttpStatus.OK, "操作成功"),
    CREATED(HttpStatus.CREATED, "创建成功"),
    NO_CONTENT(HttpStatus.NO_CONTENT, "删除成功"),
    BAD_REQUEST(HttpStatus.BAD_REQUEST, "请求参数错误"),
    UNAUTHORIZED(HttpStatus.UNAUTHORIZED, "未授权"),
    FORBIDDEN(HttpStatus.FORBIDDEN, "权限不足"),
    NOT_FOUND(HttpStatus.NOT_FOUND, "资源不存在"),
    INTERNAL_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "服务器内部错误");

    private final HttpStatus httpStatus;
    private final String message;

    ApiStatus(HttpStatus httpStatus, String message) {
        this.httpStatus = httpStatus;
        this.message = message;
    }

    // getter 方法...
}
```

## 📊 总结

`@ResponseStatus` 注解是 Spring 框架中管理 HTTP 响应状态的重要工具：

- 🎯 **适用场景**：简单的状态码设置、异常处理、RESTful API 设计
- ⚡ **优势**：代码简洁、声明式配置、易于维护
- ⚠️ **限制**：reason 属性会清空响应体、灵活性不如 ResponseEntity
- 🔧 **建议**：结合全局异常处理器使用，避免使用 reason 属性

通过合理使用 `@ResponseStatus` 注解，可以让你的 Spring Boot 应用具有更好的 API 设计和错误处理机制。

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 10 月 1 日**
