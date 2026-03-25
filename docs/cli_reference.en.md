---
comments: true
---

# Nexa CLI Command Reference

This document details all commands, parameters, and usage examples for the Nexa command-line tool.

---

## 📖 Overview

Nexa CLI is the command-line interface for the Nexa language, providing compilation, execution, testing, and debugging features.

### Installation Verification

```bash
# Check installed version
nexa --version

# View help information
nexa --help
```

---

## 1. Core Commands

### 1.1 `nexa run` - Run Program

The main command for executing Nexa programs.

**Syntax**:

```bash
nexa run [OPTIONS] <FILE>
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--file` | `-f` | Nexa file to run | Required |
| `--model` | `-m` | Override default model | Config value |
| `--verbose` | `-v` | Show verbose output | `false` |
| `--debug` | `-d` | Enable debug mode | `false` |
| `--output` | `-o` | Output directory | `./out` |
| `--config` | `-c` | Configuration file path | `./nexa.yaml` |
| `--dry-run` | | Compile only without execution | `false` |
| `--env` | `-e` | Environment variable (KEY=VALUE) | - |

**Examples**:

```bash
# Basic run
nexa run main.nexa

# Specify model
nexa run main.nexa --model gpt-4

# Debug mode
nexa run main.nexa --debug --verbose

# Set environment variables
nexa run main.nexa -e API_KEY=sk-xxx -e DEBUG=true

# Compile only without execution
nexa run main.nexa --dry-run

# Specify output directory
nexa run main.nexa --output ./build
```

**Output Description**:

```
[INFO] Compiling main.nexa...
[INFO] Generated: ./out/main.py
[INFO] Executing...
[INFO] Agent 'Analyst' started
[INFO] Tool 'web_search' called with query: "..."
[RESULT] Execution result...
```

---

### 1.2 `nexa compile` - Compile Program

Compile Nexa code to Python code without execution.

**Syntax**:

```bash
nexa compile [OPTIONS] <FILE>
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--file` | `-f` | Nexa file to compile | Required |
| `--output` | `-o` | Output directory | `./out` |
| `--optimize` | `-O` | Optimization level (0-2) | `1` |
| `--target` | `-t` | Target format (`python`, `ast`, `bytecode`) | `python` |

**Examples**:

```bash
# Compile to Python
nexa compile main.nexa

# Specify output directory
nexa compile main.nexa -o ./dist

# Output AST (Abstract Syntax Tree)
nexa compile main.nexa --target ast

# Output bytecode (AVM)
nexa compile main.nexa --target bytecode

# Highest optimization level
nexa compile main.nexa --optimize 2
```

**Compilation Artifacts**:

```
out/
├── main.py           # Generated Python code
├── main.ast.json     # AST structure (--target ast)
└── main.bytecode     # AVM bytecode (--target bytecode)
```

---

### 1.3 `nexa test` - Run Tests

Execute Nexa test declarations.

**Syntax**:

```bash
nexa test [OPTIONS] [FILE_PATTERN]
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--pattern` | `-p` | Test name pattern | `*` |
| `--verbose` | `-v` | Show verbose output | `false` |
| `--report` | `-r` | Test report format (`text`, `json`, `html`) | `text` |
| `--fail-fast` | | Stop after first failure | `false` |
| `--coverage` | | Generate coverage report | `false` |

**Examples**:

```bash
# Run all tests
nexa test

# Run tests in specific file
nexa test tests/main_test.nexa

# Run tests matching pattern
nexa test --pattern "financial_*"

# Verbose output + JSON report
nexa test --verbose --report json

# Generate coverage report
nexa test --coverage --report html
```

**Test Output Example**:

```
Running tests...

✓ test_basic_pipeline (0.45s)
✓ test_intent_routing (1.23s)
✓ test_protocol_validation (0.89s)
✗ test_edge_case (0.12s) - Assertion failed: "output not as expected"

Summary: 3 passed, 1 failed
Total time: 2.69s
```

---

### 1.4 `nexa check` - Syntax Check

Static check of Nexa code syntax and types.

**Syntax**:

```bash
nexa check [OPTIONS] <FILE>
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--strict` | | Enable strict mode | `false` |
| `--format` | `-f` | Output format (`text`, `json`) | `text` |

**Examples**:

```bash
# Basic check
nexa check main.nexa

# Strict mode
nexa check main.nexa --strict

# JSON format output
nexa check main.nexa --format json
```

**Check Output Example**:

```
Checking main.nexa...

Warning: Line 15 - Unused agent 'TempAgent'
Error: Line 23 - Undefined protocol 'ReportFormat'
  --> main.nexa:23:5
   |
23 | agent Reporter implements ReportFormat {
   |                          ^^^^^^^^^^^^ not found
   |

Found 1 error, 1 warning
```

---

## 2. Project Management Commands

### 2.1 `nexa init` - Initialize Project

Create a new Nexa project structure.

**Syntax**:

```bash
nexa init [OPTIONS] [PROJECT_NAME]
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--template` | `-t` | Project template (`basic`, `web`, `cli`, `api`) | `basic` |
| `--path` | `-p` | Project path | Current directory |

