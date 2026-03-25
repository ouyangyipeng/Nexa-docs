---
comments: true
---

# Nexa Language Reference Manual

This manual provides a detailed description of the Nexa language syntax specifications, semantic rules, and type system. It is the authoritative reference documentation for the Nexa language.

---

## 📖 About This Manual

This reference manual is organized according to the following principles:

- **Precision**: Every syntax construct has a clear semantic definition
- **Completeness**: Covers all language features, including edge cases
- **Practicality**: Provides sufficient examples to aid understanding

!!! tip "Reading Suggestion"
    If you are new to Nexa, we recommend reading [Quickstart](quickstart.md) and [Basic Syntax](part1_basic.md) first, then returning to this manual for reference.

---

## 1. Lexical Structure

### 1.1 Identifiers

Nexa identifiers follow these rules:

```
identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
```

**Valid Identifier Examples**:

```nexa
MyAgent           // PascalCase (recommended for Agent)
my_tool          // snake_case (recommended for tool)
_process_data    // Starting with underscore
Parser2          // Contains numbers (cannot start with number)
```

**Invalid Identifier Examples**:

```nexa
2ndAgent         // Starts with number
my-agent         // Contains hyphen
agent.name       // Contains dot
```

### 1.2 Keywords

Nexa reserves the following keywords that cannot be used as identifiers:

| Category | Keywords |
|------|--------|
| Declarations | `agent`, `tool`, `protocol`, `flow`, `test` |
| Control Flow | `match`, `intent`, `loop`, `until`, `if`, `else` |
| Semantic Control | `semantic_if`, `fast_match`, `against` |
| Exception Handling | `try`, `catch` |
| Type Constraints | `implements`, `uses` |
| Others | `print`, `assert`, `fallback`, `join`, `agent`, `role`, `model`, `prompt`, `memory`, `stream`, `cache`, `experience` |

### 1.3 Literals

#### String Literals

```nexa
"Hello, World!"           // Plain string
"Line 1\nLine 2"         // Contains escape characters
"Quote: \"nested\""      // Contains quotes
```

#### Regular Expression Literals

```nexa
r"\d{4}-\d{2}-\d{2}"     // Date format
r"^[a-zA-Z_]\w*$"        // Identifier pattern
r"https?://[^\s]+"      // URL pattern
```

#### Numeric Literals

```nexa
42              // Integer
3.14            // Float
2048            // For max_tokens and other parameters
```

### 1.4 Comments

```nexa
// Single-line comment

/*
 * Multi-line comment
 * Can span multiple lines
 */

/// Documentation comment (for Agent, Tool descriptions)
agent MyAgent {
    role: "Documentation comment example"
}
```

---

## 2. Top-Level Declarations

Nexa programs consist of a series of top-level declarations. Each declaration is a first-class citizen.

### 2.1 Agent Declaration

**Full Syntax**:

```ebnf
agent_decl ::= [agent_modifier] "agent" IDENTIFIER 
                ["implements" IDENTIFIER] 
                ["uses" identifier_list] 
                "{" agent_body "}"

agent_modifier ::= "@" IDENTIFIER "(" parameter_list ")"

agent_body ::= (IDENTIFIER ":" value ",")*
```

**Property Specification**:

| Property | Type | Required | Description |
|------|------|------|------|
| `role` | string | ✅ | Agent's role positioning |
| `prompt` | string | ✅ | Task execution instructions |
| `model` | string | ❌ | Model identifier, uses config default if not specified |
| `memory` | string | ❌ | Memory strategy: `short`, `long`, `session` |
| `stream` | bool | ❌ | Streaming output switch, default `false` |
| `cache` | bool/string | ❌ | Cache strategy: `true`, `false`, `"smart"` |
| `experience` | bool | ❌ | Long-term memory switch, default `false` |
| `fallback` | string | ❌ | Model degradation fallback |

**Decorator Specification**:

```nexa
@limit(max_tokens=2048)
@timeout(seconds=30)
@retry(max_attempts=3)
agent MyAgent {
    role: "Constrained Agent",
    prompt: "Output no more than 2048 tokens"
}
```

**Semantic Rules**:

1. **Name Uniqueness**: Agent names must be unique within the same scope
2. `protocol` referenced by `implements` must be declared
3. `tool` referenced by `uses` must be declared or be a standard library tool
4. Properties `role` and `prompt` are required

### 2.2 Tool Declaration

**Full Syntax**:

```ebnf
tool_decl ::= "tool" IDENTIFIER "{" tool_body "}"

tool_body ::= ("description:" STRING_LITERAL "," "parameters:" json_object)
            | ("mcp:" STRING_LITERAL)
            | ("python:" STRING_LITERAL)
```

