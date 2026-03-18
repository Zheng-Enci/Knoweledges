# Linux基础技术专栏

## 📝 专栏介绍

本专栏专注于Linux系统基础技术，从入门到进阶，系统学习Linux操作系统的核心知识和实用技能。适合后端开发者、系统管理员、运维工程师以及所有对Linux感兴趣的学习者。

## 🗺️ 学习路线图

### 第一阶段：Linux基础入门（L1系列）

```mermaid
graph TD
    L1["第一阶段：Linux基础入门"]
    L1A["Linux系统概述与发行版选择"]
    L1B["系统启动流程：BIOS→引导→内核→用户空间"]
    L1C["VMware虚拟机安装Linux系统"]
    L1D["80+基础命令详解：ls/cd/pwd/cp/mv/rm"]
    L1E["文件与目录操作进阶"]
    L1F["文件内容查看：cat/more/less/head/tail"]
    L1G["vi/vim编辑器完全指南"]
    L1H["重定向与管道操作深入"]
    L1I["通配符、特殊符号与正则基础"]
    L1J["Linux帮助系统：man/help/info/apropos"]
    
    L1 --> L1A --> L1B --> L1C --> L1D --> L1E --> L1F --> L1G --> L1H --> L1I --> L1J
    
    style L1 fill:#e1f5fe,stroke:#0288d1
```

### 第二阶段：文件系统与权限管理（L2系列）

```mermaid
graph TD
    L2["第二阶段：文件系统与权限管理"]
    L2A["Linux文件系统结构详解：FHS标准"]
    L2B["文件类型与权限基础：rwx深入理解"]
    L2C["chmod命令详解：数字模式与符号模式"]
    L2D["chown/chgrp命令与文件归属管理"]
    L2E["文件查找命令：find/locate/whereis/which"]
    L2F["文本处理三剑客：grep/awk/sed实战"]
    L2G["文件压缩与解压：tar/gzip/bzip2/xz"]
    L2H["硬链接与软链接：原理与应用场景"]
    L2I["磁盘分区管理与挂载操作"]
    L2J["磁盘空间管理：df/du及磁盘配额"]
    
    L2 --> L2A --> L2B --> L2C --> L2D --> L2E --> L2F --> L2G --> L2H --> L2I --> L2J
    
    style L2 fill:#e8f5e9,stroke:#388e3c
```

### 第三阶段：用户管理与进程控制（L3系列）

```mermaid
graph TD
    L3["第三阶段：用户管理与进程控制"]
    L3A["Linux用户和用户组体系架构"]
    L3B["用户管理命令：useradd/userdel/usermod"]
    L3C["用户组管理：groupadd/groupdel/groupmod"]
    L3D["passwd命令与密码策略配置"]
    L3E["sudo命令与权限提升机制"]
    L3F["进程概念、状态与生命周期"]
    L3G["进程查看命令：ps/pgrep/pstree"]
    L3H["系统监控：top/htop/iotop"]
    L3I["进程控制：kill/killall/pkill"]
    L3J["系统服务管理：systemctl全面掌握"]
    
    L3 --> L3A --> L3B --> L3C --> L3D --> L3E --> L3F --> L3G --> L3H --> L3I --> L3J
    
    style L3 fill:#fff3e0,stroke:#f57c00
```

### 第四阶段：软件包管理与环境配置（L4系列）

```mermaid
graph TD
    L4["第四阶段：软件包管理与环境配置"]
    L4A["Linux软件包管理体系概述"]
    L4B["RPM包管理：查询/安装/卸载/验证"]
    L4C["YUM包管理器：仓库配置与使用"]
    L4D["DNF新一代包管理器"]
    L4E["源码编译安装：configure/make/make install"]
    L4F["环境变量配置：PATH/LD_LIBRARY_PATH"]
    L4G["Python开发环境搭建与管理"]
    L4H["Java开发环境：JDK安装与配置"]
    L4I["Node.js环境安装与npm使用"]
    L4J["软件仓库镜像源配置与优化"]
    
    L4 --> L4A --> L4B --> L4C --> L4D --> L4E --> L4F --> L4G --> L4H --> L4I --> L4J
    
    style L4 fill:#f3e5f5,stroke:#7b1fa2
```

