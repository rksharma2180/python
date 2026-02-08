# Python File Modes

Python provides several file modes for different operations when working with files.

## Basic File Modes

| Mode | Name | Description |
|------|------|-------------|
| `'r'` | Read | Opens file for reading (default). File must exist. |
| `'w'` | Write | Opens file for writing. Creates new file or **truncates** existing file. |
| `'a'` | Append | Opens file for writing. Creates new file or appends to existing file. |
| `'x'` | Exclusive Create | Creates new file. **Fails if file exists**. |

## Binary Mode Modifier

Add `'b'` to work with binary files (images, videos, PDFs, etc.):

| Mode | Description |
|------|-------------|
| `'rb'` | Read binary |
| `'wb'` | Write binary |
| `'ab'` | Append binary |
| `'xb'` | Exclusive create binary |

## Read + Write Modes

Add `'+'` for simultaneous read and write:

| Mode | Description |
|------|-------------|
| `'r+'` | Read and write. File must exist. Pointer at start. |
| `'w+'` | Read and write. **Truncates** existing file or creates new. |
| `'a+'` | Read and append. Creates new or appends. Pointer at end. |
| `'x+'` | Read and write. Creates new file. Fails if exists. |

## Combined Binary + Read/Write

| Mode | Description |
|------|-------------|
| `'rb+'` or `'r+b'` | Read and write binary |
| `'wb+'` or `'w+b'` | Write and read binary (truncates) |
| `'ab+'` or `'a+b'` | Append and read binary |
| `'xb+'` or `'x+b'` | Exclusive create binary with read |

## Examples

```python
# Read mode (default)
with open('file.txt', 'r') as f:
    content = f.read()

# Write mode (overwrites existing content!)
with open('file.txt', 'w') as f:
    f.write('New content')

# Append mode (adds to end)
with open('file.txt', 'a') as f:
    f.write('\nAppended line')

# Exclusive create (fails if exists)
with open('newfile.txt', 'x') as f:
    f.write('Only if file doesn\'t exist')

# Binary read (for images, PDFs, etc.)
with open('image.png', 'rb') as f:
    binary_data = f.read()

# Read and write
with open('file.txt', 'r+') as f:
    content = f.read()
    f.write('\nAdded text')
```

## Quick Reference Table

| Mode | Read | Write | Create | Truncate | Pointer Position |
|------|------|-------|--------|----------|------------------|
| `r` | ✅ | ❌ | ❌ | ❌ | Start |
| `r+` | ✅ | ✅ | ❌ | ❌ | Start |
| `w` | ❌ | ✅ | ✅ | ✅ | Start |
| `w+` | ✅ | ✅ | ✅ | ✅ | Start |
| `a` | ❌ | ✅ | ✅ | ❌ | End |
| `a+` | ✅ | ✅ | ✅ | ❌ | End |
| `x` | ❌ | ✅ | ✅ (only if new) | ❌ | Start |
| `x+` | ✅ | ✅ | ✅ (only if new) | ❌ | Start |

## Important Notes

> [!WARNING]
> **`'w'` mode is destructive** - it erases existing file content!

> [!TIP]
> **`'a'` mode is safe** - it only adds to the end

> [!NOTE]
> **`'x'` mode is safe** - it prevents accidental overwrites

> [!IMPORTANT]
> **Default mode is `'r'`** - if you omit the mode parameter
