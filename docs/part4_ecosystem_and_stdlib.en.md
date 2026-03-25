---
comments: true
---

# 5. Ecosystem Integration and Standard Library: The Gateway to the Physical World

The power of intelligent agents comes not only from internal logic flows and thinking, but also from the breadth and depth of their reach into the external physical world. In recent version iterations, Nexa has introduced powerful modularization and native device penetration capabilities (Vision/Standard Library modules). This chapter will detail these interfaces to the "greater world".

---

## 📦 Standard Library Extensions

In traditional glue frameworks, to implement an Agent that crawls web pages and saves them, you need to install requests yourself, hand-write beautifulsoup parsers, then package them into lengthy Tools for large models to call. Nexa has a built-in native `std` standard library.

You can directly declare agent permissions through the `uses` keyword, and Nexa will automatically handle sandbox environment isolation and calling context.

### Standard Library Namespaces

| Namespace | Description | Main Tools |
|---------|------|---------|
| `std.fs` | File system operations | `read`, `write`, `list`, `delete` |
| `std.http` | HTTP network requests | `get`, `post`, `put`, `delete` |
| `std.time` | Time-related operations | `now`, `sleep`, `format` |
| `std.shell` | System terminal commands | `execute` |
| `std.ask_human` | Human-computer interaction | `call` |
| `std.json` | JSON processing | `parse`, `stringify` |
| `std.math` | Mathematical operations | `calculate`, `random` |

---

## 📁 std.fs - File System Operations

File system operations are the basic capability for agents to interact with the local environment.

### Available Tools

| Tool | Description | Parameters |
|-----|------|------|
| `std.fs.read` | Read file content | `path: string` |
| `std.fs.write` | Write to file | `path: string`, `content: string` |
| `std.fs.append` | Append content | `path: string`, `content: string` |
| `std.fs.list` | List directory contents | `path: string` |
| `std.fs.delete` | Delete file | `path: string` |
| `std.fs.exists` | Check if file exists | `path: string` |

### Usage Example

```nexa
// File processing assistant
agent FileAssistant uses std.fs {
    role: "File Management Assistant",
    model: "deepseek/deepseek-chat",
    prompt: """
    You can help users manage files:
    - Read file content
    - Create and write files
    - List directory contents
    """
}

flow main {
    task = "Read the content of /tmp/notes.txt and summarize";
    result = FileAssistant.run(task);
    print(result);
}
```

### Complete Example: Log Management

```nexa
agent LogManager uses std.fs, std.time {
    role: "Log Manager",
    prompt: "Manage system log files, support reading, writing, and archiving"
}

flow main {
    // Create log entry
    timestamp = std.time.now();
    log_entry = f"[{timestamp}] System started";
    
    // Write log
    LogManager.run(f"Write '{log_entry}' to /var/log/system.log");
    
    // Read log
    logs = LogManager.run("Read the last 10 lines of /var/log/system.log");
    print(logs);
}
```

---

## 🌐 std.http - HTTP Network Requests

Native network request hooks that not only make requests but also have built-in parsers that automatically clean huge HTML/noise into clean readable Markdown to feed back into the model's context.

### Available Tools

| Tool | Description | Parameters |
|-----|------|------|
| `std.http.get` | GET request | `url: string`, `headers?: dict` |
| `std.http.post` | POST request | `url: string`, `data: dict`, `headers?: dict` |
| `std.http.put` | PUT request | `url: string`, `data: dict` |
| `std.http.delete` | DELETE request | `url: string` |

### Usage Example

```nexa
// Network request assistant
agent WebScraper uses std.http {
    role: "Web Scraping Assistant",
    model: "deepseek/deepseek-chat",
    prompt: "Scrape web content and extract key information"
}

flow main {
    url = "https://example.com/api/data";
    result = WebScraper.run(f"Get content from {url} and extract the title");
    print(result);
}
```

### Complete Example: News Aggregation

```nexa
agent NewsAggregator uses std.http, std.fs, std.time {
    role: "News Aggregator",
    model: "deepseek/deepseek-chat",
    prompt: """
    Get latest news from multiple news sources and aggregate.
    Save results to local file.
    """,
    cache: true
}

flow main {
    news_sources = [
        "https://news.example.com/tech",
        "https://news.example.com/business"
    ];
    
    aggregated = NewsAggregator.run(f"""
    Get today's news from the following sources and aggregate:
    {news_sources}
    
    Save to ~/news_summary.txt
    """);
    
    print(aggregated);
}
```

---

## ⏰ std.time - Time System

Give models trapped in static weights a "real sense of time".

### Available Tools

| Tool | Description | Return Value |
|-----|------|--------|
| `std.time.now` | Get current time | ISO format time string |
| `std.time.timestamp` | Get timestamp | Integer |
| `std.time.sleep` | Sleep | None |
| `std.time.format` | Format time | Formatted string |

