# Python Variable Scoping: A Comprehensive Guide

## Introduction: Python vs Java Execution Model

### Java's Strict Structure
In Java, **everything must be inside a class**:

```java
// Java - Everything must be in a class
public class Main {
    // Class-level variables
    static int count = 0;
    
    // Static initialization block
    static {
        System.out.println("Static block executed");
        count = 10;
    }
    
    // Instance initialization block
    {
        System.out.println("Instance block executed");
    }
    
    // Methods
    public static void main(String[] args) {
        System.out.println("Main method");
    }
}
```

### Python's Flexible Structure
In Python, **code can exist at the module level** (top-level of the file):

```python
# Python - Code can exist directly in the file

# Module-level variables (executed immediately when file is imported/run)
count = 0
print("This runs immediately when the file is loaded")

# Module-level code
for i in range(3):
    print(f"Loop iteration {i}")

# Class definitions
class MyClass:
    class_var = 10
    
    def __init__(self):
        self.instance_var = 20

# More module-level code
def my_function():
    local_var = 30
    return local_var

# This executes immediately
result = my_function()
print(f"Result: {result}")

# Object creation at module level
obj = MyClass()
```

**Key Difference**: Python files are **scripts that execute from top to bottom** when imported or run, whereas Java requires explicit entry points (main method).

---

## Python's Execution Model

### How Python Source Files Work

When you run or import a Python file:

1. **Top-to-bottom execution**: Python reads and executes code sequentially
2. **Definitions are executed**: Class and function definitions are executed (creating the class/function objects)
3. **Module-level code runs immediately**: Any code not inside a function/class runs right away
4. **Namespace creation**: A module namespace is created to store all defined names

### Example: Understanding Execution Order

```python
# example.py
print("1. File starts executing")

# Module-level variable
MODULE_VAR = "I'm at module level"
print(f"2. MODULE_VAR defined: {MODULE_VAR}")

# Class definition (executed, but methods don't run yet)
class Person:
    print("3. Inside Person class definition")
    class_var = "Class variable"
    
    def __init__(self, name):
        print(f"5. __init__ called for {name}")
        self.name = name
    
    def greet(self):
        print(f"Hello from {self.name}")

print("4. Person class defined")

# Object creation (now __init__ runs)
person = Person("Alice")

# Method call
person.greet()

print("6. File execution complete")
```

**Output:**
```
1. File starts executing
2. MODULE_VAR defined: I'm at module level
3. Inside Person class definition
4. Person class defined
5. __init__ called for Alice
Hello from Alice
6. File execution complete
```

---

## The LEGB Rule: Python's Scope Resolution

Python uses the **LEGB rule** to resolve variable names:

