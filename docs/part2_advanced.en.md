---
comments: true
---

# 3. Advanced Features: Orchestration of Complex Agent Networks

If defining roles with the `agent` keyword is just creating individual gears, then the true "industrial revolution" in the Nexa universe is embodied in its unparalleled **collaborative orchestration network**.

Nexa's core design moat since the v0.5 architecture upgrade has been elevating complex, asynchronous and race-condition-filled multi-stage agent interactions to the level of **language keywords**. In this chapter, we'll explore in detail how to leverage pipelines (`>>`), intent routing (`match intent`), concurrent aggregation (`join`), DAG operators, and the incredible semantic loops (`loop until`) in enterprise-grade Agent frameworks.

---

## 🛤️ Pipeline Operator: `>>` (Pipeline Data Bus)

In most tasks (such as academic translation, code writing and testing chains), multi-agent collaboration is simply a pure pipeline: the output of the previous Agent (Output Task) along with its historical context should be passed completely and without loss as input to the next Agent.

### Pain Points of Traditional Approach

If we use the traditional approach represented by LangChain to build this chain segment:

```python
# Pain points of traditional languages: filled with intermediate variables and implicit state loss
draft = Writer.run(topic)
translated_draft = Translator.run(draft)
reviewer_feedback = Reviewer.run(translated_draft)
```

You'll find that not only do you define a bunch of single-use intermediate variables (leading to poor memory management), but you're also prone to various runtime errors due to different type wrappers (like `BaseMessage` objects vs plain `str`).

### Nexa Pipeline Operator

In Nexa, we can use the expressive Unix-like pipeline operator `>>` in one go:

```nexa
// From Nexa practical code collection (Pipeline Pattern)
flow main {
    res = Coder.run("Generate a fast sorting algorithm in Python") >> Reviewer >> HumanInterface;
    
    // The return result will directly be the final form produced by the pipeline end (HumanInterface)
}
```

### Pipeline Operator Details

| Operation | Equivalent Code | Description |
|-----|---------|------|
| `A >> B` | `B.run(A.run(input))` | Pass A's output to B |
| `A >> B >> C` | `C.run(B.run(A.run(input)))` | Three-stage pipeline |
| `input >> A >> B` | `B.run(A.run(input))` | Start from input |

!!! success "Compiler Magic Behind the Elegance"
    When you type `A >> B`, the Nexa compiler doesn't simply transpile it to linear function blocking calls. Under the hood, Nexa's Orchestrator automatically builds a DAG (Directed Acyclic Graph), which preserves the context sliding window from `Coder` to `Reviewer`, and strictly follows Promise ready state to activate the next node. This saves you countless lines of state maintenance code.

### Pipeline Operator Complete Example

```nexa
// Translation pipeline
agent Translator {
    role: "Professional Translator",
    prompt: "Translate English to Chinese, preserve original meaning, fluent language"
}

agent Proofreader {
    role: "Proofreading Editor",
    prompt: "Proofread translation, correct errors, polish language"
}

agent Formatter {
    role: "Formatting Expert",
    prompt: "Organize text into standard format"
}

flow main {
    english_text = "Artificial intelligence is transforming the world.";
    
    // Three-stage pipeline
    final_result = english_text >> Translator >> Proofreader >> Formatter;
    
    print(final_result);
}
```

**Execution Result**:
```
人工智能正在改变世界。
```

---

## 🔀 Intent Routing: `match intent` Protocol

User instructions are always unpredictable. In many customer service/support bots, some users want to check the weather, some want to send emails, and others just want to hear a joke or chat.

If we use a "super large model" to handle all tasks:

1. It consumes a large amount of billing tokens even when receiving trivial messages.
2. Context is severely polluted, potentially incorrectly triggering system high-risk "delete database" tools when chatting.

Therefore, high-concurrency systems in the industry often advocate "front-end micro routing classifiers" (NLU/Intent Router) to achieve peak shaving and valley filling, then hand over actual processing to domain expert agents mounted behind.

### Basic Syntax

```nexa
match user_input {
    intent("intent description 1") => Agent1.run(user_input),
    intent("intent description 2") => Agent2.run(user_input),
    _ => DefaultAgent.run(user_input)  // Default branch
}
```

