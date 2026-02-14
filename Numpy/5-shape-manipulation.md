[← Previous: Array Operations](4-array-operations.md) | [🏠 Home](README.md) | [Next: Universal Functions →](6-universal-functions.md)

---

# 5. Shape Manipulation

## Table of Contents
- [Reshaping Arrays](#reshaping-arrays)
- [Transposing](#transposing)
- [Stacking Arrays](#stacking-arrays)
- [Splitting Arrays](#splitting-arrays)
- [Adding/Removing Dimensions](#addingremoving-dimensions)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Reshaping Arrays

### Basic Reshaping

```python
import numpy as np

# 1D to 2D
arr = np.arange(12)  # [0 1 2 3 4 5 6 7 8 9 10 11]
reshaped = arr.reshape(3, 4)
print(reshaped)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 1D to 3D
arr = np.arange(24)
reshaped = arr.reshape(2, 3, 4)
print(reshaped.shape)  # (2, 3, 4)

# Automatic dimension with -1
arr = np.arange(12)
reshaped = arr.reshape(3, -1)  # -1 means "figure it out"
print(reshaped.shape)  # (3, 4)

reshaped = arr.reshape(-1, 4)
print(reshaped.shape)  # (3, 4)
```

### Flattening

```python
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])

# flatten() - returns a copy
flat = arr2d.flatten()
print(flat)  # [1 2 3 4 5 6]

# ravel() - returns a view (when possible)
flat = arr2d.ravel()
print(flat)  # [1 2 3 4 5 6]

# Difference: flatten is always a copy
flat = arr2d.flatten()
flat[0] = 999
print(arr2d)  # [[1 2 3] [4 5 6]] - unchanged

# ravel can be a view
flat = arr2d.ravel()
flat[0] = 999
print(arr2d)  # [[999 2 3] [4 5 6]] - changed!
```

---

## Transposing

### Basic Transpose

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
print(arr.shape)  # (2, 3)

# Transpose
transposed = arr.T
print(transposed)
# [[1 4]
#  [2 5]
#  [3 6]]
print(transposed.shape)  # (3, 2)

# Alternative: transpose()
transposed = arr.transpose()
```

### Multi-dimensional Transpose

```python
arr = np.arange(24).reshape(2, 3, 4)
print(arr.shape)  # (2, 3, 4)

# Specify axis order
transposed = arr.transpose(2, 0, 1)
print(transposed.shape)  # (4, 2, 3)

# Swap specific axes
swapped = np.swapaxes(arr, 0, 2)
print(swapped.shape)  # (4, 3, 2)
```

---

## Stacking Arrays

### Vertical Stacking (vstack)

```python
a = np.array([[1, 2, 3]])
b = np.array([[4, 5, 6]])

# Stack vertically (along rows)
stacked = np.vstack([a, b])
print(stacked)
# [[1 2 3]
#  [4 5 6]]

# Multiple arrays
c = np.array([[7, 8, 9]])
stacked = np.vstack([a, b, c])
print(stacked)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
```

### Horizontal Stacking (hstack)

```python
a = np.array([[1], [2], [3]])
b = np.array([[4], [5], [6]])

# Stack horizontally (along columns)
stacked = np.hstack([a, b])
print(stacked)
# [[1 4]
#  [2 5]
#  [3 6]]
```

### Depth Stacking (dstack)

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# Stack along third dimension
stacked = np.dstack([a, b])
print(stacked.shape)  # (2, 2, 2)
print(stacked)
# [[[1 5]
#   [2 6]]
#  [[3 7]
#   [4 8]]]
```

### Concatenate (General)

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# Concatenate along axis 0 (rows)
concat = np.concatenate([a, b], axis=0)
print(concat)
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

# Concatenate along axis 1 (columns)
concat = np.concatenate([a, b], axis=1)
print(concat)
# [[1 2 5 6]
#  [3 4 7 8]]
```

---

## Splitting Arrays

### Horizontal Split

```python
arr = np.array([[1, 2, 3, 4, 5, 6],
                [7, 8, 9, 10, 11, 12]])

# Split into 3 equal parts
parts = np.hsplit(arr, 3)
print(parts[0])
# [[1 2]
#  [7 8]]

# Split at specific indices
parts = np.hsplit(arr, [2, 4])  # Split at columns 2 and 4
print(len(parts))  # 3 parts
```

### Vertical Split

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [10, 11, 12]])

# Split into 2 equal parts
parts = np.vsplit(arr, 2)
print(parts[0])
# [[1 2 3]
#  [4 5 6]]
```

### General Split

```python
arr = np.arange(12).reshape(3, 4)

# Split along axis 0
parts = np.split(arr, 3, axis=0)

# Split along axis 1
parts = np.split(arr, 2, axis=1)
```

---

## Adding/Removing Dimensions

### Adding Dimensions

```python
arr = np.array([1, 2, 3])
print(arr.shape)  # (3,)

# Add dimension with np.newaxis
arr_2d = arr[np.newaxis, :]
print(arr_2d.shape)  # (1, 3)

arr_2d = arr[:, np.newaxis]
print(arr_2d.shape)  # (3, 1)

# Using expand_dims
arr_2d = np.expand_dims(arr, axis=0)
print(arr_2d.shape)  # (1, 3)

arr_2d = np.expand_dims(arr, axis=1)
print(arr_2d.shape)  # (3, 1)
```

### Removing Dimensions

```python
arr = np.array([[[1, 2, 3]]])
print(arr.shape)  # (1, 1, 3)

# Remove single-dimensional entries
squeezed = np.squeeze(arr)
print(squeezed.shape)  # (3,)

# Remove specific axis
arr = np.array([[[1, 2, 3]]])
squeezed = np.squeeze(arr, axis=0)
print(squeezed.shape)  # (1, 3)
```

---

## Common Mistakes

### 1. Incompatible Reshape

```python
# ❌ WRONG - Total elements don't match
arr = np.arange(10)
# arr.reshape(3, 4)  # Error! 10 elements can't fit in 3×4

# ✅ CORRECT
arr = np.arange(12)
reshaped = arr.reshape(3, 4)  # 12 = 3×4 ✓
```

### 2. Modifying Flattened Array

```python
arr = np.array([[1, 2], [3, 4]])

# ❌ WRONG - Using ravel() when you don't want to modify original
flat = arr.ravel()
flat[0] = 999
print(arr)  # [[999 2] [3 4]] - Oops!

# ✅ CORRECT - Use flatten() for a copy
flat = arr.flatten()
flat[0] = 999
print(arr)  # [[1 2] [3 4]] - Safe
```

### 3. Stacking Incompatible Shapes

```python
a = np.array([[1, 2, 3]])
b = np.array([[4, 5]])

# ❌ WRONG - Shapes don't match
# np.vstack([a, b])  # Error!

# ✅ CORRECT - Make shapes compatible
b = np.array([[4, 5, 6]])
stacked = np.vstack([a, b])
```

---

## Best Practices

### 1. Use -1 for Automatic Dimension

```python
# ✅ GOOD - Let NumPy figure it out
arr = np.arange(24)
reshaped = arr.reshape(4, -1)  # Automatically becomes (4, 6)
```

### 2. Check Shapes Before Stacking

```python
# ✅ GOOD
print(f"a shape: {a.shape}, b shape: {b.shape}")
if a.shape[1] == b.shape[1]:
    stacked = np.vstack([a, b])
```

### 3. Use Appropriate Stacking Method

```python
# ✅ GOOD - Clear intent
np.vstack([a, b])  # Stack rows
np.hstack([a, b])  # Stack columns
np.concatenate([a, b], axis=0)  # General, explicit axis
```

---

## Quick Reference

```python
# Reshaping
arr.reshape(3, 4)         # Reshape
arr.reshape(-1, 4)        # Auto dimension
arr.flatten()             # Flatten (copy)
arr.ravel()               # Flatten (view)

# Transposing
arr.T                     # Transpose
arr.transpose()           # Transpose
np.swapaxes(arr, 0, 1)    # Swap axes

# Stacking
np.vstack([a, b])         # Vertical
np.hstack([a, b])         # Horizontal
np.dstack([a, b])         # Depth
np.concatenate([a, b], axis=0)  # General

# Splitting
np.hsplit(arr, 3)         # Horizontal
np.vsplit(arr, 2)         # Vertical
np.split(arr, 3, axis=0)  # General

# Dimensions
arr[np.newaxis, :]        # Add dimension
np.expand_dims(arr, 0)    # Add dimension
np.squeeze(arr)           # Remove dimensions
```

---

[← Previous: Array Operations](4-array-operations.md) | [🏠 Home](README.md) | [Next: Universal Functions →](6-universal-functions.md)
