# Demonstrating `__new__` and `__init__` in Inheritance

## Understanding `__new__` vs `__init__`

- **`__new__`**: The actual constructor - creates the object
- **`__init__`**: The initializer - sets up the object after creation

This example demonstrates how both methods work in parent and child classes during inheritance.

---

## Complete Example with `__new__` and `__init__`

```python
# Parent Class
class Shape:
    """Base class for all shapes"""
    
    def __new__(cls, *args, **kwargs):
        print(f"1. Shape.__new__ called (Creating object)")
        print(f"   - cls: {cls}")
        print(f"   - args: {args}")
        
        # Create the instance using object's __new__
        instance = super().__new__(cls)
        print(f"   - Instance created: {instance}")
        print(f"   - Instance type: {type(instance)}")
        
        return instance
    
    def __init__(self, shape_type):
        print(f"3. Shape.__init__ called (Initializing parent)")
        print(f"   - self: {self}")
        print(f"   - shape_type: {shape_type}")
        self.shape_type = shape_type
        print(f"   - Parent initialization complete")
    
    def draw_shape(self):
        """Draw the shape"""
        print(f'Drawing {self.shape_type}...')


# Child Class
class Rectangle(Shape):
    """Rectangle class that inherits from Shape"""
    
    def __new__(cls, *args, **kwargs):
        print(f"2. Rectangle.__new__ called (Before parent __new__)")
        print(f"   - cls: {cls}")
        print(f"   - args: {args}")
        
        # Call parent's __new__ to create the instance
        instance = super().__new__(cls, *args, **kwargs)
        
        print(f"   - Back in Rectangle.__new__ (After parent __new__)")
        print(f"   - Instance: {instance}")
        
        # You can add attributes here (before __init__)
        # But it's not recommended - use __init__ instead
        
        return instance
    
    def __init__(self, length, width):
        print(f"4. Rectangle.__init__ called (Initializing child)")
        print(f"   - self: {self}")
        print(f"   - length: {length}, width: {width}")
        
        # Call parent's __init__
        super().__init__('Rectangle')
        
        print(f"5. Back in Rectangle.__init__ (After parent __init__)")
        # Set child-specific attributes
        self.length = length
        self.width = width
        print(f"   - Child initialization complete")
    
    def calculate_area(self):
        """Calculate and return the area of the rectangle"""
        area = self.length * self.width
        print(f'\nArea of {self.shape_type} = {area}')
        return area


# Create a Rectangle object
print("=" * 60)
print("CREATING RECTANGLE OBJECT")
print("=" * 60)

rec = Rectangle(5, 20)

print("\n" + "=" * 60)
print("OBJECT CREATION COMPLETE")
print("=" * 60)

# Use the object
print("\n" + "=" * 60)
print("CALLING METHODS")
print("=" * 60)
rec.calculate_area()
rec.draw_shape()
```

---

## Expected Output

```
============================================================
CREATING RECTANGLE OBJECT
============================================================
2. Rectangle.__new__ called (Before parent __new__)
   - cls: <class '__main__.Rectangle'>
   - args: (5, 20)
1. Shape.__new__ called (Creating object)
   - cls: <class '__main__.Rectangle'>
   - args: (5, 20)
   - Instance created: <__main__.Rectangle object at 0x...>
   - Instance type: <class '__main__.Rectangle'>
   - Back in Rectangle.__new__ (After parent __new__)
   - Instance: <__main__.Rectangle object at 0x...>
4. Rectangle.__init__ called (Initializing child)
   - self: <__main__.Rectangle object at 0x...>
   - length: 5, width: 20
3. Shape.__init__ called (Initializing parent)
   - self: <__main__.Rectangle object at 0x...>
   - shape_type: Rectangle
   - Parent initialization complete
5. Back in Rectangle.__init__ (After parent __init__)
   - Child initialization complete

============================================================
OBJECT CREATION COMPLETE
============================================================

============================================================
CALLING METHODS
============================================================

Area of Rectangle = 100
Drawing Rectangle...
```

---

## Execution Flow Diagram

```
Rectangle(5, 20)
    ↓
┌─────────────────────────────────────────┐
│ 1. Rectangle.__new__(cls, 5, 20)       │
│    - cls = Rectangle class              │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 2. super().__new__(cls, 5, 20)          │
│    Calls Shape.__new__                  │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 3. Shape.__new__(cls, 5, 20)            │
│    - Creates instance                   │
│    - Returns instance                   │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 4. Back to Rectangle.__new__            │
│    - Returns instance                   │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 5. Rectangle.__init__(self, 5, 20)      │
│    - self is the created instance       │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 6. super().__init__('Rectangle')        │
│    Calls Shape.__init__                 │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 7. Shape.__init__(self, 'Rectangle')    │
│    - Sets self.shape_type               │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│ 8. Back to Rectangle.__init__           │
│    - Sets self.length, self.width       │
└─────────────────┬───────────────────────┘
                  ↓
         Object Ready to Use
```

---

## Key Observations

### 1. **Call Order**

