[← Previous: Linear Algebra](7-linear-algebra.md) | [🏠 Home](README.md) | [Next: Random Numbers →](9-random.md)

---

# 8. Statistics and Aggregations

## Table of Contents
- [Basic Statistics](#basic-statistics)
- [Aggregation Functions](#aggregation-functions)
- [Statistical Distributions](#statistical-distributions)
- [Correlation and Covariance](#correlation-and-covariance)
- [Percentiles and Quantiles](#percentiles-and-quantiles)
- [Best Practices](#best-practices)

---

## Basic Statistics

### Central Tendency

```python
import numpy as np

data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Mean (average)
print(np.mean(data))     # 5.5
print(data.mean())       # 5.5

# Median (middle value)
print(np.median(data))   # 5.5

# Mode (most common) - use scipy.stats for this
from scipy import stats
print(stats.mode(data))  # Not in NumPy

# Weighted average
weights = np.array([1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
print(np.average(data, weights=weights))  # 6.5
```

### Spread/Dispersion

```python
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Variance
print(np.var(data))      # 8.25

# Standard deviation
print(np.std(data))      # 2.872

# Min and Max
print(np.min(data))      # 1
print(np.max(data))      # 10

# Range
print(np.ptp(data))      # 9 (peak-to-peak, max - min)
```

---

## Aggregation Functions

### Basic Aggregations

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

# Sum
print(arr.sum())         # 21 (all elements)
print(arr.sum(axis=0))   # [5 7 9] (column sums)
print(arr.sum(axis=1))   # [6 15] (row sums)

# Product
print(arr.prod())        # 720 (1*2*3*4*5*6)
print(arr.prod(axis=0))  # [4 10 18]

# Cumulative sum
print(arr.cumsum())      # [1 3 6 10 15 21]
```

### Min/Max Functions

```python
arr = np.array([[1, 5, 3],
                [9, 2, 7]])

# Minimum and maximum
print(arr.min())         # 1
print(arr.max())         # 9

# Argmin and argmax (indices)
print(arr.argmin())      # 0 (flattened index)
print(arr.argmax())      # 3 (flattened index)

# Along axis
print(arr.min(axis=0))   # [1 2 3] (column minimums)
print(arr.max(axis=1))   # [5 9] (row maximums)

# Argmin/argmax along axis
print(arr.argmin(axis=0))  # [0 1 0]
print(arr.argmax(axis=1))  # [1 0]
```

---

## Statistical Distributions

### Descriptive Statistics

```python
data = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5])

# Mean
mean = np.mean(data)     # 3.0

# Variance (population)
var_pop = np.var(data)   # 1.111

# Variance (sample)
var_sample = np.var(data, ddof=1)  # 1.25

# Standard deviation
std = np.std(data)       # 1.054

# Standard error
std_err = std / np.sqrt(len(data))  # 0.351
```

### Histogram

```python
data = np.random.randn(1000)

# Create histogram
counts, bin_edges = np.histogram(data, bins=10)
print("Counts:", counts)
print("Bin edges:", bin_edges)

# Histogram with specific range
counts, bins = np.histogram(data, bins=10, range=(-3, 3))
```

---

## Correlation and Covariance

### Covariance

```python
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# Covariance matrix
cov_matrix = np.cov(x, y)
print(cov_matrix)
# [[2.5  1.75]
#  [1.75 1.7 ]]

# Covariance value
print(cov_matrix[0, 1])  # 1.75
```

### Correlation

```python
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# Correlation coefficient
corr_matrix = np.corrcoef(x, y)
print(corr_matrix)
# [[1.    0.849]
#  [0.849 1.   ]]

# Correlation value
print(corr_matrix[0, 1])  # 0.849
```

### Multi-variable Correlation

```python
# Multiple variables
data = np.array([[1, 2, 3, 4, 5],
                 [2, 4, 5, 4, 5],
                 [5, 4, 3, 2, 1]])

# Correlation matrix
corr = np.corrcoef(data)
print(corr)
# [[ 1.     0.849 -1.   ]
#  [ 0.849  1.    -0.849]
#  [-1.    -0.849  1.   ]]
```

---

## Percentiles and Quantiles

### Percentiles

```python
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 25th, 50th, 75th percentiles
print(np.percentile(data, 25))   # 3.25
print(np.percentile(data, 50))   # 5.5 (median)
print(np.percentile(data, 75))   # 7.75

# Multiple percentiles
print(np.percentile(data, [25, 50, 75]))
# [3.25 5.5  7.75]

# Quantiles (0 to 1 scale)
print(np.quantile(data, 0.25))   # 3.25
print(np.quantile(data, [0.25, 0.5, 0.75]))
# [3.25 5.5  7.75]
```

### Interquartile Range (IQR)

```python
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100])  # With outlier

q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
iqr = q3 - q1

print(f"Q1: {q1}, Q3: {q3}, IQR: {iqr}")

# Outlier detection
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = data[(data < lower_bound) | (data > upper_bound)]
print("Outliers:", outliers)  # [100]
```

---

## Advanced Statistics

### Binning Data

```python
data = np.array([1, 5, 10, 15, 20, 25, 30])
bins = [0, 10, 20, 30]

# Digitize (assign to bins)
bin_indices = np.digitize(data, bins)
print(bin_indices)  # [1 1 1 2 2 3 3]

# Histogram-based binning
counts, bin_edges = np.histogram(data, bins=3)
print("Counts:", counts)
print("Bin edges:", bin_edges)
```

### Moving Average

```python
def moving_average(data, window_size):
    """Calculate moving average"""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
ma = moving_average(data, window_size=3)
print(ma)  # [2. 3. 4. 5. 6. 7. 8. 9.]
```

---

## Common Mistakes

### 1. Population vs Sample Variance

```python
data = np.array([1, 2, 3, 4, 5])

# ❌ WRONG - Population variance (biased)
var = np.var(data)  # Divides by n

# ✅ CORRECT - Sample variance (unbiased)
var = np.var(data, ddof=1)  # Divides by n-1
```

### 2. Axis Confusion

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

# ❌ WRONG - Confusing axis
print(arr.mean(axis=0))  # Column means, not row means!

# ✅ CORRECT - Be explicit
row_means = arr.mean(axis=1)    # [2. 5.]
col_means = arr.mean(axis=0)    # [2.5 3.5 4.5]
```

---

## Best Practices

### 1. Use Appropriate Statistics

```python
# ✅ GOOD - Use median for skewed data
data_with_outliers = np.array([1, 2, 3, 4, 5, 100])
print(np.median(data_with_outliers))  # 3.5 (robust)
print(np.mean(data_with_outliers))    # 19.17 (affected by outlier)
```

### 2. Specify ddof for Sample Statistics

```python
# ✅ GOOD - Sample statistics
sample_var = np.var(data, ddof=1)
sample_std = np.std(data, ddof=1)
```

### 3. Check for NaN Values

```python
# ✅ GOOD - Use nanmean, nanstd for data with NaN
data = np.array([1, 2, np.nan, 4, 5])
print(np.nanmean(data))  # 3.0 (ignores NaN)
print(np.nanstd(data))   # 1.581
```

---

## Quick Reference

```python
# Central tendency
np.mean(arr)              # Mean
np.median(arr)            # Median
np.average(arr, weights)  # Weighted average

# Spread
np.var(arr, ddof=1)       # Variance
np.std(arr, ddof=1)       # Standard deviation
np.ptp(arr)               # Range (max - min)

# Aggregations
arr.sum(axis=0)           # Sum
arr.prod(axis=1)          # Product
arr.cumsum()              # Cumulative sum

# Min/Max
arr.min(), arr.max()      # Minimum, maximum
arr.argmin(), arr.argmax()  # Indices

# Percentiles
np.percentile(arr, 50)    # Percentile
np.quantile(arr, 0.5)     # Quantile

# Correlation
np.cov(x, y)              # Covariance
np.corrcoef(x, y)         # Correlation

# NaN-aware
np.nanmean(arr)           # Mean (ignore NaN)
np.nanstd(arr)            # Std (ignore NaN)
```

---

[← Previous: Linear Algebra](7-linear-algebra.md) | [🏠 Home](README.md) | [Next: Random Numbers →](9-random.md)
