---
comments: true
---

# 4. Syntax Extensions: Contracts, Types, and Protocols

Previously, we learned about macro-level routing control flows with topological structures. But in the real, ruthless enterprise production environment, the most fatal issue is always the **unstructured output mechanism** of large models bringing indeterminacy.

Traditional microservices exchange strict JSON using Thrift, gRPC, or RESTful protocols. However, large models may at any time return a passage full of thinking and tone like "Here is your result:\n {...}". This will easily break through the fragile decoders of downstream Java/Go systems.

This chapter focuses on introducing Nexa's innovative high-level reshaping features for this pain point: **Type Protocols** and **Multi-Model Intelligent Routing**. They are the ballast stones of system stability.

---

## 📜 Introducing the `protocol` Keyword (Compiler-Level Pydantic)

Whenever business flows need to be consumed by downstream non-LLM services (like database writes, frontend rendering), we must force the large model to return only specific format data.

Previously, you needed to import complex JSON parsing tools (like `Pydantic` in Python or `Zod` in TypeScript), then serialize schemas into dozens of lines of JSON constraints forcefully appended at the end of prompts.

In the Nexa language, we've elevated constraint syntax to first-class citizen status, using `protocol` just like defining `struct` or `class`.

### Basic Syntax

```nexa
// Nexa language built-in protocol definition, supporting rich type system
protocol ReviewResult {
    score: "int",
    summary: "string",
    bug_list: "list[string]",
    is_critical: "boolean"
}
```

### Supported Types

| Type | Description | Example Value |
|-----|------|--------|
| `"string"` | String | `"hello"` |
| `"int"` | Integer | `42` |
| `"float"` | Float | `3.14` |
| `"boolean"` | Boolean | `true` |
| `"list[string]"` | String list | `["a", "b"]` |
| `"list[int]"` | Integer list | `[1, 2, 3]` |
| `"dict"` | Dictionary | `{"key": "value"}` |

### Type Annotation Specification

!!! warning "Important: Types Must Be Strings"
    In `protocol`, types must be wrapped in quotes:

    ```nexa
    // ✅ Correct
    protocol UserInfo {
        name: "string",
        age: "int"
    }
    
    // ❌ Wrong - Types without quotes
    protocol UserInfo {
        name: string,  // Compilation error!
        age: int       // Compilation error!
    }
    ```

---

## 🛡️ `implements` Implementation Guarantee and Black-Box Retry Mechanism

Defining a protocol is just the first step. How should an Agent create a mandatory intersection with it? Simply use the inheritance logic familiar from object-oriented languages—the `implements` interface inheritance.

### Basic Usage

```nexa
@limit(max_tokens=600)
agent Coder {
    prompt: "Write a short Python implementation of quicksort.",
    model: "minimax/minimax-m2.5"
}

// This Reviewer model will be bound by the contract, ensuring the system only receives clean JSON property entities.
agent Reviewer implements ReviewResult {
    prompt: "Review the provided code. Provide your score and list all bugs.",
    model: "deepseek/deepseek-chat"
}

flow main {
    // The entire data structure will seamlessly pass as Python Object/JSON to external API
    result = Coder.run("Generate Quicksort") >> Reviewer;
    
    // result is a structured object, can access properties directly
    print("Score: " + result.score);
    print("Summary: " + result.summary);
}
```

### Runtime Magic: Automatic Retry Correction

!!! warning "This is a mechanism you could never easily write in conventional systems"
    On the surface, `implements` just binds a declaration. But behind the scenes, large models sometimes still misbehave (like only giving `score` but forgetting `bug_list`, or incorrectly spelling `is_critical` as string "true").
    
    In this situation, your previous Python script would definitely crash on the spot due to `JSONDecodeError`.
    
    **But within Nexa's defense line, the underlying Evaluator will intercept this returned Token and immediately compare it against the Schema. If it detects type derailment—it will automatically convert the Pydantic/Traceback error message into natural language and feed it back, silently triggering the model's "secondary introspection"!**
    
    ```
    "Sorry, your output is missing bug_list, please correct and re-output"
    ```
    
    This entire cycle is **completely transparent** to the front-end code writer.

### Automatic Correction Flow

