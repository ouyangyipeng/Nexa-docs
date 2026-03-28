---
comments: true
---

# Nexa Standard Library Reference

This document describes all namespaces, tool functions, parameters, and usage examples of the Nexa standard library (`std`).

---

## 📋 Overview

The Nexa standard library provides built-in tools that enable Agents to interact with the external world. After declaring usage permissions via the `uses` keyword, Agents can call these tools.

### Namespace Overview

| Namespace | Description | Tool Count |
|---------|------|---------|
| [`std.fs`](#stdfs-file-system-operations) | File system operations | 6 |
| [`std.http`](#stdhttp-http-network-requests) | HTTP network requests | 4 |
| [`std.time`](#stdtime-time-and-date-operations) | Time and date operations | 5 |
| [`std.json`](#stdjson-json-data-processing) | JSON data processing | 3 |
| [`std.text`](#stdtext-text-processing) | Text processing | 4 |
| [`std.hash`](#stdhash-encryption-and-encoding) | Encryption and encoding | 4 |
| [`std.math`](#stdmath-mathematical-operations) | Mathematical operations | 2 |
| [`std.regex`](#stdregex-regular-expressions) | Regular expressions | 2 |
| [`std.shell`](#stdshell-shell-commands) | Shell command execution | 2 |
| [`std.ask_human`](#stdask_human-human-interaction) | Human interaction | 1 |

---

## 📁 std.fs - File System Operations

File system operations are fundamental capabilities for agents to interact with the local environment.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`file_read`](#file_read) | Read file content | `path` |
| [`file_write`](#file_write) | Write to file | `path`, `content` |
| [`file_append`](#file_append) | Append to file | `path`, `content` |
| [`file_exists`](#file_exists) | Check if file exists | `path` |
| [`file_list`](#file_list) | List directory files | `directory` |
| [`file_delete`](#file_delete) | Delete file | `path` |

---

#### file_read

Read file content.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |
| `encoding` | string | No | `utf-8` | Encoding format |

**Return Value**: File content string, or error message on failure.

**Example**:

```nexa
agent FileReader uses std.fs {
    role: "File reading assistant",
    prompt: "Help users read file content"
}

flow main {
    content = FileReader.run("Read file /tmp/data.txt");
    print(content);
}
```

---

#### file_write

Write content to file. Creates directory if it doesn't exist.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |
| `content` | string | **Yes** | - | File content |
| `encoding` | string | No | `utf-8` | Encoding format |

**Return Value**: Success message with character count.

**Example**:

```nexa
agent FileWriter uses std.fs {
    role: "File writing assistant",
    prompt: "Help users write files"
}

flow main {
    result = FileWriter.run("Write 'Hello Nexa' to /tmp/output.txt");
    print(result);
}
```

---

#### file_append

Append content to end of file.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |
| `content` | string | **Yes** | - | Content to append |
| `encoding` | string | No | `utf-8` | Encoding format |

**Return Value**: Success message with appended character count.

**Example**:

```nexa
agent LogWriter uses std.fs {
    role: "Log recording assistant",
    prompt: "Help users append logs"
}

flow main {
    LogWriter.run("Append '[2024-01-01] New log entry' to /var/log/app.log");
}
```

---

#### file_exists

Check if file or directory exists.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File/directory path |

**Return Value**: JSON format `{ "exists": bool, "path": string }`.

**Example**:

```nexa
agent FileChecker uses std.fs {
    role: "File checking assistant",
    prompt: "Check if file exists"
}

flow main {
    result = FileChecker.run("Check if /tmp/config.json exists");
    print(result);  // {"exists": true, "path": "/tmp/config.json"}
}
```

---

#### file_list

List files in directory.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `directory` | string | **Yes** | - | Directory path |
| `pattern` | string | No | `*` | File match pattern (glob format) |

**Return Value**: JSON format `{ "files": [string], "count": int }`.

**Example**:

```nexa
agent DirectoryScanner uses std.fs {
    role: "Directory scanning assistant",
    prompt: "List files in directory"
}

flow main {
    // List all files
    all_files = DirectoryScanner.run("List all files in /tmp directory");
    
    // List only .txt files
    txt_files = DirectoryScanner.run("List *.txt files in /tmp directory");
    print(txt_files);
}
```

---

#### file_delete

Delete file.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `path` | string | **Yes** | - | File path |

**Return Value**: Success or error message.

**Example**:

```nexa
agent FileCleaner uses std.fs {
    role: "File cleanup assistant",
    prompt: "Delete specified files"
}

flow main {
    result = FileCleaner.run("Delete /tmp/old_data.txt");
    print(result);
}
```

---

## 🌐 std.http - HTTP Network Requests

Native network request capabilities supporting RESTful API calls.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`http_get`](#http_get) | GET request | `url` |
| [`http_post`](#http_post) | POST request | `url`, `data` |
| [`http_put`](#http_put) | PUT request | `url`, `data` |
| [`http_delete`](#http_delete) | DELETE request | `url` |

---

#### http_get

Send HTTP GET request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `headers` | object | No | `{}` | Request headers dictionary |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return Value**: Response content string.

**Example**:

```nexa
agent WebFetcher uses std.http {
    role: "Web fetching assistant",
    prompt: "Fetch web content"
}

flow main {
    content = WebFetcher.run("GET https://api.example.com/data");
    print(content);
}
```

---

#### http_post

Send HTTP POST request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `data` | string | **Yes** | - | Request body content |
| `headers` | object | No | `{}` | Request headers dictionary |
| `content_type` | string | No | `application/json` | Content type |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return Value**: JSON format `{ "status": int, "body": string }`.

**Example**:

```nexa
agent ApiClient uses std.http {
    role: "API client",
    prompt: "Call RESTful API"
}

flow main {
    payload = '{"name": "Nexa", "version": "1.0"}';
    result = ApiClient.run(f"POST {payload} to https://api.example.com/create");
    print(result);
}
```

---

#### http_put

Send HTTP PUT request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `data` | string | **Yes** | - | Request body content |
| `headers` | object | No | `{}` | Request headers dictionary |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return Value**: JSON format `{ "status": int, "body": string }`.

**Example**:

```nexa
agent DataUpdater uses std.http {
    role: "Data update assistant",
    prompt: "Update remote data"
}

flow main {
    update_data = '{"status": "completed"}';
    result = DataUpdater.run(f"PUT {update_data} to https://api.example.com/item/123");
}
```

---

#### http_delete

Send HTTP DELETE request.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `url` | string | **Yes** | - | Request URL |
| `headers` | object | No | `{}` | Request headers dictionary |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return Value**: JSON format `{ "status": int, "body": string }`.

**Example**:

```nexa
agent ResourceDeleter uses std.http {
    role: "Resource deletion assistant",
    prompt: "Delete remote resources"
}

flow main {
    result = ResourceDeleter.run("DELETE https://api.example.com/item/123");
}
```

---

## 🕐 std.time - Time and Date Operations

Time-related operation tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`time_now`](#time_now) | Get current time | None |
| [`time_diff`](#time_diff) | Calculate time difference | `start`, `end` |
| [`time_format`](#time_format) | Format time | `iso_string` |
| [`time_sleep`](#time_sleep) | Sleep for specified seconds | `seconds` |
| [`time_timestamp`](#time_timestamp) | Get timestamp | None |

---

#### time_now

Get current time.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `format` | string | No | `%Y-%m-%d %H:%M:%S` | Time format |

**Return Value**: Formatted time string.

**Format Specifiers**:

| Format | Description | Example |
|-------|------|------|
| `%Y` | Year | 2024 |
| `%m` | Month | 01-12 |
| `%d` | Day | 01-31 |
| `%H` | Hour (24-hour) | 00-23 |
| `%M` | Minute | 00-59 |
| `%S` | Second | 00-59 |

**Example**:

```nexa
agent TimeHelper uses std.time {
    role: "Time assistant",
    prompt: "Provide time-related services"
}

flow main {
    // Default format
    now = TimeHelper.run("Get current time");
    print(now);  // 2024-01-15 10:30:00
    
    // Custom format
    date_only = TimeHelper.run("Get current date in format %Y-%m-%d");
    print(date_only);  // 2024-01-15
}
```

---

#### time_diff

Calculate difference between two times.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `start` | string | **Yes** | - | Start time (ISO format) |
| `end` | string | **Yes** | - | End time (ISO format) |
| `unit` | string | No | `seconds` | Unit: `seconds`/`minutes`/`hours`/`days` |

**Return Value**: JSON format `{ "value": float, "unit": string, "days": int, "seconds": float }`.

**Example**:

```nexa
agent DurationCalculator uses std.time {
    role: "Duration calculator",
    prompt: "Calculate time difference"
}

flow main {
    result = DurationCalculator.run(
        "Calculate hours between 2024-01-01T00:00:00 and 2024-01-02T12:00:00"
    );
    print(result);  // {"value": 36, "unit": "hours", ...}
}
```

---

#### time_format

Convert ISO format time to specified format.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `iso_string` | string | **Yes** | - | ISO time string |
| `format` | string | No | `%Y-%m-%d %H:%M:%S` | Output format |

**Return Value**: Formatted time string.

**Example**:

```nexa
agent DateFormatter uses std.time {
    role: "Date formatting assistant",
    prompt: "Convert time format"
}

flow main {
    result = DateFormatter.run(
        "Format 2024-01-15T10:30:00 to show only date"
    );
    print(result);  // 2024-01-15
}
```

---

#### time_sleep

Pause execution for specified seconds.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `seconds` | int | **Yes** | - | Sleep seconds |

**Return Value**: JSON format `{ "sleep": int }`.

**Example**:

```nexa
agent DelayedTask uses std.time {
    role: "Delayed task assistant",
    prompt: "Execute delayed tasks"
}

flow main {
    print("Starting wait...");
    DelayedTask.run("Wait for 5 seconds");
    print("Wait complete!");
}
```

---

#### time_timestamp

Get current Unix timestamp.

**Parameters**: None

**Return Value**: JSON format `{ "timestamp": int }`.

**Example**:

```nexa
agent TimestampGenerator uses std.time {
    role: "Timestamp generator",
    prompt: "Generate timestamps"
}

flow main {
    ts = TimestampGenerator.run("Get current timestamp");
    print(ts);  // {"timestamp": 1705312200}
}
```

---

## 📦 std.json - JSON Data Processing

JSON data parsing, querying, and serialization.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`json_parse`](#json_parse) | Parse JSON | `text` |
| [`json_get`](#json_get) | Get JSON path value | `text`, `path` |
| [`json_stringify`](#json_stringify) | Serialize to JSON | `data` |

---

#### json_parse

Parse JSON string.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | JSON string |

**Return Value**: Formatted JSON string (easy to read).

**Example**:

```nexa
agent JsonParser uses std.json {
    role: "JSON parsing assistant",
    prompt: "Parse JSON data"
}

flow main {
    raw = '{"name":"Nexa","version":1.0}';
    parsed = JsonParser.run(f"Parse {raw}");
    print(parsed);
}
```

---

#### json_get

Extract value from specified JSON path.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | JSON string |
| `path` | string | **Yes** | - | Path (e.g., `data.items.0`) |

**Return Value**: Value at the specified path.

**Path Format**:
- Use `.` to separate levels
- Array indices use numbers, e.g., `items.0.name`

**Example**:

```nexa
agent DataExtractor uses std.json {
    role: "Data extraction assistant",
    prompt: "Extract data from JSON"
}

flow main {
    json_data = '{"user":{"name":"Alice","age":30}}';
    name = DataExtractor.run(f"Get user.name from {json_data}");
    print(name);  // "Alice"
}
```

---

#### json_stringify

Serialize data to JSON string.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `data` | string | **Yes** | - | Data object (JSON format string) |
| `indent` | int | No | `2` | Indent spaces |

**Return Value**: Formatted JSON string.

**Example**:

```nexa
agent JsonSerializer uses std.json {
    role: "JSON serialization assistant",
    prompt: "Serialize data to JSON"
}

flow main {
    data = '{"name":"Nexa"}';
    result = JsonSerializer.run(f"Serialize {data} with 4-space indent");
    print(result);
}
```

---

## 📝 std.text - Text Processing

Text processing tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`text_split`](#text_split) | Split text | `text` |
| [`text_replace`](#text_replace) | Replace text | `text`, `old`, `new` |
| [`text_upper`](#text_upper) | Convert to uppercase | `text` |
| [`text_lower`](#text_lower) | Convert to lowercase | `text` |

---

#### text_split

Split text into parts.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Text to split |
| `delimiter` | string | No | `\n` | Delimiter |
| `max_splits` | int | No | `-1` | Maximum splits (-1 means unlimited) |

**Return Value**: JSON format `{ "parts": [string], "count": int }`.

**Example**:

```nexa
agent TextSplitter uses std.text {
    role: "Text splitting assistant",
    prompt: "Split text"
}

flow main {
    text = "one,two,three,four";
    result = TextSplitter.run(f"Split {text} by comma");
    print(result);  // {"parts": ["one", "two", "three", "four"], "count": 4}
}
```

---

#### text_replace

Replace content in text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Original text |
| `old` | string | **Yes** | - | Content to replace |
| `new` | string | **Yes** | - | Replacement content |
| `count` | int | No | `-1` | Replace count (-1 means all) |

**Return Value**: Replaced text.

**Example**:

```nexa
agent TextReplacer uses std.text {
    role: "Text replacement assistant",
    prompt: "Replace content in text"
}

flow main {
    text = "Hello World, Hello Nexa";
    result = TextReplacer.run(f"Replace Hello with Hi in {text}");
    print(result);  // "Hi World, Hi Nexa"
}
```

---

#### text_upper

Convert text to uppercase.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return Value**: Uppercase text.

---

#### text_lower

Convert text to lowercase.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return Value**: Lowercase text.

---

## 🔐 std.hash - Encryption and Encoding

Hash calculation and encoding tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`hash_md5`](#hash_md5) | MD5 hash | `text` |
| [`hash_sha256`](#hash_sha256) | SHA256 hash | `text` |
| [`base64_encode`](#base64_encode) | Base64 encode | `text` |
| [`base64_decode`](#base64_decode) | Base64 decode | `text` |

---

#### hash_md5

Calculate MD5 hash of text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return Value**: 32-character MD5 hash string.

**Example**:

```nexa
agent HashHelper uses std.hash {
    role: "Hash calculation assistant",
    prompt: "Calculate text hash"
}

flow main {
    hash = HashHelper.run("Calculate MD5 of 'Hello Nexa'");
    print(hash);  // 32-character hash value
}
```

---

#### hash_sha256

Calculate SHA256 hash of text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return Value**: 64-character SHA256 hash string.

---

#### base64_encode

Encode text to Base64 format.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Input text |

**Return Value**: Base64 encoded string.

---

#### base64_decode

Decode Base64 text.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `text` | string | **Yes** | - | Base64 encoded text |

**Return Value**: Decoded original text.

---

## 🔢 std.math - Mathematical Operations

Mathematical calculation tools.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`math_calc`](#math_calc) | Calculate math expression | `expression` |
| [`math_random`](#math_random) | Generate random number | `min_val`, `max_val` |

---

#### math_calc

Safely calculate mathematical expression.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `expression` | string | **Yes** | - | Math expression |

**Return Value**: JSON format `{ "result": number, "expression": string }`.

!!! warning "Security Limitation"
    Only allows digits and `+-*/.()` characters, other characters are rejected.

**Example**:

```nexa
agent Calculator uses std.math {
    role: "Math calculation assistant",
    prompt: "Calculate math expressions"
}

flow main {
    result = Calculator.run("Calculate (10 + 5) * 2");
    print(result);  // {"result": 30, "expression": "(10 + 5) * 2"}
}
```

---

#### math_random

Generate random integer within specified range.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `min_val` | int | **Yes** | - | Minimum value |
| `max_val` | int | **Yes** | - | Maximum value |

**Return Value**: Random integer.

**Example**:

```nexa
agent RandomGenerator uses std.math {
    role: "Random number generator",
    prompt: "Generate random numbers"
}

flow main {
    num = RandomGenerator.run("Generate random number between 1 and 100");
    print(num);
}
```

---

## 🔍 std.regex - Regular Expressions

Regular expression matching and replacement.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`regex_match`](#regex_match) | Regex match | `pattern`, `text` |
| [`regex_replace`](#regex_replace) | Regex replace | `pattern`, `replacement`, `text` |

---

#### regex_match

Match text using regular expression.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `pattern` | string | **Yes** | - | Regex pattern |
| `text` | string | **Yes** | - | Text to match |
| `flags` | string | No | `""` | Flags: `i`(ignore case), `m`(multiline), `s`(singleline) |

**Return Value**: JSON format `{ "matches": [string], "count": int }`.

**Example**:

```nexa
agent PatternMatcher uses std.regex {
    role: "Pattern matching assistant",
    prompt: "Match regex patterns"
}

flow main {
    text = "Email: test@example.com, Phone: 123-456-7890";
    emails = PatternMatcher.run(f"Match all email addresses in {text}");
    print(emails);
}
```

---

#### regex_replace

Replace text using regular expression.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `pattern` | string | **Yes** | - | Regex pattern |
| `replacement` | string | **Yes** | - | Replacement content |
| `text` | string | **Yes** | - | Text to process |
| `flags` | string | No | `""` | Flags |

**Return Value**: Replaced text.

---

## 💻 std.shell - Shell Commands

Execute system shell commands.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`shell_exec`](#shell_exec) | Execute command | `command` |
| [`shell_which`](#shell_which) | Find command path | `command` |

---

#### shell_exec

Execute shell command.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `command` | string | **Yes** | - | Command to execute |
| `timeout` | int | No | `30` | Timeout in seconds |

**Return Value**: JSON format `{ "stdout": string, "stderr": string, "returncode": int, "success": bool }`.

!!! warning "Security Warning"
    Shell command execution has potential risks. Please ensure:
    - Don't execute dangerous commands (like `rm -rf /`)
    - Validate input parameters
    - Set reasonable timeout

**Example**:

```nexa
agent ShellRunner uses std.shell {
    role: "Shell execution assistant",
    prompt: "Execute system commands"
}

flow main {
    result = ShellRunner.run("Execute ls -la /tmp");
    print(result.stdout);
}
```

---

#### shell_which

Find executable file path for command.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `command` | string | **Yes** | - | Command name |

**Return Value**: JSON format `{ "command": string, "path": string, "found": bool }`.

---

## 🙋 std.ask_human - Human Interaction

Human-in-the-Loop interaction tool.

### Tool List

| Tool | Description | Required Parameters |
|-----|------|---------|
| [`ask_human`](#ask_human) | Request user input | `prompt` |

---

#### ask_human

Request user input for Human-in-the-Loop interaction.

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----|------|-----|-------|------|
| `prompt` | string | **Yes** | - | Prompt message |
| `default` | string | No | `""` | Default value (used when user doesn't input) |

**Return Value**: User input string.

**Example**:

```nexa
agent HumanInterface uses std.ask_human {
    role: "Human interaction assistant",
    prompt: "Interact with user for confirmation"
}

flow main {
    // Wait for user input
    confirmation = HumanInterface.run("Please confirm if to continue? [y/n]");
    
    if (confirmation == "y") {
        print("User confirmed, continuing...");
    } else {
        print("User rejected, stopping");
    }
}
```

---

## 🔧 Usage

### Declare Usage Permission

Use `uses` keyword in Agent definition:

```nexa
// Single namespace
agent MyAgent uses std.fs {
    prompt: "..."
}

// Multiple namespaces
agent MultiToolAgent uses std.fs, std.http, std.time {
    prompt: "..."
}
```

### Runtime Invocation

Agents call tools via natural language instructions:

```nexa
agent Assistant uses std.fs, std.http {
    role: "Multi-function assistant",
    prompt: "Help users complete file and network operations"
}

flow main {
    // Natural language tool invocation
    result = Assistant.run("Read /tmp/data.txt and POST to https://api.example.com/upload");
    print(result);
}
```

---

## 📚 Complete Examples

### Log Management Agent

```nexa
agent LogManager uses std.fs, std.time {
    role: "Log management expert",
    model: "deepseek/deepseek-chat",
    prompt: """
    You are a log management expert, you can:
    - Read and analyze log files
    - Create and append log entries
    - Provide timestamp information
    """
}

flow main {
    task = """
    1. Get current timestamp
    2. Create log entry: [timestamp] System started
    3. Append to /var/log/nexa.log
    """;
    
    result = LogManager.run(task);
    print(result);
}
```

### API Data Fetcher Agent

```nexa
agent DataFetcher uses std.http, std.json {
    role: "Data fetching expert",
    prompt: "Fetch data from API and parse JSON"
}

flow main {
    task = """
    1. GET https://api.example.com/users
    2. Parse returned JSON
    3. Extract name field of first user
    """;
    
    name = DataFetcher.run(task);
    print(f"First user: {name}");
}
```

---

## 📊 Version History

| Version | Updates |
|-----|---------|
| v1.0 | Added `std.text`, `std.hash`, `std.math`, `std.regex` namespaces |
| v0.9.7 | Added `std.shell`, `std.ask_human` namespaces |
| v0.9 | Completed file operation tools (`append`, `delete`) |
| v0.8 | Added HTTP PUT/DELETE methods |
| v0.7 | Initial standard library release (`std.fs`, `std.http`, `std.time`) |

---

*Last updated: 2026-03-28 | Based on Nexa v0.9.7-alpha / v1.0-alpha AVM*