# Multiple Inheritance in Python

## What is Multiple Inheritance?

**Multiple inheritance** allows a class to inherit from more than one parent class, gaining attributes and methods from all of them.

```python
class Parent1:
    pass

class Parent2:
    pass

class Child(Parent1, Parent2):  # Inherits from both
    pass
```

---

## Basic Multiple Inheritance Example

```python
class Father:
    def __init__(self):
        self.father_name = "John"
    
    def gardening(self):
        return "I enjoy gardening"

class Mother:
    def __init__(self):
        self.mother_name = "Jane"
    
    def cooking(self):
        return "I enjoy cooking"

class Child(Father, Mother):
    def __init__(self):
        Father.__init__(self)
        Mother.__init__(self)
        self.child_name = "Tom"
    
    def sports(self):
        return "I enjoy sports"

# Create child object
child = Child()
print(child.father_name)  # John
print(child.mother_name)  # Jane
print(child.child_name)   # Tom
print(child.gardening())  # I enjoy gardening
print(child.cooking())    # I enjoy cooking
print(child.sports())     # I enjoy sports
```

---

## The Diamond Problem

### What is the Diamond Problem?

The **diamond problem** occurs when a class inherits from two classes that both inherit from the same base class, creating a diamond-shaped inheritance hierarchy.

```
      A
     / \
    B   C
     \ /
      D
```

If both B and C override a method from A, which version should D inherit?

### Example of Diamond Problem

```python
class A:
    def __init__(self):
        print("A.__init__")
        self.value = "A"
    
    def method(self):
        return "Method from A"

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()
        self.value = "B"
    
    def method(self):
        return "Method from B"

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()
        self.value = "C"
    
    def method(self):
        return "Method from C"

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()

# Create instance
d = D()
print(d.method())  # Which method is called?
print(d.value)     # Which value is set?
```

**Output:**
```
D.__init__
B.__init__
C.__init__
A.__init__
Method from B
C
```

---

## Python's Solution: Method Resolution Order (MRO)

Python solves the diamond problem using the **C3 Linearization algorithm** to create a **Method Resolution Order (MRO)**.

### What is MRO?

MRO is the order in which Python searches for methods and attributes in a class hierarchy.

### Viewing the MRO

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

# View MRO
print(D.__mro__)
# Output: (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, 
#          <class '__main__.A'>, <class 'object'>)

# Or use mro() method
print(D.mro())

# Human-readable format
for cls in D.__mro__:
    print(cls.__name__)
# Output:
# D
# B
# C
# A
# object
```

### MRO Rules (C3 Linearization)

1. **Child before parents**: The child class comes before its parents
2. **Left-to-right**: Parents are searched left to right as listed
3. **Parent before grandparent**: A parent class comes before its own parents
4. **Consistency**: The order must be consistent across the hierarchy

---

## Detailed Diamond Problem Example

```python
class Animal:
    def __init__(self):
        print("Animal.__init__")
        self.category = "Animal"
    
    def speak(self):
        return "Some sound"
    
    def info(self):
        return f"I am an {self.category}"

class Mammal(Animal):
    def __init__(self):
        print("Mammal.__init__")
        super().__init__()
        self.category = "Mammal"
    
    def speak(self):
        return "Mammal sound"
    
    def feed_milk(self):
        return "Feeding milk to babies"

class WingedAnimal(Animal):
    def __init__(self):
        print("WingedAnimal.__init__")
        super().__init__()
        self.category = "Winged Animal"
    
    def speak(self):
        return "Winged animal sound"
    
    def fly(self):
        return "Flying in the sky"

class Bat(Mammal, WingedAnimal):
    def __init__(self):
        print("Bat.__init__")
        super().__init__()
        self.category = "Bat"
    
    def speak(self):
        return "Screech!"

# Create bat
print("Creating Bat:")
print("=" * 50)
bat = Bat()

print("\n" + "=" * 50)
print("MRO for Bat:")
print("=" * 50)
for cls in Bat.__mro__:
    print(f"  {cls.__name__}")

print("\n" + "=" * 50)
print("Calling methods:")
print("=" * 50)
print(f"bat.speak() = {bat.speak()}")
print(f"bat.feed_milk() = {bat.feed_milk()}")
print(f"bat.fly() = {bat.fly()}")
print(f"bat.info() = {bat.info()}")
print(f"bat.category = {bat.category}")
```

**Output:**
```
Creating Bat:
==================================================
Bat.__init__
Mammal.__init__
WingedAnimal.__init__
Animal.__init__

