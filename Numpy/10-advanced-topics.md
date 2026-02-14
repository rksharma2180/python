[← Previous: Random Numbers](9-random.md) | [🏠 Home](README.md)

---

# 10. Advanced Topics and Best Practices

## Table of Contents
- [Memory Layout and Performance](#memory-layout-and-performance)
- [Vectorization Techniques](#vectorization-techniques)
- [Broadcasting Advanced](#broadcasting-advanced)
- [Memory Management](#memory-management)
- [Performance Optimization](#performance-optimization)
- [NumPy for AI/ML](#numpy-for-aiml)
- [Common Pitfalls](#common-pitfalls)
- [Best Practices Summary](#best-practices-summary)

---

## Memory Layout and Performance

### C-order vs Fortran-order

```python
import numpy as np
import time

# C-order (row-major) - default
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')
print(arr_c.flags['C_CONTIGUOUS'])  # True

# Fortran-order (column-major)
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')
print(arr_f.flags['F_CONTIGUOUS'])  # True

# Performance difference
large_c = np.random.random((10000, 10000))  # C-order by default
large_f = np.asfortranarray(large_c)        # Convert to Fortran order

# Row-wise operations faster on C-order
start = time.time()
for row in large_c:
    _ = row.sum()
print(f"C-order row-wise: {time.time() - start:.4f}s")

# Column-wise operations faster on Fortran-order
start = time.time()
for col in large_f.T:
    _ = col.sum()
print(f"F-order column-wise: {time.time() - start:.4f}s")
```

### Strides and Memory Access

```python
arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64)

print(f"Shape: {arr.shape}")      # (2, 3)
print(f"Strides: {arr.strides}")  # (24, 8)
print(f"Itemsize: {arr.itemsize}")  # 8 bytes

# Strides explanation:
# - 24 bytes to next row (3 elements × 8 bytes)
# - 8 bytes to next column (1 element × 8 bytes)

# Accessing arr[1, 2]:
# Offset = 1 * 24 + 2 * 8 = 40 bytes
```

---

## Vectorization Techniques

### Replacing Loops with Vectorization

```python
# ❌ BAD - Python loop
arr = np.arange(1000000)
result = []
for x in arr:
    result.append(x ** 2 + 2 * x + 1)
result = np.array(result)

# ✅ GOOD - Vectorized
result = arr ** 2 + 2 * arr + 1

# ✅ GOOD - Using np.vectorize for complex functions
def complex_func(x):
    if x > 0:
        return np.sqrt(x)
    else:
        return 0

vec_func = np.vectorize(complex_func)
result = vec_func(arr)

# ✅ BETTER - Use np.where for conditionals
result = np.where(arr > 0, np.sqrt(arr), 0)
```

### Advanced Vectorization

```python
# Multiple conditions
arr = np.arange(-10, 11)

# Using np.select
conditions = [arr < -5, (arr >= -5) & (arr < 5), arr >= 5]
choices = [-1, 0, 1]
result = np.select(conditions, choices)
print(result)

# Piecewise function
def piecewise_func(x):
    return np.piecewise(x,
                       [x < 0, (x >= 0) & (x < 5), x >= 5],
                       [lambda x: -x, lambda x: x**2, lambda x: 25])

result = piecewise_func(arr)
```

---

## Broadcasting Advanced

### Broadcasting Rules Visualization

```
Rule 1: If arrays have different dimensions, pad smaller shape with 1s on left
Rule 2: Arrays compatible if dimensions are equal or one is 1
Rule 3: After broadcasting, each array behaves as if it had larger shape

Example: (3, 1) + (4,)
Step 1: Pad (4,) → (1, 4)
Step 2: Check compatibility:
        (3, 1)
        (1, 4)
        Both dimensions compatible (3 vs 1, 1 vs 4)
Step 3: Broadcast to (3, 4)
```

```python
# Complex broadcasting
a = np.arange(3).reshape(3, 1)      # (3, 1)
b = np.arange(4)                     # (4,)
c = a + b                            # (3, 4)

print(c)
# [[0 1 2 3]
#  [1 2 3 4]
#  [2 3 4 5]]

# 3D broadcasting
a = np.arange(2).reshape(2, 1, 1)   # (2, 1, 1)
b = np.arange(3).reshape(1, 3, 1)   # (1, 3, 1)
c = np.arange(4).reshape(1, 1, 4)   # (1, 1, 4)
result = a + b + c                   # (2, 3, 4)
print(result.shape)
```

---

## Memory Management

### Views vs Copies

```python
arr = np.array([1, 2, 3, 4, 5])

# View (shares memory)
view = arr[1:4]
view[0] = 999
print(arr)  # [1 999 3 4 5] - original changed!

# Copy (independent memory)
copy = arr[1:4].copy()
copy[0] = 777
print(arr)  # [1 999 3 4 5] - original unchanged

# Check if view or copy
print(view.base is arr)  # True (view)
print(copy.base is None)  # True (copy)
```

### Memory Efficiency

```python
# ❌ BAD - Creates unnecessary copies
arr = np.arange(1000000)
result = arr.copy()
result = result * 2
result = result + 1

# ✅ GOOD - In-place operations
arr = np.arange(1000000)
arr *= 2
arr += 1

# ✅ GOOD - Preallocate
result = np.empty(1000000)
result[:] = arr * 2 + 1
```

---

## Performance Optimization

### Timing Code

```python
import time

# Method 1: time module
start = time.time()
result = np.sum(np.arange(1000000))
print(f"Time: {time.time() - start:.6f}s")

# Method 2: %timeit in Jupyter
# %timeit np.sum(np.arange(1000000))

# Method 3: timeit module
import timeit
time_taken = timeit.timeit('np.sum(np.arange(1000000))',
                           setup='import numpy as np',
                           number=100)
print(f"Average time: {time_taken/100:.6f}s")
```

### Optimization Tips

```python
# 1. Use appropriate dtype
# ❌ BAD - Wastes memory
arr = np.zeros(1000000, dtype=np.float64)  # 8 MB

# ✅ GOOD - Use smaller dtype when possible
arr = np.zeros(1000000, dtype=np.float32)  # 4 MB

# 2. Avoid unnecessary copies
# ❌ BAD
result = arr.copy()
result = result + 1

# ✅ GOOD
result = arr + 1  # No copy needed

# 3. Use ufuncs instead of Python functions
# ❌ BAD
result = [math.sqrt(x) for x in arr]

# ✅ GOOD
result = np.sqrt(arr)

# 4. Preallocate arrays
# ❌ BAD
result = []
for i in range(1000000):
    result.append(i ** 2)

# ✅ GOOD
result = np.empty(1000000)
for i in range(1000000):
    result[i] = i ** 2

# ✅ BEST - Vectorized
result = np.arange(1000000) ** 2
```

---

## NumPy for AI/ML

### Data Preparation

```python
# Normalization
def normalize(X):
    """Min-max normalization to [0, 1]"""
    return (X - X.min()) / (X.max() - X.min())

# Standardization
def standardize(X):
    """Z-score standardization"""
    return (X - X.mean()) / X.std()

# One-hot encoding
def one_hot_encode(y, num_classes):
    """Convert labels to one-hot vectors"""
    n_samples = len(y)
    one_hot = np.zeros((n_samples, num_classes))
    one_hot[np.arange(n_samples), y] = 1
    return one_hot

# Example
labels = np.array([0, 1, 2, 1, 0])
one_hot = one_hot_encode(labels, num_classes=3)
print(one_hot)
```

### Mini-batch Generation

```python
def create_mini_batches(X, y, batch_size=32, shuffle=True, random_state=None):
    """Create mini-batches for training"""
    rng = np.random.default_rng(random_state)
    n_samples = len(X)
    
    if shuffle:
        indices = rng.permutation(n_samples)
        X = X[indices]
        y = y[indices]
    
    for start_idx in range(0, n_samples, batch_size):
        end_idx = min(start_idx + batch_size, n_samples)
        yield X[start_idx:end_idx], y[start_idx:end_idx]

# Example
X = np.arange(100).reshape(100, 1)
y = np.arange(100)

for X_batch, y_batch in create_mini_batches(X, y, batch_size=32):
    print(f"Batch shape: {X_batch.shape}")
```

### Simple Neural Network Operations

```python
# Activation functions
def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

# Forward pass example
X = np.random.randn(100, 10)  # 100 samples, 10 features
W1 = np.random.randn(10, 20)  # First layer weights
b1 = np.zeros(20)              # First layer bias

# Layer 1
z1 = X @ W1 + b1
a1 = relu(z1)

W2 = np.random.randn(20, 3)   # Output layer
b2 = np.zeros(3)

# Output layer
z2 = a1 @ W2 + b2
output = softmax(z2)

print(f"Output shape: {output.shape}")  # (100, 3)
print(f"Output sums: {output.sum(axis=1)[:5]}")  # All 1.0
```

---

## Common Pitfalls

### 1. Integer Division

```python
# ❌ WRONG - Integer division truncates
arr = np.array([1, 2, 3, 4, 5])
result = arr / 2  # [0.5 1. 1.5 2. 2.5] ✓

arr_int = np.array([1, 2, 3, 4, 5], dtype=int)
result = arr_int / 2  # [0.5 1. 1.5 2. 2.5] ✓ (converts to float)

# But be careful with in-place operations
arr_int //= 2  # [0 1 1 2 2] (integer division)
```

### 2. Dimension Mismatch

```python
# ⚠️ SURPRISING BROADCASTING - This actually works!
a = np.array([[1, 2, 3]])  # (1, 3)
b = np.array([[1], [2]])   # (2, 1)
print(a + b)  # Works! Result is (2, 3)
# [[2 3 4]
#  [3 4 5]]

# ❌ ACTUAL ERROR - Matrix multiplication inner dims must match
A = np.array([[1, 2]])      # (1, 2)
B = np.array([[1], [2], [3]])  # (3, 1)
# A @ B  # Error! (1,2) @ (3,1) - inner dims 2 ≠ 3

# ✅ CORRECT - Ensure compatible shapes
print(f"A: {A.shape}, B: {B.shape}")
```

### 3. Modifying Array During Iteration

```python
# ❌ WRONG
arr = np.array([1, 2, 3, 4, 5])
for i, val in enumerate(arr):
    if val > 2:
        arr = np.delete(arr, i)  # Don't modify during iteration!

# ✅ CORRECT - Use boolean indexing
arr = arr[arr <= 2]
```

---

## Best Practices Summary

### 1. Performance
- ✅ Use vectorized operations instead of loops
- ✅ Preallocate arrays when size is known
- ✅ Use appropriate dtypes to save memory
- ✅ Avoid unnecessary copies
- ✅ Use in-place operations when possible

### 2. Code Quality
- ✅ Use meaningful variable names
- ✅ Add docstrings to functions
- ✅ Check array shapes before operations
- ✅ Use assertions for debugging

### 3. Reproducibility
- ✅ Set random seeds for experiments
- ✅ Use new Generator API for random numbers
- ✅ Document random state in functions

### 4. Memory
- ✅ Use views when possible
- ✅ Delete large arrays when done
- ✅ Use generators for large datasets
- ✅ Monitor memory usage

### 5. Readability
- ✅ Use broadcasting instead of loops
- ✅ Break complex operations into steps
- ✅ Add comments for non-obvious code
- ✅ Use descriptive axis names

---

## Quick Reference

```python
# Performance
arr *= 2                    # In-place operation
result = np.empty(n)        # Preallocate
arr.astype(np.float32)      # Smaller dtype

# Memory
view = arr[1:5]             # View (shares memory)
copy = arr[1:5].copy()      # Copy (independent)
del large_array             # Free memory

# Debugging
print(arr.shape)            # Check shape
print(arr.dtype)            # Check type
print(arr.flags)            # Check memory layout
assert arr.shape == (10,)   # Assertion

# Vectorization
np.where(condition, x, y)   # Conditional
np.select(conditions, choices)  # Multiple conditions
np.vectorize(func)          # Vectorize function
```

---

## Congratulations! 🎉

You've completed the NumPy learning guide! You now have the knowledge to:

- ✅ Create and manipulate NumPy arrays efficiently
- ✅ Perform vectorized operations
- ✅ Use broadcasting effectively
- ✅ Apply linear algebra operations
- ✅ Generate and work with random data
- ✅ Optimize NumPy code for performance
- ✅ Prepare data for AI/ML applications

### Next Steps

1. **Practice**: Work on real datasets
2. **Pandas**: Learn data manipulation with Pandas (built on NumPy)
3. **Scikit-learn**: Apply NumPy in machine learning
4. **TensorFlow/PyTorch**: Deep learning frameworks
5. **LangChain/LangGraph**: Apply NumPy in LLM applications

---

[← Previous: Random Numbers](9-random.md) | [🏠 Home](README.md)
