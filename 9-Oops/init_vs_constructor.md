# Why `__init__` is Called an Initializer, Not a Constructor

## The Key Distinction

In Python, **object creation** and **object initialization** are two separate steps handled by different methods:

1. **`__new__`** - The actual **constructor** (creates the object)
2. **`__init__`** - The **initializer** (initializes the object)

This is different from many other programming languages where a single constructor does both jobs.

---

## How Object Creation Actually Works

When you create an object in Python, two methods are called in sequence:

```python
class Person:
    def __new__(cls, *args, **kwargs):
        print("1. __new__ called - CREATING the object")
        instance = super().__new__(cls)
        print(f"2. Object created: {instance}")
        return instance
    
    def __init__(self, name, age):
        print("3. __init__ called - INITIALIZING the object")
        self.name = name
        self.age = age
        print("4. Object initialized")

person = Person("Alice", 25)
```

**Output:**
```
1. __new__ called - CREATING the object
2. Object created: <__main__.Person object at 0x7f8b1c3d4e50>
3. __init__ called - INITIALIZING the object
4. Object initialized
```

---

## The Internal Process

When you write:
```python
person = Person("Alice", 25)
```

Python internally does this:

```python
# Step 1: __new__ creates the empty object (CONSTRUCTION)
instance = Person.__new__(Person, "Alice", 25)

# Step 2: __init__ initializes the object (INITIALIZATION)
Person.__init__(instance, "Alice", 25)

# Step 3: Return the initialized object
person = instance
```

---

## Key Differences Between `__new__` and `__init__`

| Aspect | `__new__` (Constructor) | `__init__` (Initializer) |
|--------|------------------------|-------------------------|
| **Purpose** | Creates the object | Initializes the object |
| **When called** | Before object exists | After object exists |
| **First parameter** | `cls` (the class) | `self` (the instance) |
| **Return value** | Must return an instance | Returns `None` |
| **Frequency of use** | Rarely overridden | Almost always defined |
| **Control** | Controls object creation | Controls object setup |
| **Memory allocation** | Allocates memory | Works with allocated memory |

---

## Why `__init__` is an Initializer

By the time `__init__` is called:
- ✅ The object **already exists** in memory
- ✅ Memory has been **allocated**
- ✅ The object has been **created**

What `__init__` does:
- Sets up the object's **initial state**
- Assigns **attributes**
- Performs **setup logic**

**It does NOT create the object** - that's already done by `__new__`.

---

## Why We Usually Don't See `__new__`

In 99% of cases, you don't need to override `__new__` because Python's default implementation works perfectly:

```python
class Person:
    # We only define __init__, not __new__
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Python automatically uses the default __new__ from object class
person = Person("Alice", 25)
```

The default `__new__` inherited from `object` handles object creation automatically.

---

## When You Need to Use `__new__`

### 1. Inheriting from Immutable Types

When subclassing immutable types like `int`, `str`, `tuple`, you **must** use `__new__` because you can't modify them after creation:

```python
class PositiveInt(int):
    def __new__(cls, value):
        if value < 0:
            raise ValueError("Value must be positive")
        # Must use __new__ because int is immutable
        return super().__new__(cls, abs(value))
    
    def __init__(self, value):
        # This runs, but can't modify the int value
        print(f"Initialized with {value}")

num = PositiveInt(-42)
print(num)  # 42 (absolute value)
```

### 2. Singleton Pattern

Controlling that only one instance of a class exists:

```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating new database connection")
            cls._instance = super().__new__(cls)
        else:
            print("Returning existing connection")
        return cls._instance
    
    def __init__(self):
        print("Initializing connection")

db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True - same object
```

**Output:**
```
Creating new database connection
Initializing connection
Returning existing connection
Initializing connection
True
```

**Note**: `__init__` is called every time, even when returning an existing instance!

### 3. Factory Pattern

Returning different types of objects:

```python
class Shape:
    def __new__(cls, shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        else:
            return super().__new__(cls)

class Circle:
    def draw(self):
        print("Drawing a circle")

class Square:
    def draw(self):
        print("Drawing a square")

shape1 = Shape("circle")
shape2 = Shape("square")

shape1.draw()  # Drawing a circle
shape2.draw()  # Drawing a square

print(type(shape1))  # <class '__main__.Circle'>
print(type(shape2))  # <class '__main__.Square'>
```

---

## Comparison with Other Languages

### Java (Constructor Does Both)

```java
public class Person {
    private String name;
    private int age;
    
    // Constructor creates AND initializes
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

### C++ (Constructor Does Both)

```cpp
class Person {
private:
    string name;
    int age;
public:
    // Constructor creates AND initializes
    Person(string n, int a) : name(n), age(a) {}
};
```

### Python (Separated)

```python
class Person:
    # __new__ creates (usually implicit)
    # __init__ initializes (usually explicit)
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

---

## Practical Demonstration

### `__new__` Can Return Different Objects

```python
class SmartFactory:
    def __new__(cls, type_name):
        print(f"__new__ called with type: {type_name}")
        if type_name == "list":
            return []
        elif type_name == "dict":
            return {}
        else:
            return super().__new__(cls)
    
    def __init__(self, type_name):
        # This won't be called for list/dict!
        print(f"__init__ called for {type_name}")

obj1 = SmartFactory("list")
print(f"Type: {type(obj1)}\n")

obj2 = SmartFactory("dict")
print(f"Type: {type(obj2)}\n")

obj3 = SmartFactory("custom")
print(f"Type: {type(obj3)}")
```

**Output:**
```
__new__ called with type: list
Type: <class 'list'>

__new__ called with type: dict
Type: <class 'dict'>

__new__ called with type: custom
__init__ called for custom
Type: <class '__main__.SmartFactory'>
```

**Key Observation**: `__init__` is **not called** when `__new__` returns a different type!

---

## The `__init__` Cannot Create Objects

```python
class Example:
    def __init__(self):
        # By this point, 'self' already exists!
        print(f"self already exists: {self}")
        print(f"self's type: {type(self)}")
        print(f"self's id: {id(self)}")

obj = Example()
```

**Output:**
```
self already exists: <__main__.Example object at 0x7f8b1c3d4e50>
self's type: <class '__main__.Example'>
self's id: 140241234567890
```

The `self` parameter proves the object already exists when `__init__` is called.

---

## Why the Confusion Exists

### Common (But Technically Incorrect) Usage

Many Python developers and tutorials call `__init__` a "constructor" because:
- It's the method you **always** define
- It's where you set up your object
- It **feels** like a constructor from other languages
- The distinction doesn't matter for most use cases

### Technically Correct Usage

- **Constructor**: `__new__` (creates the object)
- **Initializer**: `__init__` (sets up the object)

---

## Summary

### The Truth

1. **`__new__`** is the true constructor - it creates the object
2. **`__init__`** is the initializer - it sets up the object
3. When you call `Person("Alice", 25)`, both are called in sequence

### Why It Matters

- Understanding this helps with advanced patterns (Singleton, Factory, etc.)
- Explains why you can't modify immutable objects in `__init__`
- Clarifies the object creation lifecycle

### Practical Takeaway

- For 99% of cases, just define `__init__` and call it a day
- Use `__new__` only for special cases (immutable types, singletons, factories)
- It's okay to casually call `__init__` a "constructor" in conversation
- But know the technical distinction when it matters

---

## Quick Reference

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        # Called FIRST
        # Creates and returns the object
        # Rarely overridden
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, *args, **kwargs):
        # Called SECOND (after __new__)
        # Initializes the already-created object
        # Almost always defined
        self.attribute = "value"
```

**Remember**: By the time `__init__` runs, the object already exists. That's why it's an **initializer**, not a **constructor**.