```
LLM Output
    │
    ▼
┌─────────────────────┐
│   Schema Validator  │
└─────────────────────┘
    │
    ├── Validation Passed ──────► Return structured object
    │
    └── Validation Failed
            │
            ▼
    ┌─────────────────────┐
    │ Generate Error Msg  │
    └─────────────────────┘
            │
            ▼
    ┌─────────────────────┐
    │ Auto Re-request LLM │
    └─────────────────────┘
            │
            └──► Max 3 retries
```

---

## 🎯 Protocol Use Case Details

### Case 1: Structured Data Extraction

When you need to extract structured data from unstructured text, Protocol is the best choice.

```nexa
// Define output protocol
protocol UserInfo {
    name: "string",
    age: "int",
    occupation: "string",
    location: "string"
}

agent InfoExtractor implements UserInfo {
    role: "Information Extraction Expert",
    prompt: """
    Extract personal information from user input.
    If a field cannot be determined, fill in "Unknown".
    """
}

flow main {
    user_input = "My name is Zhang San, 28 years old, working as a software engineer in Beijing";
    
    result = InfoExtractor.run(user_input);
    
    // Result is structured
    print("Name: " + result.name);        // Zhang San
    print("Age: " + result.age);          // 28
    print("Occupation: " + result.occupation);   // Software Engineer
    print("Location: " + result.location);     // Beijing
}
```

### Case 2: API Response Format Constraint

When you need Agent to output data that can be directly consumed by APIs:

```nexa
// Define API response format
protocol APIResponse {
    status: "string",      // "success" or "error"
    code: "int",           // HTTP status code
    data: "dict",          // Response data
    message: "string"      // Message
}

agent APIHandler implements APIResponse {
    prompt: "Process user request and return standard API response format"
}

flow main {
    request = "Query orders for user ID 123";
    response = APIHandler.run(request);
    
    // Can be returned directly to frontend
    return response;  // {"status": "success", "code": 200, ...}
}
```

### Case 3: Multi-Agent Data Transfer

When you need to ensure data format consistency between Agents:

```nexa
// Define unified research report format
protocol ResearchReport {
    title: "string",
    summary: "string",
    key_findings: "list[string]",
    confidence: "float"  // 0.0 - 1.0
}

agent Researcher implements ResearchReport {
    role: "Researcher",
    prompt: "Research specified topic and generate structured report"
}

agent Reviewer {
    role: "Reviewer",
    prompt: "Review research report completeness and accuracy"
}

agent Formatter {
    role: "Formatting Expert",
    prompt: "Format research report into final output"
}

flow main {
    topic = "AI Industry Trends 2024";
    
    // Researcher outputs structured data
    report = Researcher.run(topic);
    
    // Reviewer receives structured data
    review = Reviewer.run(report);
    
    // Formatter final processing
    final = Formatter.run(report);
    
    print(final);
}
```

### Case 4: Form Data Processing

```nexa
protocol ContactForm {
    name: "string",
    email: "string",
    phone: "string",
    message: "string",
    priority: "string"  // "high", "medium", "low"
}

agent FormProcessor implements ContactForm {
    prompt: "Extract contact form information from user input"
}

flow main {
    user_input = """
    Hello, I'm Li Si, email is lisi@example.com.
    Phone 138-1234-5678.
    I'd like to inquire about product pricing, hoping for a quick reply.
    """;
    
    form = FormProcessor.run(user_input);
    
    // Can be saved directly to database
    save_to_database(form);
}
```

### Case 5: Classification and Tagging

```nexa
protocol ClassificationResult {
    category: "string",
    confidence: "float",
    tags: "list[string]",
    reasoning: "string"
}

agent Classifier implements ClassificationResult {
    prompt: "Classify input content, provide classification result and confidence"
}

flow main {
    content = "New iPhone 15 released, powered by A17 chip";
    
    result = Classifier.run(content);
    
    print("Category: " + result.category);     // "Tech News"
    print("Confidence: " + result.confidence);  // 0.95
    print("Tags: " + result.tags);          // ["Apple", "Phone", "New Product"]
}
```

---

## 🧠 Model Routing (Splitting Brain Regions by Task Capability)

Not just strict control of data structures, an excellent language also needs to solve the "money" problem for developers. Large model token computing power is extremely expensive.

