# @RestControllerAdvice 注解详解

## 📋 概述

`@RestControllerAdvice` 是 Spring Boot 框架中的一个重要注解，用于全局处理 REST 控制器中的异常、数据绑定和预处理。它是 `@ControllerAdvice` 和 `@ResponseBody` 的组合注解，专门适用于返回 JSON 数据的 RESTful 应用程序。

## 🎯 主要功能

### 1. 全局异常处理
通过 `@ExceptionHandler` 注解的方法，可以捕获并处理所有控制器中抛出的异常，实现统一的异常处理逻辑。

### 2. 全局数据绑定
使用 `@InitBinder` 注解的方法，可以对请求参数进行预处理或格式化。

### 3. 全局数据预处理
通过 `@ModelAttribute` 注解的方法，可以在所有控制器方法调用前绑定特定的数据。

## 💡 基本用法

### 简单示例

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 处理特定异常
    @ExceptionHandler(value = CustomException.class)
    public ResponseEntity<String> handleCustomException(CustomException e) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
    }

    // 处理所有未捕获的异常
    @ExceptionHandler(value = Exception.class)
    public ResponseEntity<String> handleException(Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("服务器内部错误");
    }
}
```

## 🔧 高级配置

### 作用域控制

`@RestControllerAdvice` 支持多种方式控制作用范围：

```java
// 1. 指定包路径
@RestControllerAdvice(basePackages = "com.example.controller")
public class PackageSpecificHandler {
    // 仅作用于指定包下的控制器
}

// 2. 指定注解类型
@RestControllerAdvice(annotations = RestController.class)
public class AnnotationSpecificHandler {
    // 仅作用于带有 @RestController 注解的控制器
}

// 3. 指定类类型
@RestControllerAdvice(assignableTypes = {UserController.class, OrderController.class})
public class ClassSpecificHandler {
    // 仅作用于指定的控制器类
}
```

## 📝 完整示例

### 全局异常处理器

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    /**
     * 处理业务异常
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException e) {
        log.error("业务异常: {}", e.getMessage());
        ErrorResponse error = new ErrorResponse("BUSINESS_ERROR", e.getMessage());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    /**
     * 处理参数验证异常
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(MethodArgumentNotValidException e) {
        log.error("参数验证异常: {}", e.getMessage());
        String message = e.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining(", "));
        ErrorResponse error = new ErrorResponse("VALIDATION_ERROR", message);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    /**
     * 处理 HTTP 请求方法不支持异常
     */
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ResponseEntity<ErrorResponse> handleMethodNotSupported(HttpRequestMethodNotSupportedException e) {
        log.error("请求方法不支持: {}", e.getMessage());
        ErrorResponse error = new ErrorResponse("METHOD_NOT_SUPPORTED", "请求方法不支持");
        return ResponseEntity.status(HttpStatus.METHOD_NOT_ALLOWED).body(error);
    }

    /**
     * 处理通用异常
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception e) {
        log.error("系统异常: ", e);
        ErrorResponse error = new ErrorResponse("INTERNAL_ERROR", "系统内部错误");
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### 错误响应实体类

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ErrorResponse {
    private String code;
    private String message;
    private Long timestamp;
    
    public ErrorResponse(String code, String message) {
        this.code = code;
        this.message = message;
        this.timestamp = System.currentTimeMillis();
    }
}
```

### 数据绑定处理器

```java
@RestControllerAdvice
public class GlobalDataBinder {

    /**
     * 全局数据绑定
     */
    @InitBinder
    public void initBinder(WebDataBinder binder) {
        // 注册自定义日期格式化器
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        dateFormat.setLenient(false);
        binder.registerCustomEditor(Date.class, new CustomDateEditor(dateFormat, true));
        
        // 设置字段验证器
        binder.setValidator(new CustomValidator());
    }

    /**
     * 全局模型属性
     */
    @ModelAttribute("currentUser")
    public User getCurrentUser(HttpServletRequest request) {
        // 从请求中获取当前用户信息
        return (User) request.getAttribute("currentUser");
    }
}
```

## ⚠️ 注意事项

1. **适用场景**: `@RestControllerAdvice` 适用于返回 JSON 数据的控制器，如果需要返回视图页面，建议使用 `@ControllerAdvice`。

2. **异常处理优先级**: 更具体的异常处理器会优先于通用的异常处理器。

3. **性能考虑**: 避免在异常处理器中执行耗时操作，以免影响系统性能。

4. **日志记录**: 建议在异常处理器中添加适当的日志记录，便于问题排查。

## 🆚 与 @ControllerAdvice 的区别

| 特性 | @RestControllerAdvice | @ControllerAdvice |
|------|----------------------|-------------------|
| 适用场景 | RESTful API | 传统 MVC 应用 |
| 返回格式 | JSON 数据 | 视图页面 |
| 组合注解 | @ControllerAdvice + @ResponseBody | 单独注解 |
| 使用场景 | 微服务、前后端分离 | 传统 Web 应用 |

## 🚀 最佳实践

1. **异常分类处理**: 根据不同的异常类型创建对应的处理方法。

2. **统一错误格式**: 定义统一的错误响应格式，便于前端处理。

3. **日志记录**: 在异常处理器中记录详细的错误信息。

4. **作用域控制**: 根据实际需求合理设置注解的作用范围。

5. **测试覆盖**: 为异常处理器编写单元测试，确保异常处理逻辑正确。

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 10 月 1 日**
