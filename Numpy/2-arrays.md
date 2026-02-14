[← Previous: Introduction](1-introduction.md) | [🏠 Home](README.md) | [Next: Indexing & Slicing →](3-indexing-slicing.md)

---

# 2. NumPy Arrays

## Table of Contents
- [Array Creation Methods](#array-creation-methods)
- [Array Types and dtypes](#array-types-and-dtypes)
- [Array Properties](#array-properties)
- [Internal Memory Layout](#internal-memory-layout)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Array Creation Methods

### 1. From Python Lists/Tuples

```python
import numpy as np

# 1D array from list
arr1d = np.array([1, 2, 3, 4, 5])
print(arr1d)  # [1 2 3 4 5]

# 2D array from nested lists
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]]

# 3D array
arr3d = np.array([[[1, 2], [3, 4]],
                  [[5, 6], [7, 8]]])
print(arr3d.shape)  # (2, 2, 2)
```

### 2. Using Built-in Functions

```python
# Zeros
zeros = np.zeros((3, 4))  # 3x4 array of zeros
print(zeros)
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]

# Ones
ones = np.ones((2, 3))  # 2x3 array of ones
print(ones)
# [[1. 1. 1.]
#  [1. 1. 1.]]

# Full (constant value)
fives = np.full((2, 2), 5)
print(fives)
# [[5 5]
#  [5 5]]

# Empty (uninitialized - faster but random values)
empty = np.empty((2, 3))  # Values are whatever was in memory

# Identity matrix
identity = np.eye(3)  # 3x3 identity matrix
print(identity)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]
```

### 3. Range-based Creation

```python
# arange (like Python range)
arr = np.arange(10)  # [0 1 2 3 4 5 6 7 8 9]
arr = np.arange(5, 15)  # [5 6 7 8 9 10 11 12 13 14]
arr = np.arange(0, 10, 2)  # [0 2 4 6 8]

# linspace (evenly spaced values)
arr = np.linspace(0, 1, 5)  # 5 values from 0 to 1
print(arr)  # [0.   0.25 0.5  0.75 1.  ]

arr = np.linspace(0, 10, 11)  # [0. 1. 2. 3. 4. 5. 6. 7. 8. 9. 10.]

# logspace (logarithmically spaced)
arr = np.logspace(0, 3, 4)  # [1. 10. 100. 1000.]
```

### 4. Random Arrays

```python
# Random values between 0 and 1
rand = np.random.random((2, 3))

# Random integers
rand_int = np.random.randint(0, 10, size=(3, 3))

# Normal distribution
normal = np.random.randn(3, 3)  # Mean=0, Std=1

# More in Chapter 9: Random Number Generation
```

### 5. From Existing Arrays

```python
arr = np.array([1, 2, 3])

# zeros_like, ones_like, empty_like
zeros = np.zeros_like(arr)  # Same shape as arr
ones = np.ones_like(arr)

# copy
arr_copy = arr.copy()  # Deep copy
arr_view = arr.view()  # Shallow copy (shares data)
```

---

## Array Types and dtypes

### Common Data Types

```python
# Integer types
int8 = np.array([1, 2, 3], dtype=np.int8)      # -128 to 127
int16 = np.array([1, 2, 3], dtype=np.int16)    # -32768 to 32767
int32 = np.array([1, 2, 3], dtype=np.int32)    # -2^31 to 2^31-1
int64 = np.array([1, 2, 3], dtype=np.int64)    # -2^63 to 2^63-1

# Unsigned integers
uint8 = np.array([1, 2, 3], dtype=np.uint8)    # 0 to 255
uint16 = np.array([1, 2, 3], dtype=np.uint16)  # 0 to 65535

# Float types
float16 = np.array([1.0, 2.0], dtype=np.float16)  # Half precision
float32 = np.array([1.0, 2.0], dtype=np.float32)  # Single precision
float64 = np.array([1.0, 2.0], dtype=np.float64)  # Double precision

# Boolean
bool_arr = np.array([True, False, True], dtype=np.bool_)

# Complex
complex_arr = np.array([1+2j, 3+4j], dtype=np.complex128)

# String (fixed length)
str_arr = np.array(['hello', 'world'], dtype='U10')  # Max 10 chars
```

### Type Conversion

```python
# Automatic conversion
arr = np.array([1, 2, 3.5])  # Becomes float64
print(arr.dtype)  # float64

# Explicit conversion
int_arr = np.array([1.1, 2.9, 3.5])
print(int_arr.astype(int))  # [1 2 3] (truncates)

float_arr = np.array([1, 2, 3])
print(float_arr.astype(float))  # [1. 2. 3.]
```

### dtype Information

```python
arr = np.array([1, 2, 3], dtype=np.int32)

print(arr.dtype)       # int32
print(arr.dtype.name)  # 'int32'
print(arr.itemsize)    # 4 (bytes per element)
print(arr.nbytes)      # 12 (total bytes: 3 elements × 4 bytes)
```

---

## Array Properties

```python
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# Shape (dimensions)
print(arr.shape)   # (3, 4) - 3 rows, 4 columns

# Number of dimensions
print(arr.ndim)    # 2

# Total number of elements
print(arr.size)    # 12

# Data type
print(arr.dtype)   # int64 (or int32)

# Item size (bytes per element)
print(arr.itemsize)  # 8 bytes (for int64)

# Total bytes
print(arr.nbytes)  # 96 (12 elements × 8 bytes)

# Strides (bytes to step in each dimension)
print(arr.strides)  # (32, 8) - 32 bytes per row, 8 bytes per column
```

---

## Internal Memory Layout

### Contiguous Memory

```
2D Array: [[1, 2, 3],
           [4, 5, 6]]

Memory Layout (Row-major / C-order):
┌───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │
└───┴───┴───┴───┴───┴───┘
 Row 0      Row 1

Memory Layout (Column-major / Fortran-order):
┌───┬───┬───┬───┬───┬───┐
│ 1 │ 4 │ 2 │ 5 │ 3 │ 6 │
└───┴───┴───┴───┴───┴───┘
 Col 0  Col 1  Col 2
```

```python
# C-order (row-major) - default
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')
print(arr_c.flags['C_CONTIGUOUS'])  # True
print(arr_c.flags['F_CONTIGUOUS'])  # False

# Fortran-order (column-major)
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')
print(arr_f.flags['C_CONTIGUOUS'])  # False
print(arr_f.flags['F_CONTIGUOUS'])  # True
```

### Strides Explained

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print(arr.strides)  # (24, 8) for int64

# Strides meaning:
# - 24 bytes to move to next row (3 elements × 8 bytes)
# - 8 bytes to move to next column (1 element × 8 bytes)

# Accessing arr[1, 2]:
# Memory offset = 1 * 24 + 2 * 8 = 40 bytes from start
```

### Views vs Copies

```python
original = np.array([1, 2, 3, 4, 5])

# View (shares data)
view = original[1:4]
view[0] = 999
print(original)  # [1 999 3 4 5] - original changed!

# Copy (independent data)
copy = original[1:4].copy()
copy[0] = 777
print(original)  # [1 999 3 4 5] - original unchanged
```

---

## Common Mistakes

### 1. Mixing Lists and Arrays

```python
# ❌ WRONG
arr = [1, 2, 3]  # This is a list!
arr * 2  # [1, 2, 3, 1, 2, 3] (list repetition)

# ✅ CORRECT
arr = np.array([1, 2, 3])
arr * 2  # [2 4 6] (element-wise multiplication)
```

### 2. Unexpected Type Conversion

```python
# ❌ WRONG - Loses precision
arr = np.array([1, 2, 3])  # int64
arr[0] = 3.14  # Becomes 3 (truncated!)

# ✅ CORRECT
arr = np.array([1, 2, 3], dtype=float)
arr[0] = 3.14  # Now it works
```

### 3. Modifying Views Unintentionally

```python
# ❌ WRONG
original = np.array([1, 2, 3, 4, 5])
subset = original[1:4]  # This is a view!
subset[0] = 999
print(original)  # [1 999 3 4 5] - Oops!

# ✅ CORRECT
subset = original[1:4].copy()  # Make a copy
subset[0] = 999
print(original)  # [1 2 3 4 5] - Safe
```

### 4. Using Wrong Dimension

```python
# ❌ WRONG
arr = np.array([[1, 2, 3]])  # Shape: (1, 3)
print(arr.shape)  # (1, 3) - 2D array!

# ✅ CORRECT
arr = np.array([1, 2, 3])  # Shape: (3,)
print(arr.shape)  # (3,) - 1D array
```

### 5. Not Specifying dtype

```python
# ❌ POTENTIALLY WRONG
arr = np.array([1, 2, 3])  # Could be int32 or int64 depending on platform

# ✅ BETTER
arr = np.array([1, 2, 3], dtype=np.int32)  # Explicit
```

---

## Best Practices

### 1. Specify dtype When Needed

```python
# ✅ GOOD - Explicit about data type
arr = np.zeros((1000, 1000), dtype=np.float32)  # Saves memory vs float64
```

### 2. Use Appropriate Creation Functions

```python
# ❌ BAD - Wasteful
arr = np.array([0, 0, 0, 0, 0])

# ✅ GOOD - More efficient
arr = np.zeros(5)
```

### 3. Preallocate Arrays

```python
# ❌ BAD - Slow for large arrays
result = []
for i in range(10000):
    result.append(i ** 2)
result = np.array(result)

# ✅ GOOD - Preallocate
result = np.empty(10000)
for i in range(10000):
    result[i] = i ** 2

# ✅ BEST - Vectorized
result = np.arange(10000) ** 2
```

### 4. Use copy() When Needed

```python
# ✅ GOOD - Explicit about copying
original = np.array([1, 2, 3])
independent = original.copy()
```

### 5. Check Array Properties

```python
# ✅ GOOD PRACTICE
print(f"Shape: {arr.shape}")
print(f"Dtype: {arr.dtype}")
print(f"Size: {arr.size}")
print(f"Memory: {arr.nbytes} bytes")
```

---

## Quick Reference

```python
# Creation
np.array([1, 2, 3])              # From list
np.zeros((3, 4))                 # Zeros
np.ones((2, 3))                  # Ones
np.full((2, 2), 7)               # Constant value
np.eye(3)                        # Identity matrix
np.arange(0, 10, 2)              # Range
np.linspace(0, 1, 5)             # Evenly spaced

# Properties
arr.shape                         # Dimensions
arr.dtype                         # Data type
arr.size                          # Total elements
arr.ndim                          # Number of dimensions
arr.itemsize                      # Bytes per element
arr.nbytes                        # Total bytes

# Type conversion
arr.astype(float)                 # Convert type

# Copying
arr.copy()                        # Deep copy
arr.view()                        # Shallow copy
```

---

## Summary

- NumPy arrays are **homogeneous** (single data type)
- Created using `np.array()` or specialized functions
- **dtype** determines memory usage and precision
- Arrays have **shape**, **size**, **ndim**, and other properties
- Memory is **contiguous** for efficiency
- **Views** share data, **copies** are independent
- Always specify **dtype** when precision matters

---

## Next Steps

Now that you understand array creation and properties, let's learn how to access and manipulate array elements:

### 👉 [Next: Indexing and Slicing](3-indexing-slicing.md)

---

[← Previous: Introduction](1-introduction.md) | [🏠 Home](README.md) | [Next: Indexing & Slicing →](3-indexing-slicing.md)