Nexa allows you to specify differentiated capability fallback through arrays and dictionaries in `model` declarations, building a robust high-availability model hub.

### Elegant Fallback Degradation Mechanism

When the main model goes down, is rate-limited by the platform, or encounters timeouts, you typically need large sections of `try...except...retry` and rotation logic for protection. In Nexa, it only takes one declaration:

```nexa
// If the main super-large model cannot respond, or even has internal errors, automatically downgrade to request Opus or smaller open-source models.
agent HeavyMathBot {
    model: ["gpt-4-turbo", fallback: "claude-3-opus", fallback: "llama-3-8b"],
    prompt: "You solve extreme math problems."
}
```

### Model Selection Strategy

```nexa
// Task type and model selection
agent QuickRouter {
    // Simple tasks use fast models
    model: "deepseek/deepseek-chat",
    prompt: "..."
}

agent HeavyThinker {
    // Complex tasks use powerful models
    model: "openai/gpt-4",
    prompt: "..."
}

agent BudgetFriendly {
    // Cost-sensitive scenarios use cheap models
    model: "minimax/minimax-m2.5",
    prompt: "..."
}
```

### High Availability Configuration

```nexa
agent ProductionBot {
    // Main model + multi-level backup
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

---

## 📊 Protocol Advanced Techniques

### Technique 1: Nested Structures (Using String Representation)

Although Protocol doesn't support direct nesting, you can use strings to represent complex structures:

```nexa
protocol ComplexReport {
    title: "string",
    metadata: "string",   // JSON string representing complex structure
    sections: "list[string]"  // Each element is a JSON string
}
```

### Technique 2: Optional Field Handling

Explain field handling in the Prompt:

```nexa
protocol FlexibleData {
    required_field: "string",
    optional_field: "string"  // Prompt explains can be empty
}

agent FlexibleAgent implements FlexibleData {
    prompt: """
    Extract data.
    required_field must have a value.
    optional_field if not found, fill in "N/A".
    """
}
```

### Technique 3: Enum Value Constraints

Specify enum values explicitly in the Prompt:

```nexa
protocol StatusReport {
    status: "string",  // Must be "pending", "processing", "completed", "failed"
    message: "string"
}

agent StatusAgent implements StatusReport {
    prompt: """
    Report task status.
    status can only be one of the following values:
    - "pending"
    - "processing"  
    - "completed"
    - "failed"
    """
}
```

---

## ⚠️ Protocol Common Errors

### Error 1: Types Without Quotes

```nexa
// ❌ Wrong
protocol Bad {
    name: string,  // Compilation error
    age: int       // Compilation error
}

// ✅ Correct
protocol Good {
    name: "string",
    age: "int"
}
```

### Error 2: Forgetting implements Keyword

```nexa
// ❌ Wrong: Defined Protocol but Agent doesn't implement
protocol MyProtocol {
    field: "string"
}

agent MyAgent {  // Missing implements MyProtocol
    prompt: "..."
}

// ✅ Correct
agent MyAgent implements MyProtocol {
    prompt: "..."
}
```

### Error 3: Protocol Too Complex

```nexa
// ❌ Too complex, LLM difficult to output accurately
protocol TooComplex {
    nested: "dict[string, list[dict[string, any]]]"
}

// ✅ Simplified design
protocol SimpleAndClear {
    data: "string"  // JSON string
}
```

---

## 📝 Chapter Summary

In this chapter, we learned:

| Feature | Description | Use Case |
|-----|------|---------|
| `protocol` | Define output format constraints | Structured data extraction |
| `implements` | Agent implements protocol | Ensure output format consistency |
| Auto Retry | Validation failure auto-correction | Improve system reliability |
| Model Routing | Multi-model routing | Cost optimization, high availability |

By combining the rigid contracts of `protocol` with dynamic `fallback` flow networks, Nexa never abandons the "robustness and boundary determinism" genes accumulated over decades of traditional software engineering while granting high "thinking flexibility." This is also a decisive step for Agent development toward the track of formalization.

---

## 🔗 Related Resources

- [Complete Example Collection](examples.md) - View more Protocol examples
- [Best Practices](part6_best_practices.md) - Enterprise-level Protocol design patterns
- [Troubleshooting Guide](troubleshooting.md) - Protocol-related problem solving