**Examples**:

```bash
# Initialize in current directory
nexa init

# Create named project
nexa init my-agent-app

# Use template
nexa init my-web-bot --template web

# Specify path
nexa init my-project --path ~/projects/
```

**Generated Project Structure**:

```
my-agent-app/
├── main.nexa          # Main entry file
├── agents/            # Agent definitions directory
│   └── example.nexa
├── tools/             # Tool definitions directory
│   └── helper.nexa
├── tests/             # Tests directory
│   └── main_test.nexa
├── config/
│   └── nexa.yaml      # Configuration file
└── secrets.nxs        # Secrets file (needs configuration)
```

---

### 2.2 `nexa config` - Configuration Management

View and manage Nexa configuration.

**Syntax**:

```bash
nexa config [COMMAND] [OPTIONS]
```

**Subcommands**:

| Command | Description |
|------|------|
| `list` | List all configuration |
| `get <KEY>` | Get configuration value |
| `set <KEY> <VALUE>` | Set configuration value |
| `init` | Initialize configuration file |

**Examples**:

```bash
# List all configuration
nexa config list

# Get specific configuration
nexa config get model.default

# Set configuration
nexa config set model.default gpt-4
nexa config set debug.verbose true

# Initialize configuration file
nexa config init
```

**Configuration File Example** (`nexa.yaml`):

```yaml
# Nexa configuration file
model:
  default: gpt-4
  fallback: gpt-3.5-turbo
  
runtime:
  timeout: 300
  max_retries: 3
  
cache:
  enabled: true
  ttl: 3600
  
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
secrets:
  file: secrets.nxs
```

---

### 2.3 `nexa doctor` - Environment Diagnosis

Check runtime environment and dependencies.

**Syntax**:

```bash
nexa doctor
```

**Output Example**:

```
Nexa Environment Diagnostic

✓ Nexa version: 1.0.0-alpha
✓ Python version: 3.11.5
✓ Python path: /usr/bin/python3
✓ Dependencies installed
✓ Configuration valid

Model Connectivity:
✓ OpenAI API: Connected
✓ Anthropic API: Connected
✗ Local LLM: Not configured

Warnings:
! OpenAI API key expires in 7 days
! Cache directory is large (2.3GB)

Environment Status: HEALTHY (with warnings)
```

---

## 3. Interactive Mode Commands

### 3.1 `nexa repl` - Interactive REPL

Start an interactive Nexa interpreter.

**Syntax**:

```bash
nexa repl [OPTIONS]
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--model` | `-m` | Default model | Config value |
| `--history` | | History file | `~/.nexa/history` |

**REPL Commands**:

| Command | Description |
|------|------|
| `.help` | Show help |
| `.load <file>` | Load file |
| `.run <agent>` | Run specified Agent |
| `.clear` | Clear session |
| `.exit` | Exit REPL |

**Example Session**:

```bash
$ nexa repl

Nexa REPL v1.0.0-alpha
Type .help for commands

>>> agent Greeter {
...     role: "Friendly Greeter",
...     prompt: "Greet the user in a friendly manner"
... }
Created agent: Greeter

>>> Greeter.run("Hello")
Hello! Nice to meet you! How can I help you?

>>> .load examples/chat.nexa
Loaded 3 agents, 2 tools

>>> .exit
Goodbye!
```

---

### 3.2 `nexa chat` - Chat Mode

Direct conversational interaction with an Agent.

**Syntax**:

```bash
nexa chat [OPTIONS] [AGENT_NAME]
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--model` | `-m` | Specify model | Config value |
| `--system` | `-s` | System prompt | - |
| `--stream` | | Enable streaming output | `true` |

**Examples**:

```bash
# Start default chat
nexa chat

# Specify Agent
nexa chat Assistant

# Specify model and prompt
nexa chat --model claude-3 --system "You are a professional programming assistant"

# Disable streaming output
nexa chat --no-stream
```

---

## 4. Tools and Package Management

### 4.1 `nexa tool` - Tool Management

Manage custom tools.

**Subcommands**:

| Command | Description |
|------|------|
| `list` | List available tools |
| `add <name>` | Add new tool |
| `remove <name>` | Remove tool |
| `validate <file>` | Validate tool definition |

**Examples**:

```bash
# List tools
nexa tool list

# Add tool
nexa tool add my_custom_tool

# Validate tool definition
nexa tool validate tools/api.nexa
```

---

### 4.2 `nexa mcp` - MCP Management

Manage MCP (Model Context Protocol) servers.

**Subcommands**:

| Command | Description |
|------|------|
| `list` | List configured MCP servers |
| `add <name> <url>` | Add MCP server |
| `remove <name>` | Remove MCP server |
| `test <name>` | Test MCP connection |

**Examples**:

```bash
# List MCP servers
nexa mcp list

# Add MCP server
nexa mcp add web-search "github.com/nexa-ai/web-search-mcp"

# Test connection
nexa mcp test web-search

# Remove server
nexa mcp remove web-search
```

