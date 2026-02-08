# Functions vs Methods: A Comprehensive Guide

## General Difference

### Function
A **function** is a standalone block of code that performs a specific task. It exists independently and is not tied to any object or class.

**Characteristics:**
- Standalone, independent code block
- Called by its name directly
- Not associated with any object or class
- Can be defined at module/global level

### Method
A **method** is a function that is associated with an object or class. It operates on the data contained within the object.

**Characteristics:**
- Belongs to a class or object
- Called on an object (or class)
- Has access to object's data (via `self`, `this`, etc.)
- First parameter typically references the object

---

## Visual Comparison

```
Function:
┌─────────────┐
│  function() │  ← Standalone
└─────────────┘

Method:
┌──────────────────┐
│     Object       │
│  ┌────────────┐  │
│  │  method()  │  │  ← Belongs to object
│  └────────────┘  │
└──────────────────┘
```

---

## Python: Functions vs Methods

### Functions in Python

```python
# Standalone function
def greet(name):
    return f"Hello, {name}!"

# Call directly
result = greet("Alice")
print(result)  # Hello, Alice!

# Function is an object itself
print(type(greet))  # <class 'function'>
```

### Methods in Python

```python
class Person:
    def __init__(self, name):
        self.name = name
    
    # Instance method - operates on instance
    def greet(self):
        return f"Hello, I'm {self.name}!"
    
    # Class method - operates on class
    @classmethod
    def species(cls):
        return "Human"
    
    # Static method - doesn't access instance or class
    @staticmethod
    def is_adult(age):
        return age >= 18

# Instance method - needs an object
person = Person("Alice")
print(person.greet())  # Hello, I'm Alice!

# Class method - called on class
print(Person.species())  # Human

# Static method - like a function but in class namespace
print(Person.is_adult(20))  # True
```

### Key Differences in Python

```python
# Function
def standalone_function():
    return "I'm a function"

# Method
class MyClass:
    def instance_method(self):
        return "I'm a method"

# Calling
print(standalone_function())  # Direct call

obj = MyClass()
print(obj.instance_method())  # Called on object

# Type checking
print(type(standalone_function))  # <class 'function'>
print(type(obj.instance_method))  # <class 'method'>
```

### Bound vs Unbound Methods

```python
class Calculator:
    def add(self, a, b):
        return a + b

# Unbound - accessed via class
print(Calculator.add)  # <function Calculator.add at 0x...>

# Bound - accessed via instance
calc = Calculator()
print(calc.add)  # <bound method Calculator.add of <__main__.Calculator object>>

# Calling unbound (must pass instance manually)
result = Calculator.add(calc, 5, 3)  # 8

# Calling bound (instance passed automatically)
result = calc.add(5, 3)  # 8
```

---

## Java: Functions vs Methods

### No Standalone Functions in Java

Java doesn't have standalone functions - everything must be in a class. What might be called "functions" in other languages are **static methods** in Java.

```java
public class MathUtils {
    // Static method - acts like a function
    public static int add(int a, int b) {
        return a + b;
    }
    
    // Instance method - true method
    public int multiply(int a, int b) {
        return a * b;
    }
}

// Usage
// "Function-like" - called on class
int sum = MathUtils.add(5, 3);

// Method - called on instance
MathUtils utils = new MathUtils();
int product = utils.multiply(5, 3);
```

### Java Methods

```java
public class Person {
    private String name;
    
    // Constructor
    public Person(String name) {
        this.name = name;
    }
    
    // Instance method - operates on instance data
    public String greet() {
        return "Hello, I'm " + this.name;
    }
    
    // Static method - doesn't access instance data
    public static String species() {
        return "Human";
    }
}

// Usage
Person person = new Person("Alice");
System.out.println(person.greet());  // Instance method

System.out.println(Person.species());  // Static method (function-like)
```

---

## JavaScript: Functions vs Methods

### Functions in JavaScript

```javascript
// Function declaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Function expression
const greetFunc = function(name) {
    return `Hello, ${name}!`;
};

// Arrow function
const greetArrow = (name) => `Hello, ${name}!`;

// All are standalone functions
console.log(greet("Alice"));
console.log(greetFunc("Bob"));
console.log(greetArrow("Charlie"));
```

### Methods in JavaScript

```javascript
// Object literal with methods
const person = {
    name: "Alice",
    
    // Method
    greet: function() {
        return `Hello, I'm ${this.name}!`;
    },
    
    // Shorthand method syntax
    introduce() {
        return `My name is ${this.name}`;
    },
    
    // Arrow function (careful with 'this'!)
    arrowMethod: () => {
        // 'this' doesn't refer to person here!
        return `Arrow function`;
    }
};

console.log(person.greet());      // Hello, I'm Alice!
console.log(person.introduce());  // My name is Alice
```

### Class Methods in JavaScript (ES6+)

```javascript
class Person {
    constructor(name) {
        this.name = name;
    }
    
