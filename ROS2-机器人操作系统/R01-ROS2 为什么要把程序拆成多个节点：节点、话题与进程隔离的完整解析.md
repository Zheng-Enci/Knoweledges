# ROS2 为什么要把程序拆成多个节点：节点、话题与进程隔离的完整解析

ROS 2 里根本没有「主程序」这回事，只有一堆靠 topic（话题）连线的 node（节点）。拆节点的真正收益是 fault isolation（故障隔离）和部署自由：一个节点崩了，其他节点照跑；代价是每条消息多一次 serialization（序列化）。而节点又不等于进程——composition（组件化）可以把高频链路塞进同一个 container（容器），换来零拷贝。

## 目录

- 全文摘要
- 1. 先说结论：ROS 2 里没有「主程序」
- 2. 一个 node（节点）到底是什么
- 3. 节点之间怎么协作：topic（话题）、service（服务）、action（动作）
- 4. 为什么要拆：四个收益和三个代价
- 5. 拆过头怎么办：composition（组件化）与 executor（执行器）
- 6. 一段能直接跑的代码：一个进程里跑两个节点
- 7. 五类症状对照表
- 8. 小结：拆的是职责，不是文件

## 全文摘要

ROS 2 是分布式框架，不是一套「写个 main 全调进去」的库。每个 node（节点）只做一件逻辑上的事，节点之间用 topic（话题）、service（服务）、action（动作）三种接口通信，靠 DDS（数据分发服务）自动发现彼此。拆节点换来故障隔离与可替换性，代价是序列化和网络开销；节点数量要按职责划，不能按函数划。

## 1. 先说结论：ROS 2 里没有「主程序」

如果你带着写 Spring Boot 的习惯进 ROS 2，第一反应一定是：`main` 函数在哪？我把相机、定位、规划、控制全 `new` 出来，按顺序调一遍不就行了？

不行。而且不是「不推荐」，是 **架构上就没这个东西** 。

ROS 1 时代还有个 `roscore`（节点管理器）当大总管，所有节点都得去它那儿登记；ROS 2 把这个总管直接删了，换成 DDS（Data Distribution Service，数据分发服务）的去中心化发现机制——节点上线自己广播，谁关心谁订阅，没有中间商赚差价 🙂。

于是整个系统长成一张 graph（计算图）：一堆 node（节点）作为独立参与者，边是 topic（话题）、service（服务）、action（动作）。以一台常见的差速小车为例，跑起来的时候后台同时活着的节点大概是这样一批：

| 环节 | 典型节点 | 干什么 |
|------|----------|--------|
| 传感器驱动 | 激光雷达驱动、相机驱动、IMU 驱动 | 把硬件数据转成 msg（消息） |
| 状态估计 | `robot_state_publisher`、`amcl`、EKF 融合节点 | 我在哪、我朝哪 |
| 规划 | `planner_server`、`bt_navigator` | 从 A 到 B 怎么走 |
| 控制 | `controller_server`、`velocity_smoother` | 把路径变成轮速指令 |
| 行为与容错 | `behavior_server`、`lifecycle_manager` | 卡住了怎么办、谁先上电 |

光是 Nav2（Navigation 2，导航框架）一套导航栈，`lifecycle_manager` 默认就要按顺序拉起 `controller_server`、`planner_server`、`behavior_server`、`bt_navigator`、`waypoint_follower`、`smoother_server` 等近十个节点。再加上驱动和底盘，二三十个节点同时在跑是常态，不是炫技 😅。

打个比方：ROS 2 不是在写一本书，而是在办一份报纸。记者、编辑、排版、印刷各干各的，稿件通过「稿件架」（topic，话题）流转，谁也不需要把别人的活儿揽过来自己干。

本节参考资料：

