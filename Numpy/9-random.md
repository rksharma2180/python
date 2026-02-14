[← Previous: Statistics](8-statistics.md) | [🏠 Home](README.md) | [Next: Advanced Topics →](10-advanced-topics.md)

---

# 9. Random Number Generation

## Table of Contents
- [Random Number Basics](#random-number-basics)
- [Random Distributions](#random-distributions)
- [Random Sampling](#random-sampling)
- [Reproducibility](#reproducibility)
- [Random Generator (New API)](#random-generator-new-api)
- [Best Practices](#best-practices)

---

## Random Number Basics

### Simple Random Numbers

```python
import numpy as np

# Random float between 0 and 1
print(np.random.random())  # e.g., 0.548

# Random floats in array
print(np.random.random(5))  # 5 random numbers
print(np.random.random((2, 3)))  # 2x3 array

# Random integers
print(np.random.randint(0, 10))  # Random int from 0 to 9
print(np.random.randint(0, 10, size=5))  # 5 random ints
print(np.random.randint(0, 10, size=(2, 3)))  # 2x3 array
```

### Random Choice

```python
# Random choice from array
arr = np.array([1, 2, 3, 4, 5])
print(np.random.choice(arr))  # Random element

# Multiple choices
print(np.random.choice(arr, size=3))  # 3 random elements

# Without replacement
print(np.random.choice(arr, size=3, replace=False))  # No duplicates

# With probabilities
probs = [0.1, 0.1, 0.1, 0.1, 0.6]  # 60% chance of 5
print(np.random.choice(arr, size=10, p=probs))
```

---

## Random Distributions

### Uniform Distribution

```python
# Uniform distribution [0, 1)
print(np.random.rand(5))  # 5 random numbers

# Uniform distribution [low, high)
print(np.random.uniform(5, 10, size=5))  # Between 5 and 10
```

### Normal (Gaussian) Distribution

```python
# Standard normal (mean=0, std=1)
print(np.random.randn(5))

# Normal with custom mean and std
mean = 100
std = 15
print(np.random.normal(mean, std, size=5))

# 2D array
print(np.random.normal(0, 1, size=(3, 3)))
```

### Other Distributions

```python
# Binomial distribution
n_trials = 10
prob_success = 0.5
print(np.random.binomial(n_trials, prob_success, size=5))

# Poisson distribution
lambda_param = 5
print(np.random.poisson(lambda_param, size=5))

# Exponential distribution
scale = 2.0
print(np.random.exponential(scale, size=5))

# Beta distribution
alpha, beta = 2, 5
print(np.random.beta(alpha, beta, size=5))

# Gamma distribution
shape, scale = 2, 2
print(np.random.gamma(shape, scale, size=5))
```

---

## Random Sampling

### Shuffling

```python
arr = np.array([1, 2, 3, 4, 5])

# Shuffle in-place
np.random.shuffle(arr)
print(arr)  # e.g., [3, 1, 5, 2, 4]

# Permutation (returns shuffled copy)
arr = np.array([1, 2, 3, 4, 5])
shuffled = np.random.permutation(arr)
print(shuffled)  # e.g., [2, 5, 1, 3, 4]
print(arr)  # [1, 2, 3, 4, 5] (unchanged)

# Random permutation of indices
indices = np.random.permutation(10)
print(indices)  # Random order of 0-9
```

### Sampling

```python
# Sample without replacement
data = np.arange(100)
sample = np.random.choice(data, size=10, replace=False)
print(sample)

# Sample with replacement
sample = np.random.choice(data, size=10, replace=True)
print(sample)

# Stratified sampling (manual)
def stratified_sample(data, labels, n_per_class):
    """Sample n_per_class from each unique label"""
    samples = []
    for label in np.unique(labels):
        class_data = data[labels == label]
        class_sample = np.random.choice(class_data, size=n_per_class, replace=False)
        samples.append(class_sample)
    return np.concatenate(samples)
```

---

## Reproducibility

### Setting Random Seed

```python
# Set seed for reproducibility
np.random.seed(42)
print(np.random.random(3))  # [0.374 0.950 0.731]

# Reset seed
np.random.seed(42)
print(np.random.random(3))  # [0.374 0.950 0.731] (same!)

# Different seed
np.random.seed(123)
print(np.random.random(3))  # Different numbers
```

### Random State

```python
# Save random state
state = np.random.get_state()

# Generate some numbers
print(np.random.random(3))

# Restore state
np.random.set_state(state)

# Generate same numbers again
print(np.random.random(3))  # Same as before!
```

---

## Random Generator (New API)

### Modern Approach (NumPy 1.17+)

```python
# Create generator with seed
rng = np.random.default_rng(42)

# Use generator
print(rng.random(5))
print(rng.integers(0, 10, size=5))
print(rng.normal(0, 1, size=5))

# Multiple independent generators
rng1 = np.random.default_rng(42)
rng2 = np.random.default_rng(123)

print(rng1.random(3))  # Different from rng2
print(rng2.random(3))
```

### Why Use New API?

```python
# ✅ NEW API - Better for parallel code
rng = np.random.default_rng(42)
result = rng.random(5)

# ❌ OLD API - Global state (problematic in parallel)
np.random.seed(42)
result = np.random.random(5)

# New API benefits:
# - Independent generators
# - Better for parallel/concurrent code
# - More modern algorithms
# - Cleaner interface
```

---

## Practical Examples

### Train/Test Split

```python
def train_test_split(X, y, test_size=0.2, random_state=None):
    """Split data into train and test sets"""
    rng = np.random.default_rng(random_state)
    n_samples = len(X)
    n_test = int(n_samples * test_size)
    
    # Random permutation
    indices = rng.permutation(n_samples)
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]

# Example
X = np.arange(100).reshape(100, 1)
y = np.arange(100)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
```

### Bootstrap Sampling

```python
def bootstrap_sample(data, n_bootstrap=1000, random_state=None):
    """Generate bootstrap samples"""
    rng = np.random.default_rng(random_state)
    n_samples = len(data)
    
    bootstrap_samples = []
    for _ in range(n_bootstrap):
        # Sample with replacement
        indices = rng.integers(0, n_samples, size=n_samples)
        bootstrap_samples.append(data[indices])
    
    return np.array(bootstrap_samples)

# Example
data = np.array([1, 2, 3, 4, 5])
samples = bootstrap_sample(data, n_bootstrap=5, random_state=42)
print(samples)
```

### Monte Carlo Simulation

```python
def estimate_pi(n_samples=1000000, random_state=None):
    """Estimate π using Monte Carlo method"""
    rng = np.random.default_rng(random_state)
    
    # Random points in [0, 1] x [0, 1]
    x = rng.random(n_samples)
    y = rng.random(n_samples)
    
    # Count points inside quarter circle
    inside_circle = (x**2 + y**2) <= 1
    pi_estimate = 4 * np.sum(inside_circle) / n_samples
    
    return pi_estimate

print(f"π ≈ {estimate_pi(1000000, random_state=42)}")  # ~3.14159
```

---

## Common Mistakes

### 1. Not Setting Seed for Reproducibility

```python
# ❌ WRONG - Results not reproducible
result = np.random.random(5)

# ✅ CORRECT - Reproducible
rng = np.random.default_rng(42)
result = rng.random(5)
```

### 2. Using Global Random State

```python
# ❌ WRONG - Global state (bad for parallel code)
np.random.seed(42)
result1 = np.random.random(5)
result2 = np.random.random(5)  # Depends on previous call!

# ✅ CORRECT - Independent generators
rng = np.random.default_rng(42)
result1 = rng.random(5)
result2 = rng.random(5)  # Independent
```

### 3. Sampling Without Replacement from Small Population

```python
# ❌ WRONG - Can't sample 100 from 10 without replacement
# np.random.choice(10, size=100, replace=False)  # Error!

# ✅ CORRECT - Use replacement or reduce sample size
sample = np.random.choice(10, size=100, replace=True)
```

---

## Best Practices

### 1. Use New Generator API

```python
# ✅ GOOD - Modern approach
rng = np.random.default_rng(42)
result = rng.random(1000)
```

### 2. Always Set Seed for Reproducibility

```python
# ✅ GOOD - Reproducible experiments
def my_experiment(random_state=None):
    rng = np.random.default_rng(random_state)
    # ... experiment code ...
    return results
```

### 3. Use Appropriate Distribution

```python
# ✅ GOOD - Choose right distribution
# Continuous uniform: rng.random()
# Discrete uniform: rng.integers()
# Normal: rng.normal()
# Binomial: rng.binomial()
```

---

## Quick Reference

```python
# Old API (legacy)
np.random.seed(42)           # Set seed
np.random.random(5)          # Uniform [0, 1)
np.random.randint(0, 10, 5)  # Random integers
np.random.randn(5)           # Standard normal
np.random.choice(arr, 5)     # Random choice
np.random.shuffle(arr)       # Shuffle in-place
np.random.permutation(arr)   # Shuffled copy

# New API (recommended)
rng = np.random.default_rng(42)  # Create generator
rng.random(5)                # Uniform [0, 1)
rng.integers(0, 10, 5)       # Random integers
rng.normal(0, 1, 5)          # Normal distribution
rng.choice(arr, 5)           # Random choice
rng.shuffle(arr)             # Shuffle in-place
rng.permutation(arr)         # Shuffled copy

# Distributions
rng.uniform(low, high, size)     # Uniform
rng.normal(mean, std, size)      # Normal
rng.binomial(n, p, size)         # Binomial
rng.poisson(lam, size)           # Poisson (lam = lambda parameter)
rng.exponential(scale, size)     # Exponential
```

---

[← Previous: Statistics](8-statistics.md) | [🏠 Home](README.md) | [Next: Advanced Topics →](10-advanced-topics.md)
