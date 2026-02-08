# The `dir()` Function in Python

## What is `dir()`?

The `dir()` function is a built-in Python function that returns a **sorted list of valid attributes and methods** of an object. It's one of the most useful tools for **introspection** and **exploration** in Python.

## Syntax

```python
dir()           # Without arguments - returns names in current scope
dir(object)     # With an object - returns attributes and methods of that object
```

---

## Basic Examples

### 1. Using `dir()` on Built-in Types

#### String

```python
text = "hello"
print(dir(text))
```

**Output (partial):**
```python
['capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 
 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 
 'isspace', 'isupper', 'join', 'lower', 'lstrip', 'replace', 'split', 
 'startswith', 'strip', 'swapcase', 'title', 'upper', 'zfill', ...]
```

#### List

```python
my_list = [1, 2, 3]
print(dir(my_list))
```

**Output (partial):**
```python
['append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 
 'pop', 'remove', 'reverse', 'sort', ...]
```

#### Dictionary

```python
my_dict = {"key": "value"}
print(dir(my_dict))
```

**Output (partial):**
```python
['clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 
 'popitem', 'setdefault', 'update', 'values', ...]
```

---

## Using `dir()` with Custom Classes

### Example 1: Simple Class

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    def celebrate_birthday(self):
        self.age += 1

person = Person("Alice", 25)
print(dir(person))
```

**Output (partial):**
```python
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
 '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', 
 '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
 '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
 '__str__', '__subclasshook__', '__weakref__', 
 'age', 'celebrate_birthday', 'greet', 'name']
```

**Notice**: Custom attributes (`age`, `name`) and methods (`greet`, `celebrate_birthday`) appear at the end!

### Example 2: Filtering Out Dunder Methods

```python
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.speed = 0
    
    def accelerate(self):
        self.speed += 10
    
    def brake(self):
        self.speed = max(0, self.speed - 10)

car = Car("Toyota", "Camry")

# Get only public (non-dunder) attributes and methods
public_attrs = [attr for attr in dir(car) if not attr.startswith('_')]
print(public_attrs)
```

**Output:**
```python
['accelerate', 'brake', 'brand', 'model', 'speed']
```

---

## Using `dir()` on Modules

```python
import math

# See all functions and constants in the math module
print(dir(math))
```

**Output (partial):**
```python
['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 
 'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'e', 'erf', 
 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 
 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 
 'isnan', 'isqrt', 'lcm', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 
 'log2', 'modf', 'nan', 'pi', 'pow', 'prod', 'radians', 'sin', 'sinh', 
 'sqrt', 'tan', 'tanh', 'tau', 'trunc']
```

---

## Practical Use Cases

### 1. Exploring Unknown Objects

When you receive an object and want to discover what methods are available:

```python
# Exploring a dictionary
response = {"status": "success", "data": [1, 2, 3]}
methods = [attr for attr in dir(response) if not attr.startswith('_')]
print(methods)
```

**Output:**
```python
['clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 
 'popitem', 'setdefault', 'update', 'values']
```

### 2. Debugging and Inspection

```python
class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.balance = balance
        self._account_id = "ACC12345"  # Private attribute
        self.__pin = "1234"            # Name-mangled attribute

account = BankAccount("John Doe", 1000)

# See all attributes (including private ones)
all_attrs = [attr for attr in dir(account) if not attr.startswith('__') or attr.endswith('__')]
print(all_attrs)
```

**Output:**
```python
['_BankAccount__pin', '_account_id', 'account_holder', 'balance']
```

### 3. Checking for Method Existence

```python
# Check if an object has a specific method
my_list = [1, 2, 3]

if 'append' in dir(my_list):
    print("Lists have an append method")
    my_list.append(4)
    print(my_list)  # [1, 2, 3, 4]
```

### 4. Dynamic Attribute Access

```python
class Config:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080
        self.debug = True
        self.database = "mydb"

config = Config()

# Dynamically access all configuration attributes
print("Configuration Settings:")
for attr in dir(config):
    if not attr.startswith('_'):
        value = getattr(config, attr)
        print(f"  {attr}: {value}")
```

**Output:**
```
Configuration Settings:
  database: mydb
  debug: True
  host: localhost
  port: 8080
```

### 5. Comparing Objects

```python
class Animal:
    def eat(self):
        print("Eating...")
    
    def sleep(self):
        print("Sleeping...")

class Dog(Animal):
    def bark(self):
        print("Woof!")

class Cat(Animal):
    def meow(self):
        print("Meow!")

dog = Dog()
cat = Cat()

# Compare available methods
dog_methods = [m for m in dir(dog) if not m.startswith('_')]
cat_methods = [m for m in dir(cat) if not m.startswith('_')]