==================================================
MRO for Bat:
==================================================
  Bat
  Mammal
  WingedAnimal
  Animal
  object

==================================================
Calling methods:
==================================================
bat.speak() = Screech!
bat.feed_milk() = Feeding milk to babies
bat.fly() = Flying in the sky
bat.info() = I am an Bat
bat.category = Bat
```

### How `super()` Works with MRO

```python
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()  # Calls next in MRO (A)

class C(A):
    def method(self):
        print("C.method")
        super().method()  # Calls next in MRO (A)

class D(B, C):
    def method(self):
        print("D.method")
        super().method()  # Calls next in MRO (B)

d = D()
d.method()

print("\nMRO:", [cls.__name__ for cls in D.__mro__])
```

**Output:**
```
D.method
B.method
C.method
A.method

MRO: ['D', 'B', 'C', 'A', 'object']
```

**Explanation**: `super()` doesn't call the parent class - it calls the **next class in the MRO**.

---

## Common Methods and Variables from Different Parents

### Scenario 1: Different Methods from Different Parents

```python
class DatabaseMixin:
    def save(self):
        return "Saving to database"
    
    def delete(self):
        return "Deleting from database"

class CacheMixin:
    def cache(self):
        return "Caching data"
    
    def invalidate_cache(self):
        return "Invalidating cache"

class User(DatabaseMixin, CacheMixin):
    def __init__(self, name):
        self.name = name

user = User("Alice")
print(user.save())              # Saving to database
print(user.cache())             # Caching data
print(user.delete())            # Deleting from database
print(user.invalidate_cache())  # Invalidating cache
```

### Scenario 2: Same Method Name in Multiple Parents

```python
class Parent1:
    def greet(self):
        return "Hello from Parent1"

class Parent2:
    def greet(self):
        return "Hello from Parent2"

class Child(Parent1, Parent2):
    pass

child = Child()
print(child.greet())  # Hello from Parent1 (first in MRO)

# Check MRO
print([cls.__name__ for cls in Child.__mro__])
# ['Child', 'Parent1', 'Parent2', 'object']
```

**Rule**: The method from the **first parent in the MRO** is used.

### Scenario 3: Calling All Parent Methods

```python
class Logger:
    def log(self):
        print("Logger: Logging event")

class Validator:
    def log(self):
        print("Validator: Validating data")

class Processor(Logger, Validator):
    def log(self):
        print("Processor: Processing")
        # Call all parent log methods
        Logger.log(self)
        Validator.log(self)

processor = Processor()
processor.log()
```

**Output:**
```
Processor: Processing
Logger: Logging event
Validator: Validating data
```

### Scenario 4: Same Variable Name in Multiple Parents

```python
class Parent1:
    def __init__(self):
        self.value = "Parent1"
        self.parent1_specific = "P1"

class Parent2:
    def __init__(self):
        self.value = "Parent2"
        self.parent2_specific = "P2"

class Child(Parent1, Parent2):
    def __init__(self):
        Parent1.__init__(self)
        Parent2.__init__(self)  # This overwrites self.value
        self.child_value = "Child"

child = Child()
print(child.value)             # Parent2 (last one called)
print(child.parent1_specific)  # P1
print(child.parent2_specific)  # P2
print(child.child_value)       # Child
```

---

## Using `super()` Correctly in Multiple Inheritance

### ❌ Wrong Way: Calling Parents Directly

```python
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        A.__init__(self)  # Direct call - can cause issues

class C(A):
    def __init__(self):
        print("C.__init__")
        A.__init__(self)  # Direct call - can cause issues

class D(B, C):
    def __init__(self):
        print("D.__init__")
        B.__init__(self)
        C.__init__(self)

d = D()
```

**Output:**
```
D.__init__
B.__init__
A.__init__
C.__init__
A.__init__  # A.__init__ called TWICE!
```

### ✅ Correct Way: Using `super()`

```python
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()  # Calls next in MRO

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()  # Calls next in MRO

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()  # Calls next in MRO

