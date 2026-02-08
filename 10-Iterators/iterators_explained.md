# Python Iterators: A Complete Guide

## Table of Contents
1. [What is an Iterator?](#what-is-an-iterator)
2. [Types of Iterators](#types-of-iterators)
3. [Internal Working of Iterators](#internal-working-of-iterators)
4. [Creating Custom Iterators](#creating-custom-iterators)
5. [Examples and Walkthroughs](#examples-and-walkthroughs)
6. [Best Practices](#best-practices)

---

## What is an Iterator?

An **iterator** is an object in Python that implements the iterator protocol, consisting of two methods:
- `__iter__()`: Returns the iterator object itself
- `__next__()`: Returns the next value from the iterator

Iterators allow you to traverse through all elements of a collection (like lists, tuples, dictionaries) one at a time without needing to know the underlying structure.

### Key Characteristics
- **Lazy Evaluation**: Values are generated on-demand, not all at once
- **Memory Efficient**: Only one element is in memory at a time
- **One-way Traversal**: Can only move forward, not backward
- **Stateful**: Remembers its position during iteration

---

## Types of Iterators

### 1. **Built-in Iterators**

Python provides several built-in iterators for common data structures:

#### a) Sequence Iterators
```python
# List Iterator
my_list = [1, 2, 3, 4, 5]
list_iter = iter(my_list)
print(next(list_iter))  # Output: 1
print(next(list_iter))  # Output: 2

# Tuple Iterator
my_tuple = ('a', 'b', 'c')
tuple_iter = iter(my_tuple)
print(next(tuple_iter))  # Output: 'a'

# String Iterator
my_string = "Hello"
string_iter = iter(my_string)
print(next(string_iter))  # Output: 'H'
```

#### b) Dictionary Iterators
```python
my_dict = {'name': 'Alice', 'age': 30, 'city': 'NYC'}

# Keys iterator (default)
keys_iter = iter(my_dict)
print(next(keys_iter))  # Output: 'name'

# Values iterator
values_iter = iter(my_dict.values())
print(next(values_iter))  # Output: 'Alice'

# Items iterator
items_iter = iter(my_dict.items())
print(next(items_iter))  # Output: ('name', 'Alice')
```

#### c) Set Iterator
```python
my_set = {10, 20, 30}
set_iter = iter(my_set)
print(next(set_iter))  # Output: 10 (order not guaranteed)
```

#### d) File Iterator
```python
# Files are iterators by default
with open('example.txt', 'r') as file:
    for line in file:  # file object is an iterator
        print(line.strip())
```

### 2. **Generator Iterators**

Generators are a special type of iterator created using functions with `yield` statements.

```python
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

counter = count_up_to(5)
print(next(counter))  # Output: 1
print(next(counter))  # Output: 2
```

### 3. **Iterator Functions (itertools module)**

Python's `itertools` module provides powerful iterator building blocks:

```python
import itertools

# count() - infinite iterator
counter = itertools.count(start=10, step=2)
print(next(counter))  # Output: 10
print(next(counter))  # Output: 12

# cycle() - cycles through an iterable infinitely
colors = itertools.cycle(['red', 'green', 'blue'])
print(next(colors))  # Output: 'red'
print(next(colors))  # Output: 'green'

# repeat() - repeats an object
repeater = itertools.repeat('Hello', 3)
print(list(repeater))  # Output: ['Hello', 'Hello', 'Hello']

# chain() - combines multiple iterables
combined = itertools.chain([1, 2], [3, 4], [5, 6])
print(list(combined))  # Output: [1, 2, 3, 4, 5, 6]
```

### 4. **Custom Iterators**

You can create your own iterators by implementing the iterator protocol:

```python
class MyIterator:
    def __init__(self, max_value):
        self.max_value = max_value
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max_value:
            self.current += 1
            return self.current
        else:
            raise StopIteration

my_iter = MyIterator(5)
for num in my_iter:
    print(num)  # Output: 1, 2, 3, 4, 5
```

---

## Internal Working of Iterators

### The Iterator Protocol

The iterator protocol consists of two methods that work together:

```python
# Behind the scenes of a for loop
iterable = [1, 2, 3]

# Step 1: Get iterator from iterable
iterator = iter(iterable)  # Calls iterable.__iter__()

# Step 2: Loop through values
while True:
    try:
        value = next(iterator)  # Calls iterator.__next__()
        print(value)
    except StopIteration:
        break  # Exit when no more items
```

### Memory Diagram

```
Iterable Object (List): [1, 2, 3, 4, 5]
                         ↓
              iter() calls __iter__()
                         ↓
Iterator Object: {current_index: 0, data_reference: [1,2,3,4,5]}
                         ↓
         next() calls __next__()
                         ↓
    Returns current item & increments index
                         ↓
    When exhausted → raises StopIteration
```

### State Management

Iterators maintain internal state to track their position:

```python
my_list = [10, 20, 30]
iter1 = iter(my_list)
iter2 = iter(my_list)

print(next(iter1))  # Output: 10
print(next(iter1))  # Output: 20
print(next(iter2))  # Output: 10 (independent state)
```

### Difference: Iterable vs Iterator

| Aspect | Iterable | Iterator |
|--------|----------|----------|
| Definition | Object that can return an iterator | Object that produces values one at a time |
| Methods | `__iter__()` | `__iter__()` and `__next__()` |
| Reusable | Yes (can create multiple iterators) | No (exhausted after one pass) |
| Examples | list, tuple, dict, set, string | iter(list), generator objects |

```python
# Iterable (can be iterated multiple times)
my_list = [1, 2, 3]
for x in my_list:
    print(x)
for x in my_list:  # Works again
    print(x)

# Iterator (exhausted after one pass)
my_iter = iter(my_list)
for x in my_iter:
    print(x)
for x in my_iter:  # Nothing printed (exhausted)
    print(x)
```

---

## Creating Custom Iterators

### Example 1: Fibonacci Iterator

```python
class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.a, self.b = 0, 1
        self.count = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count < self.limit:
            result = self.a
            self.a, self.b = self.b, self.a + self.b
            self.count += 1
            return result
        else:
            raise StopIteration

# Usage
fib = Fibonacci(10)
for num in fib:
    print(num, end=' ')
# Output: 0 1 1 2 3 5 8 13 21 34
```

### Example 2: Reverse Iterator

```python
class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index > 0:
            self.index -= 1
            return self.data[self.index]
        else:
            raise StopIteration

# Usage
rev = ReverseIterator([1, 2, 3, 4, 5])
print(list(rev))  # Output: [5, 4, 3, 2, 1]
```

### Example 3: Even Numbers Iterator

```python
class EvenNumbers:
    def __init__(self, start, end):
        self.current = start if start % 2 == 0 else start + 1
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= self.end:
            result = self.current
            self.current += 2
            return result
        else:
            raise StopIteration

# Usage
evens = EvenNumbers(1, 10)
print(list(evens))  # Output: [2, 4, 6, 8, 10]
```

---

## Examples and Walkthroughs

### Walkthrough 1: Understanding Iterator Exhaustion

```python
# Create a list and its iterator
numbers = [1, 2, 3]
num_iter = iter(numbers)

# First iteration
print("First iteration:")
for num in num_iter:
    print(num)
# Output: 1, 2, 3

# Second iteration (iterator is exhausted)
print("\nSecond iteration:")
for num in num_iter:
    print(num)
# Output: (nothing - iterator is exhausted)

# Solution: Create a new iterator
num_iter = iter(numbers)
print("\nNew iterator:")
for num in num_iter:
    print(num)
# Output: 1, 2, 3
```

### Walkthrough 2: Manual Iteration with next()

```python
fruits = ['apple', 'banana', 'cherry']
fruit_iter = iter(fruits)

# Manual iteration
print(next(fruit_iter))  # apple
print(next(fruit_iter))  # banana
print(next(fruit_iter))  # cherry

# This will raise StopIteration
try:
    print(next(fruit_iter))
except StopIteration:
    print("No more items!")
```

### Walkthrough 3: Using Default Value with next()

```python
colors = ['red', 'green', 'blue']
color_iter = iter(colors)

# Exhaust the iterator
print(next(color_iter))  # red
print(next(color_iter))  # green
print(next(color_iter))  # blue

# Use default value instead of raising exception
print(next(color_iter, 'No more colors'))  # No more colors
```

### Walkthrough 4: Infinite Iterator with Break Condition

```python
import itertools

# Infinite counter
counter = itertools.count(1)

# Use with break condition
for num in counter:
    if num > 5:
        break
    print(num)
# Output: 1, 2, 3, 4, 5
```

### Walkthrough 5: Chaining Iterators

```python
import itertools

list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

# Chain multiple iterators
combined = itertools.chain(list1, list2, list3)
print(list(combined))
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## Best Practices

### 1. **Use Iterators for Large Datasets**
```python
# Bad: Loads entire file into memory
with open('large_file.txt') as f:
    lines = f.readlines()  # All lines in memory
    for line in lines:
        process(line)

# Good: Processes one line at a time
with open('large_file.txt') as f:
    for line in f:  # File object is an iterator
        process(line)
```

### 2. **Prefer Generators for Simple Iterators**
```python
# Custom iterator class (verbose)
class SquareIterator:
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

# Generator function (concise)
def square_generator(n):
    for i in range(n):
        yield i ** 2
```

### 3. **Handle StopIteration Gracefully**
```python
my_iter = iter([1, 2, 3])

# Use default value
value = next(my_iter, None)

# Or use try-except
try:
    value = next(my_iter)
except StopIteration:
    print("Iterator exhausted")
```

### 4. **Don't Modify Collections During Iteration**
```python
# Bad: Modifying list during iteration
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Dangerous!

# Good: Create new list or use list comprehension
numbers = [1, 2, 3, 4, 5]
numbers = [num for num in numbers if num % 2 != 0]
```

---

## Summary

- **Iterators** provide a memory-efficient way to traverse collections
- They implement `__iter__()` and `__next__()` methods
- Python has **built-in iterators** for lists, tuples, dicts, sets, strings, and files
- **Generators** are a convenient way to create iterators using `yield`
- The **itertools module** provides powerful iterator utilities
- Iterators are **stateful** and **one-way** - they can't be reset or reversed
- Use iterators for **large datasets** to save memory
- Always handle **StopIteration** exceptions or use default values with `next()`

---

## Additional Resources

- [Python Official Documentation - Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [Python itertools module](https://docs.python.org/3/library/itertools.html)
- [PEP 234 - Iterators](https://www.python.org/dev/peps/pep-0234/)
