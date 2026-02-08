# Python's Class Object and Metaclasses

## Java's Class Object vs Python's Class Object

### Java's `Class` Object

In Java, every class has an associated `Class` object (an instance of `java.lang.Class`):

```java
// Java
public class Person {
    private String name;
}

// Getting the Class object (which is itself an object)
Class<?> personClass = Person.class;
Class<?> personClass2 = new Person().getClass();

// The Class object is an instance of java.lang.Class
System.out.println(personClass.getClass().getName());  // java.lang.Class

// Using reflection
String className = personClass.getName();
Method[] methods = personClass.getMethods();
```

**Key Point**: In Java, the `Class` object is a **separate object** that represents metadata about the class. The class definition itself is not directly an object you can manipulate.

### Python's Equivalent: Everything is an Object

In Python, **classes themselves are objects**. This is a fundamental difference from Java.

```python
# Python
class Person:
    def __init__(self, name):
        self.name = name

# The class itself is an object!
print(type(Person))  # <class 'type'>
print(isinstance(Person, object))  # True

# Getting class information
print(Person.__name__)  # 'Person'
print(Person.__bases__)  # (<class 'object'>,)
print(Person.__dict__)  # Class attributes and methods
```

---

## Understanding Python's Class Objects

### 1. Classes Are Objects of Type `type`

```python
class MyClass:
    pass

# The class is an instance of 'type'
print(type(MyClass))  # <class 'type'>

# 'type' is the metaclass (class of classes)
print(type(type))  # <class 'type'>
```

**Key Insight**: In Python, `type` is the **metaclass** that creates all classes.

### 2. How Class Objects Are Created

When you write a class definition, Python internally does this:

```python
# What you write:
class Person:
    species = "Human"
    
    def __init__(self, name):
        self.name = name

# What Python actually does (simplified):
Person = type(
    'Person',                    # Class name
    (object,),                   # Base classes
    {                            # Class attributes
        'species': 'Human',
        '__init__': lambda self, name: setattr(self, 'name', name)
    }
)
```

### 3. Creating Classes Dynamically with `type()`

You can create classes at runtime using `type()`:

```python
# Method 1: Normal class definition
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says Woof!"

# Method 2: Using type() - creates the same class
def dog_init(self, name):
    self.name = name

def dog_bark(self):
    return f"{self.name} says Woof!"

Dog = type(
    'Dog',                           # Class name
    (object,),                       # Base classes (tuple)
    {                                # Class dictionary
        '__init__': dog_init,
        'bark': dog_bark
    }
)

# Both work the same way
dog1 = Dog("Buddy")
print(dog1.bark())  # Buddy says Woof!
```

---

## Class Object Attributes and Methods

### Accessing Class Information

```python
class Person:
    """A class representing a person"""
    species = "Human"
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, I'm {self.name}"

# Class object attributes
print(Person.__name__)       # 'Person'
print(Person.__doc__)        # 'A class representing a person'
print(Person.__bases__)      # (<class 'object'>,)
print(Person.__module__)     # '__main__'
print(Person.__dict__)       # All class attributes and methods

# Class attributes
print(Person.species)        # 'Human'

# Check if it's a class
print(isinstance(Person, type))  # True
```

### Inspecting Class Members

```python
import inspect

class Example:
    class_var = 10
    
    def __init__(self):
        self.instance_var = 20
    
    def method(self):
        pass
    
    @classmethod
    def class_method(cls):
        pass
    
    @staticmethod
    def static_method():
        pass

# Get all members
print(dir(Example))

# Get methods only
methods = inspect.getmembers(Example, predicate=inspect.isfunction)
print(methods)

# Get class attributes
attrs = {k: v for k, v in Example.__dict__.items() 
         if not k.startswith('_') and not callable(v)}
print(attrs)  # {'class_var': 10}
```

---

## Metaclasses: The Class of Classes

### What is a Metaclass?

A **metaclass** is a class whose instances are classes.

```python
# type is the default metaclass
class MyClass:
    pass

print(type(MyClass))  # <class 'type'>
print(type(type))     # <class 'type'>

# Relationship:
# Instance → Class → Metaclass
obj = MyClass()
print(type(obj))           # <class '__main__.MyClass'>
print(type(type(obj)))     # <class 'type'>
```

### Creating Custom Metaclasses

```python
class MyMeta(type):
    """Custom metaclass"""
    
    def __new__(mcs, name, bases, attrs):
        print(f"Creating class: {name}")
        print(f"Base classes: {bases}")
        print(f"Attributes: {list(attrs.keys())}")
        
        # Modify the class before creation
        attrs['created_by'] = 'MyMeta'
        
        # Create the class
        cls = super().__new__(mcs, name, bases, attrs)
        return cls
    
    def __init__(cls, name, bases, attrs):
        print(f"Initializing class: {name}")
        super().__init__(name, bases, attrs)

# Use the custom metaclass
class MyClass(metaclass=MyMeta):
    x = 10
    
    def method(self):
        pass

# Output:
# Creating class: MyClass
# Base classes: ()
# Attributes: ['__module__', '__qualname__', 'x', 'method']
# Initializing class: MyClass

# Check the metaclass
print(type(MyClass))  # <class '__main__.MyMeta'>
print(MyClass.created_by)  # 'MyMeta'
```

---

## Practical Use Cases

### 1. Singleton Pattern with Metaclass

```python
class SingletonMeta(type):
    """Metaclass that creates singleton classes"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        print(f"Connecting to {connection_string}")

# Create instances
db1 = Database("localhost:5432")
db2 = Database("localhost:5432")

print(db1 is db2)  # True - same instance
```

