[🏠 Home](README.md) | [Next: Series →](2-series.md)

---

# 1. Introduction to Pandas

## Table of Contents
- [What is Pandas?](#what-is-pandas)
- [Installation](#installation)
- [Why Pandas?](#why-pandas)
- [Pandas vs Traditional Python](#pandas-vs-traditional-python)
- [Core Data Structures](#core-data-structures)
- [Internal Architecture](#internal-architecture)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## What is Pandas?

**Pandas** stands for **Pan**el **Da**ta (from econometrics). It is the most popular Python library for data manipulation and analysis.

```
Pandas is to Data Analysis what NumPy is to Numerical Computing
```

### Key Features
- **Labeled data** - rows and columns have names (not just indices)
- **Heterogeneous data** - columns can have different types (int, str, float)
- **Built-in I/O** - read/write CSV, Excel, JSON, SQL, HTML, etc.
- **Missing data handling** - built-in NaN support
- **Powerful grouping** - SQL-like GROUP BY operations
- **Time series** - built-in date/time support

---

## Installation

```bash
pip install pandas
```

```python
import pandas as pd   # Standard convention
import numpy as np    # Often used together

print(pd.__version__)
```

> **Why `pd`?** It's the universally accepted alias, just like `np` for NumPy.

---

## Why Pandas?

### The Problem

```python
# Traditional Python: Working with structured data is painful

employees = [
    {"name": "Alice", "age": 25, "salary": 50000, "dept": "IT"},
    {"name": "Bob", "age": 30, "salary": 60000, "dept": "HR"},
    {"name": "Charlie", "age": 35, "salary": 70000, "dept": "IT"},
    {"name": "Diana", "age": 28, "salary": 55000, "dept": "HR"},
]

# Q: What is the average salary by department?

# Traditional Python way:
from collections import defaultdict
dept_salaries = defaultdict(list)
for emp in employees:
    dept_salaries[emp["dept"]].append(emp["salary"])

avg_by_dept = {dept: sum(sals)/len(sals) for dept, sals in dept_salaries.items()}
print(avg_by_dept)  # {'IT': 60000.0, 'HR': 57500.0}
```

### The Pandas Solution

```python
import pandas as pd

df = pd.DataFrame(employees)
avg_by_dept = df.groupby("dept")["salary"].mean()
print(avg_by_dept)
# dept
# HR    57500.0
# IT    60000.0
```

**One line vs seven lines!**

---

## Pandas vs Traditional Python

### Example 1: Filter Data

```python
# Traditional Python
high_earners = [e for e in employees if e["salary"] > 55000]

# Pandas
high_earners = df[df["salary"] > 55000]
```

### Example 2: Sort Data

```python
# Traditional Python
sorted_emps = sorted(employees, key=lambda x: x["salary"], reverse=True)

# Pandas
sorted_df = df.sort_values("salary", ascending=False)
```

### Example 3: Add Calculated Column

```python
# Traditional Python
for emp in employees:
    emp["bonus"] = emp["salary"] * 0.1

# Pandas
df["bonus"] = df["salary"] * 0.1
```

### Example 4: Read CSV File

```python
# Traditional Python
import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    data = [row for row in reader]
    # Now manually convert types...

# Pandas
df = pd.read_csv("data.csv")  # Done! Types auto-detected
```

### Comparison Table

| Operation | Traditional Python | Pandas |
|-----------|-------------------|--------|
| Read CSV | 5-10 lines | 1 line |
| Filter rows | List comprehension | Boolean indexing |
| Group & aggregate | defaultdict + loops | `.groupby().agg()` |
| Sort | `sorted()` with lambda | `.sort_values()` |
| Missing values | Manual if/else | Built-in NaN handling |
| Join datasets | Nested loops | `.merge()` |
| Statistics | Manual calculation | `.describe()` |

---

## Core Data Structures

### Overview

```
Pandas has 2 main data structures:

┌──────────────────────────────────┐
│  Series  (1D - like a column)   │
│  [10, 20, 30, 40]               │
│   with labels: [a, b, c, d]     │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│  DataFrame (2D - like a table)  │
│     Name    Age   Salary        │
│  0  Alice    25   50000         │
│  1  Bob      30   60000         │
│  2  Charlie  35   70000         │
│                                  │
│  (Collection of Series)         │
└──────────────────────────────────┘
```

### Series

```python
# A Series is a 1D labeled array
s = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])
print(s)
# a    10
# b    20
# c    30
# d    40
# dtype: int64
```

### DataFrame

```python
# A DataFrame is a 2D labeled table (collection of Series)
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
})
print(df)
#       Name  Age  Salary
# 0    Alice   25   50000
# 1      Bob   30   60000
# 2  Charlie   35   70000
```

### Relationship

```
DataFrame = Dictionary of Series (one per column)

df["Name"]   → Series: ["Alice", "Bob", "Charlie"]
df["Age"]    → Series: [25, 30, 35]
df["Salary"] → Series: [50000, 60000, 70000]
```

---

## Internal Architecture

### How Pandas Works Under the Hood

```
┌─────────────────────────────────────┐
│          Pandas DataFrame           │
│  ┌──────────────────────────────┐   │
│  │     Index (row labels)       │   │
│  │     [0, 1, 2, ...]          │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │    Block Manager             │   │
│  │  ┌─────┐ ┌─────┐ ┌───────┐  │   │
│  │  │int64│ │float│ │object │  │   │
│  │  │block│ │block│ │block  │  │   │
│  │  └─────┘ └─────┘ └───────┘  │   │
│  │  (NumPy arrays internally)  │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Key insight**: Pandas stores data in **NumPy arrays** grouped by dtype. This is why:
- Same-type operations are fast (NumPy vectorization)
- Mixed-type operations can be slower
- Memory layout matters for performance

```python
# Verify internal NumPy arrays
df = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
print(type(df["A"].values))  # <class 'numpy.ndarray'>
print(df["A"].dtype)         # int64
print(df["B"].dtype)         # float64
```

---

## Common Mistakes

### 1. Confusing Series and DataFrame

```python
# ❌ WRONG - Single bracket gives Series
column = df["Name"]
print(type(column))  # <class 'pandas.core.series.Series'>

# ✅ Double bracket gives DataFrame
column = df[["Name"]]
print(type(column))  # <class 'pandas.core.frame.DataFrame'>
```

### 2. Not Understanding Index

```python
# ❌ WRONG assumption - index always starts at 0
df = pd.DataFrame({"A": [1, 2, 3]}, index=[10, 20, 30])
# df[0]  # KeyError! Index is [10, 20, 30], not [0, 1, 2]

# ✅ CORRECT - Use .iloc for position, .loc for label
print(df.iloc[0])  # First row (by position)
print(df.loc[10])  # Row with index label 10
```

### 3. Forgetting inplace Parameter

```python
# ❌ WRONG - sort_values returns new DataFrame
df.sort_values("Age")  # Original df unchanged!

# ✅ CORRECT - Assign back or use inplace
df = df.sort_values("Age")          # Option 1
df.sort_values("Age", inplace=True) # Option 2
```

---

## Best Practices

### 1. Always Import with Standard Alias
```python
import pandas as pd  # ✅ Always use pd
```

### 2. Examine Data First
```python
df.head()      # First 5 rows
df.tail()      # Last 5 rows
df.info()      # Column types and non-null counts
df.describe()  # Statistical summary
df.shape       # (rows, columns)
```

### 3. Use Method Chaining
```python
# ✅ GOOD - Method chaining is clean
result = (df
    .query("age > 25")
    .sort_values("salary")
    .head(10)
)
```

---

## Quick Reference

```python
import pandas as pd

# Creation
pd.Series([1, 2, 3])                    # Series
pd.DataFrame({"A": [1, 2], "B": [3, 4]}) # DataFrame

# Inspect
df.head(), df.tail()         # First/last rows
df.info()                    # Column info
df.describe()                # Statistics
df.shape                     # Dimensions
df.dtypes                    # Column types
df.columns                   # Column names
df.index                     # Row labels

# Basic operations
df["column"]                 # Select column (Series)
df[["col1", "col2"]]        # Select columns (DataFrame)
df.sort_values("column")    # Sort
df.drop("column", axis=1)   # Drop column
```

---

[🏠 Home](README.md) | [Next: Series →](2-series.md)