    // Instance method
    greet() {
        return `Hello, I'm ${this.name}!`;
    }
    
    // Static method (function-like)
    static species() {
        return "Human";
    }
}

// Instance method
const person = new Person("Alice");
console.log(person.greet());  // Hello, I'm Alice!

// Static method
console.log(Person.species());  // Human
```

### JavaScript's Flexible Nature

```javascript
// Function can become a method
function greet() {
    return `Hello, I'm ${this.name}!`;
}

const person1 = { name: "Alice" };
const person2 = { name: "Bob" };

// Assign function as method
person1.greet = greet;
person2.greet = greet;

console.log(person1.greet());  // Hello, I'm Alice!
console.log(person2.greet());  // Hello, I'm Bob!
```

---

## Detailed Comparison Across Languages

### Syntax Comparison

| Language | Function | Method |
|----------|----------|--------|
| **Python** | `def func():` | `def method(self):` |
| **Java** | `static void func()` | `void method()` |
| **JavaScript** | `function func()` | `method()` in class/object |

### Calling Comparison

```python
# Python
result = function()           # Function
result = obj.method()         # Method
result = Class.static_method() # Static method
```

```java
// Java
int result = ClassName.staticMethod();  // Static (function-like)
int result = object.method();           // Instance method
```

```javascript
// JavaScript
let result = func();              // Function
let result = obj.method();        // Method
let result = Class.staticMethod(); // Static method
```

---

## Key Differences Summary

### 1. Association

**Function:**
- Independent, standalone
- Not tied to any object or class
- Exists in global/module scope

**Method:**
- Belongs to a class or object
- Operates on object's data
- Part of object's behavior

### 2. Access to Data

**Function:**
```python
# Python - no access to object data
def calculate_area(length, width):
    return length * width

area = calculate_area(5, 10)
```

**Method:**
```python
# Python - has access to object data via self
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def calculate_area(self):
        return self.length * self.width

rect = Rectangle(5, 10)
area = rect.calculate_area()
```

### 3. First Parameter

**Python:**
```python
# Function - no special first parameter
def function(param1, param2):
    pass

# Method - first parameter is self
class MyClass:
    def method(self, param1, param2):
        pass
```

**Java:**
```java
// Static method - no implicit parameter
public static void function(int param) { }

// Instance method - implicit 'this' parameter
public void method(int param) {
    // 'this' refers to current object
}
```

**JavaScript:**
```javascript
// Function - 'this' depends on how it's called
function func() {
    console.log(this);
}

// Method - 'this' refers to the object
const obj = {
    method() {
        console.log(this);  // refers to obj
    }
};
```

---

## Special Cases

### Python: Functions as First-Class Objects

```python
# Functions can be assigned to variables
def greet(name):
    return f"Hello, {name}!"

my_func = greet
print(my_func("Alice"))  # Hello, Alice!

# Functions can be passed as arguments
def apply_function(func, value):
    return func(value)

result = apply_function(greet, "Bob")
print(result)  # Hello, Bob!
```

### JavaScript: Method Borrowing

```javascript
const person1 = {
    name: "Alice",
    greet() {
        return `Hello, I'm ${this.name}`;
    }
};

const person2 = { name: "Bob" };

// Borrow method from person1
console.log(person1.greet.call(person2));  // Hello, I'm Bob
```

### Java: Method References

```java
// Java 8+ - method references
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// Instance method reference
names.forEach(System.out::println);

// Static method reference
names.stream().map(String::toUpperCase);
```

---

## Comparison Table

| Aspect | Function | Method |
|--------|----------|--------|
| **Definition** | Standalone code block | Part of a class/object |
| **Association** | Independent | Belongs to class/object |
| **Calling** | Direct by name | On object/class |
| **Data Access** | Only parameters | Object data + parameters |
| **First Parameter** | User-defined | `self`/`this` (implicit/explicit) |
| **Namespace** | Global/module | Class namespace |
| **Python Type** | `function` | `method` |

---

## Best Practices

### When to Use Functions

✅ Utility operations not tied to specific objects
✅ Pure computations without state
✅ Helper functions for general use
✅ Mathematical operations

```python
# Good use of function
def calculate_tax(amount, rate):
    return amount * rate

def validate_email(email):
    return "@" in email and "." in email
```

### When to Use Methods

✅ Operations on object data
✅ Behavior specific to a class
✅ Need access to instance state
✅ Object-oriented design

```python
# Good use of method
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
```

---

## Summary

### Functions
- Standalone, independent
- Called directly by name
- No implicit object reference
- Exist at module/global level

### Methods
- Belong to classes/objects
- Called on instances or classes
- Have implicit object reference (`self`, `this`)
- Part of object's behavior

### Language Differences
- **Python**: Clear distinction, both supported
- **Java**: Everything in classes, static methods act like functions
- **JavaScript**: Very flexible, functions can become methods
