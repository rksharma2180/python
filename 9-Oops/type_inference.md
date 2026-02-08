# Type Inference and Dynamic Typing in Python

## How Python Handles Types

Python is a **dynamically typed** language, which means:
- Variables don't have fixed types
- Type is determined at **runtime** based on the assigned value
- The same variable can hold different types at different times

### Key Concept: No Type Inference, Just Dynamic Typing

Python doesn't "infer" types in the traditional sense (like TypeScript or Kotlin). Instead, it **determines the type at runtime** based on the object assigned to a variable.

```python
# Python doesn't infer - it assigns the type of the object
x = 5           # x now references an int object
print(type(x))  # <class 'int'>

x = "hello"     # x now references a str object
print(type(x))  # <class 'str'>

x = [1, 2, 3]   # x now references a list object
print(type(x))  # <class 'list'>
```

---

## How Python Identifies Types

### The Truth: Variables Don't Have Types, Objects Do

```python
# The variable 'x' is just a name (reference)
# The object 5 has the type 'int'
x = 5

# What actually happens:
# 1. Python creates an int object with value 5
# 2. Python binds the name 'x' to that object
# 3. The type belongs to the object, not the variable
```

### Visualizing References

```python
a = 42
b = a

# Both 'a' and 'b' reference the same int object
print(id(a))  # Memory address
print(id(b))  # Same memory address
print(a is b) # True - same object

# When you reassign:
a = 100

# Now 'a' references a different object
print(id(a))  # Different memory address
print(id(b))  # Still the old address
print(a is b) # False - different objects
```

---

## Type Determination at Different Levels

### 1. Module-Level Variables

```python
# module.py

# Type determined when assigned
MODULE_CONSTANT = 100        # int
module_var = "hello"         # str
module_list = [1, 2, 3]      # list

# Can be reassigned to different types
module_var = 42              # Now int
module_var = {"key": "val"}  # Now dict

print(type(MODULE_CONSTANT))  # <class 'int'>
print(type(module_var))       # <class 'dict'>
```

### 2. Class-Level Variables

```python
class MyClass:
    # Class variable - type determined at class definition
    class_var = "I'm a string"  # str
    count = 0                   # int
    
    def __init__(self):
        # Instance variable - type determined when object created
        self.instance_var = 42  # int
    
    def method(self):
        # Can access and check types
        print(type(self.class_var))      # <class 'str'>
        print(type(self.instance_var))   # <class 'int'>

# Class variable type
print(type(MyClass.class_var))  # <class 'str'>

# Instance variable type
obj = MyClass()
print(type(obj.instance_var))   # <class 'int'>
```

### 3. Method/Function Local Variables

```python
def my_function():
    # Local variable - type determined when assigned
    local_var = "hello"
    print(type(local_var))  # <class 'str'>
    
    # Can change type
    local_var = 123
    print(type(local_var))  # <class 'int'>
    
    return local_var

result = my_function()
print(type(result))  # <class 'int'>
```

### 4. Function Parameters

```python
def process(param):
    # Type determined by what's passed at runtime
    print(f"Type of param: {type(param)}")
    return param

# Different types can be passed
process(42)           # <class 'int'>
process("hello")      # <class 'str'>
process([1, 2, 3])    # <class 'list'>
process(MyClass())    # <class '__main__.MyClass'>
```

---

## Runtime Type Checking

### Using `type()`

```python
x = 42
print(type(x))           # <class 'int'>
print(type(x).__name__)  # 'int'

# Check exact type
if type(x) == int:
    print("x is an int")
```

### Using `isinstance()`

```python
x = 42

# Better than type() - handles inheritance
print(isinstance(x, int))     # True
print(isinstance(x, object))  # True (everything inherits from object)

# Check multiple types
print(isinstance(x, (int, str, float)))  # True
```

### Type Checking in Functions

```python
def add(a, b):
    # Runtime type checking
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a + b

print(add(5, 3))      # 8
# add("5", "3")       # TypeError
```

---

## How Python Determines Type at Runtime

### Step-by-Step Process

```python
x = 42

# What Python does internally:
# 1. Create an int object with value 42
# 2. The int object has a __class__ attribute pointing to the int type
# 3. Bind the name 'x' to this object
# 4. When you call type(x), Python returns x.__class__
```

### Demonstrating `__class__`

```python
x = 42
print(x.__class__)           # <class 'int'>
print(x.__class__.__name__)  # 'int'
print(type(x) is x.__class__) # True

# Every object knows its type
s = "hello"
print(s.__class__)  # <class 'str'>

lst = [1, 2, 3]
print(lst.__class__)  # <class 'list'>
```

---

## Type Annotations (Hints) - Python 3.5+