### 第五阶段：网络配置与安全管理（L5系列）

```mermaid
graph TD
    L5["第五阶段：网络配置与安全管理"]
    L5A["TCP/IP协议基础与网络模型"]
    L5B["Linux网络配置：ifconfig/ip/nmcli"]
    L5C["网络诊断工具：ping/traceroute/netstat/ss"]
    L5D["SSH服务配置与远程连接安全"]
    L5E["防火墙：firewalld与iptables"]
    L5F["SELinux安全机制详解"]
    L5G["系统日志分析：rsyslog/journalctl"]
    L5H["系统安全加固实践"]
    L5I["性能分析工具：top/htop/iostat/vmstat"]
    L5J["系统故障排查方法论"]
    
    L5 --> L5A --> L5B --> L5C --> L5D --> L5E --> L5F --> L5G --> L5H --> L5I --> L5J
    
    style L5 fill:#ffebee,stroke:#d32f2f
```

### 第六阶段：Shell脚本编程（L6系列）

```mermaid
graph TD
    L6["第六阶段：Shell脚本编程"]
    L6A["Shell脚本基础语法与执行方式"]
    L6B["变量定义、作用域与数据类型"]
    L6C["条件判断：if/elif/else/case语句"]
    L6D["循环结构：for/while/until循环"]
    L6E["函数定义、调用与参数传递"]
    L6F["数组与关联数组操作"]
    L6G["字符串处理技巧与模式匹配"]
    L6H["文件操作编程：读写/判断/遍历"]
    L6I["错误处理机制：exit/trap信号捕获"]
    L6J["实用脚本案例：备份/监控/自动化"]
    
    L6 --> L6A --> L6B --> L6C --> L6D --> L6E --> L6F --> L6G --> L6H --> L6I --> L6J
    
    style L6 fill:#e0f2f1,stroke:#00695c
```

### 第七阶段：服务器应用部署（L7系列）

```mermaid
graph TD
    L7["第七阶段：服务器应用部署"]
    L7A["Web服务器：Nginx安装与虚拟主机配置"]
    L7B["数据库：MySQL/MariaDB部署与优化"]
    L7C["缓存服务：Redis安装与性能调优"]
    L7D["版本控制：Git服务器搭建与管理"]
    L7E["CI/CD：Jenkins自动化部署流水线"]
    L7F["监控系统：Prometheus+Grafana搭建"]
    L7G["日志收集：ELK Stack日志分析平台"]
    L7H["负载均衡：Nginx反向代理与 upstream"]
    L7I["高可用集群：Keepalived+HAProxy"]
    L7J["自动化运维：Ansible批量管理"]
    
    L7 --> L7A --> L7B --> L7C --> L7D --> L7E --> L7F --> L7G --> L7H --> L7I --> L7J
    
    style L7 fill:#fff8e1,stroke:#ffa000
```

## 📚 文档链接目录

### 📋 基础篇

### 🎯 第一阶段：Linux基础入门

- [L1C-VMware创建CentOS虚拟机完全指南](f:\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Knowledges\玩转Linux\L1C-VMware创建CentOS虚拟机完全指南.md) - [掘金](https://juejin.cn/post/7616598497153253426) | [CSDN](https://blog.csdn.net/2301_79239314/article/details/159048570)

### 📊 第二阶段：文件系统与权限管理

### ⚙️ 第三阶段：用户管理与进程控制

### 🏗️ 第四阶段：软件包管理与环境配置

### 🔒 第五阶段：网络配置与安全管理

### 💻 第六阶段：Shell脚本编程

### 🚀 第七阶段：服务器应用部署

---

*本专栏持续更新中，欢迎提出宝贵建议！*