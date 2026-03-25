---
comments: true
---

# Nexa Architecture Evolution Plan

> This document records the technical planning and design blueprint for Nexa language's future architecture evolution

## 1. Rust AVM Foundation (Agent Virtual Machine)

### 1.1 Design Goals

Transition from Python script interpretation transpilation mode to an independently compiled Agent Virtual Machine (AVM) written in Rust.

### 1.2 Architecture Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Nexa AVM Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Nexa       │  │  AST        │  │  Bytecode           │  │
│  │  Compiler   │→ │  Generator  │→ │  Generator          │  │
│  │  (Rust)     │  │  (Rust)     │  │  (Rust)             │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                              ↓                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    AVM Runtime (Rust)                    │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────┐ │ │
│  │  │ Scheduler │ │ Memory    │ │ Tool      │ │ Sandbox │ │ │
│  │  │           │ │ Manager   │ │ Registry  │ │ (WASM)  │ │ │
│  │  └───────────┘ └───────────┘ └───────────┘ └─────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Core Components

#### Compiler Frontend
- **Language**: Rust
- **Lexical Analysis**: Using `logos` crate for high-performance lexical analysis
- **Syntax Parsing**: Using `lalrpop` or hand-written recursive descent parser
- **AST**: Type-safe abstract syntax tree representation

#### Bytecode Design
```rust
// Nexa bytecode instruction set
enum NexaOpcode {
    // Agent operations
    AgentCreate { name: StringId },
    AgentRun { agent_id: u32 },
    AgentClone { agent_id: u32 },
    
    // Flow control
    Pipeline { stages: Vec<u32> },
    Fork { agents: Vec<u32> },
    Merge { strategy: MergeStrategy },
    
    // Memory operations
    MemStore { key: StringId, scope: MemoryScope },
    MemLoad { key: StringId },
    
    // Tool calls
    ToolCall { tool_id: u32, args: Vec<Value> },
    
    // Control flow
    Jump { offset: i32 },
    JumpIf { condition: bool, offset: i32 },
    SemanticIf { pattern: StringId },
    
    // LLM calls
    LLMCall { model: StringId },
    LLMStream { model: StringId },
}
```

#### AVM Runtime
- **Scheduler**: Tokio-based async task scheduling
- **Memory Management**: Zero-copy message passing, arena allocator
- **Tool Registry**: Dynamic WASM module loading
- **Security Sandbox**: WASMI integration, resource limits

### 1.4 Performance Targets

| Metric | Python Transpiler | Rust AVM |
|------|--------------|----------|
| Compilation Time | ~100ms | ~5ms |
| Startup Time | ~500ms | ~10ms |
| Memory Footprint | ~100MB | ~10MB |
| Concurrent Agents | ~100 | ~10000 |

### 1.5 Migration Path

1. **Phase 1**: Rewrite compiler frontend in Rust, generate Python code (current)
2. **Phase 2**: Implement bytecode compiler and simple VM
3. **Phase 3**: Migrate core runtime to Rust
4. **Phase 4**: Fully independent AVM, Python as FFI extension

---

## 2. WASM Security Sandbox

### 2.1 Design Goals

Introduce WebAssembly in AVM to provide strong isolation and cross-platform compatibility for external `tool` execution.

### 2.2 Architecture Design

```
┌─────────────────────────────────────────────────────────────┐
│                    WASM Sandbox Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Host Interface                      │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │  │
│  │  │ stdin/stdout│ │ filesystem  │ │ network (HTTP)  │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                              ↓ WASI                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    WASM Runtime                        │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Tool 1 (WASM)  │  Tool 2 (WASM)  │  Tool N     │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  Resource Limits: CPU Time | Memory | Filesystem | Network  │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Security Policy

```rust
// WASM resource limit configuration
struct WasmResourceLimits {
    max_memory_pages: u32,      // Maximum memory pages
    max_table_elements: u32,    // Maximum table elements
    max_cpu_time_ms: u64,       // Maximum CPU time
    max_file_size: u64,         // Maximum file size
    allowed_paths: Vec<PathBuf>, // Allowed access paths
    allowed_hosts: Vec<String>,  // Allowed access hosts
    network_enabled: bool,       // Whether network is allowed
}

