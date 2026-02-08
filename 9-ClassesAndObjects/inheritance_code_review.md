# Code Review: Inheritance Example

## Original Code

```python
## Inheritance
# Parent Class
class Shape:
    def __init__(self, type):
        print('Parent class constructor called')
        self.type = type

    def draw_shape(self):
        print('Shap class starting to drawing shape')    

# Child Class
class Rectangle(Shape):## extending parent class
    def __init__(self, type, length, width):
        super().__init__(type) ## Calling parent class initializer
        self.length = length
        self.width = width
    
    def calculate_area(self):
        print(f'Area of {self.type} = {self.length * self.width}')

rec = Rectangle('Rectangle', 5, 20)
rec.calculate_area()
```

**Output:**
```
Parent class constructor called
Area of Rectangle = 100
```

---

## Detailed Explanation

### 1. Parent Class: `Shape`

```python
class Shape:
    def __init__(self, type):
        print('Parent class constructor called')
        self.type = type
```

**What it does:**
- Defines a parent (base) class called `Shape`
- The `__init__` method is the **initializer** (often called constructor)
- Takes a parameter `type` to specify what kind of shape it is
- Prints a message when the initializer is called
- Stores the `type` as an instance attribute

**Purpose:** This is the base class that other shapes will inherit from.

### 2. Parent Class Method: `draw_shape`

```python
def draw_shape(self):
    print('Shap class starting to drawing shape')
```

**What it does:**
- A method that can be called on any `Shape` object
- Currently just prints a message (placeholder for actual drawing logic)

**Note:** This method is defined but never called in the example.

### 3. Child Class: `Rectangle`

```python
class Rectangle(Shape):  ## extending parent class
```

**What it does:**
- Defines a child class `Rectangle` that **inherits** from `Shape`
- The syntax `Rectangle(Shape)` means: "Rectangle is a subclass of Shape"
- Rectangle automatically gets all attributes and methods from Shape

**Inheritance relationship:**
```
Shape (Parent)
  ↓
Rectangle (Child)
```

### 4. Child Class Initializer

```python
def __init__(self, type, length, width):
    super().__init__(type)  ## Calling parent class initializer
    self.length = length
    self.width = width
```

**What it does:**
1. **Overrides** the parent's `__init__` method
2. Takes three parameters: `type`, `length`, and `width`
3. **`super().__init__(type)`**: Calls the parent class's initializer
   - This ensures the parent class is properly initialized
   - Sets `self.type` through the parent's `__init__`
4. Adds two new instance attributes specific to rectangles: `length` and `width`

**Why use `super()`?**
- Ensures the parent class initialization code runs
- Maintains the inheritance chain properly
- Allows the parent to set up its own attributes

### 5. Child Class Method: `calculate_area`

```python
def calculate_area(self):
    print(f'Area of {self.type} = {self.length * self.width}')
```

**What it does:**
- A method specific to the `Rectangle` class (not in parent)
- Calculates area by multiplying `length * width`
- Uses `self.type` (inherited from parent) and `self.length`, `self.width` (from child)
- Prints the result using an f-string

### 6. Object Creation and Method Call

```python
rec = Rectangle('Rectangle', 5, 20)
rec.calculate_area()
```

**What happens:**
1. Creates a `Rectangle` object with:
   - `type` = 'Rectangle'
   - `length` = 5
   - `width` = 20
2. During creation:
   - `Rectangle.__init__` is called
   - Which calls `Shape.__init__` via `super()`
   - Prints "Parent class constructor called"
3. Calls `calculate_area()` method
   - Calculates: 5 × 20 = 100
   - Prints: "Area of Rectangle = 100"

---

## Errors and Issues Found

### ❌ Error 1: Typo in `draw_shape` Method

**Line:**
```python
print('Shap class starting to drawing shape')
```

**Issues:**
- "Shap" should be "Shape"
- "starting to drawing" is grammatically incorrect

**Fix:**
```python
print('Shape class starting to draw shape')
# OR better:
print('Drawing shape...')
```

### ❌ Error 2: Using `type` as Parameter Name

**Line:**
```python
def __init__(self, type):
```

**Issue:**
- `type` is a **built-in Python function**
- Using it as a parameter name **shadows** the built-in
- This is a bad practice and can cause confusion

**Fix:**
```python
def __init__(self, shape_type):
    self.shape_type = shape_type
```

### ⚠️ Convention Issue 1: Comment Style

**Line:**
```python
class Rectangle(Shape):## extending parent class
```

**Issue:**
- No space after `:`
- Comment should be on separate line or have space before `##`

**Fix:**
```python
class Rectangle(Shape):  # Extending parent class
# OR
# Child class extending Shape
class Rectangle(Shape):
```