### Complete Example

```nexa
// Nexa in action: Multi-intent routing
flow main {
    req = "Tell me what is happening in the global tech world today!";
    
    // Using natural semantics and intent matching mechanism to directly decouple verbose and fragile if-else
    match req {
        intent("Check local weather") => WeatherBot.run(req) >> Translator,
        intent("Check daily news")    => NewsBot.run(req) >> Translator,
        _ => SmallTalkBot.run(req)
    }
}
```

### Intent Routing Flow Diagram

```
User Input
    │
    ▼
┌─────────────────────┐
│  Intent Classifier  │
│    (Built-in)       │
│ Embedding + Similarity │
└─────────────────────┘
    │
    ├── intent("weather") ──────► WeatherBot
    │
    ├── intent("news") ──────► NewsBot
    │
    └── default (_) ────────────► SmallTalkBot
```

!!! info "Parsing `intent()` Underlying Implementation"
    Here `intent("...")` is essentially not simple string or regex matching. Nexa internally carries an ultra-lightweight Embeddings matching model specifically for intent classification. In the background, it rapidly calculates cosine similarity with each branch's `Condition`, seamlessly routing execution flow into the most appropriate branch. To implement a similar mechanism in Python, you would need at least a ChromaDB service and a complex Top-K retrieval pool.

### Intent Routing Best Practices

1. **Be specific with intent descriptions**: Avoid vague descriptions
2. **Set reasonable default branch**: Handle unknown intents
3. **Consider using fast models**: Intent classification doesn't require complex reasoning

```nexa
// ✅ Good intent descriptions
intent("Check weather forecast or current weather conditions")
intent("Check stock prices or financial data")
intent("Book flights, hotels, or restaurants")

// ❌ Bad intent descriptions
intent("weather")  // Too vague
intent("other")    // No practical meaning
```

---

## 🕸️ DAG Topology Orchestration: Ultimate Multi-way Fork and Merge (v0.9.7+)

When dealing with intelligence-intensive tasks (such as investment research report generation or core system difficult code optimization), it's necessary to have multiple roles conduct "back-to-back" independent research separately, then aggregate for cross-discussion. Nexa v0.9.7 revolutionarily introduced native handling of complex graph structures (DAG) topology operators.

### DAG Operator Overview

| Operator | Name | Description | Example |
|-------|------|------|------|
| `>>` | Pipeline | Sequential passing | `A >> B` |
| `|>>` | Fan-out | Parallel send to multiple Agents | `input |>> [A, B, C]` |
| `&>>` | Merge/Fan-in | Merge multiple results to one Agent | `[A, B] &>> C` |
| `??` | Conditional Branch | Select path based on condition | `input ?? A : B` |
| `||` | Async Fork | Send without waiting for result | `input || [A, B]` |
| `&&` | Consensus Merge | Require all Agents to agree | `[A, B] && Judge` |

### Fork Operator `|>>` (Fan-out)

**Parallel clone** upstream data and send to multiple Agents, waiting for all results to return.

```nexa
// Fork operator - Parallel send to multiple Agents
flow main {
    topic = "Quantum Computing Applications";
    
    // Send topic to three Agents in parallel simultaneously
    results = topic |>> [Researcher, Analyst, Writer];
    
    // results is an array containing outputs from all three Agents
    print(results);
}
```

**Flow Diagram**:
```
       topic
         │
         ├──────────┬──────────┐
         │          │          │
         ▼          ▼          ▼
    Researcher   Analyst    Writer
         │          │          │
         └──────────┴──────────┘
                    │
                    ▼
               [Result Array]
```

**Use Cases**:
- Multi-angle analysis of the same problem
- Multi-language translation
- Multi-model comparison verification

### Merge Operator `&>>` (Merge/Fan-in)

**Merge** outputs from multiple Agents and send to downstream Agent.

```nexa
// Merge operator - Combine outputs from multiple Agents
flow main {
    // Wait for Researcher and Analyst to complete
    // Merge both outputs and send to Reviewer
    final_report = [Researcher, Analyst] &>> Reviewer;
    
    print(final_report);
}
```

