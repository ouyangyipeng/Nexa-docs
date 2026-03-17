---
comments: true
---

# 4. 语法扩展：契约、类型与协议 (Protocols & Types)

在前面我们学习了宏观的、具有拓扑结构的路由控制流。但在真实的、冷酷的企业级生产环境中，最致命的永远是**大模型的非结构化输出**机制带来的不可确定性。

传统的微服务之间使用 Thrift, gRPC 或 RESTful 协议交换严格的 JSON。然而大模型随时可能给你返回一段充满思考和语气的 “Here is your result:\n {...}”。这将轻易击穿后续 Java/Go 系统脆弱的解码器（Decoder）。

本章着眼于介绍 Nexa 针对该痛点独创的高阶重塑特性：**类型协议 (Protocols)** 和 **多模智能路由**。它们是系统稳定性的压舱石。

---

## 📜 引入 `protocol` 关键字 (编译器级别的 Pydantic)

只要业务流需要被下游其他非大语言模型服务（如数据库写入、前端渲染）所消费，我们就必须强制约束大模型仅仅返回特定格式的数据。

以往，你需要导入复杂的 JSON 解析工具（比如 Python 中的 `Pydantic` 或者 TypeScript 的 `Zod`），再将 Schema 序列化为数十行的 JSON 约束强行附加在 Prompt 的末尾。
在 Nexa 语言中，我们直接将约束语法提权成了第一公民，像定义 `struct` 或是 `class` 那样使用 `protocol`：

```nexa
// Nexa 语言内建的协议定义，支持丰富的类型系统包括 list, dictionary 以及嵌套协议
protocol ReviewResult {
    score: "int"
    summary: "string"
    bug_list: "list[string]"
    is_critical: "boolean"
}
```

Nexa 对于类型的偏执达到了编译层面的深度。所有此处定义的属性不仅会在执行前被转化为各大模型（如 GPT-4, Claude-3）原生支持的 `Structured Output / Function Schema` 参数体系，还会被内嵌到反序列化保护沙盒内。

## 🛡️ `implements` 实现保障与黑箱重试机制

定义完协议只是第一步，Agent 应该如何与其产生强制交集？只需要用我们再熟悉不过的面向对象语言当中的继承逻辑——`implements` 接口继承即可：

```nexa
@limit(max_tokens=600)
agent Coder {
    prompt: "Write a short Python implementation of quicksort.",
    model: "minimax/m2.5"
}

// Reviewer 这个模型将受到契约约束，确保最终系统只能收到干净的 JSON 属性实体。
agent Reviewer implements ReviewResult {
    prompt: "Review the provided code. Provide your score and list all bugs.",
    model: "deepseek/deepseek-chat"
}

flow main {
    // 整个数据结构将无缝作为 Python Object/JSON 传入外部 API
    result = Coder.run("Generate Quicksort") >> Reviewer;
}
```

!!! warning "运行时的魔法：自动重试纠偏 (Auto-Retry Matrix)"
    这是你在常规系统里绝不可能轻松写出的机制：
    表面上看，`implements` 只是绑定了一个声明。但在背地里，大模型有时候依然会犯病（比如只给了 `score` 却忘了给 `bug_list`，或者把 `is_critical` 错误地拼成字符串 "true"）。
    遇到这种情况，你以前的 Python 脚本由于 `JSONDecodeError` 肯定当场崩溃了。
    **但是在 Nexa 的防线中，底层 Evaluator 会拦截这笔返回 Token，立即对比 Schema。如果发现类型脱轨——它会自动将 Pydantic/Traceback 的报错信息转换为自然语言塞回去，静默触发模型的“二次内省”！**
    “对不起，你的输出少了 bug_list，请修正并重新输出”。这一整个轮回对前台代码编写者是**完全无感**的。

---

## 🧠 Model Routing (按任务能力切分脑区)

不仅仅是数据结构的严格管控，一门优秀的语言还需要为开发者解决“金钱”问题。大模型的 Token 计算力是极其昂贵的。

Nexa 允许你在 `model` 声明上通过数组和字典指定差异化的能力退让（Fallback），构建出健壮的高可用模型中枢。

### 优雅的 Fallback 降级机制

当主线模型宕机、被平台限流（Rate Limit）或者遭遇超时（Timeout）时，通常需要大段的 `try...except...retry` 与轮换逻辑进行保护。在 Nexa 中仅需一句宣告：

```nexa
// 如果主力超大杯模型无法响应，甚至发生内部错误，自动降级去请求 Opus 或更小的开源模型。
agent HeavyMathBot {
    model: ["gpt-4-turbo", fallback: "claude-3-opus", fallback: "llama-3-8b"] 
    prompt: "You solve extreme math problems."
}
```

通过将 `protocol` 的刚性契约与动态 `fallback` 流转网络相结合，Nexa 在赋予高度“思考灵活性”的同时，从未抛弃几十年来传统软件工程所积累的“鲁棒性与边界确定性”基因。这也是 Agent 开发向正规化轨道迈出的决定性一步。