### 2. Automatic Registration

```python
class RegistryMeta(type):
    """Metaclass that automatically registers classes"""
    registry = {}
    
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        # Register the class
        if name != 'Plugin':  # Don't register base class
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=RegistryMeta):
    """Base plugin class"""
    pass

class EmailPlugin(Plugin):
    def send(self):
        print("Sending email...")

class SMSPlugin(Plugin):
    def send(self):
        print("Sending SMS...")

# All plugins are automatically registered
print(RegistryMeta.registry)
# {'EmailPlugin': <class '__main__.EmailPlugin'>, 
#  'SMSPlugin': <class '__main__.SMSPlugin'>}

# Use the registry
for name, plugin_class in RegistryMeta.registry.items():
    plugin = plugin_class()
    plugin.send()
```

### 3. Validation and Enforcement

```python
class ValidatedMeta(type):
    """Metaclass that enforces class structure"""
    
    def __new__(mcs, name, bases, attrs):
        # Enforce that all classes have a 'validate' method
        if name != 'BaseModel' and 'validate' not in attrs:
            raise TypeError(f"Class {name} must implement 'validate' method")
        
        return super().__new__(mcs, name, bases, attrs)

class BaseModel(metaclass=ValidatedMeta):
    """Base model class"""
    pass

class User(BaseModel):
    def validate(self):
        print("Validating user...")

# This works
user = User()

# This would raise TypeError
# class Product(BaseModel):
#     pass
# TypeError: Class Product must implement 'validate' method
```

### 4. Attribute Modification

```python
class UpperAttrMeta(type):
    """Metaclass that converts all attribute names to uppercase"""
    
    def __new__(mcs, name, bases, attrs):
        uppercase_attrs = {}
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith('__'):
                uppercase_attrs[attr_name.upper()] = attr_value
            else:
                uppercase_attrs[attr_name] = attr_value
        
        return super().__new__(mcs, name, bases, uppercase_attrs)

class MyClass(metaclass=UpperAttrMeta):
    x = 10
    y = 20
    
    def method(self):
        return "Hello"

# Attributes are now uppercase
print(MyClass.X)  # 10
print(MyClass.Y)  # 20
print(MyClass.METHOD())  # Hello
```

---

## Class Methods and Static Methods

### Using the Class Object

```python
class MathOperations:
    pi = 3.14159
    
    @classmethod
    def circle_area(cls, radius):
        """Class method - receives the class as first argument"""
        return cls.pi * radius ** 2
    
    @staticmethod
    def add(a, b):
        """Static method - doesn't receive class or instance"""
        return a + b

# Call via class object
print(MathOperations.circle_area(5))  # 78.53975
print(MathOperations.add(10, 20))     # 30

# Can also call via instance
obj = MathOperations()
print(obj.circle_area(5))  # 78.53975
```

---

## Comparison: Java vs Python

| Aspect | Java | Python |
|--------|------|--------|
| **Class object type** | `java.lang.Class` | `type` |
| **Getting class** | `obj.getClass()` or `ClassName.class` | `type(obj)` or `obj.__class__` |
| **Classes are objects** | No (classes are not first-class) | Yes (classes are objects) |
| **Metaclass** | No direct equivalent | `type` (can be customized) |
| **Dynamic class creation** | Complex (requires ClassLoader) | Simple (`type()` function) |
| **Reflection** | `java.lang.reflect` package | Built-in (`__dict__`, `dir()`, `getattr()`) |

---

## When to Use Class Objects and Metaclasses

### ✅ Use Class Objects When:

1. **Introspection and Reflection**
   ```python
   def describe_class(cls):
       print(f"Class: {cls.__name__}")
       print(f"Bases: {cls.__bases__}")
       print(f"Methods: {[m for m in dir(cls) if not m.startswith('_')]}")
   ```

2. **Factory Patterns**
   ```python
   def create_instance(class_name, *args):
       cls = globals()[class_name]
       return cls(*args)
   ```

3. **Class Decorators**
   ```python
   def add_timestamp(cls):
       cls.created_at = datetime.now()
       return cls
   
   @add_timestamp
   class MyClass:
       pass
   ```

### ✅ Use Metaclasses When:

1. **Automatic Registration** (like Django models, Flask routes)
2. **Singleton Pattern** (ensure only one instance)
3. **Validation and Enforcement** (enforce class structure)
4. **Attribute Modification** (modify class attributes automatically)
5. **ORM Frameworks** (like SQLAlchemy)
6. **API Frameworks** (like Django REST Framework)

### ❌ Don't Use Metaclasses When:

- Simple class decorators would work
- You're just learning Python (start with basics first)
- The problem can be solved with inheritance
- You don't fully understand them (they add complexity)

---

## Summary

### Key Concepts

1. **In Python, classes are objects** of type `type`
2. **`type` is the default metaclass** that creates all classes
3. **Classes can be created dynamically** using `type()`
4. **Metaclasses control class creation** (like `__new__` and `__init__` for classes)
5. **Class objects have attributes** like `__name__`, `__bases__`, `__dict__`

### Hierarchy

```
object (base of all classes)
  ↑
type (metaclass - creates classes)
  ↑
CustomMeta (custom metaclass)
  ↑
MyClass (class created by metaclass)
  ↑
instance (object created by class)
```

### Best Practice

- Use **class objects** for introspection and reflection
- Use **metaclasses** sparingly for framework-level features
- For most cases, **regular classes and decorators** are sufficient
- Metaclasses are powerful but add complexity - use only when necessary
