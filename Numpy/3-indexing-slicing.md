[← Previous: Arrays](2-arrays.md) | [🏠 Home](README.md) | [Next: Array Operations →](4-array-operations.md)

---

# 3. Indexing and Slicing

## Table of Contents
- [Basic Indexing](#basic-indexing)
- [Slicing](#slicing)
- [Boolean Indexing](#boolean-indexing)
- [Fancy Indexing](#fancy-indexing)
- [Multi-dimensional Indexing](#multi-dimensional-indexing)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Basic Indexing

### 1D Arrays

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Positive indexing (0-based)
print(arr[0])    # 10 (first element)
print(arr[2])    # 30 (third element)
print(arr[4])    # 50 (last element)

# Negative indexing (from end)
print(arr[-1])   # 50 (last element)
print(arr[-2])   # 40 (second to last)
print(arr[-5])   # 10 (first element)
```

### 2D Arrays

```python
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12]])

# Access single element: arr[row, col]
print(arr2d[0, 0])    # 1 (first row, first column)
print(arr2d[1, 2])    # 7 (second row, third column)
print(arr2d[-1, -1])  # 12 (last row, last column)

# Access entire row
print(arr2d[0])       # [1 2 3 4] (first row)
print(arr2d[1])       # [5 6 7 8] (second row)

# Access entire column (requires slicing)
print(arr2d[:, 0])    # [1 5 9] (first column)
print(arr2d[:, 2])    # [3 7 11] (third column)
```

---

## Slicing

### 1D Slicing

```python
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# Syntax: arr[start:stop:step]
print(arr[2:7])      # [2 3 4 5 6] (from index 2 to 6)
print(arr[:5])       # [0 1 2 3 4] (first 5 elements)
print(arr[5:])       # [5 6 7 8 9] (from index 5 to end)
print(arr[::2])      # [0 2 4 6 8] (every 2nd element)
print(arr[1::2])     # [1 3 5 7 9] (every 2nd, starting from index 1)
print(arr[::-1])     # [9 8 7 6 5 4 3 2 1 0] (reversed)
```

### 2D Slicing

```python
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12]])

# Slice rows and columns
print(arr2d[0:2, 1:3])
# [[2 3]
#  [6 7]]

# All rows, specific columns
print(arr2d[:, 1:3])
# [[2 3]
#  [6 7]
#  [10 11]]

# Specific rows, all columns
print(arr2d[1:3, :])
# [[5 6 7 8]
#  [9 10 11 12]]

# Step in both dimensions
print(arr2d[::2, ::2])
# [[1 3]
#  [9 11]]
```

### Slicing Creates Views

```python
arr = np.array([1, 2, 3, 4, 5])
slice_view = arr[1:4]  # [2 3 4]

# Modifying the slice modifies the original!
slice_view[0] = 999
print(arr)  # [1 999 3 4 5]

# To avoid this, make a copy
slice_copy = arr[1:4].copy()
slice_copy[0] = 777
print(arr)  # [1 999 3 4 5] (unchanged)
```

---

## Boolean Indexing

### Basic Boolean Indexing

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Create boolean mask
mask = arr > 5
print(mask)  # [False False False False False True True True True True]

# Use mask to filter
print(arr[mask])  # [6 7 8 9 10]

# Or in one line
print(arr[arr > 5])  # [6 7 8 9 10]
```

### Complex Conditions

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Multiple conditions with & (and), | (or), ~ (not)
print(arr[(arr > 3) & (arr < 8)])  # [4 5 6 7]
print(arr[(arr < 3) | (arr > 8)])  # [1 2 9 10]
print(arr[~(arr % 2 == 0)])        # [1 3 5 7 9] (odd numbers)

# Even numbers
print(arr[arr % 2 == 0])  # [2 4 6 8 10]
```

### 2D Boolean Indexing

```python
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# Elements greater than 5
print(arr2d[arr2d > 5])  # [6 7 8 9] (flattened)

# Replace values
arr2d[arr2d > 5] = 0
print(arr2d)
# [[1 2 3]
#  [4 5 0]
#  [0 0 0]]
```

---

## Fancy Indexing

### Integer Array Indexing

```python
arr = np.array([10, 20, 30, 40, 50, 60])

# Select specific indices
indices = [0, 2, 4]
print(arr[indices])  # [10 30 50]

# Can repeat indices
indices = [0, 0, 1, 1, 2]
print(arr[indices])  # [10 10 20 20 30]
```

### 2D Fancy Indexing

```python
arr2d = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12]])

# Select specific rows
rows = [0, 2]
print(arr2d[rows])
# [[1 2 3 4]
#  [9 10 11 12]]

# Select specific elements
rows = [0, 1, 2]
cols = [0, 1, 2]
print(arr2d[rows, cols])  # [1 6 11] (diagonal elements)

