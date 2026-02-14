[← Previous: Indexing & Slicing](3-indexing-slicing.md) | [🏠 Home](README.md) | [Next: Shape Manipulation →](5-shape-manipulation.md)

---

# 4. Array Operations

## Table of Contents
- [Arithmetic Operations](#arithmetic-operations)
- [Broadcasting](#broadcasting)
- [Comparison Operations](#comparison-operations)
- [Aggregation Functions](#aggregation-functions)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Arithmetic Operations

### Element-wise Operations

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# Basic arithmetic
print(a + b)   # [11 22 33 44]
print(a - b)   # [-9 -18 -27 -36]
print(a * b)   # [10 40 90 160]
print(a / b)   # [0.1 0.1 0.1 0.1]
print(a ** 2)  # [1 4 9 16]
print(a % 3)   # [1 2 0 1]

# With scalars
print(a + 10)  # [11 12 13 14]
print(a * 2)   # [2 4 6 8]
```

### Mathematical Functions

```python
arr = np.array([1, 4, 9, 16, 25])

# Square root, exponential, logarithm
print(np.sqrt(arr))    # [1. 2. 3. 4. 5.]
print(np.exp(arr))     # [e^1, e^4, e^9, ...]
print(np.log(arr))     # [0. 1.386 2.197 ...]
print(np.log10(arr))   # [0. 0.602 0.954 ...]

# Trigonometric
angles = np.array([0, np.pi/2, np.pi])
print(np.sin(angles))  # [0. 1. 0.]
print(np.cos(angles))  # [1. 0. -1.]
print(np.tan(angles))  # [0. 16331239353195370. -0.]

# Rounding
arr = np.array([1.2, 2.5, 3.7, 4.9])
print(np.round(arr))   # [1. 2. 4. 5.]
print(np.floor(arr))   # [1. 2. 3. 4.]
print(np.ceil(arr))    # [2. 3. 4. 5.]

# Note: NumPy uses "round half to even" (banker's rounding)
# 2.5 rounds to 2.0, 3.5 rounds to 4.0 (rounds to nearest even)
print(np.round([0.5, 1.5, 2.5, 3.5]))  # [0. 2. 2. 4.]
```

---

## Broadcasting

### What is Broadcasting?

Broadcasting allows NumPy to perform operations on arrays of different shapes.

```
Broadcasting Rules:
1. If arrays have different dimensions, pad the smaller shape with 1s on the left
2. Arrays are compatible if dimensions are equal or one of them is 1
3. After broadcasting, each array behaves as if it had the larger shape
```

### Broadcasting Examples

```python
# Scalar broadcasting
arr = np.array([1, 2, 3, 4])
print(arr + 10)  # [11 12 13 14]

# 1D + 1D (same shape)
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b)  # [11 22 33]

# 2D + 1D
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
vector = np.array([10, 20, 30])
print(matrix + vector)
# [[11 22 33]
#  [14 25 36]]

# 2D + column vector
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])
col_vector = np.array([[10],
                       [20]])
print(matrix + col_vector)
# [[11 12 13]
#  [24 25 26]]
```

### Broadcasting Visualization

```
Example: (3, 1) + (1, 4)

Array A (3, 1):        Array B (1, 4):
[[1]                   [[10, 20, 30, 40]]
 [2]
 [3]]

After Broadcasting (3, 4):
[[1, 1, 1, 1]          [[10, 20, 30, 40]
 [2, 2, 2, 2]    +      [10, 20, 30, 40]
 [3, 3, 3, 3]]          [10, 20, 30, 40]]

Result (3, 4):
[[11, 21, 31, 41]
 [12, 22, 32, 42]
 [13, 23, 33, 43]]
```

```python
a = np.array([[1], [2], [3]])  # Shape: (3, 1)
b = np.array([[10, 20, 30, 40]])  # Shape: (1, 4)
print(a + b)
# [[11 21 31 41]
#  [12 22 32 42]
#  [13 23 33 43]]
```

---

## Comparison Operations

### Element-wise Comparisons

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([5, 4, 3, 2, 1])

print(a == b)  # [False False  True False False]
print(a != b)  # [ True  True False  True  True]
print(a < b)   # [ True  True False False False]
print(a > b)   # [False False False  True  True]
print(a <= b)  # [ True  True  True False False]
print(a >= b)  # [False False  True  True  True]
```

### Array Comparisons

```python
a = np.array([1, 2, 3])
b = np.array([1, 2, 3])
c = np.array([1, 2, 4])

# Element-wise comparison
print(a == b)  # [ True  True  True]

# Array equality
print(np.array_equal(a, b))  # True
print(np.array_equal(a, c))  # False

# Close comparison (for floats)
a = np.array([1.0, 2.0, 3.0])
b = np.array([1.0, 2.0, 3.00001])
print(np.allclose(a, b))  # True (within tolerance)
```

---

## Aggregation Functions

### Basic Aggregations

```python
arr = np.array([1, 2, 3, 4, 5])

print(arr.sum())      # 15
print(arr.mean())     # 3.0
print(arr.std())      # 1.414... (standard deviation)
print(arr.var())      # 2.0 (variance)
print(arr.min())      # 1
print(arr.max())      # 5
print(arr.argmin())   # 0 (index of minimum)
print(arr.argmax())   # 4 (index of maximum)
```

### Axis-based Aggregations

```python
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])

# Sum along axis 0 (columns)
print(arr2d.sum(axis=0))  # [5 7 9]

# Sum along axis 1 (rows)
print(arr2d.sum(axis=1))  # [6 15]

# Mean
print(arr2d.mean(axis=0))  # [2.5 3.5 4.5]
print(arr2d.mean(axis=1))  # [2. 5.]

# Min/Max
print(arr2d.min(axis=0))  # [1 2 3]
print(arr2d.max(axis=1))  # [3 6]
```

### Cumulative Operations

```python
arr = np.array([1, 2, 3, 4, 5])

print(arr.cumsum())   # [1 3 6 10 15] (cumulative sum)
print(arr.cumprod())  # [1 2 6 24 120] (cumulative product)
```

---

## Common Mistakes

### 1. Matrix Multiplication vs Element-wise

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# ❌ WRONG - Element-wise multiplication
print(a * b)
# [[5 12]
#  [21 32]]

# ✅ CORRECT - Matrix multiplication
print(a @ b)  # or np.dot(a, b)
# [[19 22]
#  [43 50]]
```

### 2. Broadcasting Shape Mismatch

```python
a = np.array([[1, 2, 3]])  # Shape: (1, 3)
b = np.array([[1], [2]])   # Shape: (2, 1)

# ❌ This works but might not be what you expect
print(a + b)
# [[2 3 4]
#  [3 4 5]]

# ✅ Check shapes first
print(f"a shape: {a.shape}, b shape: {b.shape}")
```

### 3. In-place Operations

```python
arr = np.array([1, 2, 3], dtype=np.int32)

# ❌ WRONG - Creates new array
arr = arr / 2  # Now float64!

# ✅ CORRECT - In-place
arr //= 2  # Stays int32
```

---

## Best Practices

### 1. Use Vectorized Operations

```python
# ❌ BAD - Slow
result = []
for x in arr:
    result.append(x ** 2)

# ✅ GOOD - Fast
result = arr ** 2
```

### 2. Understand Broadcasting

```python
# ✅ GOOD - Explicit reshaping
matrix = np.array([[1, 2, 3], [4, 5, 6]])
vector = np.array([10, 20, 30])
result = matrix + vector  # Broadcasting happens

# ✅ BETTER - Explicit for clarity
vector_reshaped = vector.reshape(1, 3)
result = matrix + vector_reshaped
```

### 3. Use Appropriate Aggregation Axis

```python
# ✅ GOOD - Clear intent
row_sums = arr2d.sum(axis=1)
col_sums = arr2d.sum(axis=0)
```

---

## Quick Reference

```python
# Arithmetic
a + b, a - b, a * b, a / b, a ** 2

# Math functions
np.sqrt(), np.exp(), np.log(), np.sin(), np.cos()

# Aggregations
arr.sum(), arr.mean(), arr.std(), arr.min(), arr.max()

# Axis operations
arr.sum(axis=0)  # Column-wise
arr.sum(axis=1)  # Row-wise

# Comparisons
a == b, a < b, np.array_equal(a, b)

# Matrix multiplication
a @ b  # or np.dot(a, b)
```

---

[← Previous: Indexing & Slicing](3-indexing-slicing.md) | [🏠 Home](README.md) | [Next: Shape Manipulation →](5-shape-manipulation.md)
