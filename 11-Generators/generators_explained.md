# Python Generators: A Complete Guide

## Table of Contents
1. [What are Generators?](#what-are-generators)
2. [Types of Iterators in Python](#types-of-iterators-in-python)
3. [Generator Functions vs Generator Expressions](#generator-functions-vs-generator-expressions)
4. [Generators vs Iterators](#generators-vs-iterators)
5. [Python Iterators vs Java 8+ Suppliers](#python-iterators-vs-java-8-suppliers)
6. [Advanced Generator Concepts](#advanced-generator-concepts)
7. [Examples and Use Cases](#examples-and-use-cases)

---

## What are Generators?

**Generators** are a special type of iterator in Python that allow you to declare a function that behaves like an iterator. They are created using functions with the `yield` keyword instead of `return`.

### Key Characteristics

- **Lazy Evaluation**: Values are generated on-demand, not all at once
- **Memory Efficient**: Only one value is held in memory at a time
- **Stateful**: Automatically maintains state between calls
- **One-time Use**: Once exhausted, cannot be reused (must create a new generator)
- **Simpler Syntax**: Easier to write than custom iterator classes

### Basic Example

```python
# Generator function
def simple_generator():
    yield 1
    yield 2
    yield 3

# Create generator object
gen = simple_generator()

# Iterate through values
print(next(gen))  # Output: 1
print(next(gen))  # Output: 2
print(next(gen))  # Output: 3
# next(gen) would raise StopIteration
```

### How Generators Work Internally

When a generator function is called:
1. It returns a generator object without executing the function body
2. When `next()` is called, execution starts/resumes
3. Execution continues until a `yield` statement is encountered
4. The value is returned and execution pauses
5. State (local variables, instruction pointer) is saved
6. Next `next()` call resumes from where it paused

```python
def count_up():
    print("Starting...")
    yield 1
    print("Between 1 and 2")
    yield 2
    print("Between 2 and 3")
    yield 3
    print("Done!")

gen = count_up()
print("Generator created")
print(next(gen))  # Prints: Starting... then 1
print(next(gen))  # Prints: Between 1 and 2, then 2
print(next(gen))  # Prints: Between 2 and 3, then 3
# next(gen) would print "Done!" then raise StopIteration
```

---

## Types of Iterators in Python

Python provides several types of iterators, each serving different purposes:

### 1. **Built-in Collection Iterators**

These are iterators for Python's built-in data structures:

```python
# List Iterator
my_list = [1, 2, 3, 4, 5]
list_iter = iter(my_list)
print(type(list_iter))  # <class 'list_iterator'>

# Tuple Iterator
my_tuple = (10, 20, 30)
tuple_iter = iter(my_tuple)
print(type(tuple_iter))  # <class 'tuple_iterator'>

# String Iterator
my_string = "Hello"
string_iter = iter(my_string)
print(type(string_iter))  # <class 'str_iterator'>

# Dictionary Iterators
my_dict = {'a': 1, 'b': 2, 'c': 3}
keys_iter = iter(my_dict.keys())      # dict_keyiterator
values_iter = iter(my_dict.values())  # dict_valueiterator
items_iter = iter(my_dict.items())    # dict_itemiterator

# Set Iterator
my_set = {1, 2, 3}
set_iter = iter(my_set)
print(type(set_iter))  # <class 'set_iterator'>
```

### 2. **Generator Iterators**

Created using generator functions or generator expressions:

```python
# Generator Function
def squares(n):
    for i in range(n):
        yield i ** 2

gen = squares(5)
print(type(gen))  # <class 'generator'>

# Generator Expression
gen_expr = (x ** 2 for x in range(5))
print(type(gen_expr))  # <class 'generator'>
```

### 3. **File Iterators**

File objects are iterators that yield lines:

```python
# File iterator (reads line by line)
with open('example.txt', 'r') as file:
    print(type(file))  # <class '_io.TextIOWrapper'>
    for line in file:  # file is an iterator
        print(line.strip())
```

### 4. **Range Iterator**

The `range()` function returns an iterator:

```python
r = range(5)
print(type(r))  # <class 'range'>
r_iter = iter(r)
print(type(r_iter))  # <class 'range_iterator'>
```

### 5. **Enumerate Iterator**

Returns index-value pairs:

```python
fruits = ['apple', 'banana', 'cherry']
enum = enumerate(fruits)
print(type(enum))  # <class 'enumerate'>

for index, fruit in enum:
    print(f"{index}: {fruit}")
# Output:
# 0: apple
# 1: banana
# 2: cherry
```

### 6. **Zip Iterator**

Combines multiple iterables:

```python
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
cities = ['NYC', 'LA', 'Chicago']

zipped = zip(names, ages, cities)
print(type(zipped))  # <class 'zip'>

for name, age, city in zipped:
    print(f"{name}, {age}, {city}")
```

### 7. **Map Iterator**

Applies a function to each item:

```python
numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
print(type(squared))  # <class 'map'>
print(list(squared))  # [1, 4, 9, 16, 25]
```

### 8. **Filter Iterator**

Filters items based on a condition:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = filter(lambda x: x % 2 == 0, numbers)
print(type(evens))  # <class 'filter'>
print(list(evens))  # [2, 4, 6, 8, 10]
```

### 9. **Itertools Iterators**

The `itertools` module provides specialized iterators:

```python
import itertools

# Infinite Iterators
count_iter = itertools.count(10, 2)  # 10, 12, 14, 16...
cycle_iter = itertools.cycle([1, 2, 3])  # 1, 2, 3, 1, 2, 3...
repeat_iter = itertools.repeat('A', 3)  # 'A', 'A', 'A'

# Combinatoric Iterators
perm = itertools.permutations([1, 2, 3], 2)  # All 2-element permutations
comb = itertools.combinations([1, 2, 3], 2)  # All 2-element combinations

# Terminating Iterators
chain_iter = itertools.chain([1, 2], [3, 4])  # 1, 2, 3, 4
compress_iter = itertools.compress('ABCDEF', [1, 0, 1, 0, 1, 1])  # A, C, E, F
```

### 10. **Reversed Iterator**

Reverses a sequence:

```python
numbers = [1, 2, 3, 4, 5]
rev = reversed(numbers)
print(type(rev))  # <class 'list_reverseiterator'>
print(list(rev))  # [5, 4, 3, 2, 1]
```

### 11. **Custom Iterators**

User-defined classes implementing `__iter__()` and `__next__()`:

```python
class CountDown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

countdown = CountDown(5)
print(list(countdown))  # [5, 4, 3, 2, 1]
```

---

## Generator Functions vs Generator Expressions

### Generator Functions

Defined using `def` and `yield`:

```python
def fibonacci(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Usage
fib = fibonacci(10)
for num in fib:
    print(num, end=' ')
# Output: 0 1 1 2 3 5 8 13 21 34
```

### Generator Expressions

Similar to list comprehensions but with parentheses:

```python
# List Comprehension (creates entire list in memory)
squares_list = [x ** 2 for x in range(1000000)]

# Generator Expression (lazy evaluation)
squares_gen = (x ** 2 for x in range(1000000))

# Memory comparison
import sys
print(sys.getsizeof(squares_list))  # Large (e.g., 8697464 bytes)
print(sys.getsizeof(squares_gen))   # Small (e.g., 112 bytes)
```

### Comparison Table

| Feature | Generator Function | Generator Expression |
|---------|-------------------|---------------------|
| Syntax | `def` with `yield` | `(expr for item in iterable)` |
| Complexity | Can have complex logic | Simple transformations |
| Reusability | Can be called multiple times | Single-use expression |
| Readability | Better for complex logic | Better for simple cases |
| State | Can maintain complex state | Limited state |

---

## Generators vs Iterators

### Similarities
- Both implement the iterator protocol
- Both support lazy evaluation
- Both are one-time use (exhausted after iteration)
- Both use `next()` to get values

### Differences

| Aspect | Generator | Custom Iterator |
|--------|-----------|-----------------|
| Implementation | Function with `yield` | Class with `__iter__()` and `__next__()` |
| Code Length | Shorter, more concise | Longer, more verbose |
| State Management | Automatic (local variables) | Manual (instance variables) |
| Complexity | Best for simple cases | Better for complex state |
| Memory | Minimal overhead | More overhead (class instance) |

### Example Comparison

```python
# Using Generator (Simple)
def squares_gen(n):
    for i in range(n):
        yield i ** 2

# Using Custom Iterator (Verbose)
class SquaresIterator:
    def __init__(self, n):
        self.n = n
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.n:
            result = self.current ** 2
            self.current += 1
            return result
        raise StopIteration

# Both work the same way
gen = squares_gen(5)
iter_obj = SquaresIterator(5)

print(list(gen))       # [0, 1, 4, 9, 16]
print(list(iter_obj))  # [0, 1, 4, 9, 16]
```

---

## Python Iterators vs Java 8+ Suppliers

### Conceptual Comparison

While Python iterators and Java Suppliers share some similarities, they serve different purposes:

| Aspect | Python Iterator/Generator | Java 8+ Supplier |
|--------|---------------------------|------------------|
| **Primary Purpose** | Sequential traversal of collections | Lazy value generation/supply |
| **State** | Stateful (remembers position) | Can be stateless or stateful |
| **Exhaustion** | Gets exhausted after one pass | Can be called repeatedly |
| **Method** | `__next__()` / `next()` | `get()` |
| **Lazy Evaluation** | Yes | Yes |
| **Use Case** | Iterating over sequences | Deferred computation, factory pattern |

### Python Iterator Example

```python
# Python Generator (Iterator)
def number_generator():
    yield 1
    yield 2
    yield 3

gen = number_generator()
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# next(gen) raises StopIteration (exhausted)
```

### Java Supplier Equivalent

```java
// Java Supplier (can be called multiple times)
import java.util.function.Supplier;

Supplier<Integer> randomSupplier = () -> (int)(Math.random() * 100);

System.out.println(randomSupplier.get());  // e.g., 42
System.out.println(randomSupplier.get());  // e.g., 73
System.out.println(randomSupplier.get());  // e.g., 15
// Can be called indefinitely
```

### More Accurate Java Equivalent: Iterator

Python iterators are more similar to Java's `Iterator` interface:

```java
// Java Iterator (closer to Python iterator)
import java.util.*;

List<Integer> numbers = Arrays.asList(1, 2, 3);
Iterator<Integer> iterator = numbers.iterator();

System.out.println(iterator.next());  // 1
System.out.println(iterator.next());  // 2
System.out.println(iterator.next());  // 3
// iterator.next() throws NoSuchElementException (exhausted)
```

### Python Equivalent to Java Supplier

For a reusable, non-exhausting supplier pattern in Python, use a callable or function:

```python
import random

# Python callable (similar to Java Supplier)
def random_supplier():
    return random.randint(1, 100)

# Or using lambda
random_supplier = lambda: random.randint(1, 100)

# Can be called multiple times
print(random_supplier())  # e.g., 42
print(random_supplier())  # e.g., 73
print(random_supplier())  # e.g., 15
# Can be called indefinitely
```

### Key Differences Summary

**Python Iterators/Generators:**
- ✅ Sequential access to a series of values
- ✅ Stateful (remembers position)
- ✅ One-time use (exhausted after iteration)
- ✅ Used with `for` loops and `next()`
- ❌ Not reusable once exhausted

**Java Suppliers:**
- ✅ Provides values on-demand
- ✅ Can be stateless or stateful
- ✅ Reusable (can call `get()` multiple times)
- ✅ Used for lazy initialization, factory patterns
- ❌ Not designed for sequential iteration

**Closest Match:**
- Python Iterator ≈ Java Iterator
- Python Callable/Function ≈ Java Supplier

---

## Advanced Generator Concepts

### 1. Generator with `send()`

Generators can receive values using the `send()` method:

```python
def echo_generator():
    while True:
        received = yield
        print(f"Received: {received}")

gen = echo_generator()
next(gen)  # Prime the generator
gen.send("Hello")   # Output: Received: Hello
gen.send("World")   # Output: Received: World
```

### 2. Generator with `return`

Generators can have a return value (available in the StopIteration exception):

```python
def generator_with_return():
    yield 1
    yield 2
    return "Done!"

gen = generator_with_return()
print(next(gen))  # 1
print(next(gen))  # 2

try:
    next(gen)
except StopIteration as e:
    print(e.value)  # Done!
```

### 3. Generator Delegation with `yield from`

Delegate to another generator:

```python
def inner_generator():
    yield 1
    yield 2

def outer_generator():
    yield 'Start'
    yield from inner_generator()  # Delegate
    yield 'End'

gen = outer_generator()
print(list(gen))  # ['Start', 1, 2, 'End']
```

### 4. Generator Pipelines

Chain generators for data processing:

```python
def read_data():
    for i in range(10):
        yield i

def filter_even(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num

def square(numbers):
    for num in numbers:
        yield num ** 2

# Pipeline
pipeline = square(filter_even(read_data()))
print(list(pipeline))  # [0, 4, 16, 36, 64]
```

---

## Examples and Use Cases

### Use Case 1: Reading Large Files

```python
def read_large_file(file_path):
    """Memory-efficient file reading"""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Process file line by line without loading entire file
for line in read_large_file('huge_file.txt'):
    process(line)
```

### Use Case 2: Infinite Sequences

```python
def fibonacci_infinite():
    """Infinite Fibonacci sequence"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Get first 10 Fibonacci numbers
fib = fibonacci_infinite()
first_10 = [next(fib) for _ in range(10)]
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Use Case 3: Data Streaming

```python
import time

def data_stream():
    """Simulate real-time data stream"""
    count = 0
    while True:
        count += 1
        yield {'id': count, 'timestamp': time.time()}
        time.sleep(1)

# Process data as it arrives
stream = data_stream()
for data in stream:
    print(data)
    if data['id'] >= 5:
        break
```

### Use Case 4: Batch Processing

```python
def batch_generator(iterable, batch_size):
    """Generate batches from an iterable"""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:  # Yield remaining items
        yield batch

# Process data in batches
data = range(25)
for batch in batch_generator(data, 10):
    print(f"Processing batch: {batch}")
# Output:
# Processing batch: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Processing batch: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
# Processing batch: [20, 21, 22, 23, 24]
```

### Use Case 5: Tree Traversal

```python
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def inorder_traversal(node):
    """Generator for inorder tree traversal"""
    if node:
        yield from inorder_traversal(node.left)
        yield node.value
        yield from inorder_traversal(node.right)

# Create tree
root = TreeNode(1,
    TreeNode(2, TreeNode(4), TreeNode(5)),
    TreeNode(3)
)

# Traverse
for value in inorder_traversal(root):
    print(value, end=' ')  # Output: 4 2 5 1 3
```

---

## Does `range()` Use `yield` Internally?

### Short Answer: **NO**

The `range()` function does **NOT** use `yield` internally. It's implemented in C as a built-in type, not as a Python generator function. However, it implements the **iterator protocol** (`__iter__()` and `__next__()`), making it behave like an iterator.

### Key Differences

| Aspect | `range()` | Generator (with `yield`) |
|--------|-----------|--------------------------|
| Implementation | C code (built-in type) | Python function with `yield` |
| Type | `<class 'range'>` | `<class 'generator'>` |
| Memory | Stores only start, stop, step | Stores function state |
| Indexing | Supports indexing `range(10)[5]` | No indexing support |
| Length | Has `__len__()` method | No `__len__()` method |
| Reversible | Supports `reversed()` efficiently | Requires consuming generator |
| Reusable | Can iterate multiple times | One-time use (exhausted) |

### Proof: `range()` is Not a Generator

```python
# Check the type
r = range(5)
print(type(r))  # <class 'range'> (NOT generator)

# Generators don't support indexing
gen = (x for x in range(5))
try:
    print(gen[2])  # TypeError: 'generator' object is not subscriptable
except TypeError as e:
    print(f"Generator error: {e}")

# But range does support indexing
print(r[2])  # 2 (works fine)

# Generators don't have len()
try:
    print(len(gen))  # TypeError: object of type 'generator' has no len()
except TypeError as e:
    print(f"Generator error: {e}")

# But range does have len()
print(len(r))  # 5 (works fine)

# Range is reusable
for x in r:
    print(x, end=' ')  # 0 1 2 3 4
print()
for x in r:
    print(x, end=' ')  # 0 1 2 3 4 (works again!)

# Generator is NOT reusable
gen = (x for x in range(3))
print(list(gen))  # [0, 1, 2]
print(list(gen))  # [] (exhausted!)
```

---

## Internal Working of `range()` - Code Walkthrough

### How `range()` Actually Works

The `range()` object is a **sequence type** that stores only three values:
- `start`: Starting value
- `stop`: Stopping value (exclusive)
- `step`: Step size

It calculates values on-the-fly using arithmetic, rather than storing them in memory.

### Python Equivalent Implementation

Here's how `range()` works internally, implemented in pure Python:

```python
class MyRange:
    """Python implementation mimicking range() behavior"""
    
    def __init__(self, *args):
        # Handle different argument patterns
        if len(args) == 1:
            self.start = 0
            self.stop = args[0]
            self.step = 1
        elif len(args) == 2:
            self.start = args[0]
            self.stop = args[1]
            self.step = 1
        elif len(args) == 3:
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
            if self.step == 0:
                raise ValueError("step argument must not be zero")
        else:
            raise TypeError(f"range expected at most 3 arguments, got {len(args)}")
    
    def __iter__(self):
        """Return an iterator object"""
        return MyRangeIterator(self.start, self.stop, self.step)
    
    def __len__(self):
        """Calculate length without generating all values"""
        if self.step > 0:
            return max(0, (self.stop - self.start + self.step - 1) // self.step)
        else:
            return max(0, (self.stop - self.start + self.step + 1) // self.step)
    
    def __getitem__(self, index):
        """Support indexing: range(10)[5]"""
        length = len(self)
        
        # Handle negative indices
        if index < 0:
            index += length
        
        # Check bounds
        if index < 0 or index >= length:
            raise IndexError("range object index out of range")
        
        # Calculate value at index
        return self.start + (index * self.step)
    
    def __repr__(self):
        """String representation"""
        if self.step == 1:
            return f"MyRange({self.start}, {self.stop})"
        return f"MyRange({self.start}, {self.stop}, {self.step})"
    
    def __contains__(self, value):
        """Support 'in' operator: 5 in range(10)"""
        if self.step > 0:
            if value < self.start or value >= self.stop:
                return False
        else:
            if value > self.start or value <= self.stop:
                return False
        
        # Check if value is reachable with the step
        return (value - self.start) % self.step == 0


class MyRangeIterator:
    """Iterator for MyRange - this is what actually generates values"""
    
    def __init__(self, start, stop, step):
        self.current = start
        self.stop = stop
        self.step = step
    
    def __iter__(self):
        """Iterator returns itself"""
        return self
    
    def __next__(self):
        """Generate next value"""
        # Check if we've reached the end
        if self.step > 0:
            if self.current >= self.stop:
                raise StopIteration
        else:
            if self.current <= self.stop:
                raise StopIteration
        
        # Calculate and return current value
        result = self.current
        self.current += self.step
        return result


# Test our implementation
print("=== Testing MyRange ===")

# Basic usage
r = MyRange(5)
print(f"MyRange(5): {list(r)}")  # [0, 1, 2, 3, 4]

# With start and stop
r = MyRange(2, 8)
print(f"MyRange(2, 8): {list(r)}")  # [2, 3, 4, 5, 6, 7]

# With step
r = MyRange(0, 10, 2)
print(f"MyRange(0, 10, 2): {list(r)}")  # [0, 2, 4, 6, 8]

# Negative step
r = MyRange(10, 0, -1)
print(f"MyRange(10, 0, -1): {list(r)}")  # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# Length
r = MyRange(5, 15)
print(f"len(MyRange(5, 15)): {len(r)}")  # 10

# Indexing
r = MyRange(10, 20)
print(f"MyRange(10, 20)[0]: {r[0]}")  # 10
print(f"MyRange(10, 20)[5]: {r[5]}")  # 15
print(f"MyRange(10, 20)[-1]: {r[-1]}")  # 19

# Membership test
r = MyRange(0, 10, 2)
print(f"4 in MyRange(0, 10, 2): {4 in r}")  # True
print(f"5 in MyRange(0, 10, 2): {5 in r}")  # False

# Reusability
r = MyRange(3)
print(f"First iteration: {list(r)}")   # [0, 1, 2]
print(f"Second iteration: {list(r)}")  # [0, 1, 2] (works again!)
```

### Step-by-Step Walkthrough

Let's trace through `range(2, 8, 2)`:

```python
# Step 1: Create range object
r = range(2, 8, 2)
# Stores: start=2, stop=8, step=2
# Memory used: ~48 bytes (just these 3 integers)

# Step 2: Start iteration (for loop calls iter())
iterator = iter(r)  # Creates a range_iterator object
# Iterator stores: current=2, stop=8, step=2

# Step 3: First next() call
value1 = next(iterator)
# Check: current (2) < stop (8)? Yes, continue
# Return: 2
# Update: current = 2 + 2 = 4

# Step 4: Second next() call
value2 = next(iterator)
# Check: current (4) < stop (8)? Yes, continue
# Return: 4
# Update: current = 4 + 2 = 6

# Step 5: Third next() call
value3 = next(iterator)
# Check: current (6) < stop (8)? Yes, continue
# Return: 6
# Update: current = 6 + 2 = 8

# Step 6: Fourth next() call
try:
    value4 = next(iterator)
except StopIteration:
    print("Iteration complete!")
# Check: current (8) < stop (8)? No, raise StopIteration
```

### Visual Representation

```
range(2, 8, 2) Object:
┌─────────────────┐
│ start: 2        │
│ stop:  8        │
│ step:  2        │
└─────────────────┘
       │
       │ iter() creates iterator
       ▼
range_iterator Object:
┌─────────────────┐
│ current: 2      │ ──next()──> Returns 2, current becomes 4
│ stop:    8      │ ──next()──> Returns 4, current becomes 6
│ step:    2      │ ──next()──> Returns 6, current becomes 8
└─────────────────┘ ──next()──> Raises StopIteration
```

### Memory Efficiency Comparison

```python
import sys

# Using range (memory efficient)
r = range(1000000)
print(f"range(1000000) size: {sys.getsizeof(r)} bytes")  # ~48 bytes

# Using list (memory intensive)
l = list(range(1000000))
print(f"list(range(1000000)) size: {sys.getsizeof(l)} bytes")  # ~8000000+ bytes

# Using generator (memory efficient but different)
g = (x for x in range(1000000))
print(f"generator size: {sys.getsizeof(g)} bytes")  # ~112 bytes
```

### Why `range()` Doesn't Use `yield`

1. **Performance**: C implementation is much faster than Python generators
2. **Features**: Needs to support indexing, length, membership tests
3. **Reusability**: Must be iterable multiple times
4. **Memory**: Only stores 3 integers regardless of range size

### Generator Equivalent (Less Efficient)

If we wanted to create a generator version (not recommended):

```python
def range_generator(start, stop, step=1):
    """Generator version of range (less efficient)"""
    current = start
    if step > 0:
        while current < stop:
            yield current
            current += step
    else:
        while current > stop:
            yield current
            current += step

# Works like range but:
# - Cannot be indexed: gen[5] ❌
# - Cannot get length: len(gen) ❌
# - Cannot reuse: exhausted after one iteration ❌
# - Cannot test membership efficiently ❌

gen = range_generator(0, 5)
print(list(gen))  # [0, 1, 2, 3, 4]
print(list(gen))  # [] (exhausted!)
```

### Key Takeaways

1. **`range()` does NOT use `yield`** - it's a C-implemented sequence type
2. **`range()` is more powerful than generators** - supports indexing, length, reusability
3. **`range()` is memory efficient** - stores only start, stop, step values
4. **`range()` calculates values on-the-fly** - using arithmetic, not by storing them
5. **`range()` creates iterators** - when you iterate over it, it returns a `range_iterator`

---

## Summary

### Generators
- Functions that use `yield` to produce values lazily
- Memory-efficient alternative to creating full lists
- Automatically implement the iterator protocol
- Simpler syntax than custom iterator classes

### Types of Iterators
Python provides 11+ types of iterators including:
- Built-in collection iterators (list, tuple, dict, set, string)
- Generator iterators (functions and expressions)
- File iterators
- Range, enumerate, zip, map, filter iterators
- Itertools iterators
- Custom iterators

### Python vs Java
- **Python Iterators ≈ Java Iterator** (stateful, one-time use, sequential)
- **Python Callable/Function ≈ Java Supplier** (reusable, on-demand values)
- Python generators are unique to Python (no direct Java equivalent)

### When to Use Generators
- ✅ Processing large datasets
- ✅ Infinite sequences
- ✅ Data streaming
- ✅ Memory-constrained environments
- ✅ Pipeline processing

---

## Additional Resources

- [Python Generator Documentation](https://docs.python.org/3/howto/functional.html#generators)
- [PEP 255 - Simple Generators](https://www.python.org/dev/peps/pep-0255/)
- [PEP 342 - Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/)
- [Itertools Module](https://docs.python.org/3/library/itertools.html)
