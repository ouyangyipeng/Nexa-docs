---
comments: true
---

# 首页：欢迎来到 Nexa 官方文档

**Nexa 语言** 是一门为大语言模型（LLM）与智能体系统（Agentic Systems）量身定制的**智能体原生 (Agent-Native) 编程语言**。

当代 AI 应用开发充斥着大量的 Prompt 拼接、臃肿的 JSON 解析套件、不可靠的正则验证，以及日益复杂的第三方生态框架。Nexa 旨在打破这种“胶水代码”的魔咒。我们将高层级的**意图路由**、**多智能体并发组装**、**管道流传输**以及**工具执行沙盒**提权为核心语法一等公民。

通过底层的 `Transpiler` 机制，Nexa 代码可直接被转换为稳定可靠的 Python Runtime，让你能够用最优雅、原生的语法定义最硬核的 LLM 计算图（DAG）。

---

## 🔥 Nexa 的核心亮点：Cognitive Architecture

Nexa 最新版本（v0.8+）引入了全新的认知架构（Cognitive Architecture）功能，重点强化了**类型安全**、**资源治理**以及**人机协同（HITL）**：

### 1. 强类型协议约束 (`protocol` & `implements`)
告别不可控的模型字符串输出！原生支持契约式编程，利用内部 Pydantic 动态编译引擎，让 Agent 的输出严格遵守指定 Schema，并自带语法级别的**自修正重试循环**机制。

```nexa
protocol ReviewResult {
    score: "int"
    summary: "string"
}

// 代理自动继承并遵守上述协议
agent Reviewer implements ReviewResult { 
    prompt: "Review the code..."
}
```

### 2. 多模型动态路由 (`model` & Routing)
从此解耦于对某一家厂商（如 OpenAI 或 Anthropic）的强依赖。你可以针对每个智能体动态指定运行时的模型端点，在一套代码内构建起极其灵活的跨厂模型流水线。

```nexa
// 复杂任务交给推理级模型
agent Coder { model: "deepseek/deepseek-chat", prompt: "..." }

// 轻量级任务交给响应及时的极速模型
agent Translator { model: "minimax/m2.5", prompt: "..." }
```

### 3. 原生管道流与数据总线 (`>>`)
智能体之间的通信不再需要编写繁琐的消息管理器。使用 `>>` 操作符将数据如 Unix 管道一般传递给下一个智能体，或者使用 `join` 机制并发收集多路信息。

```nexa
flow main {
    // 将代码生成的结果无缝传递给审查者，再传递给人类界面
    res = Coder.run("Generate code") >> Reviewer >> HumanInterface;
}
```

---

## 🎯 设计哲学：写流程，而非胶水代码

阅读本文档的开发者，想必已经受够了在传统语言中通过繁杂的 HTTP 请求和嵌套 `if-else` 来处理模型幻觉的折磨。

Nexa 把“语言模型预测”视为一个天然的计算节拍，将“不确定性”隔离在语法边界内。在接下来的章节中，我们将由浅入深，从 **Agent 声明**、**工作流调教**，到进阶的 **Pipeline 管道**与 **循环纠正语义** 为你揭开智能体原生编程的帷幕。

!!! success "立即启程"
    准备好体验未来的编程范式了吗？请点击下方导航进入 [前言：背景与理念](preface.md)！