**Local Tool Declaration**:

```nexa
tool WeatherAPI {
    description: "Get weather information for specified city",
    parameters: {
        "city": {
            "type": "string",
            "description": "City name",
            "required": true
        },
        "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "default": "celsius"
        }
    }
}
```

**MCP Tool Declaration**:

```nexa
tool WebSearch {
    mcp: "github.com/nexa-ai/web-search-mcp"
}
```

**Semantic Rules**:

1. Tool names must be unique within the same scope
2. `parameters` must conform to JSON Schema specification
3. MCP tools require MCP server configuration at runtime

### 2.3 Protocol Declaration

**Full Syntax**:

```ebnf
protocol_decl ::= "protocol" IDENTIFIER "{" field_list "}"

field_list ::= (IDENTIFIER ":" type_annotation ",")*

type_annotation ::= "string" | "number" | "boolean" | "array" | "object" 
                  | STRING_LITERAL  // Enum values
```

**Type Annotation Specification**:

```nexa
protocol UserResponse {
    name: "string",                    // String type
    age: "number",                     // Number type
    active: "boolean",                 // Boolean type
    tags: "array",                     // Array type
    metadata: "object",                // Object type
    status: "active|inactive|pending"  // Enum values (v0.9+)
}
```

**Semantic Rules**:

1. Protocol names must be unique within the same scope
2. Type annotations must be quoted
3. Enum values use `|` to separate multiple options
4. When an Agent declares `implements`, runtime validates output conforms to Protocol

### 2.4 Flow Declaration

**Full Syntax**:

```ebnf
flow_decl ::= "flow" IDENTIFIER ["(" parameter_list ")"] "{" flow_body "}"

flow_body ::= flow_stmt*

flow_stmt ::= assignment_stmt 
            | expr_stmt 
            | semantic_if_stmt 
            | loop_stmt 
            | match_stmt 
            | assert_stmt 
            | try_catch_stmt
            | print_stmt
```

**Example**:

```nexa
flow main(input: string) {
    // Assignment statement
    result = Agent1.run(input);
    
    // Pipeline expression
    final = input >> Agent1 >> Agent2;
    
    // Intent routing
    match input {
        intent("Query weather") => WeatherBot.run(input),
        intent("Set reminder") => ReminderBot.run(input),
        _ => DefaultBot.run(input)
    }
    
    // Output
    print(result);
}
```

### 2.5 Test Declaration

**Full Syntax**:

```ebnf
test_decl ::= "test" STRING_LITERAL "{" test_body "}"

test_body ::= flow_stmt*
```

**Example**:

```nexa
test "Weather query test" {
    mock_input = "What's the weather in Beijing today";
    result = WeatherBot.run(mock_input);
    
    assert "Contains weather information" against result;
    assert "Contains temperature data" against result;
}
```

---

## 3. Expression System

### 3.1 Basic Expressions

**Syntax**:

```ebnf
base_expr ::= method_call 
            | join_call 
            | STRING_LITERAL 
            | IDENTIFIER

method_call ::= IDENTIFIER ("." IDENTIFIER)? "(" argument_list? ")"

join_call ::= "join" "(" identifier_list ")" ["." IDENTIFIER "(" argument_list ")"]

argument_list ::= expression ("," expression)*
```

**Method Call**:

```nexa
Agent.run(input)           // Agent run
tool.execute(param)        // Tool execution
result.toString()          // Result conversion
```

**Join Call**:

```nexa
join([result1, result2])             // Merge results
join([result1, result2]).format()   // Format after merging
```

### 3.2 Pipeline Expression

**Syntax**:

```ebnf
pipeline_expr ::= base_expr (">>" base_expr)+
```

**Semantics**:

The `>>` operator passes the output of the left expression as input to the right expression.

```nexa
// Equivalent to Agent2.run(Agent1.run(input))
result = input >> Agent1 >> Agent2 >> Agent3
```

### 3.3 DAG Expression

Nexa v0.9.7+ supports complex DAG (Directed Acyclic Graph) topology orchestration.

#### Fork Operator `|>>`

**Syntax**:

```ebnf
dag_fork_expr ::= base_expr ("|>>" | "||") "[" identifier_list "]"
```

**Semantics**:

- `|>>`: Parallel execution, waits for all results to return
- `||`: Parallel execution, doesn't wait for results (fire-and-forget)

```nexa
// Parallel processing, wait for all results
results = input |>> [Agent1, Agent2, Agent3];

// Parallel processing, don't wait for results
input || [Logger, Analytics];
```

#### Merge Operator `&>>`

**Syntax**:

```ebnf
dag_merge_expr ::= "[" identifier_list "]" ("&>>" | "&&") base_expr
```

