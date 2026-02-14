# Comprehensive Logging Guide — Python & Java

---

## Table of Contents

1. [Logging Levels & Hierarchy](#1-logging-levels--hierarchy)
2. [Logging Format & Date Format](#2-logging-format--date-format)
3. [Handlers (Appenders)](#3-handlers-appenders)
4. [File Logging & Rotation](#4-file-logging--rotation)
5. [Multiple Loggers](#5-multiple-loggers)
6. [Logging Architecture Flow](#6-logging-architecture-flow)
7. [Java Logging APIs & Differences](#7-java-logging-apis--differences)
8. [Best Practices for Enterprise Applications](#8-best-practices-for-enterprise-applications)

---

## 1. Logging Levels & Hierarchy

The level you set acts as a **minimum threshold** — only messages at that level **or higher** get logged.

### Level Hierarchy (low → high)

```
DEBUG (10)  ←  Lowest severity (most verbose)
  ↓
INFO (20)
  ↓
WARNING (30)   ← Python default
  ↓
ERROR (40)
  ↓
CRITICAL (50)  ←  Highest severity
```

### Threshold Behavior

When you set a level, it logs **that level + everything above it**:

| Level Set To | DEBUG | INFO | WARNING | ERROR | CRITICAL |
|---|---|---|---|---|---|
| `DEBUG` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `INFO` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `WARNING` | ❌ | ❌ | ✅ | ✅ | ✅ |
| `ERROR` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `CRITICAL` | ❌ | ❌ | ❌ | ❌ | ✅ |

> **Rule:** Setting a level = *"I only care about messages this serious or more serious"*

### Python vs Java Level Names

| Python | Java (java.util.logging) | Java (Log4j/SLF4J) | Numeric (Python) |
|---|---|---|---|
| `DEBUG` | `FINE` / `FINER` / `FINEST` | `DEBUG` | 10 |
| `INFO` | `INFO` | `INFO` | 20 |
| `WARNING` | `WARNING` | `WARN` | 30 |
| `ERROR` | `SEVERE` | `ERROR` | 40 |
| `CRITICAL` | `SEVERE` | `FATAL` | 50 |

### Python Example

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.debug("This will NOT appear")      # 10 < 20 ❌
logging.info("This WILL appear")           # 20 >= 20 ✅
logging.warning("This WILL appear")        # 30 >= 20 ✅
logging.error("This WILL appear")          # 40 >= 20 ✅
logging.critical("This WILL appear")       # 50 >= 20 ✅
```

### Java Example (SLF4J + Logback)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class App {
    private static final Logger logger = LoggerFactory.getLogger(App.class);

    public static void main(String[] args) {
        logger.debug("This will NOT appear if level=INFO");
        logger.info("This WILL appear");
        logger.warn("This WILL appear");
        logger.error("This WILL appear");
    }
}
```

---

## 2. Logging Format & Date Format

### Python Format Attributes

The `format` parameter in `basicConfig` uses `%` placeholders called **LogRecord attributes**:

| Attribute | Meaning | Example Output |
|---|---|---|
| `%(asctime)s` | Timestamp | `2026-02-14 22:25:34` |
| `%(name)s` | Logger name | `root`, `myapp.module` |
| `%(levelname)s` | Level name | `INFO`, `ERROR` |
| `%(message)s` | The log message | `User logged in` |
| `%(filename)s` | Source file name | `app.py` |
| `%(lineno)d` | Line number | `42` |
| `%(funcName)s` | Function name | `process_order` |
| `%(module)s` | Module name | `app` |
| `%(pathname)s` | Full file path | `/src/app.py` |
| `%(process)d` | Process ID | `12345` |
| `%(thread)d` | Thread ID | `140735` |
| `%(threadName)s` | Thread name | `MainThread` |

### Python Format Examples

```python
# Basic format
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# Output: 2026-02-14 22:25:34,123 - INFO - User logged in

# Detailed format (good for debugging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
# Output: 2026-02-14 22:25:34,123 - myapp - ERROR - app.py:42 - Connection failed

# JSON format (good for log aggregation tools)
logging.basicConfig(
    format='{"time":"%(asctime)s", "level":"%(levelname)s", "logger":"%(name)s", "message":"%(message)s"}'
)
# Output: {"time":"2026-02-14 22:25:34", "level":"INFO", "logger":"root", "message":"User logged in"}
```

### Python Date Format (`datefmt`)

```python
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'          # 2026-02-14 22:25:34
)

# Other date format options:
# datefmt='%d/%m/%Y %I:%M:%S %p'         → 14/02/2026 10:25:34 PM
# datefmt='%Y-%m-%dT%H:%M:%S'            → 2026-02-14T22:25:34 (ISO 8601)
# datefmt='%b %d, %Y %H:%M:%S'           → Feb 14, 2026 22:25:34
```

### Java Logback Pattern (`logback.xml`)

```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <!-- Similar to Python's format string -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="CONSOLE" />
    </root>
</configuration>
```

### Java Pattern Tokens

| Token | Meaning | Python Equivalent |
|---|---|---|
| `%d{pattern}` | Date/time | `%(asctime)s` |
| `%level` / `%-5level` | Log level (padded) | `%(levelname)s` |
| `%logger{n}` | Logger name (abbreviated) | `%(name)s` |
| `%msg` | Message | `%(message)s` |
| `%thread` | Thread name | `%(threadName)s` |
| `%file` | File name | `%(filename)s` |
| `%line` | Line number | `%(lineno)d` |
| `%n` | Newline | (automatic in Python) |
| `%M` | Method name | `%(funcName)s` |

---

## 3. Handlers (Appenders)

Handlers control **where** log messages go. Python calls them **Handlers**, Java calls them **Appenders**.

### Handler Types Comparison

| Purpose | Python Handler | Java (Logback) Appender |
|---|---|---|
| Console output | `StreamHandler` | `ConsoleAppender` |
| Write to file | `FileHandler` | `FileAppender` |
| Rotating file (by size) | `RotatingFileHandler` | `RollingFileAppender` (size) |
| Rotating file (by time) | `TimedRotatingFileHandler` | `RollingFileAppender` (time) |
| Send via email | `SMTPHandler` | `SMTPAppender` |
| Send over network | `SocketHandler` | `SocketAppender` |
| System log | `SysLogHandler` | `SyslogAppender` |
| No output (discard) | `NullHandler` | `NOPAppender` |
| HTTP endpoint | `HTTPHandler` | `HttpAppender` |

### Python Handler Examples

#### StreamHandler (Console)

```python
import logging

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only INFO+ goes to console

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
```

#### FileHandler

```python
# File handler — writes to a file
file_handler = logging.FileHandler('app.log', mode='a')  # 'a' = append, 'w' = overwrite
file_handler.setLevel(logging.DEBUG)  # ALL levels go to file

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
```

#### FileHandler modes

| Mode | Behavior |
|---|---|
| `'a'` (append) | Adds to existing file — **preserves old logs** |
| `'w'` (write) | Overwrites file on each run — **old logs lost** |

#### Multiple Handlers (Console + File)

```python
import logging

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)  # Logger accepts everything

# Handler 1: Console — only WARNING+
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

# Handler 2: File — everything (DEBUG+)
file = logging.FileHandler('debug.log')
file.setLevel(logging.DEBUG)
file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'))

logger.addHandler(console)
logger.addHandler(file)

# Now:
logger.debug("Only in file")           # File ✅, Console ❌
logger.info("Only in file")            # File ✅, Console ❌
logger.warning("Both file & console")  # File ✅, Console ✅
logger.error("Both file & console")    # File ✅, Console ✅
```

### Java Logback — Multiple Appenders (`logback.xml`)

```xml
<configuration>
    <!-- Console Appender — WARNING+ only -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>WARN</level>
        </filter>
        <encoder>
            <pattern>%-5level - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- File Appender — DEBUG+ (everything) -->
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <file>debug.log</file>
        <append>true</append>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} - %-5level - %file:%line - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="DEBUG">
        <appender-ref ref="CONSOLE" />
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

---

## 4. File Logging & Rotation

### Why Rotation?

Without rotation, log files grow **forever** → fills disk → crashes server. Rotation manages log files by:
- **Size-based:** Create a new file when the current one exceeds a size limit
- **Time-based:** Create a new file every hour/day/week

### Python — RotatingFileHandler (Size-based)

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'app.log',
    maxBytes=5*1024*1024,  # 5 MB per file
    backupCount=5          # Keep 5 old files (app.log.1, app.log.2, ... app.log.5)
)
```

**Resulting files:**
```
app.log       ← Current (newest)
app.log.1     ← Previous
app.log.2     ← Older
app.log.3     ← Older
app.log.4     ← Older
app.log.5     ← Oldest (gets deleted when new rotation happens)
```

### Python — TimedRotatingFileHandler (Time-based)

```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    'app.log',
    when='midnight',   # Rotate at midnight
    interval=1,        # Every 1 day
    backupCount=30     # Keep 30 days of logs
)
handler.suffix = "%Y-%m-%d"  # File naming: app.log.2026-02-14
```

| `when` value | Rotation interval |
|---|---|
| `'S'` | Every second |
| `'M'` | Every minute |
| `'H'` | Every hour |
| `'D'` | Every day |
| `'midnight'` | At midnight |
| `'W0'`–`'W6'` | Every week (Mon=0, Sun=6) |

### Java Logback — RollingFileAppender

```xml
<!-- Size-based rotation -->
<appender name="ROLLING" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>app.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
        <fileNamePattern>app.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
        <maxFileSize>10MB</maxFileSize>     <!-- Max size per file -->
        <maxHistory>30</maxHistory>          <!-- Keep 30 days -->
        <totalSizeCap>1GB</totalSizeCap>    <!-- Total max storage -->
    </rollingPolicy>
    <encoder>
        <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
</appender>
```

---

## 5. Multiple Loggers

### Python — Logger per Module

```python
# ── auth.py ──
import logging
logger = logging.getLogger('myapp.auth')  # Child of 'myapp'

def login(user):
    logger.info(f"User {user} logged in")

# ── database.py ──
import logging
logger = logging.getLogger('myapp.database')  # Child of 'myapp'

def query(sql):
    logger.debug(f"Executing: {sql}")
```

### Logger Name Hierarchy

```
root                    ← Top-level (logging.getLogger())
 └── myapp              ← logging.getLogger('myapp')
      ├── myapp.auth    ← logging.getLogger('myapp.auth')
      └── myapp.db      ← logging.getLogger('myapp.db')
```

> Child loggers **propagate** messages to parent loggers by default. Set `logger.propagate = False` to stop this.

### Java — Logger per Class

```java
// In every class, create a logger named after the class
public class AuthService {
    private static final Logger logger = LoggerFactory.getLogger(AuthService.class);
    // Logger name becomes: "com.myapp.AuthService"
}
```

---

## 6. Logging Architecture Flow

### Python Logging Flow

```
Your Code
    │
    ▼
┌──────────┐    "logger.info('message')"
│  Logger  │    ← Has a level (e.g., DEBUG)
└────┬─────┘
     │  Is message level >= logger level?
     │  NO → message discarded
     │  YES ↓
     ▼
┌──────────┐
│ Filter   │    ← Optional: extra filtering logic
└────┬─────┘
     │  Passed filter?
     │  NO → message discarded
     │  YES ↓
     ▼
┌──────────────────────┐
│ Handler 1            │    ← Has its OWN level (e.g., WARNING)
│ (StreamHandler)      │    Is message level >= handler level?
│   └── Formatter      │    YES → format message → output to console
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Handler 2            │    ← Has its OWN level (e.g., DEBUG)
│ (FileHandler)        │    Is message level >= handler level?
│   └── Formatter      │    YES → format message → write to file
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Propagate to Parent? │    ← logger.propagate = True (default)
│ YES → send to parent │    Parent logger's handlers also process it
│ NO  → stop here      │
└──────────────────────┘
```

**Key insight:** A message must pass **two** level checks:
1. The **Logger's** level (gatekeeper)
2. Each **Handler's** level (individual filter)

### Java Logback Flow

```
Your Code
    │
    ▼
┌──────────────────┐    logger.info("message")
│  Logger           │   ← Has an effective level
│  (per class)      │   Level check: is INFO >= effective level?
└────┬─────────────┘
     │  YES ↓
     ▼
┌──────────────────┐
│  Turbo Filter    │    ← Global filter (before logger, Logback-specific)
└────┬─────────────┘
     │  YES ↓
     ▼
┌──────────────────┐
│  Appender 1      │    ← ConsoleAppender
│  ├── Filter      │    ← Per-appender filter (ThresholdFilter, etc.)
│  └── Encoder     │    ← Formats the message (like Python's Formatter)
└──────────────────┘
     │
     ▼
┌──────────────────┐
│  Appender 2      │    ← FileAppender / RollingFileAppender
│  ├── Filter      │
│  └── Encoder     │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│  Additivity?     │    ← Like Python's propagate
│  true → parent   │    Parent logger's appenders also process it
│  false → stop    │
└──────────────────┘
```

---

## 7. Java Logging APIs & Differences

Java has **multiple** logging frameworks (unlike Python which has one built-in). Here's how they compare:

### Overview of Java Logging APIs

| API | Type | Year | Key Notes |
|---|---|---|---|
| **java.util.logging (JUL)** | Built-in JDK | 2002 | No external dependency, limited features |
| **Log4j 1.x** | Library | 2001 | First popular framework, now **EOL** |
| **Log4j 2.x** | Library | 2014 | Complete rewrite, high performance, async |
| **SLF4J** | **Facade** (API only) | 2005 | Just an interface, needs a backend |
| **Logback** | Library (SLF4J backend) | 2006 | Default SLF4J implementation, by same author |
| **Commons Logging (JCL)** | Facade | 2002 | Older facade, mostly replaced by SLF4J |

### What is a Facade vs Implementation?

```
┌─────────────────────────────────────────────┐
│              YOUR APPLICATION CODE          │
│         logger.info("User logged in")       │
└──────────────────┬──────────────────────────┘
                   │
          ┌────────▼────────┐
          │   SLF4J (Facade) │  ← Your code talks to this API
          │   (Interface)    │  ← Just defines methods: info(), debug(), etc.
          └────────┬────────┘
                   │  Bound at runtime to ONE of these:
        ┌──────────┼──────────────┐
        ▼          ▼              ▼
   ┌─────────┐ ┌──────────┐ ┌──────────┐
   │ Logback │ │ Log4j 2  │ │   JUL    │
   │ (impl)  │ │ (impl)   │ │ (impl)   │
   └─────────┘ └──────────┘ └──────────┘
```

> **SLF4J** = *Simple Logging Facade for Java*. You code against SLF4J, and swap the backend without changing code.

### Detailed Comparison

#### 1. java.util.logging (JUL)

```java
import java.util.logging.Logger;
import java.util.logging.Level;
import java.util.logging.FileHandler;
import java.util.logging.SimpleFormatter;

public class JulExample {
    private static final Logger logger = Logger.getLogger(JulExample.class.getName());

    public static void main(String[] args) throws Exception {
        FileHandler fh = new FileHandler("app.log", true);
        fh.setFormatter(new SimpleFormatter());
        logger.addHandler(fh);

        logger.info("Application started");
        logger.warning("Low memory");
        logger.severe("Critical failure");     // JUL uses SEVERE, not ERROR
    }
}
```

**Pros:** No external dependency (part of JDK)
**Cons:** Clunky API, poor performance, limited formatters, no SLF4J support by default

#### 2. Log4j 2

```java
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Log4j2Example {
    private static final Logger logger = LogManager.getLogger(Log4j2Example.class);

    public static void main(String[] args) {
        logger.debug("Debug message");
        logger.info("Info message");
        logger.error("Error message");
        logger.fatal("Fatal message");         // Log4j has FATAL level
    }
}
```

Config (`log4j2.xml`):
```xml
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss} [%t] %-5level %logger{36} - %msg%n"/>
        </Console>
        <RollingFile name="File" fileName="app.log"
                     filePattern="app-%d{yyyy-MM-dd}-%i.log">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss} %-5level %logger{36} - %msg%n"/>
            <Policies>
                <SizeBasedTriggeringPolicy size="10MB"/>
            </Policies>
        </RollingFile>
    </Appenders>
    <Loggers>
        <Root level="info">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="File"/>
        </Root>
    </Loggers>
</Configuration>
```

**Pros:** Async logging (very fast), garbage-free, rich plugin system, lambda support
**Cons:** External dependency, complex config

#### 3. SLF4J + Logback (Recommended)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Slf4jExample {
    private static final Logger logger = LoggerFactory.getLogger(Slf4jExample.class);

    public static void main(String[] args) {
        logger.debug("Debug message");
        logger.info("User {} logged in from {}", username, ipAddress);  // Parameterized
        logger.error("Failed to process order", exception);  // Exception as last arg
    }
}
```

**Pros:** Clean API, parameterized messages (no string concat), swap backends easily
**Cons:** SLF4J is just a facade, you still need Logback/Log4j2 as implementation

### Feature Comparison Table

| Feature | JUL | Log4j 2 | SLF4J + Logback |
|---|---|---|---|
| **External dependency** | None (JDK) | Yes | Yes |
| **Performance** | 🔴 Slow | 🟢 Fastest (async) | 🟡 Good |
| **Parameterized logging** | ❌ | ✅ | ✅ |
| **Async logging** | ❌ | ✅ (built-in) | ✅ (with AsyncAppender) |
| **Rolling file** | Limited | ✅ Rich | ✅ Rich |
| **JSON output** | ❌ | ✅ | ✅ |
| **MDC (context)** | ❌ | ✅ | ✅ |
| **Config hot-reload** | ❌ | ✅ | ✅ |
| **Lambda support** | ❌ | ✅ `logger.debug(() -> expensiveOp())` | ❌ |
| **Spring Boot default** | ❌ | ❌ | ✅ |

### What is MDC (Mapped Diagnostic Context)?

MDC lets you attach **context data** (like user ID, request ID) to every log message in a thread:

```java
// Java (SLF4J)
MDC.put("userId", "user123");
MDC.put("requestId", "req-abc-456");

logger.info("Order processed");
// Output: 2026-02-14 22:25:34 [userId=user123, requestId=req-abc-456] INFO - Order processed

MDC.clear(); // Clean up after request
```

```python
# Python equivalent — using LoggerAdapter or Filter
import logging

extra = {'userId': 'user123', 'requestId': 'req-abc-456'}
logging.basicConfig(format='%(asctime)s [userId=%(userId)s] %(levelname)s - %(message)s')
logger = logging.LoggerAdapter(logging.getLogger(), extra)
logger.info("Order processed")
```

### Which Java API Should You Use?

```
Are you starting a new project?
    │
    ├── YES → Use SLF4J + Logback (industry standard)
    │         Spring Boot uses this by default
    │
    └── NO → What does the existing project use?
              │
              ├── Log4j 1.x → Migrate to SLF4J + Logback or Log4j 2 (Log4j 1 is EOL)
              ├── Log4j 2 → Keep it, it's excellent
              ├── JUL → Consider migrating to SLF4J (use jul-to-slf4j bridge)
              └── SLF4J + Logback → You're already on the recommended stack ✅
```

---

## 8. Best Practices for Enterprise Applications

### ✅ DO

#### 1. Use Structured Logging (JSON)
Log aggregation tools (ELK, Splunk, Datadog) parse JSON easily:

```python
# Python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)
```

```xml
<!-- Java (Logback with logstash-logback-encoder) -->
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder" />
</appender>
```

#### 2. Use Parameterized Messages (Avoid String Concatenation)

```python
# ❌ BAD — string is always built, even if DEBUG is disabled
logger.debug("Processing order " + order_id + " for user " + user_id)

# ✅ GOOD — string is only built if DEBUG is enabled
logger.debug("Processing order %s for user %s", order_id, user_id)

# ✅ ALSO GOOD (Python 3.12+ or f-string with lazy eval)
logger.debug(f"Processing order {order_id} for user {user_id}")
```

```java
// ❌ BAD
logger.debug("Processing order " + orderId + " for user " + userId);

// ✅ GOOD — SLF4J parameterized
logger.debug("Processing order {} for user {}", orderId, userId);
```

#### 3. Log at the Right Level

| Level | When to use |
|---|---|
| **DEBUG** | Detailed internal state, variable values, flow tracing |
| **INFO** | Significant business events: user login, order placed, job started |
| **WARNING** | Something unexpected but recoverable: retry, fallback used |
| **ERROR** | Operation failed but app continues: API call failed, DB timeout |
| **CRITICAL** | App is about to crash: out of memory, config missing |

#### 4. Include Context in Every Log

```python
# ❌ BAD
logger.error("Failed to process order")

# ✅ GOOD — includes WHO, WHAT, and WHY
logger.error("Failed to process order=%s for user=%s: %s", order_id, user_id, str(error))
```

#### 5. Always Log Exceptions with Stack Traces

```python
try:
    process_order(order_id)
except Exception as e:
    logger.error("Failed to process order=%s", order_id, exc_info=True)  # Includes traceback
```

```java
try {
    processOrder(orderId);
} catch (Exception e) {
    logger.error("Failed to process order={}", orderId, e);  // Exception as last arg
}
```

#### 6. Use Log Rotation in Production

```python
# Never use a single ever-growing log file in production
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=10)
```

#### 7. Use Correlation IDs for Distributed Systems

```python
import uuid

request_id = str(uuid.uuid4())
logger.info("Request started", extra={"request_id": request_id})
# Pass request_id to all downstream services
# Every service logs with the same request_id → easy tracing
```

#### 8. Separate Log Files by Purpose

```
logs/
├── app.log           ← General application logs
├── error.log         ← Only ERROR and CRITICAL
├── access.log        ← HTTP request/response logs
├── audit.log         ← Security/compliance events
└── performance.log   ← Slow queries, latency metrics
```

### ❌ DON'T

| Don't | Why |
|---|---|
| Log sensitive data (passwords, tokens, PII) | Security risk, compliance violation (GDPR) |
| Use `print()` instead of logging | No levels, no rotation, no formatting |
| Log inside tight loops | Performance killer, fills disk |
| Use `logging.basicConfig()` in libraries | Overrides the app's config; use `NullHandler` instead |
| Catch and log exceptions then re-raise | Causes duplicate log entries |
| Log at the wrong level (`logger.info("Error occurred")`) | Makes filtering useless |

### Production Logging Configuration Example

```python
import logging
import logging.handlers
import json
import os

def setup_logging(log_dir='logs', level=logging.INFO):
    os.makedirs(log_dir, exist_ok=True)

    # Root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Format
    detailed = logging.Formatter(
        '%(asctime)s [%(process)d] [%(threadName)s] %(name)s %(levelname)s %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console — INFO+
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter('%(levelname)-8s %(name)s - %(message)s'))
    root.addHandler(console)

    # App log — rotating, DEBUG+
    app_handler = logging.handlers.RotatingFileHandler(
        f'{log_dir}/app.log', maxBytes=10*1024*1024, backupCount=10
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(detailed)
    root.addHandler(app_handler)

    # Error log — rotating, ERROR+ only
    error_handler = logging.handlers.RotatingFileHandler(
        f'{log_dir}/error.log', maxBytes=10*1024*1024, backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed)
    root.addHandler(error_handler)

# Usage
setup_logging()
logger = logging.getLogger('myapp')
logger.info("Application started")
```
