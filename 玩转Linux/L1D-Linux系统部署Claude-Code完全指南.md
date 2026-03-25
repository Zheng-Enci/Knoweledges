前提（我的经验）：

在实际部署过程中，我遇到了一个关键问题：**GLIBC 版本过低导致 Claude Code 安装失败**。

**错误日志示例**：
```
Now using node v18.20.8
[root@localhost local]# node -V
'GLIBC 2.27' not found (required by node)
node: /lib64/libm.so.6: version 'GLIBC 2.25' not found (required by node)
node: /lib64/libc.so.6: version 'GLIBC_2.28' not found (required by node)
node: /lib64/libstdc++.so.6: version 'CxxABI_1.3.9' not found (required by node)
node: 'GLIBCXX 3.4.20' not found (required by node)
node: /lib64/libstdc++.so.6: version 'GLIBCXX_3.4.21' not found (required by node)
```

**安装失败日志**：
```
[root@localhost local]# npm install -g @anthropic-ai/claude-code
npm WARN config global --global, --local are deprecated. Use --location=global instead
npm WARN EBADENGINE Unsupported engine {
  package: '@anthropic-ai/claude-code@2.1.81',
  required: { node: '>=18.0.0' },
  current: { node: 'v17.9.1', npm: '8.11.0' }
}
```

**核心问题分析**：
Linux 系统的 GLIBC 版本不能太低，否则只能安装最高支持 Node.js 17 的版本。但是 Claude Code 最低要求 Node.js 版本为 18，所以 GLIBC 版本过低会导致 Claude Code 安装失败，因为连 Node.js 18 都无法成功安装。

第一步


curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

\. "$HOME/.nvm/nvm.sh"

nvm install 17

node -v 

npm -v 

第二步
npm install -g @anthropic-ai/claude-code

第三步
claude --version

第四步
claude