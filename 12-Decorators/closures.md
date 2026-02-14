# Python Closures: A Complete Guide

## Table of Contents
1. [What are Closures?](#what-are-closures)
2. [How Closures Work](#how-closures-work)
3. [Detailed Examples](#detailed-examples)
4. [Flow Diagrams](#flow-diagrams)
5. [Python vs JavaScript vs Java Closures](#python-vs-javascript-vs-java-closures)
6. [Common Use Cases](#common-use-cases)
7. [Common Mistakes](#common-mistakes)
8. [Best Practices](#best-practices)

---

## What are Closures?

A **closure** is a function object that has access to variables in its enclosing lexical scope, even after the outer function has finished executing. In simpler terms, a closure "remembers" the environment in which it was created.

### Key Characteristics

- **Nested Functions**: A function defined inside another function
- **Free Variables**: The inner function references variables from the outer function
- **Persistence**: The inner function retains access to outer variables even after the outer function returns
- **Encapsulation**: Provides data privacy and encapsulation

### Basic Syntax

```python
def outer_function(x):
    # x is a free variable for inner_function
    
    def inner_function(y):
        # inner_function can access x from outer scope
        return x + y
    
    return inner_function  # Return the function, not calling it

# Create a closure
closure = outer_function(10)

# The outer function has finished, but closure still has access to x
print(closure(5))   # Output: 15
print(closure(20))  # Output: 30
```

### Why "Closure"?

The term "closure" comes from the fact that the inner function **closes over** the free variables from the enclosing scope, capturing them in its environment.

---

## How Closures Work

### Memory and Scope

When a closure is created, Python stores the free variables in a special attribute called `__closure__`.

```python
def outer(x):
    def inner(y):
        return x + y
    return inner

closure = outer(10)

# Inspect the closure
print(closure.__name__)      # Output: inner
print(closure.__closure__)   # Output: (<cell at 0x...: int object at 0x...>,)
print(closure.__closure__[0].cell_contents)  # Output: 10
```

### Execution Flow

```python
def make_multiplier(n):
    """Returns a function that multiplies its argument by n"""
    def multiplier(x):
        return x * n
    return multiplier

# Step 1: Call make_multiplier(3)
times_3 = make_multiplier(3)
# - Creates a new scope with n = 3
# - Defines multiplier function
# - Returns multiplier function
# - make_multiplier scope "should" be destroyed, but n is preserved!

# Step 2: Call times_3(10)
result = times_3(10)
# - multiplier function executes
# - Accesses n from the closure (n = 3)
# - Returns 10 * 3 = 30

print(result)  # Output: 30
```

### Scope Chain

```python
x = "global"

def outer():
    x = "outer"
    
    def middle():
        x = "middle"
        
        def inner():
            # inner can access all outer scopes
            print(f"Inner sees: {x}")
        
        inner()
        print(f"Middle sees: {x}")
    
    middle()
    print(f"Outer sees: {x}")

outer()
# Output:
# Inner sees: middle
# Middle sees: middle
# Outer sees: outer
```

---

## Detailed Examples

### Example 1: Counter with Closure

```python
def make_counter():
    """Create a counter using closure"""
    count = 0  # Free variable
    
    def increment():
        nonlocal count  # Modify the outer variable
        count += 1
        return count
    
    return increment

# Create counters
counter1 = make_counter()
counter2 = make_counter()

# Each counter has its own count
print(counter1())  # Output: 1
print(counter1())  # Output: 2
print(counter1())  # Output: 3

print(counter2())  # Output: 1 (independent counter)
print(counter2())  # Output: 2
```

### Example 2: Function Factory

```python
def make_power_function(exponent):
    """Create functions that raise numbers to a specific power"""
    def power(base):
        return base ** exponent
    return power

# Create specialized functions
square = make_power_function(2)
cube = make_power_function(3)
fourth_power = make_power_function(4)

print(square(5))        # Output: 25
print(cube(3))          # Output: 27
print(fourth_power(2))  # Output: 16
```

### Example 3: Data Encapsulation

```python
def create_account(initial_balance):
    """Create a bank account with private balance"""
    balance = initial_balance  # Private variable
    
    def deposit(amount):
        nonlocal balance
        balance += amount
        return f"Deposited {amount}. New balance: {balance}"
    
    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return "Insufficient funds"
        balance -= amount
        return f"Withdrew {amount}. New balance: {balance}"
    
    def get_balance():
        return f"Current balance: {balance}"
    
    # Return a dictionary of functions
    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance
    }

# Create account
account = create_account(1000)

print(account['balance']())      # Current balance: 1000
print(account['deposit'](500))   # Deposited 500. New balance: 1500
print(account['withdraw'](200))  # Withdrew 200. New balance: 1300
print(account['balance']())      # Current balance: 1300

# Cannot access balance directly - it's encapsulated!
# print(balance)  # NameError: name 'balance' is not defined
```

### Example 4: Decorators Using Closures

```python
def repeat(times):
    """Decorator that repeats function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Hello, Alice!
# Hello, Alice!
# Hello, Alice!
```

### Example 5: Closure with Multiple Free Variables

```python
def create_calculator(initial_value):
    """Calculator with memory"""
    value = initial_value
    history = []
    
    def add(x):
        nonlocal value
        value += x
        history.append(f"Added {x}")
        return value
    
    def subtract(x):
        nonlocal value
        value -= x
        history.append(f"Subtracted {x}")
        return value
    
    def get_history():
        return history.copy()
    
    def reset():
        nonlocal value
        value = initial_value
        history.clear()
        return value
    
    return {
        'add': add,
        'subtract': subtract,
        'history': get_history,
        'reset': reset
    }

calc = create_calculator(100)
print(calc['add'](50))        # 150
print(calc['subtract'](30))   # 120
print(calc['add'](10))        # 130
print(calc['history']())      # ['Added 50', 'Subtracted 30', 'Added 10']
```

---

## Flow Diagrams

### Closure Creation and Execution Flow

```
Step 1: Define Outer Function
┌────────────────────────────────────┐
│ def outer(x):                      │
│     def inner(y):                  │
│         return x + y               │
│     return inner                   │
└────────────────────────────────────┘

Step 2: Call Outer Function
┌────────────────────────────────────┐
│ closure = outer(10)                │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ Outer Function Scope Created      │
│ ┌────────────────────────────────┐ │
│ │ x = 10                         │ │
│ │ inner function defined         │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ Return inner function              │
│ WITH closure over x                │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ Closure Object Created             │
│ ┌────────────────────────────────┐ │
│ │ Function: inner                │ │
│ │ Free Variables: {x: 10}        │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘

Step 3: Call Closure
┌────────────────────────────────────┐
│ result = closure(5)                │
└────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ Inner Function Executes            │
│ ┌────────────────────────────────┐ │
│ │ y = 5 (parameter)              │ │
│ │ x = 10 (from closure)          │ │
│ │ return 10 + 5 = 15             │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
```

### Memory Diagram: Multiple Closures

```
Code:
    def make_adder(x):
        def add(y):
            return x + y
        return add
    
    add_5 = make_adder(5)
    add_10 = make_adder(10)

Memory Layout:
┌─────────────────────────────────────────────────────────┐
│                    Global Scope                         │
│  ┌───────────────┐         ┌───────────────┐           │
│  │ add_5         │         │ add_10        │           │
│  └───────┬───────┘         └───────┬───────┘           │
└──────────┼─────────────────────────┼───────────────────┘
           │                         │
           ▼                         ▼
    ┌──────────────┐          ┌──────────────┐
    │ Closure 1    │          │ Closure 2    │
    │ ┌──────────┐ │          │ ┌──────────┐ │
    │ │ x = 5    │ │          │ │ x = 10   │ │
    │ │ add()    │ │          │ │ add()    │ │
    │ └──────────┘ │          │ └──────────┘ │
    └──────────────┘          └──────────────┘

Each closure has its own copy of the free variable!
```

### Scope Resolution Diagram

```
Variable Lookup Order (LEGB Rule):
L - Local (current function)
E - Enclosing (outer functions)
G - Global (module level)
B - Built-in (Python built-ins)

Example:
    x = "global"
    
    def outer():
        x = "enclosing"
        
        def inner():
            x = "local"
            print(x)  # Looks up: Local → Enclosing → Global → Built-in
        
        inner()

Lookup Flow:
┌─────────────────────────────────────┐
│ Built-in Scope                      │
│ (len, print, etc.)                  │
└─────────────────────────────────────┘
            ▲
            │ (4) Not found, check Built-in
┌─────────────────────────────────────┐
│ Global Scope                        │
│ x = "global"                        │
└─────────────────────────────────────┘
            ▲
            │ (3) Not found, check Global
┌─────────────────────────────────────┐
│ Enclosing Scope (outer)             │
│ x = "enclosing"                     │
└─────────────────────────────────────┘
            ▲
            │ (2) Not found, check Enclosing
┌─────────────────────────────────────┐
│ Local Scope (inner)                 │
│ x = "local"  ← FOUND! (1)           │
└─────────────────────────────────────┘
```

---

## Python vs JavaScript vs Java Closures

### Comparison Table

| Aspect | Python | JavaScript | Java |
|--------|--------|------------|------|
| **Support** | Full support | Full support | Partial (since Java 8) |
| **Syntax** | Nested functions | Nested functions | Lambda expressions, anonymous classes |
| **Variable Capture** | By reference | By reference | Effectively final variables only |
| **Modification** | `nonlocal` keyword needed | Direct modification | Cannot modify (must be final/effectively final) |
| **Use Cases** | Decorators, factories, encapsulation | Callbacks, async, modules | Functional interfaces, streams |
| **Garbage Collection** | Automatic | Automatic | Automatic |

---

### Python Closures

```python
def outer(x):
    def inner(y):
        return x + y
    return inner

closure = outer(10)
print(closure(5))  # Output: 15

# Modifying outer variable
def make_counter():
    count = 0
    
    def increment():
        nonlocal count  # Required to modify
        count += 1
        return count
    
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

### JavaScript Closures

```javascript
// JavaScript - Very similar to Python
function outer(x) {
    function inner(y) {
        return x + y;
    }
    return inner;
}

const closure = outer(10);
console.log(closure(5));  // Output: 15

// Modifying outer variable (no special keyword needed)
function makeCounter() {
    let count = 0;
    
    function increment() {
        count++;  // Can modify directly
        return count;
    }
    
    return increment;
}

const counter = makeCounter();
console.log(counter());  // 1
console.log(counter());  // 2

// Arrow functions (ES6)
const makeMultiplier = (x) => (y) => x * y;
const times3 = makeMultiplier(3);
console.log(times3(10));  // 30
```

### Java Closures (Lambda Expressions)

```java
// Java - More restrictive
import java.util.function.Function;
import java.util.function.IntUnaryOperator;

public class ClosureExample {
    
    // Basic closure with lambda
    public static Function<Integer, Integer> makeAdder(int x) {
        // x must be final or effectively final
        return (y) -> x + y;  // Lambda captures x
    }
    
    public static void main(String[] args) {
        Function<Integer, Integer> add10 = makeAdder(10);
        System.out.println(add10.apply(5));  // Output: 15
        
        // Cannot modify captured variables!
        // This would NOT compile:
        /*
        int count = 0;
        IntUnaryOperator increment = (x) -> {
            count++;  // ERROR: Variable used in lambda must be final
            return count;
        };
        */
        
        // Workaround: Use mutable object
        final int[] count = {0};  // Array is final, but contents can change
        IntUnaryOperator increment = (x) -> {
            count[0]++;
            return count[0];
        };
        
        System.out.println(increment.applyAsInt(0));  // 1
        System.out.println(increment.applyAsInt(0));  // 2
    }
}

// Java 8+ Functional Interface approach
@FunctionalInterface
interface Counter {
    int increment();
}

class CounterFactory {
    public static Counter makeCounter() {
        final int[] count = {0};  // Workaround for mutability
        
        return () -> {
            count[0]++;
            return count[0];
        };
    }
}
```

### Side-by-Side Comparison: Counter Example

**Python**:
```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

**JavaScript**:
```javascript
function makeCounter() {
    let count = 0;
    function increment() {
        count++;
        return count;
    }
    return increment;
}

const counter = makeCounter();
console.log(counter());  // 1
console.log(counter());  // 2
```

**Java**:
```java
import java.util.function.Supplier;

public class Counter {
    public static Supplier<Integer> makeCounter() {
        final int[] count = {0};  // Must use array/object wrapper
        return () -> {
            count[0]++;
            return count[0];
        };
    }
    
    public static void main(String[] args) {
        Supplier<Integer> counter = makeCounter();
        System.out.println(counter.get());  // 1
        System.out.println(counter.get());  // 2
    }
}
```

### Key Differences Summary

**Python**:
- ✅ Clean syntax for closures
- ✅ `nonlocal` keyword for modification
- ✅ Very flexible
- ✅ Commonly used in decorators

**JavaScript**:
- ✅ Very similar to Python
- ✅ No special keyword needed for modification
- ✅ Arrow functions make it even cleaner
- ✅ Heavily used in async/callbacks

**Java**:
- ⚠️ Variables must be final/effectively final
- ⚠️ Cannot modify captured primitives directly
- ⚠️ Need workarounds (arrays, AtomicInteger, etc.)
- ✅ Type-safe with functional interfaces
- ✅ Good for streams and functional programming

---

## Common Use Cases

### 1. Data Privacy and Encapsulation

```python
def create_person(name, age):
    """Create a person with private data"""
    _name = name  # Private
    _age = age    # Private
    
    def get_name():
        return _name
    
    def get_age():
        return _age
    
    def set_age(new_age):
        nonlocal _age
        if new_age > 0:
            _age = new_age
    
    def birthday():
        nonlocal _age
        _age += 1
        return f"Happy birthday! Now {_age} years old."
    
    return {
        'get_name': get_name,
        'get_age': get_age,
        'set_age': set_age,
        'birthday': birthday
    }

person = create_person("Alice", 30)
print(person['get_name']())  # Alice
print(person['birthday']())  # Happy birthday! Now 31 years old.
```

### 2. Callback Functions

```python
def create_button_handler(button_id):
    """Create event handler with context"""
    click_count = 0
    
    def on_click():
        nonlocal click_count
        click_count += 1
        print(f"Button {button_id} clicked {click_count} times")
    
    return on_click

button1_handler = create_button_handler("Submit")
button2_handler = create_button_handler("Cancel")

button1_handler()  # Button Submit clicked 1 times
button1_handler()  # Button Submit clicked 2 times
button2_handler()  # Button Cancel clicked 1 times
```

### 3. Memoization/Caching

```python
def memoize(func):
    """Cache function results using closure"""
    cache = {}
    
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
# ...
```

### 4. Partial Application

```python
def partial(func, *fixed_args):
    """Create a partial function using closure"""
    def wrapper(*args):
        return func(*fixed_args, *args)
    return wrapper

def multiply(x, y, z):
    return x * y * z

# Create specialized functions
double_and_multiply = partial(multiply, 2)
print(double_and_multiply(3, 4))  # 2 * 3 * 4 = 24

triple_and_multiply = partial(multiply, 3)
print(triple_and_multiply(2, 5))  # 3 * 2 * 5 = 30
```

---

## Common Mistakes

### 1. Loop Variable Closure Problem

```python
# ❌ WRONG: All closures reference the same variable
def create_multipliers_wrong():
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)
    return multipliers

funcs = create_multipliers_wrong()
print(funcs[0](10))  # Expected: 0, Actual: 40
print(funcs[1](10))  # Expected: 10, Actual: 40
print(funcs[2](10))  # Expected: 20, Actual: 40
# All return 40 because i = 4 at the end!

# ✅ CORRECT: Capture the loop variable
def create_multipliers_correct():
    multipliers = []
    for i in range(5):
        # Use default argument to capture current value
        multipliers.append(lambda x, i=i: x * i)
    return multipliers

funcs = create_multipliers_correct()
print(funcs[0](10))  # 0
print(funcs[1](10))  # 10
print(funcs[2](10))  # 20
```

### 2. Forgetting `nonlocal` Keyword

```python
# ❌ WRONG: Creates new local variable instead of modifying outer
def make_counter_wrong():
    count = 0
    
    def increment():
        count = count + 1  # UnboundLocalError!
        return count
    
    return increment

# ✅ CORRECT: Use nonlocal
def make_counter_correct():
    count = 0
    
    def increment():
        nonlocal count  # Modify outer variable
        count += 1
        return count
    
    return increment
```

### 3. Mutable Default Arguments

```python
# ❌ WRONG: Mutable default argument shared across calls
def create_appender_wrong(item, list=[]):
    list.append(item)
    return list

print(create_appender_wrong(1))  # [1]
print(create_appender_wrong(2))  # [1, 2] - Unexpected!

# ✅ CORRECT: Use None and create new list
def create_appender_correct(item, list=None):
    if list is None:
        list = []
    list.append(item)
    return list

print(create_appender_correct(1))  # [1]
print(create_appender_correct(2))  # [2] - Correct!
```

### 4. Circular References and Memory Leaks

```python
# ⚠️ POTENTIAL ISSUE: Circular reference
def create_circular():
    data = {'value': 42}
    
    def get_data():
        return data
    
    # Circular reference: data → function → data
    data['get_self'] = get_data
    return get_data

# Python's garbage collector handles this, but be aware
```

### 5. Modifying Immutable Types

```python
# ❌ WRONG: Trying to modify immutable type
def make_string_appender():
    text = "Hello"
    
    def append(suffix):
        nonlocal text
        text = text + suffix  # Creates NEW string, not modifying
        return text
    
    return append

# This works, but creates new strings each time
# For large strings, this is inefficient

# ✅ BETTER: Use mutable type
def make_list_appender():
    items = []
    
    def append(item):
        items.append(item)  # Modifies in place
        return items
    
    return append
```

---

## Best Practices

### 1. Use Closures for Data Encapsulation

```python
# ✅ GOOD: Private data with controlled access
def create_temperature_sensor(initial_temp):
    temperature = initial_temp
    readings = []
    
    def read():
        return temperature
    
    def update(new_temp):
        nonlocal temperature
        if -273.15 <= new_temp <= 1000:  # Validation
            temperature = new_temp
            readings.append(new_temp)
            return True
        return False
    
    def get_history():
        return readings.copy()  # Return copy, not reference
    
    return {
        'read': read,
        'update': update,
        'history': get_history
    }
```

### 2. Document Closure Behavior

```python
def create_rate_limiter(max_calls, time_window):
    """
    Create a rate limiter using closure.
    
    Args:
        max_calls: Maximum number of calls allowed
        time_window: Time window in seconds
    
    Returns:
        A decorator function that limits call rate
    
    Note:
        Uses closure to maintain call history across invocations
    """
    import time
    calls = []
    
    def limiter(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [t for t in calls if now - t < time_window]
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return limiter
```

### 3. Avoid Excessive Nesting

```python
# ❌ BAD: Too much nesting
def level1():
    def level2():
        def level3():
            def level4():
                return "Too deep!"
            return level4
        return level3
    return level2

# ✅ GOOD: Keep it simple
def create_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply
```

### 4. Use `functools.wraps` for Decorators

```python
from functools import wraps

# ✅ GOOD: Preserve function metadata
def my_decorator(func):
    @wraps(func)  # Preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 5. Be Mindful of Memory

```python
# ⚠️ CAUTION: Large objects in closure
def create_processor():
    large_data = [i for i in range(1000000)]  # Stays in memory!
    
    def process(index):
        return large_data[index]
    
    return process

# ✅ BETTER: Only store what you need
def create_processor_efficient():
    def process(index):
        # Generate on demand instead of storing
        return index  # Or fetch from database, file, etc.
    
    return process
```

### 6. Use Closures for Configuration

```python
def create_logger(level="INFO", prefix=""):
    """Create a configured logger using closure"""
    def log(message):
        print(f"[{level}] {prefix}{message}")
    
    return log

# Create specialized loggers
error_logger = create_logger("ERROR", "System Error: ")
info_logger = create_logger("INFO", "Info: ")

error_logger("Database connection failed")
info_logger("Application started")
```

### 7. Test Closure Behavior

```python
def test_counter():
    """Test closure-based counter"""
    counter = make_counter()
    
    assert counter() == 1
    assert counter() == 2
    assert counter() == 3
    
    # Test independence
    counter2 = make_counter()
    assert counter2() == 1
    assert counter() == 4  # First counter unaffected
    
    print("All tests passed!")

test_counter()
```

---

## Summary

### Key Takeaways

1. **Closures** allow inner functions to access outer function variables
2. **Free variables** are captured and persist after outer function returns
3. Use **`nonlocal`** keyword to modify outer variables
4. **Python closures** are more flexible than Java but similar to JavaScript
5. Common uses: **data encapsulation**, **decorators**, **callbacks**, **factories**
6. Watch out for: **loop variable problems**, **forgetting nonlocal**, **memory leaks**

### When to Use Closures

- ✅ Data privacy and encapsulation
- ✅ Creating function factories
- ✅ Implementing decorators
- ✅ Callback functions with context
- ✅ Memoization and caching
- ✅ Partial function application

### When NOT to Use Closures

- ❌ When a simple class would be clearer
- ❌ When you need complex state management
- ❌ When performance is critical (classes are faster)
- ❌ When you need inheritance or polymorphism

---

## Additional Resources

- [PEP 227 - Statically Nested Scopes](https://www.python.org/dev/peps/pep-0227/)
- [Python Scopes and Namespaces](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)
- [Closures in Python](https://www.programiz.com/python-programming/closure)
- [Real Python - Closures](https://realpython.com/inner-functions-what-are-they-good-for/)
