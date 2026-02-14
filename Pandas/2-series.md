[← Previous: Introduction](1-introduction.md) | [🏠 Home](README.md) | [Next: DataFrames →](3-dataframes.md)

---

# 2. Pandas Series

## Table of Contents
- [What is a Series?](#what-is-a-series)
- [Creating Series](#creating-series)
- [Indexing and Slicing](#indexing-and-slicing)
- [Operations](#operations)
- [String Methods](#string-methods)
- [Internal Working](#internal-working)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## What is a Series?

A **Series** is a **1D labeled array**. Think of it as a single column in a spreadsheet.

```
Traditional Python Dict       Pandas Series
┌───────┬───────┐            ┌───────┬───────┐
│  Key  │ Value │            │ Index │ Value │
├───────┼───────┤            ├───────┼───────┤
│  "a"  │  10   │   ───►    │   a   │  10   │
│  "b"  │  20   │            │   b   │  20   │
│  "c"  │  30   │            │   c   │  30   │
└───────┴───────┘            └───────┴───────┘
                              + NumPy operations!
                              + Vectorized!
                              + Broadcasting!
```

---

## Creating Series

### From a List

```python
import pandas as pd
import numpy as np

# Basic Series
s = pd.Series([10, 20, 30, 40])
print(s)
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64

# With custom index
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
print(s)
# a    10
# b    20
# c    30
# d    40
# dtype: int64
```

### From a Dictionary

```python
# Dictionary keys become the index
data = {"apples": 5, "bananas": 3, "oranges": 8}
s = pd.Series(data)
print(s)
# apples     5
# bananas    3
# oranges    8
# dtype: int64
```

### From a NumPy Array

```python
arr = np.array([100, 200, 300])
s = pd.Series(arr, index=["x", "y", "z"], name="values")
print(s)
# x    100
# y    200
# z    300
# Name: values, dtype: int64
```

### From a Scalar

```python
# Scalar is broadcast to all indices
s = pd.Series(5, index=["a", "b", "c"])
print(s)
# a    5
# b    5
# c    5
# dtype: int64
```

---

## Indexing and Slicing

### Label-based Indexing

```python
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])

# Single element
print(s["a"])      # 10

# Multiple elements
print(s[["a", "c"]])
# a    10
# c    30

# Slice by label (inclusive on both ends!)
print(s["a":"c"])
# a    10
# b    20
# c    30  ← Included! (unlike regular Python slicing)
```

### Position-based Indexing

```python
# By position (like NumPy)
print(s.iloc[0])       # 10
print(s.iloc[1:3])     # b=20, c=30 (exclusive end, like normal)

# .loc vs .iloc
print(s.loc["b"])      # 20 (by label)
print(s.iloc[1])       # 20 (by position)
```

### Boolean Indexing

```python
s = pd.Series([10, 20, 30, 40, 50])

# Filter with condition
print(s[s > 25])
# 2    30
# 3    40
# 4    50

# Multiple conditions
print(s[(s > 15) & (s < 45)])
# 1    20
# 2    30
# 3    40
```

---

## Operations

### Arithmetic Operations

```python
s = pd.Series([10, 20, 30, 40])

# Scalar operations (broadcasting)
print(s + 5)    # [15 25 35 45]
print(s * 2)    # [20 40 60 80]
print(s ** 2)   # [100 400 900 1600]

# Series operations (aligned by index!)
s1 = pd.Series([1, 2, 3], index=["a", "b", "c"])
s2 = pd.Series([10, 20, 30], index=["b", "c", "d"])
print(s1 + s2)
# a     NaN  ← "a" only in s1
# b    12.0  ← 2 + 10
# c    23.0  ← 3 + 20
# d     NaN  ← "d" only in s2
```

> **Key Insight**: Pandas **aligns by index**, not by position. Missing indices produce `NaN`.

### Traditional vs Pandas Way

```python
prices = [100, 200, 300, 400, 500]

# Traditional: Apply 10% discount
discounted = [p * 0.9 for p in prices]

# Pandas: Vectorized (faster!)
prices_s = pd.Series(prices)
discounted = prices_s * 0.9
```

### Aggregation

```python
s = pd.Series([10, 20, 30, 40, 50])

print(s.sum())     # 150
print(s.mean())    # 30.0
print(s.median())  # 30.0
print(s.std())     # 15.81
print(s.min())     # 10
print(s.max())     # 50
print(s.count())   # 5

# All at once
print(s.describe())
# count     5.0
# mean     30.0
# std      15.81
# min      10.0
# 25%      20.0
# 50%      30.0
# 75%      40.0
# max      50.0
```

### Useful Methods

```python
s = pd.Series([3, 1, 4, 1, 5, 9, 2, 6])

# Sort
print(s.sort_values())           # Sorted by values
print(s.sort_index())            # Sorted by index

# Unique values
print(s.unique())                # [3 1 4 5 9 2 6]
print(s.nunique())               # 7 unique values
print(s.value_counts())          # Count of each value

# Check conditions
print(s.isin([1, 5]))            # Boolean mask
print(s.between(2, 6))           # True if 2 <= x <= 6

# Apply function
print(s.apply(lambda x: x ** 2)) # Square each element
```

---

## String Methods

```python
names = pd.Series(["alice", "BOB", "Charlie", "  diana  "])

# String accessor: .str
print(names.str.upper())       # ALICE, BOB, CHARLIE, DIANA
print(names.str.lower())       # alice, bob, charlie, diana
print(names.str.title())       # Alice, Bob, Charlie, Diana
print(names.str.strip())       # Remove whitespace
print(names.str.len())         # Length of each string
print(names.str.contains("a", case=False))  # Boolean mask
print(names.str.replace("a", "@", case=False))  # Replace
```

### Traditional vs Pandas

```python
names = ["alice", "bob", "charlie"]

# Traditional
upper_names = [n.upper() for n in names]

# Pandas - vectorized string operations
s = pd.Series(names)
upper_names = s.str.upper()
```

---

## Internal Working

### Memory Layout

```python
s = pd.Series([10, 20, 30], index=["a", "b", "c"])

# Internally:
# ┌─── Index Object ───┐  ┌─── NumPy Array ───┐
# │ "a" → position 0   │  │ [10, 20, 30]      │
# │ "b" → position 1   │  │ dtype: int64       │
# │ "c" → position 2   │  │                    │
# └────────────────────┘  └────────────────────┘

# Access underlying NumPy array
print(s.values)        # [10 20 30] (NumPy array)
print(type(s.values))  # <class 'numpy.ndarray'>
print(s.index)         # Index(['a', 'b', 'c'], dtype='object')
```

### Index Alignment Flow

```
s1:  a=1, b=2, c=3
s2:  b=10, c=20, d=30

s1 + s2:
   Step 1: Union of indices → [a, b, c, d]
   Step 2: Align values:
           a: 1 + NaN = NaN
           b: 2 + 10  = 12
           c: 3 + 20  = 23
           d: NaN + 30 = NaN
```

---

## Common Mistakes

### 1. Label Slicing is Inclusive

```python
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])

# ❌ WRONG assumption - "c" excluded like Python slicing
print(s["a":"c"])  # "c" IS included!
# a    10
# b    20
# c    30  ← Included!

# .iloc slicing is exclusive (normal Python behavior)
print(s.iloc[0:2])  # Only indices 0 and 1
```

### 2. NaN in Index Operations

```python
s1 = pd.Series([1, 2, 3], index=["a", "b", "c"])
s2 = pd.Series([10, 20], index=["a", "b"])

# ❌ WRONG - Expecting all values
result = s1 + s2
# c will be NaN!

# ✅ CORRECT - Use fill_value
result = s1.add(s2, fill_value=0)
# a    11.0
# b    22.0
# c     3.0
```

### 3. Modifying a Copy vs View

```python
s = pd.Series([1, 2, 3, 4, 5])

# ❌ WRONG - May modify original unexpectedly
subset = s[s > 3]
subset.iloc[0] = 999  # May or may not affect s

# ✅ CORRECT - Be explicit
subset = s[s > 3].copy()
subset.iloc[0] = 999  # s is safe
```

---

## Best Practices

### 1. Use .loc and .iloc Explicitly
```python
# ✅ GOOD - Clear intent
s.loc["a"]     # By label
s.iloc[0]      # By position
```

### 2. Use Vectorized Operations
```python
# ❌ BAD - Loop
result = pd.Series([x**2 for x in s])

# ✅ GOOD - Vectorized
result = s ** 2
```

### 3. Name Your Series
```python
# ✅ GOOD - Self-documenting
revenue = pd.Series([100, 200, 300], name="monthly_revenue")
```

---

## Quick Reference

```python
# Creation
pd.Series([1, 2, 3])                       # From list
pd.Series({"a": 1, "b": 2})                # From dict
pd.Series(np.array([1, 2, 3]))             # From NumPy

# Indexing
s.loc["label"]          # By label
s.iloc[0]               # By position
s[s > 5]                # Boolean filter

# Operations
s + 5, s * 2            # Scalar operations
s1 + s2                 # Series operations (aligned!)
s.apply(func)           # Apply function

# Aggregation
s.sum(), s.mean(), s.std(), s.median()
s.min(), s.max(), s.count()
s.describe()            # All stats at once

# String
s.str.upper(), s.str.lower()
s.str.contains("pattern")
s.str.replace("old", "new")

# Utility
s.sort_values()         # Sort by values
s.value_counts()        # Frequency counts
s.unique(), s.nunique() # Unique values
s.isnull(), s.notnull() # Check NaN
```

---

[← Previous: Introduction](1-introduction.md) | [🏠 Home](README.md) | [Next: DataFrames →](3-dataframes.md)
