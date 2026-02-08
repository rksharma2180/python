# The `else` Block in Try-Except

The `else` block in a try-except statement is **optional** and executes **only if no exception occurs** in the `try` block.

## Purpose of `else` Block

The `else` block is used to:
- ✅ Execute code that should run **only when the try block succeeds**
- ✅ Separate error-prone code (in `try`) from success-handling code (in `else`)
- ✅ Make code more readable and explicit about what happens on success

## Basic Syntax

```python
try:
    # Code that might raise an exception
    risky_operation()
except ExceptionType:
    # Runs if exception occurs
    handle_error()
else:
    # Runs ONLY if no exception occurred
    success_code()
finally:
    # Always runs (optional)
    cleanup_code()
```

## Examples

### Example 1: File Reading

```python
filename = "data.txt"

try:
    file = open(filename, 'r')
except FileNotFoundError:
    print(f"Error: {filename} not found")
else:
    # This runs ONLY if file opened successfully
    content = file.read()
    print(f"File content: {content}")
    file.close()
    print("File read successfully!")
```

### Example 2: Number Conversion

```python
user_input = input("Enter a number: ")

try:
    number = int(user_input)
except ValueError:
    print("Invalid input! Please enter a valid number.")
else:
    # Runs only if conversion succeeded
    print(f"You entered: {number}")
    print(f"Double of your number: {number * 2}")
```

### Example 3: Division Calculator

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    except TypeError:
        print("Error: Please provide numbers only!")
    else:
        # Runs only if division succeeded
        print(f"Division successful!")
        print(f"{a} / {b} = {result}")
        return result

# Test cases
divide(10, 2)   # else block runs
divide(10, 0)   # except block runs, else skipped
divide(10, "a") # except block runs, else skipped
```

### Example 4: With `finally` Block

```python
def read_file(filename):
    file = None
    try:
        file = open(filename, 'r')
        data = file.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
    except PermissionError:
        print(f"No permission to read {filename}")
    else:
        # Runs only if file read successfully
        print("File read successfully!")
        print(f"Content length: {len(data)} characters")
        return data
    finally:
        # Always runs, whether exception occurred or not
        if file:
            file.close()
            print("File closed")

# Usage
content = read_file("data.txt")
```

### Example 5: User Input Validation

```python
def get_age():
    try:
        age = int(input("Enter your age: "))
        
        # Additional validation
        if age < 0:
            raise ValueError("Age cannot be negative")
        if age > 150:
            raise ValueError("Age seems unrealistic")
            
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None
    else:
        # Runs only if input is valid
        print("Age validated successfully!")
        if age >= 18:
            print("You are an adult")
        else:
            print("You are a minor")
        return age

# Usage
user_age = get_age()
```

## Why Use `else` Instead of Putting Code in `try`?

### ❌ Bad Practice: Everything in try block

```python
try:
    number = int(input("Enter number: "))
    # These shouldn't be in try block
    result = number * 2
    print(f"Result: {result}")
except ValueError:
    print("Invalid number")
```

**Problem:** If `print()` raises an exception, it will be caught incorrectly.

### ✅ Good Practice: Use else block

```python
try:
    number = int(input("Enter number: "))
except ValueError:
    print("Invalid number")
else:
    # Only runs if conversion succeeded
    result = number * 2
    print(f"Result: {result}")
```

**Benefit:** Only the risky operation is in `try`, success code is in `else`.

## Complete Flow Example

```python
def process_data(data):
    try:
        # Risky operation
        value = int(data)
        print("Conversion successful")
    except ValueError:
        # Runs if exception occurs
        print("Conversion failed")
    else:
        # Runs ONLY if no exception
        print("Processing the converted value...")
        result = value ** 2
        print(f"Result: {result}")
    finally:
        # Always runs
        print("Process completed")

# Test cases
print("Test 1:")
process_data("10")
# Output:
# Conversion successful
# Processing the converted value...
# Result: 100
# Process completed

print("\nTest 2:")
process_data("abc")
# Output:
# Conversion failed
# Process completed
```

## Execution Flow Summary

| Block | When It Runs |
|-------|-------------|
| `try` | Always executed first |
| `except` | Only if exception occurs in `try` |
| `else` | Only if NO exception occurs in `try` |
| `finally` | Always runs, regardless of exceptions |

## Key Points

> [!IMPORTANT]
> - `else` block runs **ONLY if no exception occurs** in the `try` block
> - `else` block is **skipped** if any exception is raised
> - `else` block runs **before** the `finally` block
> - Use `else` to keep the `try` block minimal (only risky code)

> [!TIP]
> **Best Practice:** Keep only the code that might raise exceptions in the `try` block, and put the success-handling code in the `else` block. This makes your code cleaner and prevents accidentally catching unintended exceptions.

## Real-World Use Case

```python
def process_user_data(user_id):
    """Fetch and process user data from database"""
    try:
        # Risky operation - database query
        user_data = fetch_from_database(user_id)
    except DatabaseError as e:
        print(f"Database error: {e}")
        return None
    except ConnectionError as e:
        print(f"Connection error: {e}")
        return None
    else:
        # Only runs if database fetch succeeded
        # Process the data safely
        processed_data = transform_data(user_data)
        save_to_cache(processed_data)
        log_success(user_id)
        return processed_data
    finally:
        # Cleanup - close database connection
        close_database_connection()
```

This pattern ensures that data processing only happens when the database fetch succeeds, and cleanup always happens regardless of success or failure.
