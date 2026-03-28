---
comments: true
---

# Nexa 标准库参考手册

本文档详细描述 Nexa 标准库 (`std`) 的所有命名空间、工具函数、参数和使用示例。

---

## 📋 概述

Nexa 标准库提供了一系列内置工具，使 Agent 能够与外部世界交互。通过 `uses` 关键字声明使用权限后，Agent 即可调用这些工具。

### 命名空间总览

| 命名空间 | 说明 | 工具数量 |
|---------|------|---------|
| [`std.fs`](#stdfs-文件系统操作) | 文件系统操作 | 6 |
| [`std.http`](#stdhttp-http-网络请求) | HTTP 网络请求 | 4 |
| [`std.time`](#stdtime-时间日期操作) | 时间日期操作 | 5 |
| [`std.json`](#stdjson-json-数据处理) | JSON 数据处理 | 3 |
| [`std.text`](#stdtext-文本处理) | 文本处理 | 4 |
| [`std.hash`](#stdhash-加密与编码) | 加密与编码 | 4 |
| [`std.math`](#stdmath-数学运算) | 数学运算 | 2 |
| [`std.regex`](#stdregex-正则表达式) | 正则表达式 | 2 |
| [`std.shell`](#stdshell-shell-命令) | Shell 命令执行 | 2 |
| [`std.ask_human`](#stdask_human-人机交互) | 人机交互 | 1 |

---

## 📁 std.fs - 文件系统操作

文件系统操作是智能体与本地环境交互的基础能力。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`file_read`](#file_read) | 读取文件内容 | `path` |
| [`file_write`](#file_write) | 写入文件 | `path`, `content` |
| [`file_append`](#file_append) | 追加文件内容 | `path`, `content` |
| [`file_exists`](#file_exists) | 检查文件是否存在 | `path` |
| [`file_list`](#file_list) | 列出目录文件 | `directory` |
| [`file_delete`](#file_delete) | 删除文件 | `path` |

---

#### file_read

读取文件内容。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |
| `encoding` | string | 否 | `utf-8` | 编码格式 |

**返回值**：文件内容字符串，或在出错时返回错误信息。

**示例**：

```nexa
agent FileReader uses std.fs {
    role: "文件读取助手",
    prompt: "帮助用户读取文件内容"
}

flow main {
    content = FileReader.run("读取 /tmp/data.txt 文件");
    print(content);
}
```

---

#### file_write

写入文件内容。如果目录不存在，会自动创建。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |
| `content` | string | **是** | - | 文件内容 |
| `encoding` | string | 否 | `utf-8` | 编码格式 |

**返回值**：成功信息，包含写入的字符数。

**示例**：

```nexa
agent FileWriter uses std.fs {
    role: "文件写入助手",
    prompt: "帮助用户写入文件"
}

flow main {
    result = FileWriter.run("将 'Hello Nexa' 写入 /tmp/output.txt");
    print(result);
}
```

---

#### file_append

追加内容到文件末尾。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |
| `content` | string | **是** | - | 追加内容 |
| `encoding` | string | 否 | `utf-8` | 编码格式 |

**返回值**：成功信息，包含追加的字符数。

**示例**：

```nexa
agent LogWriter uses std.fs {
    role: "日志记录助手",
    prompt: "帮助用户追加日志"
}

flow main {
    LogWriter.run("追加 '[2024-01-01] New log entry' 到 /var/log/app.log");
}
```

---

#### file_exists

检查文件或目录是否存在。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件/目录路径 |

**返回值**：JSON 格式 `{ "exists": bool, "path": string }`。

**示例**：

```nexa
agent FileChecker uses std.fs {
    role: "文件检查助手",
    prompt: "检查文件是否存在"
}

flow main {
    result = FileChecker.run("检查 /tmp/config.json 是否存在");
    print(result);  // {"exists": true, "path": "/tmp/config.json"}
}
```

---

#### file_list

列出目录中的文件。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `directory` | string | **是** | - | 目录路径 |
| `pattern` | string | 否 | `*` | 文件匹配模式（glob 格式） |

**返回值**：JSON 格式 `{ "files": [string], "count": int }`。

**示例**：

```nexa
agent DirectoryScanner uses std.fs {
    role: "目录扫描助手",
    prompt: "列出目录中的文件"
}

flow main {
    // 列出所有文件
    all_files = DirectoryScanner.run("列出 /tmp 目录中的所有文件");
    
    // 只列出 .txt 文件
    txt_files = DirectoryScanner.run("列出 /tmp 目录中的 *.txt 文件");
    print(txt_files);
}
```

---

#### file_delete

删除文件。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `path` | string | **是** | - | 文件路径 |

**返回值**：成功或错误信息。

**示例**：

```nexa
agent FileCleaner uses std.fs {
    role: "文件清理助手",
    prompt: "删除指定的文件"
}

flow main {
    result = FileCleaner.run("删除 /tmp/old_data.txt");
    print(result);
}
```

---

## 🌐 std.http - HTTP 网络请求

原生网络请求能力，支持 RESTful API 调用。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`http_get`](#http_get) | GET 请求 | `url` |
| [`http_post`](#http_post) | POST 请求 | `url`, `data` |
| [`http_put`](#http_put) | PUT 请求 | `url`, `data` |
| [`http_delete`](#http_delete) | DELETE 请求 | `url` |

---

#### http_get

发送 HTTP GET 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：响应内容字符串。

**示例**：

```nexa
agent WebFetcher uses std.http {
    role: "网页获取助手",
    prompt: "获取网页内容"
}

flow main {
    content = WebFetcher.run("获取 https://api.example.com/data");
    print(content);
}
```

---

#### http_post

发送 HTTP POST 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `data` | string | **是** | - | 请求体内容 |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `content_type` | string | 否 | `application/json` | 内容类型 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "status": int, "body": string }`。

**示例**：

```nexa
agent ApiClient uses std.http {
    role: "API 客户端",
    prompt: "调用 RESTful API"
}

flow main {
    payload = '{"name": "Nexa", "version": "1.0"}';
    result = ApiClient.run(f"POST {payload} 到 https://api.example.com/create");
    print(result);
}
```

---

#### http_put

发送 HTTP PUT 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `data` | string | **是** | - | 请求体内容 |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "status": int, "body": string }`。

**示例**：

```nexa
agent DataUpdater uses std.http {
    role: "数据更新助手",
    prompt: "更新远程数据"
}

flow main {
    update_data = '{"status": "completed"}';
    result = DataUpdater.run(f"PUT {update_data} 到 https://api.example.com/item/123");
}
```

---

#### http_delete

发送 HTTP DELETE 请求。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `url` | string | **是** | - | 请求 URL |
| `headers` | object | 否 | `{}` | 请求头字典 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "status": int, "body": string }`。

**示例**：

```nexa
agent ResourceDeleter uses std.http {
    role: "资源删除助手",
    prompt: "删除远程资源"
}

flow main {
    result = ResourceDeleter.run("DELETE https://api.example.com/item/123");
}
```

---

## 🕐 std.time - 时间日期操作

时间相关的操作工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`time_now`](#time_now) | 获取当前时间 | 无 |
| [`time_diff`](#time_diff) | 计算时间差 | `start`, `end` |
| [`time_format`](#time_format) | 格式化时间 | `iso_string` |
| [`time_sleep`](#time_sleep) | 休眠指定秒数 | `seconds` |
| [`time_timestamp`](#time_timestamp) | 获取时间戳 | 无 |

---

#### time_now

获取当前时间。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `format` | string | 否 | `%Y-%m-%d %H:%M:%S` | 时间格式 |

**返回值**：格式化后的时间字符串。

**格式说明**：

| 格式符 | 说明 | 示例 |
|-------|------|------|
| `%Y` | 年份 | 2024 |
| `%m` | 月份 | 01-12 |
| `%d` | 日期 | 01-31 |
| `%H` | 小时 (24小时制) | 00-23 |
| `%M` | 分钟 | 00-59 |
| `%S` | 秒 | 00-59 |

**示例**：

```nexa
agent TimeHelper uses std.time {
    role: "时间助手",
    prompt: "提供时间相关服务"
}

flow main {
    // 默认格式
    now = TimeHelper.run("获取当前时间");
    print(now);  // 2024-01-15 10:30:00
    
    // 自定义格式
    date_only = TimeHelper.run("获取当前日期，格式为 %Y-%m-%d");
    print(date_only);  // 2024-01-15
}
```

---

#### time_diff

计算两个时间之间的差值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `start` | string | **是** | - | 开始时间 (ISO 格式) |
| `end` | string | **是** | - | 结束时间 (ISO 格式) |
| `unit` | string | 否 | `seconds` | 单位：`seconds`/`minutes`/`hours`/`days` |

**返回值**：JSON 格式 `{ "value": float, "unit": string, "days": int, "seconds": float }`。

**示例**：

```nexa
agent DurationCalculator uses std.time {
    role: "时长计算器",
    prompt: "计算时间差"
}

flow main {
    result = DurationCalculator.run(
        "计算 2024-01-01T00:00:00 和 2024-01-02T12:00:00 之间的小时差"
    );
    print(result);  // {"value": 36, "unit": "hours", ...}
}
```

---

#### time_format

将 ISO 格式时间转换为指定格式。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `iso_string` | string | **是** | - | ISO 时间字符串 |
| `format` | string | 否 | `%Y-%m-%d %H:%M:%S` | 输出格式 |

**返回值**：格式化后的时间字符串。

**示例**：

```nexa
agent DateFormatter uses std.time {
    role: "日期格式化助手",
    prompt: "转换时间格式"
}

flow main {
    result = DateFormatter.run(
        "将 2024-01-15T10:30:00 格式化为 仅显示日期"
    );
    print(result);  // 2024-01-15
}
```

---

#### time_sleep

暂停执行指定秒数。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `seconds` | int | **是** | - | 休眠秒数 |

**返回值**：JSON 格式 `{ "sleep": int }`。

**示例**：

```nexa
agent DelayedTask uses std.time {
    role: "延迟任务助手",
    prompt: "执行延迟任务"
}

flow main {
    print("开始等待...");
    DelayedTask.run("等待 5 秒");
    print("等待完成！");
}
```

---

#### time_timestamp

获取当前 Unix 时间戳。

**参数**：无

**返回值**：JSON 格式 `{ "timestamp": int }`。

**示例**：

```nexa
agent TimestampGenerator uses std.time {
    role: "时间戳生成器",
    prompt: "生成时间戳"
}

flow main {
    ts = TimestampGenerator.run("获取当前时间戳");
    print(ts);  // {"timestamp": 1705312200}
}
```

---

## 📦 std.json - JSON 数据处理

JSON 数据的解析、查询和序列化。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`json_parse`](#json_parse) | 解析 JSON | `text` |
| [`json_get`](#json_get) | 获取 JSON 路径值 | `text`, `path` |
| [`json_stringify`](#json_stringify) | 序列化为 JSON | `data` |

---

#### json_parse

解析 JSON 字符串。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | JSON 字符串 |

**返回值**：格式化后的 JSON 字符串（便于阅读）。

**示例**：

```nexa
agent JsonParser uses std.json {
    role: "JSON 解析助手",
    prompt: "解析 JSON 数据"
}

flow main {
    raw = '{"name":"Nexa","version":1.0}';
    parsed = JsonParser.run(f"解析 {raw}");
    print(parsed);
}
```

---

#### json_get

从 JSON 中提取指定路径的值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | JSON 字符串 |
| `path` | string | **是** | - | 路径（如 `data.items.0`） |

**返回值**：路径对应的值。

**路径格式**：
- 使用 `.` 分隔层级
- 数组索引使用数字，如 `items.0.name`

**示例**：

```nexa
agent DataExtractor uses std.json {
    role: "数据提取助手",
    prompt: "从 JSON 中提取数据"
}

flow main {
    json_data = '{"user":{"name":"Alice","age":30}}';
    name = DataExtractor.run(f"从 {json_data} 获取 user.name");
    print(name);  // "Alice"
}
```

---

#### json_stringify

将数据序列化为 JSON 字符串。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `data` | string | **是** | - | 数据对象（JSON 格式字符串） |
| `indent` | int | 否 | `2` | 缩进空格数 |

**返回值**：格式化的 JSON 字符串。

**示例**：

```nexa
agent JsonSerializer uses std.json {
    role: "JSON 序列化助手",
    prompt: "序列化数据为 JSON"
}

flow main {
    data = '{"name":"Nexa"}';
    result = JsonSerializer.run(f"序列化 {data}，缩进为 4 空格");
    print(result);
}
```

---

## 📝 std.text - 文本处理

文本处理工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`text_split`](#text_split) | 分割文本 | `text` |
| [`text_replace`](#text_replace) | 替换文本 | `text`, `old`, `new` |
| [`text_upper`](#text_upper) | 转大写 | `text` |
| [`text_lower`](#text_lower) | 转小写 | `text` |

---

#### text_split

分割文本为多个部分。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 待分割文本 |
| `delimiter` | string | 否 | `\n` | 分隔符 |
| `max_splits` | int | 否 | `-1` | 最大分割次数 (-1 表示不限) |

**返回值**：JSON 格式 `{ "parts": [string], "count": int }`。

**示例**：

```nexa
agent TextSplitter uses std.text {
    role: "文本分割助手",
    prompt: "分割文本"
}

flow main {
    text = "one,two,three,four";
    result = TextSplitter.run(f"用逗号分割 {text}");
    print(result);  // {"parts": ["one", "two", "three", "four"], "count": 4}
}
```

---

#### text_replace

替换文本中的内容。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 原文本 |
| `old` | string | **是** | - | 被替换内容 |
| `new` | string | **是** | - | 替换内容 |
| `count` | int | 否 | `-1` | 替换次数 (-1 表示全部) |

**返回值**：替换后的文本。

**示例**：

```nexa
agent TextReplacer uses std.text {
    role: "文本替换助手",
    prompt: "替换文本中的内容"
}

flow main {
    text = "Hello World, Hello Nexa";
    result = TextReplacer.run(f"将 {text} 中的 Hello 替换为 Hi");
    print(result);  // "Hi World, Hi Nexa"
}
```

---

#### text_upper

将文本转换为大写。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：大写文本。

---

#### text_lower

将文本转换为小写。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：小写文本。

---

## 🔐 std.hash - 加密与编码

哈希计算和编码工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`hash_md5`](#hash_md5) | MD5 哈希 | `text` |
| [`hash_sha256`](#hash_sha256) | SHA256 哈希 | `text` |
| [`base64_encode`](#base64_encode) | Base64 编码 | `text` |
| [`base64_decode`](#base64_decode) | Base64 解码 | `text` |

---

#### hash_md5

计算文本的 MD5 哈希值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：32 字符的 MD5 哈希字符串。

**示例**：

```nexa
agent HashHelper uses std.hash {
    role: "哈希计算助手",
    prompt: "计算文本哈希"
}

flow main {
    hash = HashHelper.run("计算 'Hello Nexa' 的 MD5");
    print(hash);  // 32字符哈希值
}
```

---

#### hash_sha256

计算文本的 SHA256 哈希值。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：64 字符的 SHA256 哈希字符串。

---

#### base64_encode

将文本编码为 Base64 格式。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | 输入文本 |

**返回值**：Base64 编码字符串。

---

#### base64_decode

解码 Base64 文本。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `text` | string | **是** | - | Base64 编码文本 |

**返回值**：解码后的原始文本。

---

## 🔢 std.math - 数学运算

数学计算工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`math_calc`](#math_calc) | 计算数学表达式 | `expression` |
| [`math_random`](#math_random) | 生成随机数 | `min_val`, `max_val` |

---

#### math_calc

安全计算数学表达式。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `expression` | string | **是** | - | 数学表达式 |

**返回值**：JSON 格式 `{ "result": number, "expression": string }`。

!!! warning "安全限制"
    只允许数字和 `+-*/.()` 字符，其他字符会被拒绝。

**示例**：

```nexa
agent Calculator uses std.math {
    role: "数学计算助手",
    prompt: "计算数学表达式"
}

flow main {
    result = Calculator.run("计算 (10 + 5) * 2");
    print(result);  // {"result": 30, "expression": "(10 + 5) * 2"}
}
```

---

#### math_random

生成指定范围内的随机整数。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `min_val` | int | **是** | - | 最小值 |
| `max_val` | int | **是** | - | 最大值 |

**返回值**：随机整数。

**示例**：

```nexa
agent RandomGenerator uses std.math {
    role: "随机数生成器",
    prompt: "生成随机数"
}

flow main {
    num = RandomGenerator.run("生成 1 到 100 之间的随机数");
    print(num);
}
```

---

## 🔍 std.regex - 正则表达式

正则表达式匹配和替换。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`regex_match`](#regex_match) | 正则匹配 | `pattern`, `text` |
| [`regex_replace`](#regex_replace) | 正则替换 | `pattern`, `replacement`, `text` |

---

#### regex_match

使用正则表达式匹配文本。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `pattern` | string | **是** | - | 正则表达式模式 |
| `text` | string | **是** | - | 待匹配文本 |
| `flags` | string | 否 | `""` | 标志：`i`(忽略大小写)、`m`(多行)、`s`(单行) |

**返回值**：JSON 格式 `{ "matches": [string], "count": int }`。

**示例**：

```nexa
agent PatternMatcher uses std.regex {
    role: "模式匹配助手",
    prompt: "匹配正则表达式"
}

flow main {
    text = "Email: test@example.com, Phone: 123-456-7890";
    emails = PatternMatcher.run(f"从 {text} 中匹配所有邮箱地址");
    print(emails);
}
```

---

#### regex_replace

使用正则表达式替换文本。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `pattern` | string | **是** | - | 正则表达式模式 |
| `replacement` | string | **是** | - | 替换内容 |
| `text` | string | **是** | - | 待处理文本 |
| `flags` | string | 否 | `""` | 标志 |

**返回值**：替换后的文本。

---

## 💻 std.shell - Shell 命令

执行系统 Shell 命令。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`shell_exec`](#shell_exec) | 执行命令 | `command` |
| [`shell_which`](#shell_which) | 查找命令路径 | `command` |

---

#### shell_exec

执行 Shell 命令。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `command` | string | **是** | - | 要执行的命令 |
| `timeout` | int | 否 | `30` | 超时秒数 |

**返回值**：JSON 格式 `{ "stdout": string, "stderr": string, "returncode": int, "success": bool }`。

!!! warning "安全警告"
    Shell 命令执行具有潜在风险，请确保：
    - 不执行危险命令（如 `rm -rf /`）
    - 验证输入参数
    - 设置合理的超时时间

**示例**：

```nexa
agent ShellRunner uses std.shell {
    role: "Shell 执行助手",
    prompt: "执行系统命令"
}

flow main {
    result = ShellRunner.run("执行 ls -la /tmp");
    print(result.stdout);
}
```

---

#### shell_which

查找命令的可执行文件路径。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `command` | string | **是** | - | 命令名称 |

**返回值**：JSON 格式 `{ "command": string, "path": string, "found": bool }`。

---

## 🙋 std.ask_human - 人机交互

Human-in-the-Loop 交互工具。

### 工具列表

| 工具 | 说明 | 必填参数 |
|-----|------|---------|
| [`ask_human`](#ask_human) | 请求用户输入 | `prompt` |

---

#### ask_human

请求用户输入，实现 Human-in-the-Loop 交互。

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| `prompt` | string | **是** | - | 提示信息 |
| `default` | string | 否 | `""` | 默认值（用户不输入时使用） |

**返回值**：用户输入的字符串。

**示例**：

```nexa
agent HumanInterface uses std.ask_human {
    role: "人机交互助手",
    prompt: "与用户交互获取确认"
}

flow main {
    // 等待用户输入
    confirmation = HumanInterface.run("请确认是否继续执行？[y/n]");
    
    if (confirmation == "y") {
        print("用户已确认，继续执行...");
    } else {
        print("用户拒绝，终止执行");
    }
}
```

---

## 🔧 使用方式

### 声明使用权限

在 Agent 定义中使用 `uses` 关键字声明：

```nexa
// 单个命名空间
agent MyAgent uses std.fs {
    prompt: "..."
}

// 多个命名空间
agent MultiToolAgent uses std.fs, std.http, std.time {
    prompt: "..."
}
```

### 运行时调用

Agent 通过自然语言指令调用工具：

```nexa
agent Assistant uses std.fs, std.http {
    role: "多功能助手",
    prompt: "帮助用户完成文件和网络操作"
}

flow main {
    // 自然语言调用工具
    result = Assistant.run("读取 /tmp/data.txt 并 POST 到 https://api.example.com/upload");
    print(result);
}
```

---

## 📚 完整示例

### 日志管理 Agent

```nexa
agent LogManager uses std.fs, std.time {
    role: "日志管理专家",
    model: "deepseek/deepseek-chat",
    prompt: """
    你是日志管理专家，可以：
    - 读取和分析日志文件
    - 创建和追加日志条目
    - 提供时间戳信息
    """
}

flow main {
    task = """
    1. 获取当前时间戳
    2. 创建日志条目：[时间戳] 系统启动
    3. 追加到 /var/log/nexa.log
    """;
    
    result = LogManager.run(task);
    print(result);
}
```

### API 数据抓取 Agent

```nexa
agent DataFetcher uses std.http, std.json {
    role: "数据抓取专家",
    prompt: "从 API 获取数据并解析 JSON"
}

flow main {
    task = """
    1. GET https://api.example.com/users
    2. 解析返回的 JSON
    3. 提取第一个用户的 name 字段
    """;
    
    name = DataFetcher.run(task);
    print(f"第一个用户: {name}");
}
```

---

## 📊 版本历史

| 版本 | 更新内容 |
|-----|---------|
| v1.0 | 新增 `std.text`, `std.hash`, `std.math`, `std.regex` 命名空间 |
| v0.9.7 | 新增 `std.shell`, `std.ask_human` 命名空间 |
| v0.9 | 完善文件操作工具 (`append`, `delete`) |
| v0.8 | 新增 HTTP PUT/DELETE 方法 |
| v0.7 | 初始标准库发布 (`std.fs`, `std.http`, `std.time`) |

---

*最后更新: 2026-03-28 | 基于 Nexa v0.9.7-alpha / v1.0-alpha AVM*