### ⚠️ Convention Issue 2: Inconsistent Comment Markers

**Lines:**
```python
## Inheritance
# Parent Class
```

**Issue:**
- Mixing `##` and `#` for comments
- Should be consistent

**Fix:**
```python
# Inheritance
# Parent Class
```

### ⚠️ Convention Issue 3: Misleading Comment

**Line:**
```python
super().__init__(type) ## Calling parent class initializer
```

**Issue:**
- Comment says "initializer" which is correct
- But earlier comment says "constructor" which is technically less accurate

**Consistency Fix:**
Use "initializer" consistently, or explain the difference.

### ⚠️ Design Issue: Redundant Parameter

**Issue:**
- Passing `'Rectangle'` as `type` parameter is redundant
- The class already knows it's a Rectangle

**Better Design:**
```python
class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__('Rectangle')  # Set type automatically
        self.length = length
        self.width = width

# Usage
rec = Rectangle(5, 20)  # Cleaner - no need to specify 'Rectangle'
```

---

## Corrected and Improved Code

```python
# Inheritance Example

# Parent Class
class Shape:
    """Base class for all shapes"""
    
    def __init__(self, shape_type):
        """Initialize shape with a type"""
        print('Parent class initializer called')
        self.shape_type = shape_type

    def draw_shape(self):
        """Draw the shape (placeholder method)"""
        print(f'Drawing {self.shape_type}...')


# Child Class
class Rectangle(Shape):
    """Rectangle class that inherits from Shape"""
    
    def __init__(self, length, width):
        """Initialize rectangle with length and width"""
        # Call parent class initializer
        super().__init__('Rectangle')
        self.length = length
        self.width = width
    
    def calculate_area(self):
        """Calculate and return the area of the rectangle"""
        area = self.length * self.width
        print(f'Area of {self.shape_type} = {area}')
        return area
    
    def draw_shape(self):
        """Override parent's draw method with rectangle-specific implementation"""
        print(f'Drawing a {self.length}x{self.width} rectangle')


# Create rectangle object
rec = Rectangle(5, 20)

# Call methods
rec.calculate_area()  # Area of Rectangle = 100
rec.draw_shape()      # Drawing a 5x20 rectangle
```

**Output:**
```
Parent class initializer called
Area of Rectangle = 100
Drawing a 5x20 rectangle
```

---

## Key Concepts Demonstrated

### ✅ Inheritance
- `Rectangle` inherits from `Shape`
- Gets all attributes and methods from parent

### ✅ Method Overriding
- `Rectangle` can override parent methods (like `draw_shape`)

### ✅ `super()` Function
- Calls parent class methods
- Essential for proper initialization chain

### ✅ Attribute Access
- Child can access parent's attributes (`self.shape_type`)
- Child has its own attributes (`self.length`, `self.width`)

---

## Additional Improvements

### 1. Add More Shape Types

```python
class Circle(Shape):
    def __init__(self, radius):
        super().__init__('Circle')
        self.radius = radius
    
    def calculate_area(self):
        import math
        area = math.pi * self.radius ** 2
        print(f'Area of {self.shape_type} = {area:.2f}')
        return area

class Triangle(Shape):
    def __init__(self, base, height):
        super().__init__('Triangle')
        self.base = base
        self.height = height
    
    def calculate_area(self):
        area = 0.5 * self.base * self.height
        print(f'Area of {self.shape_type} = {area}')
        return area
```

### 2. Make `calculate_area` Abstract in Parent

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, shape_type):
        self.shape_type = shape_type
    
    @abstractmethod
    def calculate_area(self):
        """All shapes must implement this method"""
        pass
```

---

## Summary of Issues

| Issue | Type | Severity | Fix |
|-------|------|----------|-----|
| Typo: "Shap" | Error | Low | Change to "Shape" |
| Grammar: "starting to drawing" | Error | Low | Change to "starting to draw" |
| Using `type` as parameter | Convention | Medium | Rename to `shape_type` |
| Inconsistent comments (`##` vs `#`) | Convention | Low | Use `#` consistently |
| No space before inline comment | Convention | Low | Add space before `#` |
| Redundant type parameter | Design | Medium | Set automatically in child |
| Unused `draw_shape` method | Design | Low | Demonstrate usage |

---

## Best Practices Applied

✅ Use descriptive parameter names (not built-in names)  
✅ Add docstrings to classes and methods  
✅ Use consistent comment style  
✅ Call `super().__init__()` in child classes  
✅ Return values from calculation methods  
✅ Demonstrate method overriding  
✅ Follow PEP 8 naming conventions
