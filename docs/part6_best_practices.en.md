---
comments: true
---

# 7. Production-Level Best Practices: Building High-Performance Agent Network Architecture

The gap between writing a cool Demo (Hello World) and building an enterprise-level Agent that can withstand high concurrency tests without triggering API Rate Limits or generating astronomical bills is like the difference between building a handcart and building a launch rocket.

Many developers, when first encountering AI programming, easily fall into the fanatical trap of "letting large models solve everything." When designing complex autonomous systems, **architecture decoupling and computational planning are far more critical than the fanciness of a single Prompt**. This chapter, based on our extensive experience in high-concurrency experiments and commercial deployments, provides highly practical pitfall-avoidance guidance and best practices.

---

## 🎭 Practice 1: Adhere to the Agent "Single Responsibility Principle" (SRP)

The Single Responsibility Principle, widely recognized in traditional software engineering, **in multi-agent systems concerns not only code quality but also directly concerns money and system latency!**

### Anti-Pattern: The Monolith Dilemma

Never force all `Prompt`s and dozens of `Tool`s into a single full-stack monolith node named `SuperBot`:

```nexa
// ❌ Extremely dangerous approach! Do not imitate!
agent GodBot {
    uses [
        std.web_search, std.os.file, std.database.sql, 
        my_custom_aws_api, std.git.commit
    ]
    role: "System God"
    prompt: """
        You are an almighty god. You can make plans, search when encountering problems,
        write and execute code, query databases, and return rigorous JSON.
    """
}
```

**Why is this approach extremely terrible?**

1. **Severe Hallucination Disaster**: In the attention mechanism (Self-Attention), when providing an LLM with dozens of external tools and lengthy multi-intent instruction packages, it often gets confused when judging "which tool should be selected," and even fabricates non-existent function parameters out of thin air.

2. **Terrifying Token Billing**: Large model architecture dictates that all candidate tool descriptions (Function Schemas & docstrings) must be sent together with the `System Prompt` every time! If there are 20 tools, a single call might unnecessarily consume 3000 Token context. Every small interaction must pay the cost of this mountain.

### Best Practice: Domain Expert Network Based on Pipeline Segmentation

Let professionals do professional things. Use pipelines and strict structural decomposition:

```nexa
import "std"

agent TaskPlanner {
    role: "Architect"
    prompt: "You only break user constraints into atomic steps."
}

agent ResearchSearcher {
    uses [std.web_search]  // Only it needs to consume search tool Tokens
    role: "Librarian"
    prompt: "You only search web based on the given plan. Output raw facts."
}

agent FileCoder {
    uses [std.os.file]     // Only it needs file writing permissions and Tokens
    role: "Senior Developer"
    prompt: "You only write and save code based on the provided facts."
}

flow main(req: string) {
    // Implicit Context automatic relay, high cohesion low coupling
    req >> TaskPlanner >> ResearchSearcher >> FileCoder;
}
```

### SRP Checklist

When defining each Agent, ask yourself these questions:

- [ ] Does this Agent have only one core task?
- [ ] Are all tools in its tool list necessary?
- [ ] Does its Prompt focus on only one domain?
- [ ] Can it be further split into smaller Agents?

---

## 💰 Practice 2: "Computational Matrix Tiered Scheduling" with High-Low Combination

In existing AI black-box applications, `gpt-4` is often mounted globally for convenience. However, **the smarter the model, not only is it more expensive, but the streaming output speed (TPS) and time-to-first-token (TTFT) are usually worse**. If you let a peak reasoning model do the mindless routing classification in `match intent`, it's a huge waste of computing power.

### Model Selection Decision Tree

```
Task Type?
├── Simple Classification/Routing
│   └── Use lightweight models (deepseek-chat, gpt-3.5-turbo)
│
├── Data Extraction/Format Conversion
│   └── Use medium models (deepseek-chat, claude-haiku)
│
├── Complex Reasoning/Analysis
│   └── Use powerful models (gpt-4, claude-sonnet)
│
└── Code Generation/Technical Decisions
    └── Use top-tier models (gpt-4-turbo, claude-opus)
```

### Multi-dimensional Computational Matrix Scheduling Example

```nexa
agent RouterBot {
    model: "deepseek/deepseek-chat"  // Extremely cheap and fast routing brain
    prompt: "Analyze user request type and route to appropriate processing module"
}

agent DataExtractor {
    model: "deepseek/deepseek-chat"  // Data processing with medium model
    prompt: "Extract structured data from text"
}

agent MetaCritic {
    model: "openai/gpt-4"            // Expensive but sharp review expert
    prompt: "Conduct deep analysis and quality review"
}
```

### Cost Optimization Comparison

Through our comparative testing on real commercial recommendation business flows, adopting this "big commander with small soldiers" architecture:

