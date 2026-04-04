# Spring Security 简要介绍

## 📋 摘要

Spring Security 是 Spring 生态系统中的核心安全框架，为 Java 应用程序提供身份认证（Authentication）和授权（Authorization）功能。它通过安全过滤器链（Security Filter Chain）拦截请求，确保只有经过认证和授权的用户才能访问受保护的资源，是构建安全企业级应用（Enterprise Application）的重要工具。

---

## 🎯 什么是 Spring Security

Spring Security 是一个功能强大且高度可定制的安全框架（Security Framework），专为基于 Spring 的 Java 应用程序提供身份验证（Identity Verification）和访问控制（Access Control）功能。它最初由 Ben Alex 于 2003 年创建（前身为 Acegi Security），并于 2008 年更名为 Spring Security，成为 Spring 官方子项目（Official Sub-project）。

## 🔑 核心功能

- **身份认证（Authentication）**：验证用户身份的合法性
- **授权（Authorization）**：根据用户权限（User Permission）控制资源访问
- **防护功能**：防止常见安全攻击（Security Attack），如 CSRF（跨站请求伪造）、XSS（跨站脚本攻击）等

## ⚙️ 基础配置

### 添加依赖（Dependency）

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

### 简单配置（Configuration）

```java
@Configuration  // 配置类注解
@EnableWebSecurity  // 启用 Web 安全
public class SecurityConfig {
    
    @Bean  // Bean 注解
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .anyRequest().authenticated()  // 所有请求需要认证
            )
            .formLogin();  // 启用表单登录（Form Login）
        
        return http.build();
    }
}
```

## 🎉 总结

Spring Security 为 Java 应用提供了强大的安全防护能力（Security Protection），通过简单的配置就能实现身份认证和授权控制。无论是 Web 应用（Web Application）还是 REST API（RESTful API），Spring Security 都能提供可靠的安全保障（Security Guarantee），是 Spring 生态中不可或缺的重要组件（Component）。

现在就开始使用 Spring Security 为您的应用添加安全防护吧！🚀

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 10 月 8 日**