### Usage Example

```nexa
agent TimeAwareBot uses std.time {
    role: "Time-Aware Assistant",
    prompt: "You know the current time and can help users handle time-related tasks"
}

flow main {
    // Agent will automatically get current time
    response = TimeAwareBot.run("What time is it now? What day of the week is today?");
    print(response);
}
```

### Complete Example: Schedule Reminder

```nexa
agent Scheduler uses std.time, std.fs {
    role: "Schedule Management Assistant",
    prompt: "Manage user schedules, can create reminders and view time"
}

flow main {
    // Create schedule
    now = std.time.now();
    Scheduler.run(f"""
    Current time: {now}
    Create a meeting reminder for tomorrow at 9 AM
    """);
}
```

---

## 💻 std.shell - System Terminal Commands

System-level terminal sinking for low-level operations.

!!! warning "Security Warning"
    `std.shell` has high system permissions, please use with caution. Recommended to use with RBAC permission control.

### Available Tools

| Tool | Description | Parameters |
|-----|------|------|
| `std.shell.execute` | Execute command | `command: string` |

### Usage Example

```nexa
agent DevOpsBot uses std.shell, std.fs {
    role: "Operations Assistant",
    model: "deepseek/deepseek-chat",
    prompt: """
    Execute system operations tasks:
    - View system status
    - Manage processes
    - File operations
    """
}

flow main {
    // View system status
    status = DevOpsBot.run("View file list in current directory");
    print(status);
}
```

---

## 🙋 std.ask_human - Human-in-the-Loop (HITL)

Native human-in-the-loop (HITL) inquiry breakout mechanism. This is a key component for building reliable AI systems.

### How It Works

```
Agent encounters uncertain situation
        │
        ▼
┌─────────────────────┐
│   std.ask_human     │
│   Pause, wait       │
└─────────────────────┘
        │
        ▼
    User input
        │
        ▼
┌─────────────────────┐
│   Continue          │
└─────────────────────┘
```

### Usage Example

```nexa
agent RiskyOperationBot uses std.ask_human {
    role: "Risky Operation Assistant",
    prompt: """
    Execute potentially risky operations.
    Before executing important operations, must ask user for confirmation.
    """
}

flow main {
    result = RiskyOperationBot.run("Delete all files in /tmp/old_files directory");
    print(result);
}
```

### Complete Example: Approval Process

```nexa
agent ApprovalBot uses std.ask_human, std.fs {
    role: "Approval Assistant",
    prompt: """
    Handle requests requiring approval:
    1. Analyze the risk level of the request
    2. High-risk operations must get manual confirmation
    3. Record approval results
    """
}

flow main {
    request = "Batch update configuration files in production environment";
    
    result = ApprovalBot.run(request);
    print(result);
}
```

---

## 🔐 `secret`: Sandbox Isolation for Sensitive Keys

When handling cloud APIs and database connections, you must never write `API_KEY` in plaintext in code and prompts! Nexa designed a native security pool `.nxs` (Nexa Secure) mechanism and `secret()` function.

### Configure Key File

Create `secrets.nxs` in the project root:

```bash
# secrets.nxs
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxx"
MINIMAX_API_KEY = "xxxxxxxxxxxx"
DATABASE_URL = "postgresql://user:pass@host:5432/db"
```

### Using Keys

Developers can write real keys in `secrets.nxs` in the same directory, while in `.nx` code, what you circulate is just a runtime-protected memory reference:

```nexa
flow main {
    // Just obtained an encrypted pointer through naming, will never be printed or written to ordinary logs
    my_key = secret("MY_TEST_KEY");
    
    // Agent connects externally through secure RPC calls with this key at the底层, ensuring data security of the entire workflow
    CloudDeployAgent.run("Deploy using the API credentials: ", my_key);
}
```

!!! warning "Security Best Practices"
    - **Never** commit `secrets.nxs` to version control
    - Add `secrets.nxs` to `.gitignore`
    - Use environment variables or dedicated key management services in production

---

## 🧩 Modular Revolution: `include` and SKILLS.md

To achieve large-scale collaboration for enterprise AI systems, code must be allowed to split at microservice level! Nexa's latest modular solution allows you to achieve elegant reuse.

### 1. `.nxlib` File Reference

You can package large amounts of commonly used basic Agents or communication protocols into dedicated `.nxlib` libraries, and the main file only needs one line of `include`:

```nexa
include "utils.nxlib";

flow main {
    // LibAgent comes from the imported utils.nxlib, you can call it directly as if it were native
    LibAgent.run("Echo this: module included successfully.");
}
```

**utils.nxlib content example**:

```nexa
// utils.nxlib - Utility library

agent LibAgent {
    role: "General Utility Agent",
    prompt: "Handle general tasks"
}

protocol StandardResponse {
    status: "string",
    message: "string"
}

agent StandardAgent implements StandardResponse {
    prompt: "Return standard format response"
}
```

### 2. Cross-Language Markdown Skill Mounting (`uses "SKILLS.md"`)

For extremely complex Tools requiring manual fine-tuning (like algorithms in specific business domains), Nexa breakthroughly supports directly parsing external `.md` skill definition files. Just declare the corresponding document path in `uses`, and the underlying Runtime will automatically read, parse, and mount those lengthy rules:

```nexa
// SKILLS.md contains lengthy environment guidelines and external functions
agent StreamBot uses "examples/SKILLS.md" {
    model: "minimax/minimax-m2.5",
    prompt: "I am a helpful assistant. Apply the skills strictly to solve this issue."
}
```

**SKILLS.md format example**:

```markdown
# Agent Skill Definition

## Tool: analyze_data
Description: Analyze data and generate report
Parameters:
- data: Data to analyze (string)
- format: Output format (optional)

## Tool: send_notification
Description: Send notification message
Parameters:
- message: Notification content
- channel: Notification channel (email/slack/sms)
```

---

## 👁️ Multimodal Pioneer: Globally Built-in Vision Primitive `img(...)`

Starting from V0.8 architecture, Nexa officially entered the full multimodal perception stage. You no longer need to hand-write tedious `Base64` encoding conversion or `multipart/form-data` parsing assembly; the language-level `img` type function handles everything for you:

### Basic Usage

```nexa
agent ResilientVisionAgent {
    model: "minimax/minimax-m2.5",
    prompt: "I test fallback and vision capabilities."
}

flow main {
    // Directly convert static images at the specified path to engine-recognized in-memory multimodal tensor objects
    img_data = img("docs/img/logo.jpg");
    
    // Pass to Agent just like a regular string, the底层 will adaptively match VLM (Vision Language Model) data flow!
    result = ResilientVisionAgent.run("Inspect this image", img_data);
    print(result);
}
```

### Complete Example: Image Analysis Pipeline

```nexa
// Vision-capable model
agent ImageAnalyzer {
    model: "openai/gpt-4-vision-preview",
    prompt: "Analyze image content, identify main elements and scenes"
}

agent ImageDescriber {
    model: "deepseek/deepseek-chat",
    prompt: "Convert image analysis results to natural language description"
}

flow main {
    // Load image
    image_path = "photos/landscape.jpg";
    image_data = img(image_path);
    
    // Analyze image
    analysis = ImageAnalyzer.run("Describe this image", image_data);
    
    // Generate description
    description = analysis >> ImageDescriber;
    
    print(description);
}
```

### Supported Image Formats

| Format | Extension |
|-----|-------|
| JPEG | `.jpg`, `.jpeg` |
| PNG | `.png` |
| GIF | `.gif` |
| WebP | `.webp` |
| BMP | `.bmp` |

---

## 📊 Standard Library Best Practices

### 1. Principle of Least Privilege

Only grant necessary tool permissions to Agents:

```nexa
// ✅ Good practice: Only grant necessary permissions
agent FileReader uses std.fs {
    prompt: "Only read files"
}

// ❌ Bad practice: Granting too many permissions
agent SimpleBot uses std.fs, std.http, std.shell {
    prompt: "Just simple conversation"
}
```

### 2. Cache Common Requests

Enable caching for repeated network requests:

```nexa
agent CachedScraper uses std.http {
    cache: true,  // Reduce duplicate requests
    prompt: "Scrape web content"
}
```

### 3. Handle Sensitive Information Securely

```nexa
// ✅ Use secret function
api_key = secret("API_KEY");
agent.run("Use API", api_key);

// ❌ Don't hardcode
agent.run("Use API key: sk-xxx");  // Dangerous!
```

---

## 📝 Chapter Summary

In this chapter, we learned:

| Module | Function | Use Case |
|-----|------|---------|
| `std.fs` | File system | Read/write files, directory management |
| `std.http` | Network requests | API calls, web scraping |
| `std.time` | Time operations | Schedule management, time awareness |
| `std.shell` | System commands | Operations tasks, script execution |
| `std.ask_human` | Human-computer interaction | Approval processes, confirmation operations |
| `secret()` | Key management | API authentication, database connections |
| `img()` | Multimodal | Image analysis, vision tasks |

Nexa's encapsulation of physical world modules always takes reducing developer cognitive burden and坚守 system sandbox security as the highest principles. These features lay the most solid infrastructure for you to build an automation kingdom.

---

## 🔗 Related Resources

- [Complete Example Collection](examples.md) - View more standard library usage examples
- [Best Practices](part6_best_practices.md) - Enterprise development experience
- [Troubleshooting Guide](troubleshooting.md) - Tool call problem solving