**Semantics**:

- `&>>`: Sequential merge, passes results in order
- `&&`: Consensus merge, requires multiple Agents to agree

```nexa
// Sequential merge
result = [Researcher, Analyst] &>> Reviewer;

// Consensus merge
consensus = [Agent1, Agent2] && JudgeAgent;
```

#### Conditional Branch Operator `??`

**Syntax**:

```ebnf
dag_branch_expr ::= base_expr "??" base_expr ":" base_expr
```

**Semantics**:

Selects execution path based on input characteristics. If input matches the first Agent's processing condition, execute the first; otherwise execute the second.

```nexa
result = input ?? UrgentHandler : NormalHandler;
```

#### Complex DAG Topology

```nexa
// Fork then merge
final = topic |>> [Researcher, Analyst] &>> Writer >> Reviewer;

// Multi-stage parallel
report = data |>> [Preprocess1, Preprocess2] &>> Aggregator >> Formatter;

// Conditional branch + parallel processing
result = input ?? FastPath : StandardPath |>> [Step1, Step2] &>> FinalStep;
```

### 3.4 Fallback Expression

**Syntax**:

```ebnf
fallback_expr ::= base_expr "fallback" expression
```

**Example**:

```nexa
result = PrimaryAgent.run(input) fallback BackupAgent.run(input);
```

---

## 4. Control Flow

### 4.1 Intent Routing (Match Intent)

**Syntax**:

```ebnf
match_stmt ::= "match" IDENTIFIER "{" match_branch+ ("_=>" expression)? "}"

match_branch ::= "intent" "(" STRING_LITERAL ")" "=>" expression ","
```

**Example**:

```nexa
match user_input {
    intent("Query weather") => WeatherBot.run(user_input),
    intent("Set reminder") => ReminderBot.run(user_input),
    intent("Play music") => MusicBot.run(user_input),
    _ => DefaultBot.run(user_input)  // Default branch
}
```

**Semantic Rules**:

1. `intent()` uses LLM for semantic matching
2. Branches are evaluated in order, first matching branch executes
3. `_` is the default branch, must be placed last
4. Returns the result of the matching branch expression

### 4.2 Semantic Conditional (Semantic If)

**Syntax**:

```ebnf
semantic_if_stmt ::= "semantic_if" STRING_LITERAL 
                     ["fast_match" REGEX_LITERAL] 
                     "against" IDENTIFIER
                     "{" flow_stmt* "}"
                     ("else" "{" flow_stmt* "}")?
```

**Example**:

```nexa
semantic_if "Contains date and location information" 
    fast_match r"\d{4}-\d{2}-\d{2}" 
    against user_input {
    Scheduler.run(user_input);
} else {
    Clarifier.run(user_input);
}
```

**Semantic Rules**:

1. `semantic_if` uses LLM to evaluate semantic conditions
2. `fast_match` provides regex pre-filtering to avoid repeated token consumption
3. Semantic evaluation only executes if `fast_match` passes
4. If condition is true, execute `if` block; otherwise execute `else` block

### 4.3 Semantic Loop (Loop Until)

**Syntax**:

```ebnf
loop_stmt ::= "loop" "{" flow_stmt* "}" "until" "(" STRING_LITERAL ")"
```

**Example**:

```nexa
loop {
    draft = Editor.run(feedback);
    feedback = Critic.run(draft);
} until ("Article grammar is correct and content is engaging")
```

**Semantic Rules**:

1. Loop body executes at least once
2. `until` condition uses LLM for semantic evaluation
3. Recommended to add maximum iteration limit to prevent infinite loops

**Deadlock Prevention Best Practice**:

```nexa
max_iterations = 5;
current = 0;
loop {
    draft = Editor.run(feedback);
    feedback = Critic.run(draft);
    current = current + 1;
    
    // Safety exit condition
    if current >= max_iterations {
        print("Maximum iterations reached, exiting loop");
        break;
    }
} until ("Article grammar is correct and content is engaging")
```

### 4.4 Exception Handling (Try/Catch)

**Syntax**:

```ebnf
try_catch_stmt ::= "try" "{" flow_stmt* "}" "catch" "(" IDENTIFIER ")" "{" flow_stmt* "}"
```

**Example**:

```nexa
try {
    result = APIAgent.run(input);
    print(result);
} catch (error) {
    print("Execution failed: " + error);
    result = FallbackAgent.run(input);
}
```

**Semantic Rules**:

1. When code in `try` block executes normally, `catch` block is ignored
2. If exception occurs in `try` block, control transfers to `catch` block
3. `catch` clause parameter binds to exception information

---

## 5. Assertion System

### 5.1 Assert Statement

**Syntax**:

```ebnf
assert_stmt ::= "assert" STRING_LITERAL "against" IDENTIFIER ";"
```

**Example**:

```nexa
test "Output validation test" {
    result = Analyst.run("Analyze Apple stock");
    
    assert "Contains stock price information" against result;
    assert "Contains market trend analysis" against result;
    assert "Does not contain sensitive information" against result;
}
```

**Semantics**:

1. `assert` uses LLM to verify semantic conditions
2. Test passes if condition is true, fails otherwise
3. Can be used in test declarations for automated verification

---

## 6. Type System

### 6.1 Built-in Types

| Type | Description | Example |
|------|------|------|
| `string` | String type | `"Hello"` |
| `number` | Number type | `42`, `3.14` |
| `boolean` | Boolean type | `true`, `false` |
| `array` | Array type | `["a", "b", "c"]` |
| `object` | Object type | `{"key": "value"}` |

### 6.2 Protocol Type Constraints

Protocol defines structured output constraints:

```nexa
protocol Report {
    title: "string",
    summary: "string",
    score: "number",
    tags: "array"
}

agent Reporter implements Report {
    role: "Report generator",
    prompt: "Generate structured report with title, summary, score, and tags"
}
```

**Runtime Validation**:

1. Agent output must conform to Protocol-defined fields
2. Automatic retry on type mismatch
3. Retry count controlled by system configuration

### 6.3 Enum Types

v0.9+ supports enum constraints:

```nexa
protocol Status {
    state: "pending|processing|completed|failed"
}
```

---

## 7. Decorator System

Decorators are used to add metadata and behavioral constraints to Agents.

### 7.1 Built-in Decorators

| Decorator | Parameters | Description |
|--------|------|------|
| `@limit` | `max_tokens=N` | Limit output token count |
| `@timeout` | `seconds=N` | Set execution timeout |
| `@retry` | `max_attempts=N` | Set maximum retry attempts |
| `@temperature` | `value=N` | Set model temperature parameter |

### 7.2 Usage Example

```nexa
@limit(max_tokens=1024)
@timeout(seconds=30)
@retry(max_attempts=3)
@temperature(value=0.7)
agent ConstrainedAgent {
    role: "Constrained Agent",
    prompt: "Strictly follow token and time limits"
}
```

---

## 8. Module System

### 8.1 Include Directive

**Syntax**:

```nexa
include "path/to/module.nxlib"
```

**Example**:

```nexa
// Include local library files
include "lib/tools.nxlib"
include "lib/agents.nxlib"
```

### 8.2 Import Directive

**Syntax**:

```nexa
import namespace.module as alias
```

**Example**:

```nexa
import std.fs
import std.http
import community.tools as ct
```

---

## 9. Memory Model

### 9.1 Memory Types

| Type | Description | Lifecycle |
|------|------|----------|
| `short` | Short-term memory | Single session |
| `session` | Session memory | During user session |
| `long` | Long-term memory | Persistent storage |

### 9.2 Memory Properties

```nexa
agent RememberingAgent {
    role: "Agent with memory",
    prompt: "Remember user preferences and conversation history",
    memory: "long",
    experience: true
}
```

---

## 10. Error Handling Reference

For detailed error codes and solutions, refer to [Error Index](error_index.md).

### 10.1 Compile-time Errors

| Error Code | Description |
|--------|------|
| E001 | Undeclared identifier |
| E002 | Type mismatch |
| E003 | Missing required property |
| E004 | Duplicate declaration |

### 10.2 Runtime Errors

| Error Code | Description |
|--------|------|
| E101 | Agent execution timeout |
| E102 | Model call failed |
| E103 | Protocol validation failed |
| E104 | Tool execution error |

---

## 📝 Appendix

### A. EBNF Syntax Summary

For complete EBNF syntax definition, refer to [Syntax Reference](../nexa/docs/01_nexa_syntax_reference.md).

### B. Keyword Index

- [`agent`](#21-agent-declaration) - Define agent
- [`tool`](#22-tool-declaration) - Define tool
- [`protocol`](#23-protocol-declaration) - Define output protocol
- [`flow`](#24-flow-declaration) - Define main flow
- [`test`](#25-test-declaration) - Define test
- [`match`](#41-intent-routing) - Intent routing
- [`semantic_if`](#42-semantic-conditional) - Semantic condition
- [`loop`](#43-semantic-loop) - Loop control
- [`try/catch`](#44-exception-handling) - Exception handling
- [`assert`](#51-assert-statement) - Assertion verification

---

## 🔗 Related Resources

- [Quickstart](quickstart.md)
- [Complete Examples](examples.md)
- [Troubleshooting](troubleshooting.md)
- [Basic Syntax](part1_basic.md)