print(f"Dog methods: {dog_methods}")
print(f"Cat methods: {cat_methods}")
```

**Output:**
```
Dog methods: ['bark', 'eat', 'sleep']
Cat methods: ['eat', 'meow', 'sleep']
```

---

## Important Characteristics

### 1. Includes Inherited Attributes

```python
class Animal:
    def eat(self):
        pass

class Dog(Animal):
    def bark(self):
        pass

dog = Dog()
methods = [attr for attr in dir(dog) if not attr.startswith('_')]
print(methods)  # ['bark', 'eat'] - includes 'eat' from Animal
```

### 2. Returns Alphabetically Sorted List

The output is always sorted alphabetically, regardless of the order attributes were defined.

```python
class Example:
    def __init__(self):
        self.zebra = 1
        self.apple = 2
        self.mango = 3

obj = Example()
attrs = [a for a in dir(obj) if not a.startswith('_')]
print(attrs)  # ['apple', 'mango', 'zebra'] - sorted!
```

### 3. Shows Private and Name-Mangled Attributes

```python
class Secret:
    def __init__(self):
        self.public = "everyone can see"
        self._private = "single underscore"
        self.__very_private = "double underscore (name-mangled)"

s = Secret()
print([attr for attr in dir(s) if not attr.startswith('__') or 'private' in attr.lower()])
```

**Output:**
```python
['_Secret__very_private', '_private', 'public']
```

### 4. Without Arguments - Shows Current Scope

```python
x = 10
y = 20

def my_function():
    pass

class MyClass:
    pass

# dir() without arguments shows names in current scope
print([name for name in dir() if not name.startswith('_')])
```

**Output (partial):**
```python
['MyClass', 'my_function', 'x', 'y']
```

---

## Comparison with Related Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `dir(obj)` | Lists all attributes and methods | `dir(my_list)` |
| `vars(obj)` | Returns `__dict__` (instance attributes only) | `vars(my_obj)` |
| `help(obj)` | Shows detailed documentation | `help(str.upper)` |
| `type(obj)` | Returns the type/class of object | `type(42)` |
| `hasattr(obj, 'attr')` | Checks if attribute exists | `hasattr(obj, 'name')` |
| `getattr(obj, 'attr')` | Gets attribute value | `getattr(obj, 'name')` |
| `setattr(obj, 'attr', val)` | Sets attribute value | `setattr(obj, 'name', 'Alice')` |

### Example Comparison

```python
class Person:
    species = "Human"  # Class attribute
    
    def __init__(self, name):
        self.name = name  # Instance attribute

person = Person("Alice")

# dir() - shows everything
print("dir():", [a for a in dir(person) if not a.startswith('_')])

# vars() - shows only instance attributes
print("vars():", vars(person))

# type() - shows the class
print("type():", type(person))
```

**Output:**
```
dir(): ['name', 'species']
vars(): {'name': 'Alice'}
type(): <class '__main__.Person'>
```

---

## Practical Tips

### Tip 1: Create a Helper Function

```python
def show_public_attrs(obj):
    """Display only public attributes and methods"""
    return [attr for attr in dir(obj) if not attr.startswith('_')]

class Example:
    def __init__(self):
        self.x = 1
        self.y = 2
    
    def method(self):
        pass

obj = Example()
print(show_public_attrs(obj))  # ['method', 'x', 'y']
```

### Tip 2: Separate Attributes from Methods

```python
def categorize_members(obj):
    """Separate attributes from methods"""
    attrs = []
    methods = []
    
    for name in dir(obj):
        if not name.startswith('_'):
            attr = getattr(obj, name)
            if callable(attr):
                methods.append(name)
            else:
                attrs.append(name)
    
    return {'attributes': attrs, 'methods': methods}

class Car:
    def __init__(self):
        self.brand = "Toyota"
        self.speed = 0
    
    def accelerate(self):
        self.speed += 10

car = Car()
result = categorize_members(car)
print(result)
```

**Output:**
```python
{'attributes': ['brand', 'speed'], 'methods': ['accelerate']}
```

---

## Summary

- **`dir()`** returns a sorted list of all attributes and methods of an object
- Extremely useful for **exploration**, **debugging**, and **introspection**
- Includes **dunder methods** (like `__init__`, `__str__`)
- Includes **inherited** attributes from parent classes
- Shows **private** and **name-mangled** attributes
- Returns an **alphabetically sorted** list
- Can be filtered to show only public methods/attributes
- Without arguments, shows names in the **current scope**

The `dir()` function is one of the most essential tools for understanding and exploring Python objects!