d = D()
```

**Output:**
```
D.__init__
B.__init__
C.__init__
A.__init__  # A.__init__ called only ONCE!
```

---

## Practical Example: Mixins

Mixins are a common use case for multiple inheritance:

```python
class JSONSerializerMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class XMLSerializerMixin:
    def to_xml(self):
        xml = "<object>"
        for key, value in self.__dict__.items():
            xml += f"<{key}>{value}</{key}>"
        xml += "</object>"
        return xml

class LoggerMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class User(JSONSerializerMixin, XMLSerializerMixin, LoggerMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.log(f"User {name} created")

user = User("Alice", "alice@example.com")
print(user.to_json())
print(user.to_xml())
```

**Output:**
```
[User] User Alice created
{"name": "Alice", "email": "alice@example.com"}
<object><name>Alice</name><email>alice@example.com</email></object>
```

---

## Object Creation and Chaining

### How Object Creation Works with Multiple Inheritance

```python
class A:
    def __new__(cls, *args, **kwargs):
        print(f"A.__new__ called, cls={cls.__name__}")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self):
        print("A.__init__")

class B(A):
    def __new__(cls, *args, **kwargs):
        print(f"B.__new__ called, cls={cls.__name__}")
        return super().__new__(cls, *args, **kwargs)
    
    def __init__(self):
        print("B.__init__")
        super().__init__()

class C(A):
    def __new__(cls, *args, **kwargs):
        print(f"C.__new__ called, cls={cls.__name__}")
        return super().__new__(cls, *args, **kwargs)
    
    def __init__(self):
        print("C.__init__")
        super().__init__()

class D(B, C):
    def __new__(cls, *args, **kwargs):
        print(f"D.__new__ called, cls={cls.__name__}")
        return super().__new__(cls, *args, **kwargs)
    
    def __init__(self):
        print("D.__init__")
        super().__init__()

print("Creating D:")
print("MRO:", [cls.__name__ for cls in D.__mro__])
print()
d = D()
```

**Output:**
```
Creating D:
MRO: ['D', 'B', 'C', 'A', 'object']

D.__new__ called, cls=D
B.__new__ called, cls=D
C.__new__ called, cls=D
A.__new__ called, cls=D
D.__init__
B.__init__
C.__init__
A.__init__
```

---

## Best Practices for Multiple Inheritance

### 1. Use Mixins for Shared Functionality

```python
# Good: Mixins provide specific functionality
class TimestampMixin:
    def add_timestamp(self):
        from datetime import datetime
        self.created_at = datetime.now()

class ValidationMixin:
    def validate(self):
        # Validation logic
        pass

class User(TimestampMixin, ValidationMixin):
    def __init__(self, name):
        self.name = name
        self.add_timestamp()
```

### 2. Always Use `super()` for Cooperative Inheritance

```python
# Good: Using super() ensures proper MRO traversal
class Parent1:
    def __init__(self):
        super().__init__()
        self.p1 = "Parent1"

class Parent2:
    def __init__(self):
        super().__init__()
        self.p2 = "Parent2"

class Child(Parent1, Parent2):
    def __init__(self):
        super().__init__()
        self.child = "Child"
```

### 3. Keep Inheritance Hierarchies Shallow

```python
# Avoid deep, complex hierarchies
# Prefer composition over inheritance when possible
```

### 4. Document MRO for Complex Hierarchies

```python
class ComplexClass(A, B, C):
    """
    Inherits from A, B, and C.
    MRO: ComplexClass -> A -> B -> C -> object
    """
    pass
```

---

## Summary

### Key Concepts

1. **Multiple Inheritance**: A class can inherit from multiple parent classes
2. **Diamond Problem**: Resolved using MRO (Method Resolution Order)
3. **MRO**: Determined by C3 Linearization algorithm
4. **`super()`**: Calls the next class in MRO, not necessarily the parent
5. **Method/Variable Conflicts**: First class in MRO wins

### MRO Rules

- Child before parents
- Left-to-right order
- Parent before grandparent
- Consistent ordering

### Best Practices

✅ Use `super()` for cooperative inheritance  
✅ Use mixins for shared functionality  
✅ Keep hierarchies shallow  
✅ Document complex MRO  
✅ Avoid deep diamond hierarchies

### Common Pitfalls

❌ Calling parent `__init__` directly (can cause duplicate calls)  
❌ Not understanding MRO  
❌ Creating overly complex inheritance hierarchies  
❌ Mixing incompatible parent classes
