# 1. Introduction to NumPy

[🏠 Home](README.md) | [Next: NumPy Arrays →](2-arrays.md)

---

## What is NumPy?

**NumPy** (Numerical Python) is the fundamental package for scientific computing in Python. It provides:

- A powerful **N-dimensional array object** (`ndarray`)
- Sophisticated **broadcasting** functions
- Tools for integrating **C/C++** and Fortran code
- Useful **linear algebra**, **Fourier transform**, and **random number** capabilities

### Why NumPy?

```python
# Pure Python (SLOW)
import time

python_list = list(range(1000000))
start = time.time()
result = [x * 2 for x in python_list]
python_time = time.time() - start

# NumPy (FAST)
import numpy as np

numpy_array = np.arange(1000000)
start = time.time()
result = numpy_array * 2
numpy_time = time.time() - start

print(f"Python: {python_time:.4f}s")  # ~0.05s
print(f"NumPy: {numpy_time:.4f}s")    # ~0.002s
print(f"NumPy is {python_time/numpy_time:.1f}x faster!")  # ~25x faster
```

---

## Installation

### Using pip
```bash
pip install numpy
```

### Using conda
```bash
conda install numpy
```

### Verify Installation
```python
import numpy as np
print(np.__version__)  # Should print version like 1.24.3
```

---

## Why NumPy for AI/ML?

### 1. Foundation of ML Ecosystem

```
NumPy (Core)
    ↓
├── Pandas → Data manipulation
├── Scikit-learn → Traditional ML
├── TensorFlow → Deep Learning
├── PyTorch → Deep Learning
├── LangChain → LLM Applications
└── LangGraph → Agent Workflows
```

### 2. Performance

**Memory Efficiency:**
```python
import sys
import numpy as np

# Python list
python_list = [1, 2, 3, 4, 5] * 1000
print(f"Python list: {sys.getsizeof(python_list)} bytes")  # ~40,000 bytes

# NumPy array
numpy_array = np.array([1, 2, 3, 4, 5] * 1000)
print(f"NumPy array: {numpy_array.nbytes} bytes")  # ~20,000 bytes
```

**Speed:**
- Written in C
- Contiguous memory allocation
- Vectorized operations (no Python loops)

### 3. Vectorization

```python
# Without NumPy (slow)
result = []
for i in range(1000):
    result.append(i ** 2)

# With NumPy (fast)
result = np.arange(1000) ** 2
```

---

## Basic NumPy Concepts

### The ndarray Object

```python
import numpy as np

# Create array
arr = np.array([1, 2, 3, 4, 5])

print(type(arr))        # <class 'numpy.ndarray'>
print(arr.dtype)        # int64 (or int32 on Windows)
print(arr.shape)        # (5,)
print(arr.ndim)         # 1 (one-dimensional)
print(arr.size)         # 5 (total elements)
```

### Memory Layout

```
Python List (scattered in memory):
┌───┐    ┌───┐    ┌───┐    ┌───┐
│ 1 │ → │ 2 │ → │ 3 │ → │ 4 │
└───┘    └───┘    └───┘    └───┘
 0x100    0x250    0x180    0x320

NumPy Array (contiguous memory):
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │
└───┴───┴───┴───┘
 0x100 → 0x103
```

---

## First NumPy Program

```python
import numpy as np

# Create arrays
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Element-wise operations
print("Addition:", a + b)        # [5 7 9]
print("Multiplication:", a * b)  # [4 10 18]
print("Power:", a ** 2)          # [1 4 9]

# Aggregations
print("Sum:", a.sum())           # 6
print("Mean:", a.mean())         # 2.0
print("Max:", a.max())           # 3

# 2D array
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])

print("Shape:", matrix.shape)    # (2, 3)
print("Transpose:\n", matrix.T)
# [[1 4]
#  [2 5]
#  [3 6]]
```

---

## NumPy vs Python Lists

| Feature | Python List | NumPy Array |
|---------|-------------|-------------|
| **Type** | Heterogeneous (mixed types) | Homogeneous (single type) |
| **Speed** | Slow | Fast (10-100x) |
| **Memory** | More | Less |
| **Operations** | Limited | Extensive mathematical ops |
| **Dimensions** | 1D only | N-dimensional |
| **Size** | Dynamic | Fixed (but can be resized) |
| **Broadcasting** | No | Yes |

```python
# Python list - heterogeneous
py_list = [1, "hello", 3.14, True]  # OK

# NumPy array - homogeneous
np_array = np.array([1, "hello", 3.14, True])
print(np_array.dtype)  # <U32 (all converted to strings!)
```

---

## Common Mistakes

### 1. Not Importing NumPy
```python
# ❌ WRONG
array([1, 2, 3])  # NameError

# ✅ CORRECT
import numpy as np
np.array([1, 2, 3])
```

### 2. Confusing Lists and Arrays
```python
# ❌ WRONG - This is a list, not an array
my_array = [1, 2, 3]
my_array * 2  # [1, 2, 3, 1, 2, 3] (list repetition)

# ✅ CORRECT
my_array = np.array([1, 2, 3])
my_array * 2  # [2 4 6] (element-wise multiplication)
```

### 3. Modifying Array Type Unintentionally
```python
# ❌ WRONG
arr = np.array([1, 2, 3])  # int64
arr[0] = 3.14  # Becomes 3 (truncated!)

# ✅ CORRECT
arr = np.array([1, 2, 3], dtype=float)
arr[0] = 3.14  # Now it works
```

---

## Best Practices

### 1. Always Specify dtype When Needed
```python
# ✅ GOOD
arr = np.array([1, 2, 3], dtype=np.float64)
```

### 2. Use NumPy Functions Instead of Loops
```python
# ❌ BAD
result = []
for x in arr:
    result.append(x ** 2)

# ✅ GOOD
result = arr ** 2
```

### 3. Import Convention
```python
# ✅ STANDARD
import numpy as np

# ❌ AVOID
from numpy import *  # Pollutes namespace
```

### 4. Check Array Properties
```python
# ✅ GOOD PRACTICE
print(f"Shape: {arr.shape}")
print(f"Dtype: {arr.dtype}")
print(f"Size: {arr.size}")
```

---

## Quick Reference

```python
import numpy as np

# Creation
np.array([1, 2, 3])           # From list
np.zeros((3, 4))              # 3x4 array of zeros
np.ones((2, 3))               # 2x3 array of ones
np.arange(0, 10, 2)           # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)          # 5 evenly spaced values

# Properties
arr.shape                      # Dimensions
arr.dtype                      # Data type
arr.size                       # Total elements
arr.ndim                       # Number of dimensions

# Operations
arr + 5                        # Add 5 to all elements
arr * 2                        # Multiply all by 2
arr.sum()                      # Sum all elements
arr.mean()                     # Average
arr.max()                      # Maximum value
```

---

## Summary

- NumPy is the foundation of scientific Python
- **10-100x faster** than pure Python
- **More memory efficient** than lists
- Essential for **AI/ML** work
- Provides **N-dimensional arrays** and mathematical operations
- Used by all major ML libraries

---

## Next Steps

Now that you understand what NumPy is and why it's important, let's dive into the core data structure:

### 👉 [Next: NumPy Arrays](2-arrays.md)

---

[🏠 Home](README.md) | [Next: NumPy Arrays →](2-arrays.md)