**Flow Diagram**:
```
    Researcher ────┐
                   │
                   ▼
               Reviewer ──► Final Output
                   ▲
                   │
    Analyst ───────┘
```

**Use Cases**:
- Multi-source information aggregation
- Expert consultation
- Cross-validation

### Conditional Branch Operator `??`

**Automatically select** execution path based on input characteristics.

```nexa
// Conditional branch operator
flow main {
    user_query = "URGENT: System outage detected";
    
    // Automatically select processing Agent based on input content
    handled = user_query ?? UrgentHandler : NormalHandler;
    
    print(handled);
}
```

**Flow Diagram**:
```
         Input
          │
          ▼
    ┌─────────────┐
    │  Condition  │
    │  Judgment   │
    └─────────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
UrgentHandler  NormalHandler
    │           │
    └─────┬─────┘
          │
          ▼
        Output
```

**Use Cases**:
- Urgency classification
- Simple/complex task routing
- Different request type handling

### Combining DAG Operators

Build complex processing flows:

```nexa
// From Nexa code example 15_dag_topology.nx
flow main {
    topic = "Quantum Computing business impact";

    // 1. Fork: topic is fed to Tech and Biz researchers for parallel analysis
    // 2. Merge: After both produce output, aggregate and send to Summarizer to write final report
    final_report = topic |>> [Researcher_Tech, Researcher_Biz] &>> Summarizer;

    // Branch routing: If report is abnormal, use backup bot; otherwise execute logging and dispatch
    final_report ?? RecoveryBot : Logger;
}
```

**Complete Flow Diagram**:
```
                    topic
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
   Researcher_Tech         Researcher_Biz
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
                  Summarizer
                      │
                      ▼
              final_report
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    RecoveryBot               Logger
    (Exception)            (Normal)
```

### DAG Operator Complete Example

```nexa
// DAG topology example - Research report generation system
agent Researcher_Tech {
    role: "Technical Researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze quantum computing's technical level impact"
}

agent Researcher_Biz {
    role: "Business Researcher",
    model: "deepseek/deepseek-chat",
    prompt: "Analyze quantum computing's business level impact"
}

agent Summarizer {
    role: "Report Writer",
    model: "deepseek/deepseek-chat",
    prompt: "Integrate research results and write comprehensive report"
}

agent UrgentHandler {
    role: "Urgent Handler",
    prompt: "Quickly handle urgent issues"
}

agent NormalHandler {
    role: "Standard Handler",
    prompt: "Process according to standard procedures"
}

flow main {
    // Example 1: Simple pipeline
    simple_result = "What is AI?" >> Researcher_Tech >> Summarizer;
    
    // Example 2: Fork - Parallel processing
    parallel_results = "Quantum Computing" |>> [Researcher_Tech, Researcher_Biz];
    
    // Example 3: Merge - Integrate results
    merged_report = [Researcher_Tech, Researcher_Biz] &>> Summarizer;
    
    // Example 4: Conditional branch
    urgent_query = "URGENT: System crash!";
    handled = urgent_query ?? UrgentHandler : NormalHandler;
    
    // Example 5: Complex combination
    complex_flow = "AI trends 2024" 
        |>> [Researcher_Tech, Researcher_Biz] 
        &>> Summarizer;
}
```

---

## 🔁 Semantic Review and Reflection Loop: `loop ... until`

In many automated programming and long-text collaboration applications, the industry has concluded that a "reflective critic" mechanism must be adopted: i.e., `Model A produces draft -> Model B acts as reviewer to correct errors -> Model A receives error feedback and rewrites`.

How do traditional languages handle this logic? Developers need to hand-write an extremely fragile `while True`, then use a few awkward regex lines `if "SUCCESS" in text: break` praying the large model can precisely output the break word.

Nexa's philosophy is: **Since even computation is done by large models, why can't judgment logic be natively returned to the semantic field?** This gave birth to a **language-level loop engine** for semantic termination conditions.

### Basic Syntax

```nexa
loop {
    // Loop body
} until ("natural language termination condition")
```

### Complete Example