| Metric | All GPT-4 | Tiered Scheduling | Optimization Ratio |
|-----|---------|---------|---------|
| Token Consumption | 100% | 25% | **75% reduction** |
| Average Latency | 3.2s | 1.1s | **3x faster** |
| Monthly Cost | $1200 | $300 | **75% savings** |

---

## 🐛 Practice 3: Strong Security "Anti-Deadlock" Concession Mechanism

Using `loop ... until` semantics for Critic (adversarial training networks) is very satisfying and can greatly extract deep thinking space from large models. However, as an architect, you need to be constantly alert to AI falling into weird "rabbit hole" extremes, such as two Agents infinitely arguing over a punctuation space in code!

### Deadlock Problem Analysis

Common deadlock scenarios:

1. **Review Loop Deadlock**: Writer and Reviewer cannot agree on a detail
2. **Optimization Loop Deadlock**: Optimizer keeps "optimizing", cannot converge
3. **Discussion Loop Deadlock**: Two Agents hold different views, cannot reach consensus

### Solution: Add Fuse Mechanism

For deadlock problems, Nexa always exposes `runtime.meta.loop_count` in the runtime context engine as a powerful fuse.

**Recommend always adding soft and hard cutoffs using metadata in loop blocks:**

```nexa
flow critic_pipeline(task: string) {
    loop {
        draft = Writer.run(task);
        feedback = Reviewer.run(draft);
        
    // Combine natural language semantic inference and programming strong logic interception (dual insurance mechanism)
    } until ("Code has exactly 0 bugs inside feedback" or runtime.meta.loop_count >= 4)
    
    // If the count wall was hit, can throw human interception exception
    if (runtime.meta.loop_count >= 4) {
        raise SuspendExecution("Reviewer and Writer entered deadlock. Need Human Check.");
    }
}
```

### Loop Optimization Best Practices

```nexa
// ✅ Good practice: Clear termination condition and max count protection
loop {
    result = Agent.run(input);
    feedback = Reviewer.run(result);
    input = result;
} until ("Quality standard met" or runtime.meta.loop_count >= 5)

// ❌ Bad practice: Only vague condition, may lead to infinite loop
loop {
    result = Agent.run(input);
} until ("Result is good")  // Too subjective, may never be satisfied
```

---

## 🛡️ Practice 4: Error Handling and Disaster Recovery Design

Production environments must consider various exceptional situations.

### Model Disaster Recovery Configuration

```nexa
agent ProductionBot {
    // Multi-level backup models
    model: [
        "openai/gpt-4",
        fallback: "anthropic/claude-3-sonnet",
        fallback: "deepseek/deepseek-chat"
    ],
    prompt: "...",
    timeout: 30,    // 30 second timeout
    retry: 3        // Retry 3 times
}
```

### Exception Handling Pattern

```nexa
flow safe_processing(input: string) {
    try {
        result = RiskyAgent.run(input);
        
        // Validate result
        if (result is None or result == "") {
            raise ValueError("Empty result");
        }
        
        return result;
        
    } catch (error) {
        // Log error
        Logger.run(f"Error: {error}");
        
        // Degraded processing
        return FallbackAgent.run(input);
    }
}
```

### Fallback Strategy

| Scenario | Strategy |
|-----|------|
| Main model timeout | Switch to backup model |
| Output format error | Auto retry or use repair Agent |
| Tool call failure | Return error message or use alternative tool |
| Rate Limit | Auto backoff retry |

---

## 🔐 Practice 5: Security and Permission Control

### Principle of Least Privilege

Only grant Agents the minimum permissions needed to complete tasks:

```nexa
// ✅ Agent that only reads files
agent FileReader uses std.fs.read {
    prompt: "Read and analyze file content"
}

// ❌ Excessive permissions
agent FileReader uses std.fs {
    prompt: "Read and analyze file content"  // Has delete permission, dangerous!
}
```

### Sensitive Operation Approval

For sensitive operations, human approval must be introduced:

```nexa
agent SensitiveOperationBot uses std.ask_human, std.shell {
    prompt: """
    Before executing sensitive operations must:
    1. Clearly explain the operation to be performed
    2. Use ask_human to get user confirmation
    3. Log the operation
    """
}

flow main {
    // Operations involving sensitive data
    result = SensitiveOperationBot.run("Delete old data from production database");
}
```

### Secret Management Best Practices

```nexa
// ✅ Correct: Use secret function
api_key = secret("API_KEY");

// ❌ Wrong: Hardcode secret
api_key = "sk-xxxx";  // Never do this!
```

---

## 📊 Practice 6: Performance Optimization and Caching Strategy

### Intelligent Cache Configuration

```nexa
agent CachedBot {
    model: "deepseek/deepseek-chat",
    prompt: "...",
    cache: true,  // Enable semantic cache
    
    // Cache configuration
    cache_ttl: 3600,     // Cache validity period (seconds)
    cache_threshold: 0.95 // Semantic similarity threshold
}
```

