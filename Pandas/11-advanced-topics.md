[← Previous: Time Series](10-time-series.md) | [🏠 Home](README.md)

---

# 11. Advanced Topics & Best Practices

## Table of Contents
- [Performance Optimization](#performance-optimization)
- [Memory Management](#memory-management)
- [Vectorization Deep Dive](#vectorization-deep-dive)
- [Method Chaining](#method-chaining)
- [Working with Large Datasets](#working-with-large-datasets)
- [Pandas for AI/ML](#pandas-for-aiml)
- [Common Pitfalls Summary](#common-pitfalls-summary)
- [Best Practices Summary](#best-practices-summary)

---

## Performance Optimization

### Speed Hierarchy

```
Fastest ──────────────────────────── Slowest

Vectorized    >  apply()   >  itertuples()  >  iterrows()  >  for loop
(NumPy)          (Pandas)     (Pandas)          (Pandas)       (Python)

100x              10x           5x                1x             0.1x
(relative speed)
```

### Avoid Loops - Use Vectorization

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "A": np.random.randint(1, 100, 100000),
    "B": np.random.randint(1, 100, 100000)
})

# ❌ WORST - Python for loop
result = []
for i in range(len(df)):
    result.append(df.iloc[i]["A"] + df.iloc[i]["B"])
df["C"] = result

# ❌ BAD - iterrows
for idx, row in df.iterrows():
    df.loc[idx, "C"] = row["A"] + row["B"]

# 🟡 OK - apply
df["C"] = df.apply(lambda row: row["A"] + row["B"], axis=1)

# ✅ BEST - Vectorized
df["C"] = df["A"] + df["B"]
```

### Timing Comparison

```python
import time

# Method 1: for loop (~5 seconds)
start = time.time()
for i in range(len(df)):
    _ = df.iloc[i]["A"] + df.iloc[i]["B"]
print(f"Loop: {time.time() - start:.3f}s")

# Method 2: Vectorized (~0.001 seconds)
start = time.time()
_ = df["A"] + df["B"]
print(f"Vectorized: {time.time() - start:.3f}s")
```

---

## Memory Management

### Check Memory Usage

```python
df = pd.DataFrame({
    "int_col": np.random.randint(0, 100, 100000),
    "float_col": np.random.random(100000),
    "str_col": np.random.choice(["A", "B", "C"], 100000)
})

# Memory usage
print(df.memory_usage(deep=True))
# Index        800000
# int_col      800000  ← 8 bytes × 100000
# float_col    800000
# str_col     5600000  ← Strings use more memory!

# Total
print(f"Total: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
```

### Reduce Memory

```python
# 1. Downcast integers
df["int_col"] = pd.to_numeric(df["int_col"], downcast="integer")
# int64 (8 bytes) → int8 (1 byte) if values fit

# 2. Downcast floats
df["float_col"] = pd.to_numeric(df["float_col"], downcast="float")
# float64 (8 bytes) → float32 (4 bytes)

# 3. Use category for repeated strings
df["str_col"] = df["str_col"].astype("category")
# Huge savings! Only stores unique values + indices

# Check savings
print(f"After: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
```

### Dtype Guide

```
┌──────────────┬───────────┬────────────────────────────┐
│   Dtype      │   Bytes   │   When to Use              │
├──────────────┼───────────┼────────────────────────────┤
│  int8        │   1       │   -128 to 127              │
│  int16       │   2       │   -32768 to 32767          │
│  int32       │   4       │   -2B to 2B                │
│  int64       │   8       │   Very large integers      │
│  float32     │   4       │   6-7 decimal precision    │
│  float64     │   8       │   15-16 decimal precision  │
│  category    │   varies  │   Repeated strings         │
│  bool        │   1       │   True/False               │
└──────────────┴───────────┴────────────────────────────┘
```

---

## Vectorization Deep Dive

### Conditional Logic Without Loops

```python
df = pd.DataFrame({
    "score": np.random.randint(0, 100, 10000),
    "attendance": np.random.uniform(0.5, 1.0, 10000)
})

# ❌ BAD - apply with if/else
df["grade"] = df["score"].apply(lambda x: "A" if x >= 90 else "B" if x >= 70 else "C")

# ✅ GOOD - np.select (vectorized)
conditions = [
    df["score"] >= 90,
    df["score"] >= 70,
    df["score"] < 70
]
choices = ["A", "B", "C"]
df["grade"] = np.select(conditions, choices)

# ✅ GOOD - pd.cut for binning
df["grade"] = pd.cut(df["score"], bins=[0, 70, 90, 100], labels=["C", "B", "A"])
```

### String Operations Vectorized

```python
# ❌ BAD - apply
df["upper"] = df["name"].apply(lambda x: x.upper())

# ✅ GOOD - .str accessor
df["upper"] = df["name"].str.upper()
```

---

## Method Chaining

### The Pattern

```python
# ❌ BAD - Multiple reassignments
df = df.dropna()
df = df[df["age"] > 25]
df = df.sort_values("salary")
df = df.head(10)

# ✅ GOOD - Method chaining
result = (df
    .dropna()
    .query("age > 25")
    .sort_values("salary")
    .head(10)
)
```

### assign() for New Columns

```python
# ✅ Clean chaining with assign
result = (df
    .assign(bonus=lambda x: x["salary"] * 0.1)
    .assign(total=lambda x: x["salary"] + x["bonus"])
    .query("total > 60000")
    .sort_values("total", ascending=False)
    [["name", "salary", "bonus", "total"]]
)
```

### pipe() for Custom Functions

```python
def add_tax(df, rate=0.3):
    return df.assign(tax=df["salary"] * rate)

def add_net(df):
    return df.assign(net=df["salary"] - df["tax"])

# Chain custom functions
result = (df
    .pipe(add_tax, rate=0.25)
    .pipe(add_net)
    .sort_values("net")
)
```

---

## Working with Large Datasets

### Chunked Reading

```python
# Read in chunks
total_sales = 0
for chunk in pd.read_csv("huge_file.csv", chunksize=100000):
    total_sales += chunk["sales"].sum()

print(f"Total sales: {total_sales}")
```

### Selective Loading

```python
# Only load needed columns
df = pd.read_csv("data.csv",
    usecols=["name", "age", "salary"],
    dtype={"age": "int16", "salary": "int32"},
    nrows=50000
)
```

### Use Parquet Format

```python
# Convert CSV to Parquet (one-time)
df = pd.read_csv("data.csv")
df.to_parquet("data.parquet")

# Read Parquet (much faster!)
df = pd.read_parquet("data.parquet")

# Parquet advantages:
# - 2-10x smaller file size
# - 5-100x faster read
# - Column selection at read time
# - Type preservation
```

---

## Pandas for AI/ML

### Feature Engineering

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "salary": [50000, 60000, 70000],
    "dept": ["IT", "HR", "IT"],
    "date_joined": pd.to_datetime(["2020-01-15", "2019-06-01", "2021-03-20"])
})

# 1. One-hot encoding
dept_dummies = pd.get_dummies(df["dept"], prefix="dept")
df = pd.concat([df, dept_dummies], axis=1)

# 2. Date features
df["tenure_days"] = (pd.Timestamp.now() - df["date_joined"]).dt.days
df["join_year"] = df["date_joined"].dt.year
df["join_month"] = df["date_joined"].dt.month

# 3. Normalization (Min-Max)
df["salary_norm"] = (df["salary"] - df["salary"].min()) / (df["salary"].max() - df["salary"].min())

# 4. Standardization (Z-score)
df["age_std"] = (df["age"] - df["age"].mean()) / df["age"].std()

# 5. Binning
df["age_group"] = pd.cut(df["age"], bins=[0, 28, 33, 100],
                          labels=["Young", "Mid", "Senior"])
```

### Preparing Data for ML Models

```python
# Typical ML preparation pipeline
def prepare_for_ml(df, target_col, drop_cols=None):
    """Prepare DataFrame for ML model"""
    df = df.copy()
    
    # Drop specified columns
    if drop_cols:
        df = df.drop(columns=drop_cols)
    
    # Separate features and target
    y = df[target_col]
    X = df.drop(columns=[target_col])
    
    # Handle categoricals
    cat_cols = X.select_dtypes(include=["object", "category"]).columns
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
    
    # Handle missing values
    num_cols = X.select_dtypes(include=[np.number]).columns
    X[num_cols] = X[num_cols].fillna(X[num_cols].median())
    
    return X, y

# Usage
X, y = prepare_for_ml(df, target_col="salary", drop_cols=["name", "date_joined"])
print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
```

### Train/Test Split

```python
from sklearn.model_selection import train_test_split

# Pandas + Scikit-learn
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# All remain as DataFrames!
print(type(X_train))  # <class 'pandas.core.frame.DataFrame'>
```

---

## Common Pitfalls Summary

### 1. SettingWithCopyWarning

```python
# ❌ WRONG
df[df["age"] > 30]["salary"] = 99999  # May not modify df!

# ✅ CORRECT
df.loc[df["age"] > 30, "salary"] = 99999
```

### 2. Chained Indexing

```python
# ❌ WRONG
df["col1"]["col2"]  # Unpredictable!

# ✅ CORRECT
df.loc[:, "col1"]
```

### 3. inplace Trap

```python
# ⚠️ NOTE: inplace=True is being phased out
# Use reassignment instead
df = df.sort_values("age")  # ✅ Preferred
```

### 4. Modifying During Iteration

```python
# ❌ WRONG
for idx, row in df.iterrows():
    df.loc[idx, "col"] = transform(row["col"])

# ✅ CORRECT
df["col"] = df["col"].apply(transform)
# or better: vectorized operation
```

### 5. Not Checking dtypes After Read

```python
# ✅ Always check after reading
df = pd.read_csv("data.csv")
print(df.dtypes)
print(df.info())
```

---

## Best Practices Summary

### 1. Performance
- ✅ Use vectorized operations (NumPy/Pandas built-ins)
- ✅ Use `np.where` / `np.select` for conditionals
- ✅ Avoid `iterrows()` - use `apply()` as last resort
- ✅ Use appropriate dtypes (downcast integers/floats)
- ✅ Use `category` dtype for repeated strings

### 2. Code Quality
- ✅ Use method chaining for readability
- ✅ Use `.query()` for readable filters
- ✅ Use named aggregations in `groupby`
- ✅ Use `assign()` to add columns in chains
- ✅ Always use `.copy()` when modifying subsets

### 3. Data Handling
- ✅ Parse dates when reading (not after)
- ✅ Check for missing values early (`df.info()`)
- ✅ Validate merge keys before merging
- ✅ Use `ignore_index=True` with `pd.concat`
- ✅ Use `.loc` / `.iloc` explicitly (avoid chained indexing)

### 4. Memory
- ✅ Use selective column loading (`usecols`)
- ✅ Use chunked reading for large files
- ✅ Use Parquet instead of CSV for large data
- ✅ Downcast numeric types to save memory
- ✅ Delete unused DataFrames (`del df`)

### 5. AI/ML Workflow
- ✅ Use `pd.get_dummies()` for one-hot encoding
- ✅ Handle missing values before modeling
- ✅ Create feature engineering pipelines
- ✅ Use `df.describe()` for initial data exploration
- ✅ Keep raw data separate from processed data

---

## Congratulations! 🎉

You've completed the Pandas learning guide! You now have the knowledge to:

- ✅ Create and manipulate Series and DataFrames
- ✅ Load data from CSV, Excel, JSON, and more
- ✅ Filter, clean, and transform data efficiently
- ✅ Group, aggregate, and create pivot tables
- ✅ Merge and join multiple datasets
- ✅ Work with time series data
- ✅ Optimize performance for large datasets
- ✅ Prepare data for AI/ML applications

### Next Steps

1. **Practice** - Work on real datasets (Kaggle, government data portals)
2. **Scikit-learn** - Apply ML models to your Pandas DataFrames
3. **Visualization** - Learn Matplotlib/Seaborn for plotting Pandas data
4. **SQL** - Compare Pandas operations with SQL queries
5. **LangChain/LangGraph** - Use Pandas for data-driven LLM applications

---

[← Previous: Time Series](10-time-series.md) | [🏠 Home](README.md)
