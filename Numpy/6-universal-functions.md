[← Previous: Shape Manipulation](5-shape-manipulation.md) | [🏠 Home](README.md) | [Next: Linear Algebra →](7-linear-algebra.md)

---

# 6. Universal Functions (ufuncs)

## Table of Contents
- [What are ufuncs?](#what-are-ufuncs)
- [Mathematical ufuncs](#mathematical-ufuncs)
- [Trigonometric Functions](#trigonometric-functions)
- [Comparison Functions](#comparison-functions)
- [Custom ufuncs](#custom-ufuncs)
- [Performance Benefits](#performance-benefits)
- [Best Practices](#best-practices)

---

## What are ufuncs?

**Universal functions (ufuncs)** are functions that operate element-wise on NumPy arrays. They are:
- **Vectorized** - No Python loops needed
- **Fast** - Implemented in C
- **Broadcasting-aware** - Work with different shapes
- **Type-flexible** - Handle multiple data types

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# ufunc: operates on each element
result = np.sqrt(arr)  # [1. 1.414 1.732 2. 2.236]

# Equivalent slow Python loop
result = [np.sqrt(x) for x in arr]
```

---

## Mathematical ufuncs

### Basic Math

```python
arr = np.array([1, 4, 9, 16, 25])

# Square root
print(np.sqrt(arr))     # [1. 2. 3. 4. 5.]

# Power
print(np.power(arr, 2)) # [1 16 81 256 625]
print(arr ** 0.5)       # [1. 2. 3. 4. 5.]

# Absolute value
arr = np.array([-1, -2, 3, -4])
print(np.abs(arr))      # [1 2 3 4]

# Sign
print(np.sign(arr))     # [-1 -1  1 -1]
```

### Exponential and Logarithmic

```python
arr = np.array([1, 2, 3])

# Exponential
print(np.exp(arr))      # [2.718 7.389 20.086]
print(np.exp2(arr))     # [2. 4. 8.] (2^x)

# Logarithms
arr = np.array([1, 10, 100, 1000])
print(np.log(arr))      # [0. 2.303 4.605 6.908] (natural log)
print(np.log10(arr))    # [0. 1. 2. 3.] (base 10)
print(np.log2(arr))     # [0. 3.322 6.644 9.966] (base 2)
```

### Rounding

```python
arr = np.array([1.2, 2.5, 3.7, 4.9, -1.5])

print(np.round(arr))    # [ 1.  2.  4.  5. -2.] (round to nearest)
print(np.floor(arr))    # [ 1.  2.  3.  4. -2.] (round down)
print(np.ceil(arr))     # [ 2.  3.  4.  5. -1.] (round up)
print(np.trunc(arr))    # [ 1.  2.  3.  4. -1.] (truncate)
```

---

## Trigonometric Functions

```python
# Angles in radians
angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])

# Basic trig functions
print(np.sin(angles))
# [0. 0.5 0.707 0.866 1.]

print(np.cos(angles))
# [1. 0.866 0.707 0.5 0.]

print(np.tan(angles))
# [0. 0.577 1. 1.732 1.633e+16]

# Convert degrees to radians
degrees = np.array([0, 30, 45, 60, 90])
radians = np.deg2rad(degrees)
print(np.sin(radians))  # [0. 0.5 0.707 0.866 1.]

# Inverse trig
values = np.array([0, 0.5, 0.707, 0.866, 1])
print(np.arcsin(values))  # Angles in radians
print(np.rad2deg(np.arcsin(values)))  # Convert to degrees
```

---

## Comparison Functions

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([5, 4, 3, 2, 1])

# Element-wise maximum
print(np.maximum(a, b))  # [5 4 3 4 5]

# Element-wise minimum
print(np.minimum(a, b))  # [1 2 3 2 1]

# Clip values
arr = np.array([1, 5, 10, 15, 20])
print(np.clip(arr, 5, 15))  # [5 5 10 15 15]

# Where (conditional selection)
condition = a > 3
print(np.where(condition, a, b))  # [5 4 3 4 5]
# If condition is True, take from a, else from b
```

---

## Custom ufuncs

### Creating Custom ufuncs

```python
# Python function
def my_function(x):
    return x ** 2 + 2 * x + 1

# Convert to ufunc
my_ufunc = np.frompyfunc(my_function, 1, 1)

arr = np.array([1, 2, 3, 4, 5])
result = my_ufunc(arr)
print(result)  # [4 9 16 25 36]

# Note: frompyfunc returns object dtype
# Use vectorize for better type handling
my_vectorized = np.vectorize(my_function)
result = my_vectorized(arr)
print(result)  # [4 9 16 25 36]
```

### Using np.vectorize

```python
def complex_function(x, y):
    if x > y:
        return x + y
    else:
        return x - y

# Vectorize the function
vec_func = np.vectorize(complex_function)

a = np.array([1, 2, 3, 4])
b = np.array([4, 3, 2, 1])
result = vec_func(a, b)
print(result)  # [-3 -1  1  3]
```

---

## Performance Benefits

### ufuncs vs Python Loops

```python
import time

# Large array
arr = np.arange(1000000)

# Python loop
start = time.time()
result = [x ** 2 for x in arr]
python_time = time.time() - start

# NumPy ufunc
start = time.time()
result = arr ** 2
numpy_time = time.time() - start

print(f"Python: {python_time:.4f}s")
print(f"NumPy: {numpy_time:.4f}s")
print(f"Speedup: {python_time/numpy_time:.1f}x")
# Typical output: 50-100x faster
```

### Broadcasting with ufuncs

```python
# ufuncs automatically broadcast
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
vector = np.array([10, 20, 30])

# Element-wise addition with broadcasting
result = np.add(matrix, vector)
print(result)
# [[11 22 33]
#  [14 25 36]]

# Same as:
result = matrix + vector
```

---

## Common ufunc Methods

### Reduce

```python
arr = np.array([1, 2, 3, 4, 5])

# Sum using reduce
print(np.add.reduce(arr))  # 15 (1+2+3+4+5)

# Product
print(np.multiply.reduce(arr))  # 120 (1*2*3*4*5)

# Maximum
print(np.maximum.reduce(arr))  # 5
```

### Accumulate

```python
arr = np.array([1, 2, 3, 4, 5])

# Cumulative sum
print(np.add.accumulate(arr))  # [1 3 6 10 15]

# Cumulative product
print(np.multiply.accumulate(arr))  # [1 2 6 24 120]
```

### Outer

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

# Outer product
print(np.multiply.outer(a, b))
# [[10 20 30]
#  [20 40 60]
#  [30 60 90]]

# Addition table
print(np.add.outer(a, b))
# [[11 21 31]
#  [12 22 32]
#  [13 23 33]]
```

---

## Best Practices

### 1. Use ufuncs Instead of Loops

```python
# ❌ BAD - Slow
result = []
for x in arr:
    result.append(np.sqrt(x))

# ✅ GOOD - Fast
result = np.sqrt(arr)
```

### 2. Chain ufuncs for Complex Operations

```python
# ✅ GOOD - Efficient chaining
arr = np.array([1, 2, 3, 4, 5])
result = np.sqrt(np.abs(np.sin(arr)))
```

### 3. Use Built-in ufuncs When Available

```python
# ❌ BAD - Custom function when built-in exists
def my_square(x):
    return x ** 2
vec_square = np.vectorize(my_square)

# ✅ GOOD - Use built-in
result = np.square(arr)  # or arr ** 2
```

---

## Quick Reference

```python
# Math
np.sqrt(), np.square(), np.abs(), np.sign()
np.exp(), np.log(), np.log10(), np.log2()
np.power(arr, 2)

# Rounding
np.round(), np.floor(), np.ceil(), np.trunc()

# Trig
np.sin(), np.cos(), np.tan()
np.arcsin(), np.arccos(), np.arctan()
np.deg2rad(), np.rad2deg()

# Comparison
np.maximum(a, b), np.minimum(a, b)
np.clip(arr, min, max)
np.where(condition, x, y)

# Methods
ufunc.reduce(arr)       # Aggregate
ufunc.accumulate(arr)   # Cumulative
ufunc.outer(a, b)       # Outer product

# Custom
np.vectorize(func)
np.frompyfunc(func, nin, nout)
```

---

[← Previous: Shape Manipulation](5-shape-manipulation.md) | [🏠 Home](README.md) | [Next: Linear Algebra →](7-linear-algebra.md)