The execution order is:
1. `Rectangle.__new__` (child constructor)
2. `Shape.__new__` (parent constructor)
3. `Rectangle.__init__` (child initializer)
4. `Shape.__init__` (parent initializer)

### 2. **`__new__` Receives the Class**

```python
def __new__(cls, *args, **kwargs):
    # cls is the CLASS, not an instance
    print(cls)  # <class '__main__.Rectangle'>
```

### 3. **`__init__` Receives the Instance**

```python
def __init__(self, *args, **kwargs):
    # self is the INSTANCE created by __new__
    print(self)  # <__main__.Rectangle object at 0x...>
```

### 4. **Same Instance Throughout**

The instance created in `__new__` is the same one passed to `__init__`:

```python
# In __new__
instance = super().__new__(cls)  # Creates instance
return instance

# Later, in __init__
def __init__(self):
    # self is the same instance created above
```

### 5. **Parent's `__new__` Creates Child Instance**

Even though `Shape.__new__` is called, it creates a `Rectangle` instance (not a `Shape` instance) because `cls` is `Rectangle`.

---

## When to Override `__new__`

### ❌ Usually NOT Needed

For most cases, you **don't need** to override `__new__`:

```python
class Rectangle(Shape):
    # Just define __init__ - this is enough!
    def __init__(self, length, width):
        super().__init__('Rectangle')
        self.length = length
        self.width = width
```

### ✅ When You SHOULD Override `__new__`

#### 1. **Subclassing Immutable Types**

```python
class PositiveInt(int):
    def __new__(cls, value):
        if value < 0:
            value = abs(value)
        return super().__new__(cls, value)

num = PositiveInt(-42)
print(num)  # 42
```

#### 2. **Singleton Pattern**

```python
class DatabaseConnection(Shape):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Creating new database connection")
            cls._instance = super().__new__(cls)
        else:
            print("Returning existing connection")
        return cls._instance
    
    def __init__(self, shape_type):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            super().__init__(shape_type)
            self.initialized = True

db1 = DatabaseConnection('DB')
db2 = DatabaseConnection('DB')
print(db1 is db2)  # True - same object
```

#### 3. **Factory Pattern**

```python
class ShapeFactory(Shape):
    def __new__(cls, shape_type, *args):
        if shape_type == 'circle':
            return Circle(*args)
        elif shape_type == 'rectangle':
            return Rectangle(*args)
        else:
            return super().__new__(cls)
```

---

## Practical Example: Adding Circle

```python
class Circle(Shape):
    """Circle class with __new__ and __init__"""
    
    def __new__(cls, *args, **kwargs):
        print(f"Circle.__new__ called")
        instance = super().__new__(cls, *args, **kwargs)
        print(f"Circle instance created")
        return instance
    
    def __init__(self, radius):
        print(f"Circle.__init__ called")
        super().__init__('Circle')
        self.radius = radius
        print(f"Circle initialization complete")
    
    def calculate_area(self):
        import math
        area = math.pi * self.radius ** 2
        print(f'Area of {self.shape_type} = {area:.2f}')
        return area

# Create circle
print("\n" + "=" * 60)
print("CREATING CIRCLE OBJECT")
print("=" * 60)

circle = Circle(10)

print("\n" + "=" * 60)
print("CALLING METHODS")
print("=" * 60)
circle.calculate_area()
```

---

## Common Mistakes

### ❌ Mistake 1: Forgetting to Return Instance

```python
class BadRectangle(Shape):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        # Forgot to return!
        # This will cause TypeError

# TypeError: __new__() should return an object instance
```

### ❌ Mistake 2: Not Calling Parent's `__new__`

```python
class BadRectangle(Shape):
    def __new__(cls, *args, **kwargs):
        # Forgot to call super().__new__()
        # Instance is never created!
        return None

# This creates None, not a Rectangle
```

### ❌ Mistake 3: Modifying in `__new__` Instead of `__init__`

```python
class BadRectangle(Shape):
    def __new__(cls, length, width):
        instance = super().__new__(cls)
        # Don't do this - use __init__ instead!
        instance.length = length
        instance.width = width
        return instance
```

**Why it's bad:**
- Violates separation of concerns
- `__new__` should only create, not initialize
- Makes code harder to understand

---

## Summary

### Key Takeaways

1. **`__new__` creates**, **`__init__` initializes**
2. **`__new__` is called first**, then `__init__`
3. **`__new__` receives `cls`** (class), **`__init__` receives `self`** (instance)
4. **Must return instance** from `__new__`
5. **Usually don't need to override `__new__`** - `__init__` is enough
6. **Override `__new__` only for special cases** (immutables, singletons, factories)

### Inheritance Chain

```
Child.__new__
    ↓ (calls super())
Parent.__new__
    ↓ (creates instance)
Child.__init__
    ↓ (calls super())
Parent.__init__
    ↓ (initializes)
Complete!
```

### Best Practice

For 99% of cases, just use `__init__`:

```python
class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__('Rectangle')
        self.length = length
        self.width = width
```

Only override `__new__` when you have a specific need for it!