# Select rectangular region
rows = [[0, 0], [2, 2]]
cols = [[0, 3], [0, 3]]
print(arr2d[rows, cols])
# [[1 4]
#  [9 12]]
```

### Combining Boolean and Fancy Indexing

```python
arr = np.array([10, 20, 30, 40, 50])

# Get indices where condition is True
indices = np.where(arr > 25)
print(indices)  # (array([2, 3, 4]),)
print(arr[indices])  # [30 40 50]

# Replace values conditionally
arr[arr > 25] = 999
print(arr)  # [10 20 999 999 999]
```

---

## Multi-dimensional Indexing

### 3D Arrays

```python
arr3d = np.array([[[1, 2], [3, 4]],
                  [[5, 6], [7, 8]]])

print(arr3d.shape)  # (2, 2, 2)

# Access: arr[depth, row, col]
print(arr3d[0, 0, 0])  # 1
print(arr3d[1, 1, 1])  # 8

# Slice
print(arr3d[0, :, :])
# [[1 2]
#  [3 4]]

print(arr3d[:, 0, :])
# [[1 2]
#  [5 6]]
```

### Ellipsis (...)

```python
arr = np.arange(24).reshape(2, 3, 4)

# ... represents all dimensions not specified
print(arr[0, ...])     # Same as arr[0, :, :]
print(arr[..., 0])     # Same as arr[:, :, 0]
print(arr[0, ..., 0])  # Same as arr[0, :, 0]
```

---

## Common Mistakes

### 1. Forgetting Slices are Views

```python
# ❌ WRONG - Modifies original
arr = np.array([1, 2, 3, 4, 5])
subset = arr[1:4]
subset[0] = 999
print(arr)  # [1 999 3 4 5] - Oops!

# ✅ CORRECT - Use copy()
subset = arr[1:4].copy()
subset[0] = 999
print(arr)  # [1 2 3 4 5] - Safe
```

### 2. Using Python Lists for Indexing

```python
# ❌ WRONG
arr = np.array([10, 20, 30, 40, 50])
indices = [0, 2, 4]  # Python list
result = arr[indices]  # Works but less efficient

# ✅ BETTER
indices = np.array([0, 2, 4])  # NumPy array
result = arr[indices]
```

### 3. Boolean Indexing Parentheses

```python
arr = np.array([1, 2, 3, 4, 5])

# ❌ WRONG - Operator precedence issue
# result = arr[arr > 2 & arr < 5]  # Error!

# ✅ CORRECT - Use parentheses
result = arr[(arr > 2) & (arr < 5)]  # [3 4]
```

### 4. Confusing Comma vs Multiple Brackets

```python
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# ❌ WRONG - Returns row, then indexes that
print(arr2d[0][1])  # 2 (works but inefficient)

# ✅ CORRECT - Direct indexing
print(arr2d[0, 1])  # 2 (faster)
```

---

## Best Practices

### 1. Use Comma Notation for Multi-dimensional

```python
# ✅ GOOD
arr2d[row, col]

# ❌ AVOID
arr2d[row][col]
```

### 2. Use copy() When Needed

```python
# ✅ GOOD - Explicit about copying
independent = original[1:5].copy()
```

### 3. Use np.where() for Conditional Selection

```python
# ✅ GOOD
indices = np.where(arr > threshold)
selected = arr[indices]
```

### 4. Use Boolean Masks for Clarity

```python
# ✅ GOOD - Readable
is_positive = arr > 0
is_small = arr < 10
result = arr[is_positive & is_small]
```

---

## Quick Reference

```python
# Basic indexing
arr[5]                    # Single element
arr[-1]                   # Last element
arr2d[row, col]           # 2D element

# Slicing
arr[start:stop:step]      # 1D slice
arr2d[rows, cols]         # 2D slice
arr[::-1]                 # Reverse

# Boolean indexing
arr[arr > 5]              # Filter
arr[(arr > 3) & (arr < 8)] # Multiple conditions

# Fancy indexing
arr[[0, 2, 4]]            # Specific indices
arr2d[rows, cols]         # 2D fancy indexing

# Utilities
arr[1:5].copy()           # Copy slice
np.where(arr > 5)         # Get indices
```

---

## Summary

- **Basic indexing**: Access elements with `arr[index]`
- **Slicing**: Extract subarrays with `arr[start:stop:step]`
- **Boolean indexing**: Filter with conditions `arr[arr > 5]`
- **Fancy indexing**: Select with integer arrays `arr[[0, 2, 4]]`
- **Slices are views** - use `.copy()` for independence
- Use **comma notation** for multi-dimensional arrays

---

[← Previous: Arrays](2-arrays.md) | [🏠 Home](README.md) | [Next: Array Operations →](4-array-operations.md)