- **L** - Local (function/method scope)
- **E** - Enclosing (outer function scope)
- **G** - Global (module scope)
- **B** - Built-in (Python's built-in namespace)

### Visual Representation

```
Built-in Scope (B)
    ↑
Global/Module Scope (G)
    ↑
Enclosing Function Scope (E)
    ↑
Local Function Scope (L)
```

Python searches from **innermost to outermost** scope.

---

## 1. Local Scope (L)

Variables defined inside a function or method.

```python
def calculate():
    # Local variables
    x = 10
    y = 20
    result = x + y
    return result

print(calculate())  # 30
# print(x)  # NameError: name 'x' is not defined
```

### Local Scope in Methods

```python
class Calculator:
    def add(self, a, b):
        # a, b, and result are local to this method
        result = a + b
        return result
    
    def multiply(self, a, b):
        # Different local scope - can't access add's variables
        result = a * b
        return result

calc = Calculator()
print(calc.add(5, 3))      # 8
print(calc.multiply(5, 3))  # 15
```

### Local Scope in Loops and Conditionals

**Important**: In Python, loops and conditionals **do NOT create new scopes**:

```python
def demo():
    if True:
        x = 10  # Still in function's local scope
    
    for i in range(3):
        y = i  # Still in function's local scope
    
    # Both x and y are accessible here!
    print(f"x: {x}, y: {y}, i: {i}")

demo()  # x: 10, y: 2, i: 2
```

**Contrast with Java**:
```java
// Java - blocks create scopes
public void demo() {
    if (true) {
        int x = 10;  // Only accessible in this block
    }
    // System.out.println(x);  // Error: x not in scope
}
```

---

## 2. Enclosing Scope (E)

Variables in outer functions (for nested functions).

```python
def outer_function():
    outer_var = "I'm in outer function"
    
    def inner_function():
        # Can access outer_var from enclosing scope
        print(f"Inner can see: {outer_var}")
    
    inner_function()
    return outer_var

result = outer_function()
```

**Output:**
```
Inner can see: I'm in outer function
```

### Multiple Levels of Enclosing Scope

```python
def level1():
    var1 = "Level 1"
    
    def level2():
        var2 = "Level 2"
        
        def level3():
            var3 = "Level 3"
            # Can access all enclosing scopes
            print(f"{var1}, {var2}, {var3}")
        
        level3()
    
    level2()

level1()  # Level 1, Level 2, Level 3
```

### Modifying Enclosing Variables with `nonlocal`

```python
def counter():
    count = 0  # Enclosing scope variable
    
    def increment():
        nonlocal count  # Declare we want to modify enclosing scope
        count += 1
        return count
    
    return increment

counter_func = counter()
print(counter_func())  # 1
print(counter_func())  # 2
print(counter_func())  # 3
```

**Without `nonlocal`**:
```python
def counter():
    count = 0
    
    def increment():
        # This creates a NEW local variable instead of modifying enclosing
        count = count + 1  # UnboundLocalError!
        return count
    
    return increment
```

---

## 3. Global Scope (G)

Variables defined at the module level (top of the file).

```python
# Module level (global scope)
GLOBAL_VAR = "I'm global"
counter = 0

def function1():
    # Reading global variable (no declaration needed)
    print(GLOBAL_VAR)

def function2():
    # Modifying global variable (needs 'global' keyword)
    global counter
    counter += 1
    print(f"Counter: {counter}")

function1()  # I'm global
function2()  # Counter: 1
function2()  # Counter: 2
```

### Global Variables Across Multiple Definitions

```python
# config.py - Module-level variables
DATABASE_URL = "localhost:5432"
DEBUG_MODE = True
MAX_CONNECTIONS = 100

class DatabaseManager:
    def connect(self):
        # Accessing global variable
        print(f"Connecting to {DATABASE_URL}")
        if DEBUG_MODE:
            print("Debug mode enabled")

def configure(url):
    global DATABASE_URL
    DATABASE_URL = url

# Module-level code
db = DatabaseManager()
db.connect()

configure("production:5432")
db.connect()
```

**Output:**
```
Connecting to localhost:5432
Debug mode enabled
Connecting to production:5432
Debug mode enabled
```

---

## 4. Built-in Scope (B)

Python's built-in functions and exceptions.

```python
# These are all in the built-in scope
print(len([1, 2, 3]))      # len is built-in
print(max(5, 10))          # max is built-in
print(isinstance(5, int))  # isinstance is built-in

# You can shadow built-in names (but shouldn't!)
def len(x):
    return "I'm not the real len!"

print(len([1, 2, 3]))  # I'm not the real len!

# Access original built-in
import builtins
print(builtins.len([1, 2, 3]))  # 3
```

---

## Complete LEGB Example

```python
# Built-in: print, len, etc.

# Global scope
global_var = "Global"

def outer():
    # Enclosing scope
    enclosing_var = "Enclosing"
    
    def inner():
        # Local scope
        local_var = "Local"
        
        # Python searches: Local → Enclosing → Global → Built-in
        print(local_var)      # Found in Local
        print(enclosing_var)  # Found in Enclosing
        print(global_var)     # Found in Global
        print(len([1, 2]))    # Found in Built-in
    
    inner()

outer()
```

**Output:**
```
Local
Enclosing
Global
2
```

---

## Class and Instance Scope

Classes introduce their own namespace, separate from LEGB.

### Class Variables vs Instance Variables

```python
class Company:
    # Class variable (shared by all instances)
    company_name = "TechCorp"
    employee_count = 0
    
    def __init__(self, name, role):
        # Instance variables (unique to each instance)
        self.name = name
        self.role = role
        
        # Modifying class variable
        Company.employee_count += 1
    
    def display_info(self):
        # Accessing both class and instance variables
        print(f"{self.name} works at {Company.company_name} as {self.role}")

emp1 = Company("Alice", "Developer")
emp2 = Company("Bob", "Designer")

emp1.display_info()  # Alice works at TechCorp as Developer
emp2.display_info()  # Bob works at TechCorp as Designer

print(f"Total employees: {Company.employee_count}")  # 2
```

### Class Scope and Method Scope

```python
class Example:
    class_var = "Class level"
    
    def method(self):
        local_var = "Method level"
        
        # Accessing class variable
        print(self.class_var)      # Via instance
        print(Example.class_var)   # Via class
        
        # Accessing instance variable
        print(self.instance_var)
        
        # Accessing local variable
        print(local_var)
    
    def __init__(self):
        self.instance_var = "Instance level"

obj = Example()
obj.method()
```

---

## How Multiple Classes and Variables Work in a Single File

### Practical Example: Enterprise Application Module

```python
# app.py - A complete module with multiple components

# ============================================
# MODULE-LEVEL CONFIGURATION (Global Scope)
# ============================================
APP_NAME = "Enterprise CRM"
VERSION = "1.0.0"
DEBUG = True

# Module-level imports
from datetime import datetime
import logging

# Module-level initialization
logger = logging.getLogger(__name__)
if DEBUG:
    logger.setLevel(logging.DEBUG)

print(f"Loading {APP_NAME} v{VERSION}")

# ============================================
# UTILITY FUNCTIONS (Global Scope)
# ============================================
def log_event(message):
    """Module-level utility function"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def validate_email(email):
    """Another utility function"""
    return "@" in email and "." in email

# ============================================
# CLASS DEFINITIONS
# ============================================

class User:
    """User class with class and instance variables"""
    
    # Class variables (shared across all users)
    total_users = 0
    user_roles = ["admin", "manager", "employee"]
    
    def __init__(self, name, email, role="employee"):
        # Instance variables (unique to each user)
        self.name = name
        self.email = email
        self.role = role
        self.created_at = datetime.now()
        
        # Modify class variable
        User.total_users += 1
        
        # Use module-level function
        log_event(f"User created: {name}")
    
    def validate(self):
        """Instance method"""
        # Access module-level function
        if not validate_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")
        
        # Access class variable
        if self.role not in User.user_roles:
            raise ValueError(f"Invalid role: {self.role}")
        
        return True
    
    @classmethod
    def get_user_count(cls):
        """Class method - accesses class variables"""
        return cls.total_users
    
    @staticmethod
    def is_valid_role(role):
        """Static method - doesn't access instance or class"""
        return role in User.user_roles


class Database:
    """Database connection class"""
    
    # Class variable
    connection_pool = []
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = False
        log_event(f"Database object created for {host}:{port}")
    
    def connect(self):
        """Connect to database"""
        # Access module-level variable
        if DEBUG:
            log_event(f"Connecting to {self.host}:{self.port}")
        
        self.connected = True
        Database.connection_pool.append(self)
    
    def disconnect(self):
        """Disconnect from database"""
        self.connected = False
        if self in Database.connection_pool:
            Database.connection_pool.remove(self)


class UserManager:
    """Manager class that uses other classes"""
    
    def __init__(self, database):
        self.database = database
        self.users = []
        log_event("UserManager initialized")
    
    def add_user(self, name, email, role="employee"):
        """Add a new user"""
        # Create instance of User class
        user = User(name, email, role)
        
        # Validate using instance method
        user.validate()
        
        # Store in instance variable
        self.users.append(user)
        
        # Access module-level variable
        if DEBUG:
            log_event(f"User added: {name} (Total: {len(self.users)})")
        
        return user
    
    def get_statistics(self):
        """Get user statistics"""
        return {
            "total_users": User.get_user_count(),
            "managed_users": len(self.users),
            "app_name": APP_NAME,  # Access module-level variable
            "version": VERSION
        }


# ============================================
# MODULE-LEVEL EXECUTION CODE
# ============================================

# This code runs immediately when the module is imported/executed
print("Initializing application components...")

# Create database connection
db = Database("localhost", 5432)
db.connect()

# Create user manager
manager = UserManager(db)

# Add some users
try:
    user1 = manager.add_user("Alice Smith", "alice@example.com", "admin")
    user2 = manager.add_user("Bob Jones", "bob@example.com", "manager")
    user3 = manager.add_user("Charlie Brown", "charlie@example.com")
except ValueError as e:
    log_event(f"Error: {e}")

# Display statistics
stats = manager.get_statistics()
print(f"\nApplication Statistics:")
for key, value in stats.items():
    print(f"  {key}: {value}")

# Module-level variable tracking state
app_initialized = True

print(f"\n{APP_NAME} initialization complete!")

# ============================================
# CONDITIONAL EXECUTION
# ============================================

if __name__ == "__main__":
    # This only runs if the file is executed directly
    # Not when imported as a module
    print("\nRunning as main program...")
    
    # Additional user for testing
    user4 = manager.add_user("Diana Prince", "diana@example.com", "admin")
    
    print(f"\nFinal user count: {User.get_user_count()}")
    print(f"Database connections: {len(Database.connection_pool)}")
```

### Execution Output

```
Loading Enterprise CRM v1.0.0
Initializing application components...
[2026-02-08 05:36:32] Database object created for localhost:5432
[2026-02-08 05:36:32] Connecting to localhost:5432
[2026-02-08 05:36:32] UserManager initialized
[2026-02-08 05:36:32] User created: Alice Smith
[2026-02-08 05:36:32] User added: Alice Smith (Total: 1)
[2026-02-08 05:36:32] User created: Bob Jones
[2026-02-08 05:36:32] User added: Bob Jones (Total: 2)
[2026-02-08 05:36:32] User created: Charlie Brown
[2026-02-08 05:36:32] User added: Charlie Brown (Total: 3)

Application Statistics:
  total_users: 3
  managed_users: 3
  app_name: Enterprise CRM
  version: 1.0.0

Enterprise CRM initialization complete!
```

---

## Scope Best Practices for Enterprise Applications

### 1. Module Organization

```python
# config.py - Configuration module
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "myapp"
}

API_SETTINGS = {
    "timeout": 30,
    "retries": 3
}

# models.py - Data models
class User:
    pass

class Product:
    pass

# services.py - Business logic
from config import DATABASE_CONFIG
from models import User

class UserService:
    def __init__(self):
        self.db_config = DATABASE_CONFIG
```

### 2. Avoid Global State When Possible

**❌ Bad: Mutable global state**
```python
# Bad - mutable global state
current_users = []

def add_user(user):
    current_users.append(user)  # Modifying global state
```

**✅ Good: Encapsulate state in classes**
```python
# Good - encapsulated state
class UserRegistry:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)

registry = UserRegistry()
```

### 3. Use `__name__ == "__main__"` Guard

```python
# module.py

class MyClass:
    pass

def my_function():
    pass

# Module-level code that should always run
CONSTANT = 100

# Code that should only run when executed directly
if __name__ == "__main__":
    # Testing code
    obj = MyClass()
    my_function()
```

### 4. Explicit is Better Than Implicit

```python
# ✅ Good - explicit global declaration
def increment_counter():
    global counter
    counter += 1

# ✅ Good - explicit nonlocal declaration
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
    return inner

# ✅ Good - pass as parameter
def process_data(config):
    # Use config parameter instead of global
    return config["setting"]
```

---

## Summary

### Key Differences: Python vs Java

| Aspect | Java | Python |
|--------|------|--------|
| **Structure** | Everything in classes | Code can be at module level |
| **Execution** | Explicit entry point (main) | Top-to-bottom execution |
| **Block Scope** | Blocks create scopes | Only functions create scopes |
| **Global Variables** | Must be class static | Module-level variables |

### Python Scope Types

1. **Local (L)**: Inside functions/methods
2. **Enclosing (E)**: Outer functions (for nested functions)
3. **Global (G)**: Module level
4. **Built-in (B)**: Python's built-in namespace

### Resolution Order

Python searches: **Local → Enclosing → Global → Built-in**

### Key Takeaways

- Python files are **executable scripts** that run top-to-bottom
- **Loops and conditionals don't create scopes** (unlike Java)
- Use `global` to modify module-level variables
- Use `nonlocal` to modify enclosing function variables
- Class and instance variables are separate from LEGB
- Module-level code runs when the file is imported/executed
- Use `if __name__ == "__main__"` for script-specific code