- [Nodes -- ROS 2 Documentation](http://docs.ros.org/en/rolling/Concepts/Basic/About-Nodes.html) ⭐值得阅读
- [ROS2 对比 ROS1：去中心化与 DDS -- 古月居](https://book.guyuehome.com/ROS2/1.%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84/1.2_ROS2%E5%AF%B9%E6%AF%94ROS1/)
- [Lifecycle Manager 配置：默认接管节点列表 -- Nav2 Docs](https://docs.nav2.org/lyrical/configuration_and_development/configuration_guide/core_servers/configuring_lifecycle_manager/)

---

## 2. 一个 node（节点）到底是什么

官方定义很克制：**node 是 ROS 2 graph（计算图）里的一个参与者，是最小计算单元，每个节点应该只做一件逻辑上的事**。

落到代码里，一个 node（节点）能同时扮演五种角色：

- **publisher（发布者）**：往某个 topic（话题）上扔数据；
- **subscriber（订阅者）**：从某个 topic（话题）上收数据；
- **service server / client（服务端 / 客户端）**：提供或调用一问一答的接口；
- **action server / client（动作端 / 客户端）**：提供或调用带反馈的长任务；
- **parameter（参数）宿主**：暴露一堆可在运行时改的配置项。

所以一个「相机节点」并不是只会发图：它可能一边发 `/camera/image_raw`，一边提供 `/camera/set_exposure` 服务，还挂着一个 `exposure` 参数。**节点是职责的容器，不是函数的包装纸**。

### 2.1 最容易搞错的一点：node（节点）≠ process（进程）

这是新手最容易翻车的地方，也是本文后半段所有性能讨论的地基。

官方文档原话是：节点可以和 **同一个进程内** 的节点通信，也可以和 **不同进程** 、甚至 **不同机器** 上的节点通信。也就是说，节点是逻辑单元，进程是部署单元，两者不是一一对应关系。

| 维度 | 普通节点（可执行文件） | 可组合节点（component，组件） |
|------|------------------------|------------------------------|
| 打包形态 | 独立可执行文件 | 共享库（`.so`） |
| 加载方式 | 一个节点一个进程 | 多个节点装进一个 container（容器）进程 |
| 通信路径 | 走 DDS（数据分发服务）中间件 | 可走 intra-process（进程内）零拷贝 |
| 隔离性 | 完整进程隔离 | 共享进程空间，一起活一起死 |
| 启动方式 | `ros2 run` | `ros2 component load` 或 launch（启动文件） |

换句话说，**「拆节点」拆的是职责边界，不是物理进程数**。这条区分搞不清楚，后面就会得出「节点越多越慢」或者「节点越多越稳」两种相反的错觉。

本节参考资料：

- [Nodes -- ROS 2 Documentation](http://docs.ros.org/en/rolling/Concepts/Basic/About-Nodes.html) ⭐值得阅读
- [About Composition -- ROS 2 Documentation](http://docs.ros.org/en/ros2_documentation/foxy/Concepts/About-Composition.html)
- [ROS 2 Node Composition Explained -- Myzhar](https://myzhar.tech/tutorials/ros2/ros2-node-composition-explained/) ⭐值得阅读

---

## 3. 节点之间怎么协作：topic（话题）、service（服务）、action（动作）

节点之间 **不直接调用彼此的函数** 。这一点值得单独强调：你没法 `import` 隔壁节点的类然后 `obj.detect(img)`，因为隔壁可能跑在另一台机器上，可能是 C++ 写的，可能压根还没启动。

能用的只有三种接口，选错接口比写错算法更常见：

| 维度 | topic（话题） | service（服务） | action（动作） |
|------|---------------|-----------------|----------------|
| 通信模型 | 发布/订阅，多对多 | 请求/响应，一对一 | 目标/反馈/结果 |
| 时序 | 异步，发完不管 | 同步，等结果 | 异步，过程可见 |
| 适合的活儿 | 连续数据流 | 短任务、查状态 | 长任务、可取消 |
| 典型例子 | 图像、点云、轮速、里程计 | 查询当前地图、触发一次标定 | 导航到目标点、机械臂抓取 |
| 谁决定节奏 | 发布者 | 客户端 | 客户端发起，服务端推进 |

三者的边界，官方给得挺干脆：topic 用于持续数据流；service 用于「立刻就能做完」的同步请求响应；action 用于「要跑一会儿，中途还想知道进度，并且允许取消」的长任务。

用生活场景翻译一遍：

- **topic（话题）是广播电台**：电台只管播，谁在听、听几台收音机，它不关心；
- **service（服务）是打客服电话**：你拨号、等接通、问一句、拿答案、挂断，全程占线；
- **action（动作）是点外卖**：下单之后能看骑手到哪了（feedback，反馈），中途还能取消（cancel），最后拿到结果。

为什么非要绕这一层，而不是直接函数调用？三个理由，个个都很实际：

1. **语言与机器无关**：Python 写的规划节点可以调用 C++ 写的控制节点，跨机器也行；
2. **可观测**：`ros2 topic echo` 一敲，链路上流动的数据全看得见，函数调用可没这待遇；
3. **可替换**：只要 msg（消息）定义不变，把 A 算法换成 B 算法，别的节点一行都不用改。

本节参考资料：

- [Interfaces (topics, services, actions) -- ROS 2 Documentation](http://docs.ros.org/en/ros2_documentation/rolling/ROS-Framework/Interfaces-Topics-Services-Actions.html) ⭐值得阅读
- [Topics vs Services vs Actions -- ROS 2 Documentation](http://docs.ros.org/en/foxy/How-To-Guides/Topics-Services-Actions.html)
- [Actions 设计文档 -- ROS 2 Design](https://design.ros2.org/articles/actions.html)
- [ROS2 话题、服务、动作通讯 -- CSDN](https://blog.csdn.net/jiugeshao/article/details/161753260)

---

## 4. 为什么要拆：四个收益和三个代价

### 4.1 收益一：fault isolation（故障隔离）

这是拆节点最硬的理由，也是「一个节点崩了其他节点照跑」这句话的由来。

想象一下所有功能都在一个进程里：感知模块读图时越界了，`Segmentation fault`，整个进程被内核带走——底盘控制、刹车指令、状态发布全部陪葬。车还在动，控制权却没了，这不是段子，是真实事故的常见成因 😨。

拆成独立进程之后，感知节点崩了，控制节点还在跑，`lifecycle_manager`（生命周期管理器）可以把它拉起来重配。**崩溃域被限制在一个节点里**，这就是 fault isolation（故障隔离）的字面意思。

⚠️ 但这里有个前提：**这条结论只对「独立进程」成立**。如果你为了性能把感知、规划、控制全塞进同一个 container（容器），那它们共享同一个崩溃域，容器一挂全挂。收益和代价是一枚硬币的两面，别只记前半句。

### 4.2 收益二：可替换、可复用

接口一旦定成 msg（消息）/ srv（服务）/ action（动作）定义，节点内部就是黑盒。换激光雷达品牌？只换驱动节点。换规划算法？只换 `planner_server`。这种「插拔式」替换，是机器人项目能活过三年的关键——毕竟三年里算法换两轮、硬件换一代是常态。

### 4.3 收益三：部署自由

ROS 2 的设计文档里专门写了一条 story：**把进程布局的决定推迟到部署时**。同一份节点代码，调试时一个节点一个进程（好断点、好看日志），上线时把高频链路合成一个进程（省序列化、省拷贝）。代码不改，布局可换——这才是拆节点真正的灵活性。

### 4.4 收益四：团队并行与独立测试

节点边界天然就是团队边界。做感知的喂一段录好的 rosbag（数据包）就能跑，不用等底盘联调；做规划的给个假的目标点就能测，不用等真车。**能单独跑起来的单元，才是能单独测试的单元。**

### 4.5 代价一：serialization（序列化）与拷贝

跨进程通信不是把指针递过去，而是把数据结构压成字节流、发出去、再解回来。图像、点云这种 MB 级消息，一次序列化+拷贝的开销非常可观。

代价二：调试链路变长。一次「车不走」的排查，可能要沿着 `驱动 → 定位 → 规划 → 控制` 四五个节点逐段 `ros2 topic echo`，比在 IDE 里单步调试麻烦得多。

代价三：接口耦合。msg（消息）字段一改，全链路节点都得重新编译。这也是为什么接口定义要像 API 一样慎重评审。

### 4.6 拆到什么粒度算合适

一句话：**拆到职责，不拆到函数**。

反面案例我见过不止一次：有人把「读配置」「算角度」「发指令」各拆一个节点，最后 20 个节点配 2000 行 launch（启动文件），启动要 40 秒，调一个参数要改三个文件。这不是架构，这是把函数调用换了个更贵的语法 😑

本节参考资料：

- [Stories driving the development：Delay decision on process layout to deploy time -- ROS 2 Design](https://design.ros2.org/articles/stories.html) ⭐值得阅读
- [Changes between ROS 1 and ROS 2 -- ROS 2 Design](https://design.ros2.org/articles/changes)
- [About different ROS 2 DDS/RTPS vendors -- ROS 2 Documentation](https://docs.ros.org/en/crystal/Concepts/About-Different-Middleware-Vendors.html)
- [ROS 2 in a Nutshell: A Survey -- ACM](https://dl.acm.org/doi/pdf/10.1145/3815113)

---

## 5. 拆过头怎么办：composition（组件化）与 executor（执行器）

节点拆得越细，跨进程消息越多。ROS 2 给出的解法不是「少拆点」，而是 **让你在部署时把节点重新装进同一个进程** ——这就是 composition（组件化）。

### 5.1 composition（组件化）：把节点编成库，装进 container（容器）

做法是：节点不再写 `main`，而是继承 `rclcpp::Node` 编成共享库；启动时由一个 container（容器）进程动态加载多个节点。同容器内的节点之间可以走 intra-process（进程内）通信，C++ 下用 `unique_ptr` 或 loaned message 传递，**完全跳过序列化**。

收益有多实在？看两组实测：

- **ZED 相机官方 benchmark**：composed + zero-copy 平均延迟 18.06 ms，独立进程 20.17 ms；CPU 占用也从 93.6% 降到 89.4%；
- **RoboCup 案例研究**：开启进程内通信后，中位处理时间从 28.7 ms 降到 20.7 ms，下降约 33%。

⚠️ 但别急着全塞进去。ROS 2 的设计文档明确提醒：**只要图中还有节点在别的进程里，当前实现下开 intra-process 反而可能更差**。正确的划法是按链路划边界——高频大消息的那一段（相机→检测→跟踪）合成一个容器，低频控制指令留在外面。

### 5.2 executor（执行器）：单线程是默认，不是全部

节点内部靠 executor（执行器）驱动回调。默认的 `SingleThreadedExecutor` 就是一个线程转圈，所有 callback（回调）排队执行。

想并发就上 `MultiThreadedExecutor`，但会立刻撞上 callback group（回调组）：**每个节点的默认回调组是 MutuallyExclusive（互斥）**，同一个组里的回调永远串行。于是出现了最经典的死锁场景——在回调里同步调用一个 service，而这个 service 的回调也在同一个互斥组里排队，两边互相等，谁也不让 😵。

解法有两条：把相关回调放进 `ReentrantCallbackGroup`（可重入回调组），或者干脆改成异步调用。官方文档的说法很直白：不要在回调里做同步调用。

### 5.3 lifecycle（生命周期）：让节点有序上下电

节点多了，启动顺序就成了问题。总不能规划节点比地图节点先起来吧？

lifecycle（生命周期）节点用状态机管这件事，主状态四个：`unconfigured`（未配置）→ `inactive`（未激活）→ `active`（运行）→ `finalized`（已结束），中间还有 `configuring`、`activating`、`cleaningup` 等过渡态。Nav2 就是靠 `lifecycle_manager` 按依赖顺序把十几个节点依次 `configure`、`activate`，任何一个不响应就整体回滚。

一句话对比：普通节点是「插上电就干活」，lifecycle（生命周期）节点是「先自检、再待命、听口令上电」。

本节参考资料：

- [Setting up efficient intra-process communication -- ROS 2 Documentation](http://docs.ros.org/en/rolling/ROS-Framework/nodes/Working-with-nodes/intra-process/Intra-Process-Communication.html) ⭐值得阅读
- [Intra-process Communications in ROS 2 -- ROS 2 Design](https://design.ros2.org/articles/intraprocess_communications.html)
- [Impact of ROS 2 Node Composition in Robotic Systems -- arXiv](https://arxiv.org/pdf/2305.09933) ⭐值得阅读
- [ZED Topic Benchmark Tool：composed vs separate process -- StereoLabs](https://www.stereolabs.com/docs/integrations/ros-2/topic-benchmark-tool)
- [ROS 2 for RoboCup：进程内通信实测 -- arXiv](https://arxiv.org/pdf/1907.00282.pdf)
- [Using Callback Groups -- ROS 2 Documentation](http://docs.ros.org/en/rolling/ROS-Framework/nodes/Working-with-nodes/Using-callback-groups.html) ⭐值得阅读
- [Managed nodes -- ROS 2 Design](https://design.ros2.org/articles/node_lifecycle.html)
- [lifecycle 包状态机说明 -- ROS 2 Documentation](http://docs.ros.org/en/rolling/p/lifecycle/)

---

## 6. 一段能直接跑的代码：一个进程里跑两个节点

光说概念没意思，下面这段只用 `rclpy` 和 `std_msgs`，**一个文件、两个节点、一个 topic（话题）**，复制下来就能跑。它同时演示了两件事：节点之间确实不互相调用，以及多个节点可以共处一个进程。

```python
"""two_nodes_demo.py：一个进程里跑两个节点，通过 topic（话题）通信。

运行前先 source 你的 ROS 2 环境，然后：
    python3 two_nodes_demo.py
"""
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String


class Talker(Node):
    """发布者节点：每秒往 chatter 话题上发一条带序号的消息。"""

    def __init__(self):
        super().__init__("talker")                                           # 节点名，graph（计算图）里唯一
        self.publisher = self.create_publisher(String, "chatter", 10)        # 队列深度 10，满了丢旧消息
        self.count = 0                                                       # 自增序号，方便肉眼确认没丢包
        self.timer = self.create_timer(1.0, self.tick)                       # 1 秒触发一次回调

    def tick(self):
        """定时器回调：构造并发布一条消息。"""
        msg = String()
        msg.data = f"hello {self.count}"                                     # 载荷：hello 0、hello 1 ...
        self.publisher.publish(msg)                                          # 交给 DDS（数据分发服务）投递
        self.get_logger().info(f"发布: {msg.data}")                          # 终端可见，方便对照
        self.count += 1


class Listener(Node):
    """订阅者节点：收到 chatter 话题的消息就打印。"""

    def __init__(self):
        super().__init__("listener")
        self.subscription = self.create_subscription(
            String, "chatter", self.on_msg, 10                               # 类型、话题、回调、队列深度
        )

    def on_msg(self, msg):
        """订阅回调：只在消息到达时被 executor（执行器）调用。"""
        self.get_logger().info(f"收到: {msg.data}")


def main():
    """装配两个节点并交给多线程执行器驱动。"""
    rclpy.init()                                                             # 初始化 rclpy 上下文
    executor = MultiThreadedExecutor()                                       # 两个节点并发转，互不阻塞
    talker, listener = Talker(), Listener()                                  # 同进程内的两个独立节点
    executor.add_node(talker)
    executor.add_node(listener)
    try:
        executor.spin()                                                      # 阻塞式转圈，直到 Ctrl+C
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        talker.destroy_node()
        listener.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
```

跑起来后终端会稳定输出成对的日志：

```text
[INFO] [talker]: 发布: hello 0
[INFO] [listener]: 收到: hello 0
[INFO] [talker]: 发布: hello 1
[INFO] [listener]: 收到: hello 1
```

想验证「节点是逻辑单元、进程是部署单元」，另开一个终端跑这三条命令：

```bash
ros2 node list                  # 只看得到 /talker 和 /listener 两个节点
ros2 node info /talker          # 看到它的 publisher、timer 和参数
ros2 topic echo /chatter        # 第三个进程也能收到同一条消息
```

注意最后一条：`ros2 topic echo` 是 **第三个进程** ，它没改一行代码就接上了这条链路——这就是接口解耦的直观证据。

本节参考资料：

- [Writing a simple publisher and subscriber (Python) -- ROS 2 Documentation](http://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)
- [rclpy Node API -- ROS 2 Documentation](http://docs.ros.org/en/kilted/p/rclpy/api/node.html)
- [Executors 与回调组概念 -- ROS 2 Documentation](http://docs.ros.org/en/jazzy/p/synchros2/_sources/concepts/execution_and_callback_groups.md.txt)

---

## 7. 五类症状对照表

| 症状（Symptom） | 原因（Cause） | 解法（Fix） |
|-----------------|---------------|-------------|
| 改了一个算法，整车都要重新编译部署 | 所有功能塞在一个可执行文件里 | 按职责拆 node（节点），单节点单独构建发布 |
| 相机节点一崩，底盘也跟着停 | 所有节点共享同一个崩溃域 | 拆成独立 process（进程），用 launch（启动文件）配 `respawn` 重启策略 |
| 节点拆细后 CPU 飙高、延迟反而变大 | 每条 MB 级消息都走 DDS（数据分发服务）序列化+拷贝 | 用 composition（组件化）把高频链路装进一个 container（容器），开 intra-process（进程内）零拷贝 |
| 回调里调用 service，整个节点卡死 | 默认 MutuallyExclusive callback group（互斥回调组）自己锁自己 | 改用 `ReentrantCallbackGroup`（可重入回调组）+ 多线程 executor（执行器），或改异步调用 |
| `ros2 node list` 刷出一长串，不知道该管谁 | 缺少启动编排，节点各自为政 | 用 lifecycle（生命周期）节点 + lifecycle manager 有序上下电 |

## 8. 小结：拆的是职责，不是文件

把整篇压缩成四句话：

1. **ROS 2 没有主程序**，只有 graph（计算图）里的 node（节点），靠 topic（话题）、service（服务）、action（动作）三种接口连线；
2. **拆节点的收益是 fault isolation（故障隔离）与部署自由**，代价是 serialization（序列化）开销和更长的调试链路；
3. **node（节点）不等于 process（进程）**，composition（组件化）让「代码上拆开、部署时合并」成为可能；
4. **粒度看职责**：一个节点一件事，不是一个函数一个节点。

回到那个问题——为什么一台小车要跑二三十个节点？因为 **没人会把发动机、变速箱、刹车焊成一整块铁** 。坏了没法换，撞了没法救，想升级只能整车报废。ROS 2 的节点拆分，本质上就是把汽车工业的零件化思路搬进了软件 🚗。

至于拆多少个才合适，我的判断标准很土：**如果一个节点的代码需要写两个不同的 `TODO: 以后拆出去`，那它现在就该拆了。**

**最后更新时间**：2026-10-24
