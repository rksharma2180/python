[← Previous: Universal Functions](6-universal-functions.md) | [🏠 Home](README.md) | [Next: Statistics →](8-statistics.md)

---

# 7. Linear Algebra

## Table of Contents
- [Matrix Operations](#matrix-operations)
- [Matrix Multiplication](#matrix-multiplication)
- [Matrix Decomposition](#matrix-decomposition)
- [Solving Linear Equations](#solving-linear-equations)
- [Eigenvalues and Eigenvectors](#eigenvalues-and-eigenvectors)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Matrix Operations

### Basic Matrix Operations

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Transpose
print(A.T)
# [[1 3]
#  [2 4]]

# Trace (sum of diagonal)
print(np.trace(A))  # 5 (1 + 4)

# Determinant
print(np.linalg.det(A))  # -2.0

# Inverse
A_inv = np.linalg.inv(A)
print(A_inv)
# [[-2.   1. ]
#  [ 1.5 -0.5]]

# Verify: A @ A_inv = I
print(A @ A_inv)
# [[1. 0.]
#  [0. 1.]]
```

### Matrix Properties

```python
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# Rank
print(np.linalg.matrix_rank(A))  # 2 (not full rank)

# Norm
print(np.linalg.norm(A))  # Frobenius norm: 16.88

# Condition number
print(np.linalg.cond(A))  # Very large (ill-conditioned)
```

---

## Matrix Multiplication

### Different Types

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# Element-wise multiplication
print(a * b)
# [[ 5 12]
#  [21 32]]

# Matrix multiplication (dot product)
print(a @ b)  # Python 3.5+
# [[19 22]
#  [43 50]]

print(np.dot(a, b))  # Alternative
# [[19 22]
#  [43 50]]

print(np.matmul(a, b))  # Another alternative
# [[19 22]
#  [43 50]]
```

### Vector Operations

```python
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# Dot product
print(np.dot(v1, v2))  # 32 (1*4 + 2*5 + 3*6)

# Cross product (3D only)
print(np.cross(v1, v2))  # [-3  6 -3]

# Outer product
print(np.outer(v1, v2))
# [[ 4  5  6]
#  [ 8 10 12]
#  [12 15 18]]
```

---

## Matrix Decomposition

### QR Decomposition

```python
A = np.array([[1, 2], [3, 4], [5, 6]])

# QR decomposition: A = Q @ R
Q, R = np.linalg.qr(A)

print("Q (orthogonal):")
print(Q)
print("\nR (upper triangular):")
print(R)

# Verify
print("\nQ @ R:")
print(Q @ R)  # Should equal A
```

### SVD (Singular Value Decomposition)

```python
A = np.array([[1, 2], [3, 4], [5, 6]])

# SVD: A = U @ S @ V^T
U, s, VT = np.linalg.svd(A)

print("U shape:", U.shape)      # (3, 3)
print("s shape:", s.shape)      # (2,) - singular values
print("VT shape:", VT.shape)    # (2, 2)

# Reconstruct A
S = np.zeros((3, 2))
S[:2, :2] = np.diag(s)
A_reconstructed = U @ S @ VT
print("\nReconstructed A:")
print(A_reconstructed)
```

### Eigendecomposition

```python
A = np.array([[1, 2], [2, 1]])

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

print("Eigenvalues:", eigenvalues)    # [3. -1.]
print("Eigenvectors:\n", eigenvectors)

# Verify: A @ v = λ @ v
v1 = eigenvectors[:, 0]
lambda1 = eigenvalues[0]
print("\nA @ v1:", A @ v1)
print("λ1 * v1:", lambda1 * v1)
```

---

## Solving Linear Equations

### System of Linear Equations

```python
# Solve: Ax = b
# 2x + 3y = 8
# 4x + 5y = 14

A = np.array([[2, 3],
              [4, 5]])
b = np.array([8, 14])

# Solve
x = np.linalg.solve(A, b)
print("Solution:", x)  # [1. 2.]

# Verify
print("A @ x:", A @ x)  # [8. 14.] ✓
```

### Least Squares

```python
# Overdetermined system (more equations than unknowns)
A = np.array([[1, 1],
              [1, 2],
              [1, 3]])
b = np.array([2, 3, 4.5])

# Least squares solution
x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
print("Solution:", x)
print("Residuals:", residuals)
```

---

## Eigenvalues and Eigenvectors

### Symmetric Matrices

```python
# For symmetric matrices, use eigh (faster and more accurate)
A = np.array([[1, 2, 3],
              [2, 4, 5],
              [3, 5, 6]])

eigenvalues, eigenvectors = np.linalg.eigh(A)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)
```

### Power Iteration (Manual)

```python
def power_iteration(A, num_iterations=100):
    """Find dominant eigenvalue and eigenvector"""
    n = A.shape[0]
    v = np.random.rand(n)
    
    for _ in range(num_iterations):
        # Multiply by A
        v = A @ v
        # Normalize
        v = v / np.linalg.norm(v)
    
    # Eigenvalue
    eigenvalue = (v @ A @ v) / (v @ v)
    return eigenvalue, v

A = np.array([[2, 1], [1, 2]])
eigenvalue, eigenvector = power_iteration(A)
print("Dominant eigenvalue:", eigenvalue)
print("Eigenvector:", eigenvector)
```

---

## Common Mistakes

### 1. Element-wise vs Matrix Multiplication

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# ❌ WRONG - Element-wise
print(A * B)
# [[ 5 12]
#  [21 32]]

# ✅ CORRECT - Matrix multiplication
print(A @ B)
# [[19 22]
#  [43 50]]
```

### 2. Singular Matrix Inversion

```python
A = np.array([[1, 2], [2, 4]])  # Singular (det = 0)

# ❌ WRONG - Will raise error
try:
    A_inv = np.linalg.inv(A)
except np.linalg.LinAlgError:
    print("Matrix is singular!")

# ✅ CORRECT - Check determinant first
if np.abs(np.linalg.det(A)) > 1e-10:
    A_inv = np.linalg.inv(A)
else:
    print("Matrix is singular, use pseudoinverse")
    A_pinv = np.linalg.pinv(A)
```

### 3. Shape Mismatch

```python
A = np.array([[1, 2, 3]])  # (1, 3)
B = np.array([[4], [5]])   # (2, 1)

# ❌ WRONG - Shapes incompatible
# A @ B  # Error!

# ✅ CORRECT - Check shapes
print(f"A: {A.shape}, B: {B.shape}")
```

---

## Best Practices

### 1. Use Appropriate Functions

```python
# ✅ GOOD - Use @ for matrix multiplication
result = A @ B

# ✅ GOOD - Use eigh for symmetric matrices
eigenvalues, eigenvectors = np.linalg.eigh(symmetric_matrix)

# ✅ GOOD - Use solve instead of inv
x = np.linalg.solve(A, b)  # Better than: x = np.linalg.inv(A) @ b
```

### 2. Check Matrix Properties

```python
# ✅ GOOD - Check before inverting
if np.abs(np.linalg.det(A)) > 1e-10:
    A_inv = np.linalg.inv(A)
else:
    print("Matrix is singular")
```

### 3. Use Pseudoinverse for Robustness

```python
# ✅ GOOD - Pseudoinverse works for singular matrices too
A_pinv = np.linalg.pinv(A)
```

---

## Quick Reference

```python
# Basic operations
A.T                          # Transpose
np.trace(A)                  # Trace
np.linalg.det(A)             # Determinant
np.linalg.inv(A)             # Inverse
np.linalg.pinv(A)            # Pseudoinverse

# Matrix multiplication
A @ B                        # Matrix product
np.dot(A, B)                 # Dot product
np.matmul(A, B)              # Matrix multiplication

# Decomposition
np.linalg.qr(A)              # QR decomposition
np.linalg.svd(A)             # SVD
np.linalg.eig(A)             # Eigendecomposition
np.linalg.eigh(A)            # Symmetric eigendecomposition

# Solving equations
np.linalg.solve(A, b)        # Solve Ax = b
np.linalg.lstsq(A, b)        # Least squares

# Properties
np.linalg.norm(A)            # Norm
np.linalg.matrix_rank(A)     # Rank
np.linalg.cond(A)            # Condition number
```

---

[← Previous: Universal Functions](6-universal-functions.md) | [🏠 Home](README.md) | [Next: Statistics →](8-statistics.md)
