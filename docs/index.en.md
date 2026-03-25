---
comments: true
---

<div class="portal-hero" style="margin-top: 2rem;">
  <p class="portal-kicker">Agent-Native · Concurrent DAG · LLM</p>
  <h1>Empowering the New Era of Agent-Native Programming</h1>
  <p class="portal-lead">
    Say goodbye to verbose glue code, complex prompt concatenation, and fragile JSON parsing. Nexa elevates intent routing, multi-agent collaboration, and pipeline streaming into core syntax, enabling you to build hardcore LLM concurrency graphs with ultimate elegance.
  </p>
  <div class="portal-actions">
    <a class="md-button md-button--primary" href="en/quickstart/">🚀 Quickstart</a>
    <a class="md-button" href="en/part1_basic/">📖 Basic Syntax</a>
    <a class="md-button" href="en/examples/">💡 Examples</a>
  </div>
</div>

---

## 🆕 v1.0-alpha Revolutionary Update: The AVM Era

Nexa v1.0-alpha introduces the revolutionary **Agent Virtual Machine (AVM)** — a high-performance, securely isolated agent execution engine written in Rust:

### 🦀 Rust AVM Foundation

Transitioning from Python script transpilation to a standalone compiled Agent Virtual Machine written in Rust:

| Feature | Description |
|-----|------|
| **High-Performance Bytecode Interpreter** | Native execution of compiled Nexa bytecode |
| **Complete Compiler Frontend** | Lexer → Parser → AST → Bytecode |
| **110+ Test Coverage** | Full-link testing ensuring stability |

### 🔒 WASM Security Sandbox

Introducing WebAssembly in AVM to provide strong isolation for external `tool` execution:

- **wasmtime Integration** - High-performance WASM runtime
- **Permission Grading** - Four-tier model: None/Standard/Elevated/Full
- **Resource Limits** - Constraints on memory, CPU, and execution time
- **Audit Logs** - Complete operation audit tracking

### ⚡ Smart Scheduler

Dynamic allocation of concurrency resources at the AVM layer based on system load:

- **Priority Queue** - Task scheduling based on Agent priority
- **Load Balancing** - Strategies: RoundRobin, LeastLoaded, Adaptive
- **DAG Topological Sorting** - Automatic dependency resolution and parallelism analysis

### 📄 Vector Virtual Memory Paging

AVM manages memory, automatically performing vectorized swapping of conversation history:

- **LRU/LFU/Hybrid Eviction Policies** - Intelligent page replacement
- **Embedding Similarity Search** - Loading based on semantic relevance
- **Transparent Page Loading** - Seamless memory management

### Performance Comparison

| Metric | Python Transpiler | Rust AVM |
|------|--------------|----------|
| Compile Time | ~100ms | ~5ms |
| Startup Time | ~500ms | ~10ms |
| Memory Usage | ~100MB | ~10MB |
| Concurrent Agents | ~100 | ~10000 |

---

## 🔥 Core Advantage: Cognitive Architecture

The latest version of Nexa introduces new cognitive architecture features, focusing on **type safety**, **resource governance**, and **Human-in-the-Loop (HITL)**:

### 1. Strong Type Protocol Constraints (`protocol` & `implements`)

No more uncontrollable model string outputs! Native support for contract-based programming, utilizing an internal Pydantic dynamic compilation engine. Agent outputs strictly adhere to the specified Schema, featuring a syntax-level **self-correction retry loop**.

```nexa
protocol ReviewResult {
    score: "int",
    summary: "string"
}

// Agent automatically inherits and follows the protocol above
agent Reviewer implements ReviewResult { 
    prompt: "Review the code..."
}
```

### 2. Multi-Model Dynamic Routing (`model` & Routing)

Decouple from vendor lock-in. You can dynamically specify model endpoints at runtime for each agent, building flexible cross-vendor data flows.

```nexa
// Hand over complex tasks to reasoning-level models
agent Coder { model: "deepseek/deepseek-chat", prompt: "..." }

// Hand over lightweight tasks to lightning-fast models
agent Translator { model: "minimax/minimax-m2.5", prompt: "..." }
```
