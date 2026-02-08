# Python String to Binary Conversion

In Python, you can convert a string to binary using several methods. Here are the most common approaches:

## 1. Using `encode()` Method (Most Common)

Converts string to bytes (binary representation):

```python
text = "Hello"
binary = text.encode()  # Default: UTF-8 encoding
print(binary)  # b'Hello'
print(type(binary))  # <class 'bytes'>

# Specify encoding explicitly
binary_utf8 = text.encode('utf-8')
binary_ascii = text.encode('ascii')
```

## 2. Binary String Representation (0s and 1s)

Converts each character to its binary representation:

```python
text = "Hello"

# Method 1: Using format()
binary_string = ' '.join(format(ord(char), '08b') for char in text)
print(binary_string)
# Output: 01001000 01100101 01101100 01101100 01101111

# Method 2: Using bin()
binary_list = [bin(ord(char))[2:].zfill(8) for char in text]
print(' '.join(binary_list))
# Output: 01001000 01100101 01101100 01101100 01101111
```

## 3. Using `bytes()` Function

```python
text = "Hello"
binary = bytes(text, 'utf-8')
print(binary)  # b'Hello'
```

## Complete Examples

```python
# Example 1: String to bytes
text = "Hello world!"
binary_data = text.encode('utf-8')
print(f"Original: {text}")
print(f"Binary: {binary_data}")
print(f"Type: {type(binary_data)}")

# Example 2: String to binary representation (0s and 1s)
def string_to_binary(text):
    """Convert string to binary representation"""
    return ' '.join(format(ord(char), '08b') for char in text)

text = "Hi"
binary_repr = string_to_binary(text)
print(f"Text: {text}")
print(f"Binary: {binary_repr}")
# Output: 01001000 01101001

# Example 3: Binary back to string
binary_data = b'Hello'
original_text = binary_data.decode('utf-8')
print(f"Decoded: {original_text}")  # Hello

# Example 4: Binary string (0s and 1s) back to text
def binary_to_string(binary_str):
    """Convert binary representation back to string"""
    binary_values = binary_str.split()
    ascii_chars = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_chars)

binary = "01001000 01101001"
text = binary_to_string(binary)
print(f"Decoded: {text}")  # Hi
```

## Quick Reference

| Method | Use Case | Output |
|--------|----------|--------|
| `str.encode()` | Convert to bytes for file I/O, network | `b'Hello'` |
| `format(ord(char), '08b')` | Visual binary representation | `'01001000'` |
| `bin(ord(char))` | Binary with '0b' prefix | `'0b1001000'` |
| `bytes(str, encoding)` | Alternative to encode() | `b'Hello'` |

## Common Use Cases

```python
# Writing binary data to file
text = "Hello world!"
with open('example.bin', 'wb') as f:  # 'wb' = write binary
    f.write(text.encode('utf-8'))

# Reading binary data from file
with open('example.bin', 'rb') as f:  # 'rb' = read binary
    binary_data = f.read()
    text = binary_data.decode('utf-8')
    print(text)  # Hello world!
```

## Key Points

> [!IMPORTANT]
> - `encode()` is the standard way to convert string to bytes
> - Use `'08b'` format for 8-bit binary representation
> - `decode()` converts bytes back to string
> - Default encoding is UTF-8 (recommended)

## Explanation of Key Functions

- **`ord(char)`** - Returns the Unicode code point of a character (e.g., `ord('A')` = 65)
- **`format(num, '08b')`** - Formats number as 8-bit binary string with leading zeros
- **`bin(num)`** - Converts number to binary string with '0b' prefix
- **`chr(num)`** - Converts Unicode code point back to character
- **`int(binary_str, 2)`** - Converts binary string to integer (base 2)
