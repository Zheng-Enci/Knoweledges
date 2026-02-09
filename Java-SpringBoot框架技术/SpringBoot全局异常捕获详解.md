# Spring Boot 全局异常捕获详解 🛡️

## 📋 概述

全局异常捕获是 Spring Boot 应用中处理未捕获异常的重要机制，通过统一的异常处理器，可以优雅地处理各种异常情况，提升应用的稳定性和用户体验。

## 🏷️ 核心注解

### @ControllerAdvice
全局异常处理器的标识注解，用于定义全局异常处理类。

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    // 异常处理方法
}
```

### @ExceptionHandler
指定处理特定异常类型的方法注解。

```java
@ExceptionHandler(Exception.class)
public ResponseEntity<String> handleException(Exception e) {
    // 处理逻辑
}
```

## 🚀 基础实现

### 1. 创建全局异常处理器

```java
@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    /**
     * 处理业务异常
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException e) {
        log.error("业务异常: {}", e.getMessage(), e);
        ErrorResponse errorResponse = new ErrorResponse(
            e.getCode(), 
            e.getMessage(), 
            System.currentTimeMillis()
        );
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(errorResponse);
    }

    /**
     * 处理通用异常
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception e) {
        log.error("系统异常: {}", e.getMessage(), e);
        ErrorResponse errorResponse = new ErrorResponse(
            "SYSTEM_ERROR", 
            "系统内部错误，请联系管理员", 
            System.currentTimeMillis()
        );
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
    }
}
```

### 2. 错误响应实体类

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ErrorResponse {
    private String code;        // 错误码
    private String message;     // 错误信息
    private Long timestamp;     // 时间戳
}
```

### 3. 自定义业务异常

```java
public class BusinessException extends RuntimeException {
    private String code;
    
    public BusinessException(String code, String message) {
        super(message);
        this.code = code;
    }
    
    public String getCode() {
        return code;
    }
}
```

## ⚠️ 注意事项

1. **异常处理顺序**：具体异常优先于通用异常
2. **避免泄露敏感信息**：对异常信息进行脱敏处理
3. **性能考虑**：避免在异常处理器中执行耗时操作
4. **测试策略**：编写异常处理器的单元测试

## 📝 总结

Spring Boot 全局异常捕获通过 `@ControllerAdvice` 和 `@ExceptionHandler` 注解，可以统一处理应用中的异常，提供友好的错误响应，提升应用的稳定性和用户体验。

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 10 月 1 号**
