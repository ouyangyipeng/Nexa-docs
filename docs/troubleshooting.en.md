---
comments: true
---

# Troubleshooting Guide

This document summarizes common problems and their solutions when using Nexa. If you encounter a problem, please check this guide first.

---

## 📋 Table of Contents

- [Installation and Environment Issues](#1-installation-and-environment-issues)
- [Syntax Error Troubleshooting](#2-syntax-error-troubleshooting)
- [Runtime Error Troubleshooting](#3-runtime-error-troubleshooting)
- [Model Call Issues](#4-model-call-issues)
- [Tool Call Issues](#5-tool-call-issues)
- [Protocol Related Issues](#6-protocol-related-issues)
- [Debugging Tips](#7-debugging-tips)

---

## 1. Installation and Environment Issues

### 1.1 `pip install` Failed

**Symptom**:
```
ERROR: Could not find a version that satisfies the requirement nexa
```

**Reason**: Nexa has not been published to PyPI yet, need to install from source.

**Solution**:
```bash
git clone https://github.com/your-org/nexa.git
cd nexa
pip install -e .
```

---

### 1.2 Python Version Incompatible

**Symptom**:
```
SyntaxError: invalid syntax
```
or
```
TypeError: ... got an unexpected keyword argument
```

**Reason**: Nexa requires Python 3.10 or higher.

**Solution**:
```bash
# Check Python version
python --version

# If version is lower than 3.10, upgrade or use virtual environment
# Using conda
conda create -n nexa python=3.10
conda activate nexa

# Or using venv
python3.10 -m venv nexa-env
source nexa-env/bin/activate  # Linux/macOS
# nexa-env\Scripts\activate   # Windows
```

---

### 1.3 Dependency Conflicts

**Symptom**:
```
ERROR: Cannot install nexa because these package versions have conflicting dependencies
```

**Solution**:
```bash
# Clean and reinstall
pip uninstall nexa -y
pip cache purge
pip install -e . --no-cache-dir
```

---

### 1.4 `nexa: command not found`

**Symptom**:
```bash
$ nexa run hello.nx
bash: nexa: command not found
```

**Reason**: pip installation path is not in PATH, or virtual environment is not activated.

**Solution**:
```bash
# Option 1: Ensure virtual environment is activated
source nexa-env/bin/activate

# Option 2: Use python -m to invoke
python -m nexa run hello.nx

# Option 3: Add pip path to PATH (not recommended)
export PATH="$HOME/.local/bin:$PATH"
```

---

## 2. Syntax Error Troubleshooting

### 2.1 Parse Error: Unexpected token

**Symptom**:
```
ParseError: Unexpected token '}' at line 15
```

**Common Causes**:

1. **Missing comma or semicolon**
```nexa
// ❌ Wrong
agent Bot {
    role: "Assistant"    // Missing comma
    prompt: "..."
}

// ✅ Correct
agent Bot {
    role: "Assistant",
    prompt: "..."
}
```

2. **Mismatched brackets**
```nexa
// ❌ Wrong
flow main {
    result = Bot.run("hello"
}

// ✅ Correct
flow main {
    result = Bot.run("hello");
}
```

3. **Unclosed string**
```nexa
// ❌ Wrong
agent Bot {
    prompt: "This is a very long prompt
            with line break but not closed"
}

// ✅ Correct: Use triple quotes
agent Bot {
    prompt: """
        This is a very long prompt
        line break is fine
    """
}
```

---

### 2.2 Agent Undefined

**Symptom**:
```
NameError: name 'MyAgent' is not defined
```

**Reason**: Agent is defined after flow, or typo.

**Solution**:
```nexa
// ❌ Wrong: Agent defined after flow
flow main {
    result = MyAgent.run("hello");
}

agent MyAgent {
    prompt: "..."
}

// ✅ Correct: Agent defined before flow
agent MyAgent {
    prompt: "..."
}

flow main {
    result = MyAgent.run("hello");
}
```

---

### 2.3 Property Name Typo

**Symptom**: Agent behaves abnormally, property not taking effect.

**Common Typos**:
```nexa
// ❌ Common misspellings
agent Bot {
    promt: "...",        // Should be prompt
    moedl: "gpt-4",      // Should be model
    rol: "Assistant"     // Should be role
}

// ✅ Correct spelling
agent Bot {
    prompt: "...",
    model: "gpt-4",
    role: "Assistant"
}
```

**Checklist**:
| Correct Spelling | Common Errors |
|---------|---------|
| `prompt` | `promt`, `prompts` |
| `model` | `moedl`, `Model` |
| `role` | `rol`, `Role` |
| `tools` | `tool`, `Tool` |
| `memory` | `memmory`, `Memory` |

---

### 2.4 Protocol Syntax Error

**Symptom**:
```
InvalidProtocolError: Protocol field type must be a string
```

**Error Example**:
```nexa
// ❌ Wrong: Type not wrapped in quotes
protocol UserInfo {
    name: string,        // Should be "string"
    age: int             // Should be "int"
}

// ✅ Correct
protocol UserInfo {
    name: "string",
    age: "int"
}
```

---

## 3. Runtime Error Troubleshooting

### 3.1 API Key Not Found

**Symptom**:
```
RuntimeError: API key not found for provider 'openai'
```

**Solution**:

1. **Check if secrets.nxs file exists**
```bash
ls -la secrets.nxs
```

2. **Check if key format is correct**
```bash
# secrets.nxs content example
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxx"
MINIMAX_API_KEY = "xxxxxxxxxxxx"
MINIMAX_GROUP_ID = "xxxxxxxxxxxx"
```

3. **Check file location**
```
project/
├── secrets.nxs      # Must be in project root
├── main.nx
└── ...
```

---

### 3.2 Network Connection Timeout

**Symptom**:
```
httpx.ConnectTimeout: Connection timed out
```

**Solution**:

1. **Check network connection**
```bash
curl -I https://api.openai.com
```

2. **Configure proxy (if needed)**
```bash
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"
```

3. **Increase timeout** (in code)
```nexa
agent Bot {
    model: "openai/gpt-4",
    prompt: "...",
    timeout: 60  // 60 second timeout
}
```

---

### 3.3 Out of Memory

**Symptom**:
```
MemoryError: Unable to allocate array
```

**Reason**: Long conversation history or large number of concurrent Agents.

**Solution**:

1. **Enable context compression**
```nexa
agent Bot {
    prompt: "...",
    max_history_turns: 5  // Limit history turns
}
```

2. **Use cache to reduce repeated computation**
```nexa
agent Bot {
    prompt: "...",
    cache: true  // Enable intelligent cache
}
```

3. **Reduce concurrency**
```nexa
// ❌ Avoid too many parallel Agents
input |>> [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10]

// ✅ Batch processing
input |>> [A1, A2, A3]
```

---

### 3.4 Loop Not Terminating

**Symptom**: `loop until` keeps running until timeout.

**Reason**: Termination condition too vague, LLM cannot accurately judge.

**Solution**:

1. **Use clearer termination conditions**
```nexa
// ❌ Vague condition
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Article is perfect")  // Too subjective

// ✅ Clearer condition
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Reviewer explicitly says 'passed' with no modification suggestions")
```

2. **Add maximum loop count protection**
```nexa
loop {
    draft = Writer.run(feedback);
    feedback = Reviewer.run(draft);
} until ("Article is perfect" or runtime.meta.loop_count >= 5)

// Check if exceeded
if (runtime.meta.loop_count >= 5) {
    print("Reached maximum retry count, please check manually");
}
```

---

## 4. Model Call Issues

### 4.1 Model Name Format Error

**Symptom**:
```
ModelError: Unknown model format: gpt-4
```

**Reason**: Model name must include provider prefix.

**Correct Format**:
```nexa
// ✅ Correct format
model: "openai/gpt-4"
model: "openai/gpt-4-turbo"
model: "deepseek/deepseek-chat"
model: "minimax/minimax-m2.5"
model: "anthropic/claude-3-sonnet"

// ❌ Wrong format
model: "gpt-4"           // Missing provider
model: "GPT-4"           // Case error
model: "deepseek-chat"   // Missing slash
```

---

### 4.2 Model Does Not Support Certain Features

**Symptom**:
```
NotImplementedError: Model 'xxx' does not support function calling
```

**Solution**:

Choose models that support required features:

| Feature | Supported Models |
|-----|----------|
| Function Calling | GPT-4, GPT-3.5-turbo, DeepSeek-Chat |
| Structured Output | GPT-4, Claude-3, DeepSeek-Chat |
| Vision | GPT-4-vision, Claude-3, MiniMax-VL |

---

### 4.3 Rate Limit

**Symptom**:
```
RateLimitError: Rate limit exceeded for model
```

**Solution**:

1. **Configure Fallback model**
```nexa
agent Bot {
    model: ["openai/gpt-4", fallback: "deepseek/deepseek-chat"],
    prompt: "..."
}
```

2. **Add retry configuration**
```nexa
agent Bot {
    model: "openai/gpt-4",
    prompt: "...",
    retry: 3,           // Retry count
    retry_delay: 5      // Retry delay (seconds)
}
```

3. **Use cache to reduce requests**
```nexa
agent Bot {
    cache: true,  // Reuse results for same requests
    prompt: "..."
}
```

---

### 4.4 Output Truncation

**Symptom**: Model output is truncated in the middle.

**Reason**: Reached token limit.

**Solution**:

```nexa
agent Bot {
    prompt: "...",
    max_tokens: 4096  // Increase output length limit
}
```

Or use decorator:
```nexa
@limit(max_tokens=4096)
agent Bot {
    prompt: "..."
}
```

---

## 5. Tool Call Issues

### 5.1 Tool Not Found

**Symptom**:
```
ToolNotFoundError: Tool 'my_tool' not found in registry
```

**Reason**: Tool not properly registered or imported.

**Solution**:

1. **Check uses declaration**
```nexa
// ❌ Wrong: Tool not declared
agent Bot {
    prompt: "..."
}
// Later calling Bot.run() cannot use tools

// ✅ Correct: Declare tools to use
agent Bot uses std.http, std.fs {
    prompt: "..."
}
```

2. **Check standard library import**
```nexa
// If using custom tool, ensure path is correct
agent Bot uses "my_tools.py" {
    prompt: "..."
}
```

---

### 5.2 Tool Parameter Error

**Symptom**:
```
ToolExecutionError: Invalid parameters for tool 'xxx'
```

**Solution**:

Check tool definition parameter format:
```nexa
// ❌ Wrong: Incorrect parameter format
tool MyTool {
    description: "Tool description",
    parameters: {
        param1: string  // Missing quotes
    }
}

// ✅ Correct
tool MyTool {
    description: "Tool description",
    parameters: {
        "param1": "string",
        "param2": "number"
    }
}
```

---

### 5.3 Tool Execution Timeout

**Symptom**:
```
TimeoutError: Tool execution timed out after 30s
```

**Solution**:

```nexa
agent Bot uses std.http {
    prompt: "...",
    tool_timeout: 60  // Increase timeout
}
```

---

## 6. Protocol Related Issues

### 6.1 Output Format Does Not Match Protocol

**Symptom**:
```
ProtocolValidationError: Expected field 'xxx' but got 'yyy'
```

**Reason**: LLM output does not match defined Protocol.

**Auto-fix Mechanism**:

Nexa automatically attempts to fix, but if it fails multiple times, you can:

1. **Simplify Protocol**
```nexa
// ❌ Overly complex Protocol
protocol ComplexData {
    field1: "string",
    field2: "list[dict[string, any]]",  // Too complex
    field3: "dict[string, list[int]]"
}

// ✅ Simplified Protocol
protocol SimpleData {
    field1: "string",
    field2: "string",  // Use string to represent complex structure
    field3: "string"
}
```

2. **Specify format requirements in Prompt**
```nexa
agent DataExtractor implements MyProtocol {
    prompt: """
    Extract data and strictly output in JSON format.
    Must include fields: field1, field2, field3
    """
}
```

---

### 6.2 Protocol Type Mismatch

**Symptom**:
```
TypeError: Expected 'int' but got 'string'
```

**Solution**:

Ensure types in Protocol match expected:
```nexa
// Correct type annotations
protocol DataTypes {
    text: "string",      // String
    number: "int",       // Integer
    price: "float",      // Float
    flag: "boolean",     // Boolean
    tags: "list[string]" // String list
}
```

---

## 7. Debugging Tips

### 7.1 Use `nexa build` to View Generated Code

```bash
# Generate Python code for debugging
nexa build script.nx

# Will generate out_script.py
# You can directly run or inspect this file
python out_script.py
```

### 7.2 Enable Verbose Logging

```bash
# Enable debug mode at runtime
nexa run script.nx --debug

# Or set environment variable
export NEXA_DEBUG=1
nexa run script.nx
```

### 7.3 Check Intermediate Results

Use `print` in flow to output intermediate results:
```nexa
flow main {
    step1 = Agent1.run(input);
    print("Step 1 result: " + step1);
    
    step2 = Agent2.run(step1);
    print("Step 2 result: " + step2);
}
```

### 7.4 Debug with Python SDK

```python
from src.nexa_sdk import NexaRuntime

# Create runtime
runtime = NexaRuntime(debug=True)

# Run script
result = runtime.run_script("script.nx")

# Check result
print(result)
```

### 7.5 Check Cache Status

```bash
# View cache statistics
nexa cache stats

# Clear cache
nexa cache clear
```

---

## 8. Error Code Quick Reference

| Error Code | Meaning | Common Cause |
|---------|-----|---------|
| `E001` | Parse error | Syntax error, mismatched brackets |
| `E002` | Undefined identifier | Agent/Tool undefined or typo |
| `E003` | Type error | Parameter type mismatch |
| `E101` | API Key error | Key not configured or invalid |
| `E102` | Network error | Connection timeout, proxy issue |
| `E103` | Rate Limit | Request frequency exceeded |
| `E201` | Tool not found | uses not declared or path error |
| `E202` | Tool execution error | Parameter error, timeout |
| `E301` | Protocol validation failed | Output format doesn't match definition |
| `E302` | Protocol type error | Field type mismatch |

---

## 9. Getting Help

If the above solutions don't resolve your issue:

1. **Check Documentation**: [Complete Example Collection](examples.md) may have similar scenarios
2. **Submit Issue**: Submit an Issue on GitHub repository, including:
   - Complete error message
   - Your code (sanitized)
   - Runtime environment information
3. **Community Discussion**: Use Giscus at the bottom of the documentation page to participate in discussions

---

<div align="center">
  <p>📖 Don't panic when encountering problems, check this guide or seek community help!</p>
</div>