### Context Management

```nexa
agent LongConversationBot {
    prompt: "...",
    memory: "persistent",
    max_history_turns: 10,  // Limit history turns
    context_compression: true  // Enable context compression
}
```

### Batch Processing Optimization

```nexa
// ✅ Good practice: Batch parallel processing
flow batch_process(inputs: list) {
    results = inputs |>> [Processor1, Processor2, Processor3];
    return results;
}

// ❌ Bad practice: Sequential processing one by one
flow slow_process(inputs: list) {
    results = [];
    for input in inputs {
        result = Processor.run(input);
        results.append(result);
    }
    return results;
}
```

---

## 📝 Practice 7: Prompt Engineering Best Practices

### Good Prompt Structure

```nexa
agent WellDesignedBot {
    prompt: """
    # Role Definition
    You are a professional {domain} expert.
    
    # Task Description
    Your task is {task_description}.
    
    # Input Format
    User input will contain: {input_format}
    
    # Output Requirements
    - Format: {output_format}
    - Language: {language}
    - Length: {length_limit}
    
    # Notes
    - {attention_point_1}
    - {attention_point_2}
    """
}
```

### Prompt Optimization Checklist

- [ ] Is the role definition clear?
- [ ] Is the task description specific?
- [ ] Are input/output formats explicit?
- [ ] Does it include necessary constraints?
- [ ] Does it avoid vague expressions?
- [ ] Does it provide necessary examples?

### Common Prompt Issues

| Issue | Example | Improvement |
|-----|------|------|
| Too vague | "Help me write something" | "Write a 500-word short article about AI" |
| Conflicting instructions | "Explain in detail but concisely" | "Summarize key information in 3 points" |
| Missing constraints | "Analyze this data" | "Analyze this data, output JSON format with score and summary fields" |

---

## 🧪 Practice 8: Testing and Debugging

### Using Test Framework

```nexa
test "Translation function test" {
    input = "Hello, World!";
    result = Translator.run(input);
    
    // Validate output
    assert "contains Chinese translation" against result;
    assert "output length is reasonable" against result;
}

test "Error handling test" {
    input = "";  // Empty input
    result = SafeTranslator.run(input);
    
    // Validate error handling
    assert "returns error message" against result;
}
```

### Debugging Tips

```bash
# Enable debug mode
nexa run script.nx --debug

# View generated Python code
nexa build script.nx
cat out_script.py

# Performance profiling
nexa run script.nx --profile
```

### Logging

```nexa
agent MonitoredBot uses std.fs {
    prompt: "...",
    logging: true,     // Enable logging
    log_level: "info"  // Log level
}

flow main {
    Logger.run("Starting task processing");
    
    try {
        result = MonitoredBot.run(input);
        Logger.run(f"Processing succeeded: {result}");
    } catch (error) {
        Logger.run(f"Processing failed: {error}");
    }
}
```

---

## 📋 Production Environment Checklist

### Pre-deployment Check

- [ ] All Agents follow the single responsibility principle
- [ ] Reasonable Fallback models configured
- [ ] Sensitive operations require human confirmation
- [ ] Request timeout and retry count set
- [ ] Necessary caching enabled
- [ ] Test cases written
- [ ] Logging configured
- [ ] Stress testing performed

### Monitoring Metrics

| Metric | Description | Warning Value |
|-----|------|--------|
| Average Latency | Request response time | > 5s |
| Error Rate | Failed request ratio | > 1% |
| Token Consumption | Consumption per request | Over budget 20% |
| Cache Hit Rate | Cache utilization efficiency | < 30% |

---

## 📝 Chapter Summary

Mastering these eight internal skill systems - responsibility decomposition, computational matrix scheduling, deadlock protection, error handling, security control, performance optimization, Prompt engineering, and testing/debugging - you can completely break free from the "toy perspective" of casual players and master the Nexa native language to create top-tier automated pipeline factories with extremely high commercial stability.

### Best Practices Quick Reference

| Practice | Key Point | Benefit |
|-----|-------|------|
| Single Responsibility | Each Agent does one thing only | Reduce hallucinations, save Tokens |
| Tiered Scheduling | Simple tasks use small models | Reduce costs, improve speed |
| Deadlock Protection | Set maximum loop count | Prevent infinite loops |
| Error Handling | try/catch + Fallback | Improve stability |
| Security Control | Least privilege + Human approval | Ensure security |
| Performance Optimization | Cache + Batch processing | Improve efficiency |
| Prompt Engineering | Structured, specific | Improve quality |
| Testing & Debugging | Test framework + Logging | Easy maintenance |

---

## 🔗 Related Resources

- [Complete Example Collection](examples.md) - View more enterprise-level examples
- [Troubleshooting Guide](troubleshooting.md) - Problem solutions
- [Compiler Design](part5_compiler.md) - Understand underlying principles