### Type Hints Don't Enforce Types

```python
# Type hints are just suggestions - not enforced at runtime
def greet(name: str) -> str:
    return f"Hello, {name}"

# This works even though we passed an int!
result = greet(42)
print(result)  # Hello, 42

# Type is still determined at runtime
print(type(result))  # <class 'str'>
```

### Type Hints for Variables

```python
# Variable annotations (Python 3.6+)
age: int = 25
name: str = "Alice"
scores: list[int] = [90, 85, 95]

# But you can still assign wrong types - no runtime enforcement
age = "twenty-five"  # No error!
print(type(age))     # <class 'str'>
```

### Using Type Checkers (External Tools)

```python
# mypy, pyright, etc. can check types statically
def add(a: int, b: int) -> int:
    return a + b

# mypy will warn about this, but Python won't
result = add("5", "3")  # Python runs it, mypy complains
```

---

## Practical Examples

### Example 1: Polymorphic Function

```python
def process_data(data):
    # Type determined at runtime
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, list):
        return [x * 2 for x in data]
    elif isinstance(data, int):
        return data ** 2
    else:
        return None

print(process_data("hello"))    # HELLO
print(process_data([1, 2, 3]))  # [2, 4, 6]
print(process_data(5))          # 25
```

### Example 2: Class with Mixed Types

```python
class DataContainer:
    # Class variable
    default_value = None  # NoneType initially
    
    def __init__(self, value):
        # Instance variable - type depends on argument
        self.value = value
        
        # Type determined at runtime
        if isinstance(value, str):
            self.value_type = "string"
        elif isinstance(value, int):
            self.value_type = "integer"
        else:
            self.value_type = "other"
    
    def get_info(self):
        return f"Value: {self.value}, Type: {type(self.value).__name__}"

# Different instances, different types
container1 = DataContainer("hello")
container2 = DataContainer(42)
container3 = DataContainer([1, 2, 3])

print(container1.get_info())  # Value: hello, Type: str
print(container2.get_info())  # Value: 42, Type: int
print(container3.get_info())  # Value: [1, 2, 3], Type: list
```

### Example 3: Type Changes During Execution

```python
class Calculator:
    def __init__(self):
        self.result = 0  # int initially
    
    def add(self, value):
        self.result = self.result + value
        print(f"Result type: {type(self.result)}")
        return self.result

calc = Calculator()
calc.add(5)       # Result type: <class 'int'>
calc.add(3.5)     # Result type: <class 'float'> - type changed!
calc.add(2)       # Result type: <class 'float'> - stays float
```

---

## Comparison: Python vs Statically Typed Languages

### Java (Static Typing)

```java
// Java - type declared at compile time
int x = 5;           // x is ALWAYS an int
// x = "hello";      // Compile error!

String name = "Alice";
// name = 42;        // Compile error!
```

### Python (Dynamic Typing)

```python
# Python - type determined at runtime
x = 5           # x references an int object
x = "hello"     # x now references a str object - no problem!

name = "Alice"
name = 42       # Totally fine in Python
```

### TypeScript (Type Inference)

```typescript
// TypeScript - infers type from initial value
let x = 5;      // Inferred as number
// x = "hello"; // Error - type is locked to number

// Python doesn't lock types like this
```

---

## Summary

### How Python Identifies Types

1. **Objects have types, not variables**
   - Variables are just names/references
   - Type belongs to the object being referenced

2. **Type determined at runtime**
   - When object is created/assigned
   - Can change when variable is reassigned

3. **No type declaration needed**
   - Type is implicit from the value
   - Same variable can hold different types

4. **Type checking happens at runtime**
   - Use `type()` or `isinstance()`
   - No compile-time type checking (unless using external tools)

### At Different Levels

| Level | When Type Determined |
|-------|---------------------|
| **Module-level** | When module is loaded/executed |
| **Class-level** | When class is defined |
| **Instance-level** | When object is created |
| **Local variables** | When assigned in function |
| **Parameters** | When function is called |

### Key Differences from Static Languages

- **Python**: Type determined at runtime (dynamic)
- **Java/C++**: Type declared at compile time (static)
- **TypeScript**: Type inferred but locked (static with inference)
- **Python**: Variables can change types freely

### Type Hints (Optional)

- Introduced in Python 3.5+
- **Not enforced at runtime**
- Used by external tools (mypy, pyright)
- Improve code documentation and IDE support
- Don't affect Python's runtime behavior

### Best Practices

✅ Use `isinstance()` for type checking (handles inheritance)  
✅ Use type hints for documentation and tooling  
✅ Remember: types belong to objects, not variables  
✅ Embrace duck typing when appropriate  
✅ Use type checkers (mypy) for large projects