impl Default for WasmResourceLimits {
    fn default() -> Self {
        Self {
            max_memory_pages: 256,    // 16MB
            max_table_elements: 1024,
            max_cpu_time_ms: 5000,    // 5 seconds
            max_file_size: 10 * 1024 * 1024, // 10MB
            allowed_paths: vec![],
            allowed_hosts: vec![],
            network_enabled: false,
        }
    }
}
```

### 2.4 Tool Development SDK

```rust
// WASM tool development SDK
use nexa_wasm_sdk::*;

#[nexa_tool(
    name = "calculator",
    description = "Perform mathematical calculations"
)]
fn calculate(
    #[param(description = "Mathematical expression")] expression: String
) -> ToolResult<f64> {
    // Tool implementation
    let result = eval_expression(&expression)?;
    Ok(result)
}
```

---

## 3. Visual DAG Editor

### 3.1 Design Goals

Provide a web-based node drag-and-drop interface that supports reverse generation of Nexa code.

### 3.2 Technology Stack

- **Frontend**: React + TypeScript
- **Graphics Library**: React Flow / X6
- **Backend**: Rust (Axum) + WebSocket
- **Real-time Sync**: CRDT for collaborative editing

### 3.3 Node Type Design

```typescript
// DAG node type definition
interface DAGNode {
  id: string;
  type: 'agent' | 'tool' | 'condition' | 'fork' | 'merge' | 'transform';
  position: { x: number; y: number };
  data: {
    label: string;
    config: Record<string, any>;
    inputs: Port[];
    outputs: Port[];
  };
}

// Port definition
interface Port {
  id: string;
  name: string;
  type: 'string' | 'object' | 'stream';
  required: boolean;
}

// Edge definition
interface DAGEdge {
  id: string;
  source: string;
  target: string;
  sourceHandle: string;
  targetHandle: string;
  label?: string;
}
```

### 3.4 Code Generation

```typescript
// DAG to Nexa code generation
function generateNexaCode(dag: DAGGraph): string {
  const agents = dag.nodes.filter(n => n.type === 'agent');
  const edges = dag.edges;
  
  let code = '';
  
  // Generate Agent declarations
  for (const agent of agents) {
    code += generateAgentDeclaration(agent);
  }
  
  // Generate Flow
  code += 'flow main {\n';
  code += generateFlowBody(dag);
  code += '}\n';
  
  return code;
}
```

### 3.5 Feature Planning

1. **Phase 1**: Basic editor, support node drag-and-drop and connection
2. **Phase 2**: Real-time preview and code generation
3. **Phase 3**: Collaborative editing and version control
4. **Phase 4**: Debugging and performance analysis integration

---

## 4. Smart Scheduler

### 4.1 Design Goals

Dynamically allocate concurrent resources at the AVM layer based on system load and Agent priority.

### 4.2 Scheduling Strategies

```rust
// Scheduler configuration
struct SchedulerConfig {
    max_concurrent_agents: usize,
    priority_levels: u8,
    time_slice_ms: u64,
    load_balance_strategy: LoadBalanceStrategy,
}

enum LoadBalanceStrategy {
    RoundRobin,
    LeastLoaded,
    WeightedFair,      // Weight-based fair scheduling
    PriorityBased,     // Priority scheduling
    Adaptive,          // Adaptive scheduling
}

// Agent scheduling information
struct AgentScheduleInfo {
    agent_id: AgentId,
    priority: u8,
    weight: f32,
    estimated_duration_ms: u64,
    dependencies: Vec<AgentId>,
    resource_requirements: ResourceRequirements,
}
```

### 4.3 Scheduling Algorithm

```rust
impl Scheduler {
    // Adaptive scheduling decision
    fn schedule(&mut self, agents: Vec<AgentScheduleInfo>) -> SchedulePlan {
        // 1. Build dependency graph
        let dep_graph = self.build_dependency_graph(&agents);
        
        // 2. Topological sort
        let order = dep_graph.topological_sort();
        
        // 3. Parallelism analysis
        let parallel_groups = self.analyze_parallelism(&order);
        
        // 4. Resource allocation
        let allocation = self.allocate_resources(&parallel_groups);
        
        // 5. Generate scheduling plan
        SchedulePlan {
            stages: parallel_groups,
            allocation,
            estimated_total_time: self.estimate_completion_time(&allocation),
        }
    }
    