```nexa
flow main {
    // First step: initial production
    poem = Writer.run("Write a beautiful poem about AGI.");
    
    loop {
        // Use pipeline thinking to get critique feedback
        feedback = Critic.run(poem);
        
        // Use feedback as context guidance, rewrite in-place (Mutate)
        poem = Editor.run(poem, feedback);
        
    // Unique in the entire field: natural language judgment break condition
    } until ("The poem effectively rhymes and crucially mentions the technological singularity")
}
```

### Preventing Infinite Loops

Use loop counter protection:

```nexa
flow critic_pipeline(task: string) {
    loop {
        draft = Writer.run(task);
        feedback = Reviewer.run(draft);
        
    // Combine natural language semantic reasoning and programming strong logic interception (dual insurance mechanism)
    } until ("Code has exactly 0 bugs inside feedback" or runtime.meta.loop_count >= 4)
    
    // If hit the iteration limit, can throw manual interception exception
    if (runtime.meta.loop_count >= 4) {
        raise SuspendExecution("Reviewer and Writer entered deadlock. Need Human Check.");
    }
}
```

### Loop Control Variables

Nexa provides the following built-in variables in loops:

| Variable | Description |
|-----|------|
| `runtime.meta.loop_count` | Current loop count |
| `runtime.meta.last_result` | Result from last loop iteration |

---

## 🔧 Semantic Conditional Judgment: `semantic_if`

Besides `loop until`, Nexa also provides `semantic_if` for semantic-level conditional judgment.

### Basic Syntax

```nexa
semantic_if "natural language condition" against input_variable {
    // Execute when condition is true
} else {
    // Execute when condition is false
}
```

### Fast Match Mode

Use `fast_match` for regex pre-filtering to avoid unnecessary LLM calls:

```nexa
semantic_if "contains specific date and location" fast_match r"\d{4}-\d{2}-\d{2}" against user_input {
    schedule_tool.run(user_input);
} else {
    print("Need further clarification");
}
```

!!! tip "How fast_match Works"
    1. First check with regex quickly
    2. If regex matches, enter branch directly (saves tokens)
    3. If regex doesn't match, still call LLM for semantic judgment

### Complete Example

```nexa
flow main {
    user_input = '{"name": "Zhang San", "age": 25}';
    
    // Semantic conditional judgment - Determine if it's JSON
    semantic_if "Input content is valid JSON format" fast_match r"^\s*[\[{]" against user_input {
        result = JSONProcessor.run(user_input);
        print("Processed as JSON: " + result);
    } else {
        result = TextProcessor.run(user_input);
        print("Processed as text: " + result);
    }
}
```

---

## 🧩 Exception Handling: `try/catch`

Nexa v0.9.5 introduced native exception handling mechanism.

### Basic Syntax

```nexa
try {
    // Code that might error
} catch (error) {
    // Error handling
}
```

### Complete Example

```nexa
flow main {
    try {
        result = RiskyAgent.run("dangerous operation");
        print(result);
    } catch (error) {
        print("Error occurred: " + error);
        // Use fallback solution
        result = FallbackAgent.run("safe operation");
    }
}
```

---

## 📊 Chapter Summary

In this chapter, we learned Nexa's advanced orchestration features:

| Feature | Keyword | Use Case |
|-----|-------|------|
| Pipeline Operation | `>>` | Agent chaining |
| Intent Routing | `match intent` | Request dispatching |
| Fork Operation | `|>>` | Parallel processing |
| Merge Operation | `&>>` | Result integration |
| Conditional Branch | `??` | Path selection |
| Semantic Loop | `loop until` | Iterative optimization |
| Semantic Condition | `semantic_if` | Intelligent judgment |
| Exception Handling | `try/catch` | Error handling |

These features enable Nexa to elegantly handle the most complex agent orchestration scenarios, from simple pipelines to complex DAG topologies, from deterministic branching to semantic-level conditional judgment.

---

## 🔗 Related Resources

- [Complete Example Collection](examples.md) - View more DAG operator examples
- [Syntax Extensions](part3_extensions.md) - Learn advanced Protocol usage
- [Best Practices](part6_best_practices.md) - Enterprise development experience