---

## 5. Debug and Diagnostic Commands

### 5.1 `nexa debug` - Debug Mode

Run program with verbose debug output.

**Syntax**:

```bash
nexa debug [OPTIONS] <FILE>
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--breakpoint` | `-b` | Set breakpoint (line number) | - |
| `--trace` | | Enable execution tracing | `false` |
| `--profile` | | Enable performance profiling | `false` |

**Examples**:

```bash
# Debug mode run
nexa debug main.nexa

# Set breakpoint
nexa debug main.nexa --breakpoint 25

# Execution tracing
nexa debug main.nexa --trace

# Performance profiling
nexa debug main.nexa --profile --output ./profile
```

**Debug Output Example**:

```
[DEBUG] Loading main.nexa...
[DEBUG] Parsing AST (12ms)
[DEBUG] Type checking (5ms)
[DEBUG] Compiling to Python (23ms)

[TRACE] main() started
[TRACE] → Agent 'Analyst' called with input: "..."
[TRACE]   → Tool 'web_search' called
[TRACE]   ← Tool returned (1.2s)
[TRACE] ← Agent returned (2.5s)
[TRACE] main() completed

Profile Summary:
- Agent calls: 3
- Tool calls: 5
- Total time: 4.2s
- Token usage: 2,450
```

---

### 5.2 `nexa inspect` - Code Inspection

Inspect the structure of Agents, Tools, and Protocols.

**Syntax**:

```bash
nexa inspect [OPTIONS] <FILE> [ELEMENT]
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--format` | `-f` | Output format (`text`, `json`, `tree`) | `text` |

**Examples**:

```bash
# Inspect all elements in file
nexa inspect main.nexa

# Inspect specific Agent
nexa inspect main.nexa Analyst

# Tree structure output
nexa inspect main.nexa --format tree

# JSON format output (for program parsing)
nexa inspect main.nexa --format json
```

**Output Example**:

```
Agent: Analyst
├── Role: Financial Analyst
├── Model: gpt-4
├── Memory: session
├── Tools:
│   ├── web_search
│   └── calculator
├── Protocol: Report
│   ├── title: string
│   ├── summary: string
│   └── score: number
└── Modifiers:
    ├── @limit(max_tokens=2048)
    └── @timeout(seconds=60)
```

---

## 6. Output and Logging Commands

### 6.1 `nexa logs` - Log Viewing

View runtime logs.

**Syntax**:

```bash
nexa logs [OPTIONS]
```

**Parameters**:

| Parameter | Short | Description | Default |
|------|------|------|--------|
| `--follow` | `-f` | Follow logs in real-time | `false` |
| `--lines` | `-n` | Number of lines to show | `100` |
| `--level` | `-l` | Log level (`DEBUG`, `INFO`, `WARN`, `ERROR`) | `INFO` |
| `--since` | | Time range (`1h`, `1d`, `1w`) | - |

**Examples**:

```bash
# View recent logs
nexa logs

# Real-time follow
nexa logs --follow

# View last 500 lines
nexa logs --lines 500

# View only error logs
nexa logs --level ERROR

# View logs from last hour
nexa logs --since 1h
```

---

## 7. Global Options

The following options apply to all commands:

| Option | Short | Description |
|------|------|------|
| `--help` | `-h` | Show help information |
| `--version` | `-V` | Show version number |
| `--quiet` | `-q` | Quiet mode, only output errors |
| `--verbose` | `-v` | Verbose output |
| `--color` | | Control color output (`auto`, `always`, `never`) |
| `--config` | `-c` | Specify configuration file path |

**Examples**:

```bash
# Quiet run
nexa run main.nexa --quiet

# Verbose output
nexa run main.nexa -vvv

# Disable color output
nexa run main.nexa --color never

# Specify configuration file
nexa run main.nexa --config ./custom/nexa.yaml
```

---

## 8. Environment Variables

Nexa CLI supports the following environment variables:

| Variable | Description | Default |
|------|------|--------|
| `NEXA_CONFIG` | Configuration file path | `./nexa.yaml` |
| `NEXA_MODEL` | Default model | Config value |
| `NEXA_API_KEY` | API key | - |
| `NEXA_LOG_LEVEL` | Log level | `INFO` |
| `NEXA_CACHE_DIR` | Cache directory | `~/.nexa/cache` |
| `NEXA_OUTPUT_DIR` | Output directory | `./out` |

**Examples**:

```bash
# Set environment variables
export NEXA_MODEL=gpt-4
export NEXA_LOG_LEVEL=DEBUG
nexa run main.nexa
```

---

## 9. Exit Codes

| Exit Code | Description |
|--------|------|
| `0` | Success |
| `1` | General error |
| `2` | Configuration error |
| `3` | Compilation error |
| `4` | Runtime error |
| `5` | Test failure |
| `6` | Network error |
| `7` | Authentication error |

---

## 🔗 Related Resources

- [Language Reference Manual](reference.md)
- [Troubleshooting Guide](troubleshooting.md)
- [Quickstart](quickstart.md)