    // Dynamic load balancing
    fn rebalance(&mut self, current_load: &SystemLoad) -> Vec<ScheduleAdjustment> {
        let adjustments = Vec::new();
        
        // Detect overloaded nodes
        for node in &current_load.nodes {
            if node.utilization > 0.8 {
                // Migrate some tasks to low-load nodes
                adjustments.extend(self.migrate_tasks(node));
            }
        }
        
        adjustments
    }
}
```

---

## 5. Vector Virtual Memory Paging (Context Paging)

### 5.1 Design Goals

AVM takes over memory and automatically performs vectorized swapping and transparent loading of conversation history.

### 5.2 Architecture Design

```
┌─────────────────────────────────────────────────────────────┐
│                  Context Paging Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Active Memory (RAM)                     │    │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────────────┐  │    │
│  │  │ Context   │ │ Working   │ │ Vector           │  │    │
│  │  │ Window    │ │ Memory    │ │ Index (Hot)      │  │    │
│  │  └───────────┘ └───────────┘ └───────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↑↓ Swap                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Paged Storage (Disk/Vector DB)          │    │
│  │  ┌───────────────────────────────────────────────┐  │    │
│  │  │  Page 1   │  Page 2   │  Page 3   │  ...     │  │    │
│  │  │  (vec)    │  (vec)    │  (vec)    │          │  │    │
│  │  └───────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Paging Strategy

```rust
// Paging configuration
struct PagingConfig {
    page_size: usize,           // Messages per page
    max_active_pages: usize,    // Maximum active pages
    embedding_model: String,    // Embedding model
    similarity_threshold: f32,  // Similarity threshold
    eviction_policy: EvictionPolicy,
}

enum EvictionPolicy {
    LRU,           // Least Recently Used
    LFU,           // Least Frequently Used
    Relevance,     // Relevance-based
    Hybrid,        // Hybrid strategy
}

// Memory page
struct MemoryPage {
    id: PageId,
    messages: Vec<Message>,
    embedding: Vec<f32>,      // Page summary embedding
    last_accessed: Instant,
    access_count: u64,
    relevance_score: f32,
}
```

### 5.4 Page Loading

```rust
impl ContextPager {
    // Intelligent page loading
    async fn load_relevant_pages(&mut self, query: &str) -> Vec<MemoryPage> {
        // 1. Calculate query embedding
        let query_embedding = self.embed(query).await;
        
        // 2. Vector search to find relevant pages
        let relevant = self.vector_index
            .search(&query_embedding, self.config.max_active_pages)
            .await;
        
        // 3. Load pages to active memory
        let mut pages = Vec::new();
        for page_id in relevant {
            if !self.is_active(page_id) {
                let page = self.load_page(page_id).await;
                pages.push(page);
            }
        }
        
        // 4. Evict old pages if necessary
        self.ensure_capacity();
        
        pages
    }
    
    // Page eviction
    fn ensure_capacity(&mut self) {
        while self.active_pages.len() > self.config.max_active_pages {
            let to_evict = self.select_eviction_candidate();
            self.swap_out(to_evict);
        }
    }
}
```

---

## 6. Implementation Roadmap

### 2024 Q1-Q2: Infrastructure
- [ ] Rust compiler frontend prototype
- [ ] WASM runtime integration
- [ ] Basic scheduler implementation

### 2024 Q3-Q4: Core Features
- [ ] Bytecode compiler
- [ ] Visual editor MVP
- [ ] Vector paging prototype

### 2025 Q1-Q2: Production Ready
- [ ] AVM stable release
- [ ] Complete security sandbox
- [ ] Editor official release

### 2025 Q3-Q4: Ecosystem Expansion
- [ ] Plugin system
- [ ] Cloud deployment
- [ ] Enterprise features

---

*This document will be continuously updated as the project progresses*