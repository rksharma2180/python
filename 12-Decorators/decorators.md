# Python Decorators: A Complete Guide

## Table of Contents
1. [What are Decorators?](#what-are-decorators)
2. [Purpose of Decorators](#purpose-of-decorators)
3. [How Decorators Work](#how-decorators-work)
4. [Types of Decorators](#types-of-decorators)
5. [Advanced Decorator Concepts](#advanced-decorator-concepts)
6. [Common Use Cases](#common-use-cases)
7. [Common Mistakes](#common-mistakes)
8. [Best Practices](#best-practices)
9. [Real-World Examples](#real-world-examples)

---

## What are Decorators?

**Decorators** are a powerful feature in Python that allow you to modify or enhance the behavior of functions or classes without permanently modifying their source code. They are essentially functions that take another function as an argument and return a new function with added functionality.

### Key Characteristics

- **Higher-Order Functions**: Functions that take other functions as arguments
- **Wrapper Pattern**: Wrap existing functions with additional behavior
- **Syntactic Sugar**: Use `@decorator_name` syntax for clean, readable code
- **Non-Invasive**: Don't modify the original function's code
- **Reusable**: Can be applied to multiple functions

### Basic Syntax

```python
# Without decorator syntax
def my_function():
    print("Hello")

my_function = decorator(my_function)

# With decorator syntax (syntactic sugar)
@decorator
def my_function():
    print("Hello")
```

---

## Purpose of Decorators

Decorators serve several important purposes in Python:

### 1. **Code Reusability**
Apply common functionality to multiple functions without repeating code.

### 2. **Separation of Concerns**
Keep core business logic separate from cross-cutting concerns (logging, timing, authentication).

### 3. **Code Readability**
Make code more readable and maintainable with clear, declarative syntax.

### 4. **Aspect-Oriented Programming**
Add behavior to existing code without modifying the code itself.

### 5. **Framework Integration**
Used extensively in frameworks like Flask, Django, FastAPI for routing, authentication, etc.

---

## How Decorators Work

### Understanding First-Class Functions

In Python, functions are first-class objects, meaning they can be:
- Assigned to variables
- Passed as arguments
- Returned from other functions

```python
# Functions are objects
def greet():
    return "Hello!"

# Assign to variable
say_hello = greet
print(say_hello())  # Output: Hello!

# Pass as argument
def execute_function(func):
    return func()

print(execute_function(greet))  # Output: Hello!

# Return from function
def get_greeting_function():
    def greet():
        return "Hi there!"
    return greet

my_func = get_greeting_function()
print(my_func())  # Output: Hi there!
```

### Basic Decorator Structure

```python
def my_decorator(func):
    """Basic decorator structure"""
    def wrapper():
        # Code before the function call
        print("Before function execution")
        
        # Call the original function
        result = func()
        
        # Code after the function call
        print("After function execution")
        
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before function execution
# Hello!
# After function execution
```

### Step-by-Step Execution

```python
# What happens behind the scenes:

# 1. Define the decorator
def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

# 2. Define the function
def say_hello():
    print("Hello!")

# 3. Apply decorator (this is what @ does)
say_hello = my_decorator(say_hello)

# 4. Call the decorated function
say_hello()
# The wrapper function is actually called, which:
# - Prints "Before"
# - Calls the original say_hello()
# - Prints "After"
```

---

## Types of Decorators

### 1. **Function Decorators**

Decorators that modify or enhance functions.

#### a) Simple Function Decorator

```python
def uppercase_decorator(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@uppercase_decorator
def greet():
    return "hello, world!"

print(greet())  # Output: HELLO, WORLD!
```

#### b) Decorator with Arguments

```python
def repeat(times):
    """Decorator factory that repeats function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

#### c) Decorator Preserving Function Metadata

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        print("Decorator executed")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Greet someone by name"""
    return f"Hello, {name}!"

print(greet.__name__)  # Output: greet (not wrapper)
print(greet.__doc__)   # Output: Greet someone by name
```

### 2. **Class Decorators**

Decorators that modify or enhance classes.

```python
def add_str_method(cls):
    """Add a __str__ method to a class"""
    def __str__(self):
        return f"{cls.__name__} instance with attributes: {self.__dict__}"
    cls.__str__ = __str__
    return cls

@add_str_method
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("Alice", 30)
print(person)  # Output: Person instance with attributes: {'name': 'Alice', 'age': 30}
```

### 3. **Method Decorators**

Decorators applied to class methods.

#### a) Instance Method Decorator

```python
def method_logger(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__} on {self.__class__.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class Calculator:
    @method_logger
    def add(self, a, b):
        return a + b

calc = Calculator()
result = calc.add(5, 3)
# Output: Calling add on Calculator
print(result)  # Output: 8
```

#### b) Built-in Method Decorators

```python
class MyClass:
    class_variable = "I'm a class variable"
    
    def __init__(self, value):
        self.instance_variable = value
    
    # Regular instance method
    def instance_method(self):
        return f"Instance method: {self.instance_variable}"
    
    # Class method - receives class as first argument
    @classmethod
    def class_method(cls):
        return f"Class method: {cls.class_variable}"
    
    # Static method - doesn't receive self or cls
    @staticmethod
    def static_method(x, y):
        return f"Static method: {x + y}"
    
    # Property decorator - access method like an attribute
    @property
    def value(self):
        return self.instance_variable
    
    # Setter for property
    @value.setter
    def value(self, new_value):
        self.instance_variable = new_value

# Usage
obj = MyClass(42)
print(obj.instance_method())      # Instance method: 42
print(MyClass.class_method())     # Class method: I'm a class variable
print(MyClass.static_method(5, 3))# Static method: 8
print(obj.value)                  # 42 (accessed like attribute)
obj.value = 100                   # Set using property setter
print(obj.value)                  # 100
```

### 4. **Decorator Classes**

Using classes as decorators.

```python
class CountCalls:
    """Decorator class to count function calls"""
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # Call 1 to say_hello
say_hello()  # Call 2 to say_hello
say_hello()  # Call 3 to say_hello
```

### 5. **Chained/Stacked Decorators**

Multiple decorators applied to a single function.

```python
def bold(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def italic(func):
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper

@bold
@italic
def greet():
    return "Hello!"

print(greet())  # Output: <b><i>Hello!</i></b>

# Execution order (bottom to top):
# 1. italic decorator wraps greet
# 2. bold decorator wraps the result
# Equivalent to: bold(italic(greet))()
```

### 6. **Parameterized Decorators**

Decorators that accept arguments.

```python
def prefix_decorator(prefix):
    """Decorator factory with parameters"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f"{prefix}: {result}"
        return wrapper
    return decorator

@prefix_decorator("INFO")
def log_message(msg):
    return msg

@prefix_decorator("ERROR")
def error_message(msg):
    return msg

print(log_message("System started"))   # Output: INFO: System started
print(error_message("File not found")) # Output: ERROR: File not found
```

---

## Advanced Decorator Concepts

### 1. **Decorators with Optional Arguments**

```python
from functools import wraps

def optional_decorator(func=None, *, prefix="DEFAULT"):
    """Decorator that works with or without arguments"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            return f"{prefix}: {result}"
        return wrapper
    
    if func is None:
        # Called with arguments: @optional_decorator(prefix="INFO")
        return decorator
    else:
        # Called without arguments: @optional_decorator
        return decorator(func)

# Without arguments
@optional_decorator
def message1():
    return "Hello"

# With arguments
@optional_decorator(prefix="INFO")
def message2():
    return "World"

print(message1())  # Output: DEFAULT: Hello
print(message2())  # Output: INFO: World
```

### 2. **Decorators with State**

```python
from functools import wraps

def rate_limiter(max_calls, time_window):
    """Limit function calls within a time window"""
    import time
    
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside time window
            calls[:] = [call for call in calls if now - call < time_window]
            
            if len(calls) >= max_calls:
                raise Exception(f"Rate limit exceeded: {max_calls} calls per {time_window}s")
            
            calls.append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@rate_limiter(max_calls=3, time_window=10)
def api_call():
    print("API called")

# First 3 calls work
api_call()  # Works
api_call()  # Works
api_call()  # Works
# api_call()  # Would raise exception
```

### 3. **Class-Based Decorators with Arguments**

```python
class Retry:
    """Decorator class with arguments to retry failed operations"""
    def __init__(self, max_attempts=3, delay=1):
        self.max_attempts = max_attempts
        self.delay = delay
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            attempts = 0
            while attempts < self.max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= self.max_attempts:
                        raise
                    print(f"Attempt {attempts} failed: {e}. Retrying...")
                    time.sleep(self.delay)
        return wrapper

@Retry(max_attempts=3, delay=2)
def unstable_operation():
    import random
    if random.random() < 0.7:
        raise Exception("Random failure")
    return "Success!"
```

### 4. **Decorator with Context Manager**

```python
from functools import wraps
import time

def timer_context(func):
    """Decorator using context manager for timing"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from contextlib import contextmanager
        
        @contextmanager
        def timing():
            start = time.time()
            yield
            end = time.time()
            print(f"{func.__name__} took {end - start:.4f} seconds")
        
        with timing():
            return func(*args, **kwargs)
    return wrapper

@timer_context
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()  # Output: slow_function took 1.0001 seconds
```

---

## Common Use Cases

### 1. **Logging Decorator**

```python
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)

def log_function_call(func):
    """Log function calls with arguments and results"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        logging.info(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_function_call
def add(a, b):
    return a + b

result = add(5, 3)
# INFO:root:Calling add(5, 3)
# INFO:root:add returned 8
```

### 2. **Timing/Performance Decorator**

```python
import time
from functools import wraps

def measure_time(func):
    """Measure execution time of a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} executed in {end - start:.4f} seconds")
        return result
    return wrapper

@measure_time
def compute_sum(n):
    return sum(range(n))

compute_sum(1000000)
# Output: compute_sum executed in 0.0234 seconds
```

### 3. **Caching/Memoization Decorator**

```python
from functools import wraps

def memoize(func):
    """Cache function results"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
            print(f"Computing {func.__name__}{args}")
        else:
            print(f"Returning cached result for {func.__name__}{args}")
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))
# Computing fibonacci(5)
# Computing fibonacci(4)
# Computing fibonacci(3)
# Computing fibonacci(2)
# Computing fibonacci(1)
# Computing fibonacci(0)
# Returning cached result for fibonacci(1)
# Returning cached result for fibonacci(2)
# Returning cached result for fibonacci(3)
# Output: 5

# Python's built-in version:
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)
```

### 4. **Authentication/Authorization Decorator**

```python
from functools import wraps

def require_auth(func):
    """Require authentication before executing function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Simulate checking authentication
        user_authenticated = True  # In real app, check session/token
        
        if not user_authenticated:
            raise PermissionError("Authentication required")
        
        return func(*args, **kwargs)
    return wrapper

def require_role(role):
    """Require specific role"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = "admin"  # In real app, get from session
            
            if user_role != role:
                raise PermissionError(f"Role '{role}' required")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_auth
@require_role("admin")
def delete_user(user_id):
    return f"User {user_id} deleted"

print(delete_user(123))  # Output: User 123 deleted
```

### 5. **Validation Decorator**

```python
from functools import wraps

def validate_positive(func):
    """Validate that all arguments are positive numbers"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, (int, float)) or arg <= 0:
                raise ValueError(f"All arguments must be positive numbers, got {arg}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def calculate_area(length, width):
    return length * width

print(calculate_area(5, 3))   # Output: 15
# calculate_area(-5, 3)       # Raises ValueError
```

### 6. **Retry Decorator**

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Retry function on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    print(f"Attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2, exceptions=(ConnectionError,))
def fetch_data():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Data fetched successfully"
```

### 7. **Singleton Decorator**

```python
from functools import wraps

def singleton(cls):
    """Ensure only one instance of a class exists"""
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Database initialized")

db1 = Database()  # Output: Database initialized
db2 = Database()  # No output (returns same instance)
print(db1 is db2)  # Output: True
```

---

## Common Mistakes

### 1. **Forgetting to Use `@wraps`**

```python
# ❌ WRONG: Loses function metadata
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_function():
    """This is my function"""
    pass

print(my_function.__name__)  # Output: wrapper (WRONG!)
print(my_function.__doc__)   # Output: None (WRONG!)

# ✅ CORRECT: Preserves function metadata
from functools import wraps

def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_function():
    """This is my function"""
    pass

print(my_function.__name__)  # Output: my_function (CORRECT!)
print(my_function.__doc__)   # Output: This is my function (CORRECT!)
```

### 2. **Not Handling `*args` and `**kwargs`**

```python
# ❌ WRONG: Only works with no arguments
def bad_decorator(func):
    def wrapper():  # No *args, **kwargs
        return func()
    return wrapper

@bad_decorator
def greet(name):
    return f"Hello, {name}!"

# greet("Alice")  # TypeError: wrapper() takes 0 positional arguments

# ✅ CORRECT: Handles any arguments
def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Works!
```

### 3. **Decorator Order Confusion**

```python
# Decorators are applied bottom-to-top (inside-out)

def decorator1(func):
    print("Decorator 1 applied")
    def wrapper():
        print("Decorator 1 wrapper")
        return func()
    return wrapper

def decorator2(func):
    print("Decorator 2 applied")
    def wrapper():
        print("Decorator 2 wrapper")
        return func()
    return wrapper

@decorator1  # Applied SECOND
@decorator2  # Applied FIRST
def my_function():
    print("Original function")

# Output during decoration:
# Decorator 2 applied
# Decorator 1 applied

my_function()
# Output during execution:
# Decorator 1 wrapper
# Decorator 2 wrapper
# Original function
```

### 4. **Forgetting to Return the Result**

```python
# ❌ WRONG: Doesn't return the result
def bad_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)  # Missing return!
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: None (WRONG!)

# ✅ CORRECT: Returns the result
def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)  # Return the result
    return wrapper

@good_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8 (CORRECT!)
```

### 5. **Mutable Default Arguments in Decorator**

```python
# ❌ WRONG: Mutable default argument
def bad_cache(func, cache={}):  # cache is shared across all uses!
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# ✅ CORRECT: Create cache inside decorator
def good_cache(func):
    cache = {}  # New cache for each decorated function
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
```

### 6. **Not Handling Exceptions Properly**

```python
# ❌ WRONG: Swallows exceptions silently
def bad_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass  # Silently ignores errors!
    return wrapper

# ✅ CORRECT: Handle or re-raise exceptions
def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            raise  # Re-raise the exception
    return wrapper
```

---

## Best Practices

### 1. **Always Use `functools.wraps`**

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 2. **Use `*args` and `**kwargs` for Flexibility**

```python
def flexible_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # Handles any signature
        return func(*args, **kwargs)
    return wrapper
```

### 3. **Keep Decorators Simple and Focused**

```python
# ✅ GOOD: Single responsibility
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start}")
        return result
    return wrapper

# Apply separately
@log_calls
@measure_time
def my_function():
    pass
```

### 4. **Document Your Decorators**

```python
def my_decorator(func):
    """
    Decorator that does XYZ.
    
    Args:
        func: The function to decorate
    
    Returns:
        The wrapped function
    
    Example:
        @my_decorator
        def my_func():
            pass
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 5. **Use Class-Based Decorators for Complex State**

```python
class ComplexDecorator:
    """Use classes when you need to maintain complex state"""
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        self.state = {}
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Access self.param1, self.param2, self.state
            return func(*args, **kwargs)
        return wrapper
```

### 6. **Make Decorators Configurable**

```python
def configurable_decorator(enabled=True, log_level="INFO"):
    """Allow configuration through parameters"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enabled:
                print(f"[{log_level}] Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@configurable_decorator(enabled=True, log_level="DEBUG")
def my_function():
    pass
```

### 7. **Test Decorators Thoroughly**

```python
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Test that it works
@my_decorator
def test_function(x):
    """Test docstring"""
    return x * 2

assert test_function(5) == 10
assert test_function.__name__ == "test_function"
assert test_function.__doc__ == "Test docstring"
```

### 8. **Consider Using Built-in Decorators When Possible**

```python
from functools import lru_cache, wraps
import time

# Use built-in lru_cache instead of writing your own
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Use property decorator for getters/setters
class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
```

---

## Real-World Examples

### Example 1: Flask Web Framework

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')  # Decorator for URL routing
def home():
    return "Hello, World!"

@app.route('/user/<username>')
def show_user(username):
    return f"User: {username}"

# Flask uses decorators extensively for:
# - Routing (@app.route)
# - Authentication (@login_required)
# - Error handling (@app.errorhandler)
```

### Example 2: Django Framework

```python
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@login_required  # Require user to be logged in
@require_http_methods(["GET", "POST"])  # Only allow GET and POST
def my_view(request):
    return HttpResponse("Hello")
```

### Example 3: Property Validation

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

temp = Temperature(25)
print(temp.celsius)      # 25
print(temp.fahrenheit)   # 77.0
temp.fahrenheit = 86
print(temp.celsius)      # 30.0
```

### Example 4: API Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_second):
    """Limit API calls per second"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def api_call():
    print(f"API called at {time.time()}")

# Will be rate-limited to 2 calls per second
for _ in range(5):
    api_call()
```

### Example 5: Deprecation Warning

```python
import warnings
from functools import wraps

def deprecated(reason):
    """Mark function as deprecated"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated: {reason}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@deprecated("Use new_function() instead")
def old_function():
    return "This is old"

old_function()  # Shows deprecation warning
```

---

## Python Decorators vs Java Annotations vs Spring AOP

### Quick Answer

Python decorators are **similar to both** Java annotations and Spring AOP, but they're not exactly the same:

- **Like Java Annotations**: Similar syntax (`@` symbol), declarative approach
- **Like Spring AOP**: Actually execute code and modify behavior (aspect-oriented programming)
- **Key Difference**: Python decorators are **executable code** that runs at function definition time, while Java annotations are **metadata** that require separate processing

### Detailed Comparison

| Aspect | Python Decorators | Java Annotations | Spring AOP |
|--------|------------------|------------------|------------|
| **Nature** | Executable code (functions) | Metadata (markers) | Runtime proxy-based behavior |
| **Execution** | Runs at definition time | Processed by framework/compiler | Runs at method invocation |
| **Syntax** | `@decorator` | `@Annotation` | `@Aspect` + pointcuts |
| **Implementation** | Python functions wrapping functions | Interface with retention policy | Proxy pattern with advice |
| **Behavior Modification** | Direct (wraps function) | Indirect (requires processor) | Indirect (requires proxy) |
| **Runtime Cost** | Minimal (one-time wrapping) | None (just metadata) | Higher (proxy overhead) |
| **Flexibility** | Very flexible (any Python code) | Limited (metadata only) | Very flexible (full Java code) |
| **Use Cases** | Logging, caching, validation, routing | Configuration, documentation, validation | Cross-cutting concerns, transactions |

---

### Python Decorators vs Java Annotations

#### Similarities

1. **Syntax**: Both use `@` symbol
2. **Declarative**: Both provide declarative way to add functionality
3. **Reusability**: Both promote code reuse
4. **Placement**: Both placed above function/method/class

#### Key Differences

**Python Decorators** are **executable code**:

```python
# Python Decorator - EXECUTES CODE
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}")  # This code RUNS
        return func(*args, **kwargs)
    return wrapper

@log_execution  # This decorator WRAPS the function immediately
def greet(name):
    return f"Hello, {name}!"

# When you call greet(), the wrapper code executes
greet("Alice")  # Output: Executing greet
                #         Hello, Alice!
```

**Java Annotations** are **metadata only**:

```java
// Java Annotation - JUST METADATA
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface LogExecution {
    // This is just a marker, no code execution
}

public class MyClass {
    @LogExecution  // Just metadata, doesn't do anything by itself
    public String greet(String name) {
        return "Hello, " + name + "!";
    }
}

// Separate code needed to PROCESS the annotation
public class AnnotationProcessor {
    public void processAnnotations(Object obj) {
        for (Method method : obj.getClass().getDeclaredMethods()) {
            if (method.isAnnotationPresent(LogExecution.class)) {
                // NOW we can add behavior based on the annotation
                System.out.println("Executing " + method.getName());
            }
        }
    }
}
```

#### Side-by-Side Example

**Python Decorator (Self-Contained)**:

```python
from functools import wraps
import time

def measure_time(func):
    """Decorator that measures execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@measure_time  # Decorator immediately wraps the function
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()  # Output: slow_function took 1.0001s
```

**Java Annotation (Requires Framework)**:

```java
// 1. Define annotation (just metadata)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MeasureTime {
}

// 2. Use annotation
public class MyService {
    @MeasureTime  // Just a marker
    public String slowMethod() throws InterruptedException {
        Thread.sleep(1000);
        return "Done";
    }
}

// 3. Need separate framework/processor to make it work
// (Spring AOP, AspectJ, or custom proxy)
public class TimingAspect {
    @Around("@annotation(MeasureTime)")
    public Object measureTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long end = System.currentTimeMillis();
        System.out.println(joinPoint.getSignature().getName() + 
                          " took " + (end - start) + "ms");
        return result;
    }
}
```

---

### Python Decorators vs Spring AOP

#### Similarities

1. **Aspect-Oriented Programming**: Both implement AOP concepts
2. **Cross-Cutting Concerns**: Both handle logging, security, transactions, etc.
3. **Behavior Modification**: Both modify function/method behavior
4. **Separation of Concerns**: Both separate business logic from infrastructure code

#### Key Differences

**Python Decorators** wrap functions at **definition time**:

```python
# Python - Wrapping happens when function is defined
def transaction(func):
    def wrapper(*args, **kwargs):
        print("BEGIN TRANSACTION")
        try:
            result = func(*args, **kwargs)
            print("COMMIT TRANSACTION")
            return result
        except Exception as e:
            print("ROLLBACK TRANSACTION")
            raise
    return wrapper

@transaction  # Function is wrapped HERE (definition time)
def save_user(user):
    # Save user to database
    return f"Saved {user}"

# The wrapper is already in place
save_user("Alice")
```

**Spring AOP** uses **runtime proxies**:

```java
// Spring AOP - Proxy created at runtime

// 1. Define aspect
@Aspect
@Component
public class TransactionAspect {
    
    @Around("@annotation(Transactional)")
    public Object handleTransaction(ProceedingJoinPoint joinPoint) 
            throws Throwable {
        System.out.println("BEGIN TRANSACTION");
        try {
            Object result = joinPoint.proceed();
            System.out.println("COMMIT TRANSACTION");
            return result;
        } catch (Exception e) {
            System.out.println("ROLLBACK TRANSACTION");
            throw e;
        }
    }
}

// 2. Use annotation
@Service
public class UserService {
    
    @Transactional  // Spring creates proxy at runtime
    public String saveUser(String user) {
        // Save user to database
        return "Saved " + user;
    }
}

// 3. Spring creates a PROXY object that wraps UserService
// When you call saveUser(), you're actually calling the proxy
```

#### Conceptual Comparison

```
Python Decorator:
┌─────────────────────────────────────┐
│ @decorator                          │
│ def original_function():            │
│     # code                          │
└─────────────────────────────────────┘
         │ (at definition time)
         ▼
┌─────────────────────────────────────┐
│ wrapper_function:                   │
│   - before code                     │
│   - call original_function()        │
│   - after code                      │
└─────────────────────────────────────┘

Spring AOP:
┌─────────────────────────────────────┐
│ @Transactional                      │
│ public void originalMethod() {      │
│     // code                         │
│ }                                   │
└─────────────────────────────────────┘
         │ (at runtime)
         ▼
┌─────────────────────────────────────┐
│ Spring creates Proxy:               │
│   - before advice                   │
│   - call originalMethod()           │
│   - after advice                    │
└─────────────────────────────────────┘
```

#### Advanced Comparison: Multiple Aspects

**Python - Stacked Decorators**:

```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"LOG: Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def authenticate(func):
    def wrapper(*args, **kwargs):
        print("AUTH: Checking credentials")
        return func(*args, **kwargs)
    return wrapper

def transaction(func):
    def wrapper(*args, **kwargs):
        print("TX: Begin transaction")
        result = func(*args, **kwargs)
        print("TX: Commit transaction")
        return result
    return wrapper

@log           # Applied THIRD (outermost)
@authenticate  # Applied SECOND
@transaction   # Applied FIRST (innermost)
def save_user(user):
    print(f"Saving {user}")
    return "Success"

save_user("Alice")
# Output:
# LOG: Calling wrapper
# AUTH: Checking credentials
# TX: Begin transaction
# Saving Alice
# TX: Commit transaction
```

**Spring AOP - Multiple Aspects**:

```java
@Aspect
@Order(1)  // Execution order
public class LoggingAspect {
    @Around("@annotation(Loggable)")
    public Object log(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("LOG: Calling " + joinPoint.getSignature().getName());
        return joinPoint.proceed();
    }
}

@Aspect
@Order(2)
public class AuthenticationAspect {
    @Around("@annotation(Secured)")
    public Object authenticate(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("AUTH: Checking credentials");
        return joinPoint.proceed();
    }
}

@Aspect
@Order(3)
public class TransactionAspect {
    @Around("@annotation(Transactional)")
    public Object handleTransaction(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("TX: Begin transaction");
        Object result = joinPoint.proceed();
        System.out.println("TX: Commit transaction");
        return result;
    }
}

@Service
public class UserService {
    @Loggable
    @Secured
    @Transactional
    public String saveUser(String user) {
        System.out.println("Saving " + user);
        return "Success";
    }
}
```

---

### When Each Approach Shines

#### Use Python Decorators When:

✅ You want **simple, straightforward** behavior modification  
✅ You need **immediate wrapping** at function definition  
✅ You're working in **Python** (obviously!)  
✅ You want **minimal overhead** and complexity  
✅ You need **fine-grained control** over individual functions  

```python
# Perfect for simple, direct modifications
@cache
@validate_input
@log_errors
def process_data(data):
    return transform(data)
```

#### Use Java Annotations When:

✅ You need **metadata** for documentation or configuration  
✅ You want **compile-time checking** (with annotation processors)  
✅ You're using **frameworks** that process annotations (Spring, JPA, etc.)  
✅ You need **declarative configuration**  

```java
// Perfect for configuration and metadata
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String name;
}
```

#### Use Spring AOP When:

✅ You need **enterprise-level** cross-cutting concerns  
✅ You want **centralized** aspect management  
✅ You need **pointcut expressions** for flexible matching  
✅ You're already using **Spring Framework**  
✅ You need **transaction management**, **security**, etc.  

```java
// Perfect for enterprise cross-cutting concerns
@Aspect
@Component
public class SecurityAspect {
    
    @Before("execution(* com.example.service.*.*(..))")
    public void checkSecurity(JoinPoint joinPoint) {
        // Apply security to ALL service methods
    }
    
    @Around("@annotation(Transactional)")
    public Object handleTransaction(ProceedingJoinPoint pjp) throws Throwable {
        // Centralized transaction management
    }
}
```

---

### Summary Table

| Feature | Python Decorators | Java Annotations | Spring AOP |
|---------|------------------|------------------|------------|
| **Execution Model** | Wraps at definition time | Metadata only | Proxy at runtime |
| **Code Required** | Decorator function | Annotation + processor | Aspect + configuration |
| **Performance** | Fast (one-time wrap) | No overhead | Slower (proxy calls) |
| **Flexibility** | Very high | Low (metadata only) | Very high |
| **Complexity** | Low to medium | Low (just markers) | High (framework setup) |
| **Best For** | Function enhancement | Configuration/metadata | Enterprise AOP |
| **Learning Curve** | Easy | Easy | Steep |
| **Framework Dependency** | None | Optional | Required (Spring) |

---

### Practical Example: Same Functionality in All Three

**Requirement**: Log method execution time

#### Python Decorator

```python
import time
from functools import wraps

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@log_execution_time
def process_data(data):
    time.sleep(1)
    return f"Processed {data}"

process_data("test")  # Output: process_data took 1.0001s
```

#### Java Annotation (with AspectJ)

```java
// 1. Define annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface LogExecutionTime {
}

// 2. Create aspect
@Aspect
@Component
public class LoggingAspect {
    @Around("@annotation(LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long elapsed = System.currentTimeMillis() - start;
        System.out.println(joinPoint.getSignature().getName() + 
                          " took " + elapsed + "ms");
        return result;
    }
}

// 3. Use annotation
@Service
public class DataService {
    @LogExecutionTime
    public String processData(String data) throws InterruptedException {
        Thread.sleep(1000);
        return "Processed " + data;
    }
}
```

#### Spring AOP (without custom annotation)

```java
@Aspect
@Component
public class PerformanceAspect {
    
    @Around("execution(* com.example.service.DataService.processData(..))")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long elapsed = System.currentTimeMillis() - start;
        System.out.println(joinPoint.getSignature().getName() + 
                          " took " + elapsed + "ms");
        return result;
    }
}

@Service
public class DataService {
    public String processData(String data) throws InterruptedException {
        Thread.sleep(1000);
        return "Processed " + data;
    }
}
```

---

### Final Thoughts

**Python Decorators** are:
- ✅ **More powerful** than Java annotations (they execute code)
- ✅ **Simpler** than Spring AOP (no framework required)
- ✅ **Similar in spirit** to both (declarative, reusable, aspect-oriented)
- ✅ **Unique** in their immediate, definition-time wrapping approach

**Think of it this way**:
- **Java Annotations** = Sticky notes with instructions
- **Python Decorators** = Gift wrapping that actually adds functionality
- **Spring AOP** = Personal assistant who intercepts your calls

---

## Summary

### Key Takeaways

1. **Decorators** modify function/class behavior without changing source code
2. **Syntax**: Use `@decorator_name` above function/class definition
3. **Types**: Function, class, method, parameterized, and chained decorators
4. **Always use** `@wraps` to preserve function metadata
5. **Use** `*args, **kwargs` for flexible argument handling
6. **Common uses**: Logging, timing, caching, authentication, validation
7. **Avoid**: Forgetting to return results, mutable defaults, swallowing exceptions
8. **Best practices**: Keep simple, document well, test thoroughly

### When to Use Decorators

- ✅ Cross-cutting concerns (logging, timing, caching)
- ✅ Code reuse across multiple functions
- ✅ Framework integration (Flask, Django)
- ✅ Enforcing constraints (authentication, validation)
- ✅ Modifying behavior without changing code

### When NOT to Use Decorators

- ❌ When simple function calls are clearer
- ❌ For one-time use (no reusability benefit)
- ❌ When they make code harder to understand
- ❌ For complex logic better suited to classes

---

## Additional Resources

- [PEP 318 - Decorators for Functions and Methods](https://www.python.org/dev/peps/pep-0318/)
- [Python functools Documentation](https://docs.python.org/3/library/functools.html)
- [Real Python - Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Python Decorator Library](https://wiki.python.org/moin/PythonDecoratorLibrary)
