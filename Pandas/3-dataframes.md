[← Previous: Series](2-series.md) | [🏠 Home](README.md) | [Next: Data Loading →](4-data-loading.md)

---

# 3. DataFrames

## Table of Contents
- [What is a DataFrame?](#what-is-a-dataframe)
- [Creating DataFrames](#creating-dataframes)
- [DataFrame Properties](#dataframe-properties)
- [Column Operations](#column-operations)
- [Row Operations](#row-operations)
- [Internal Working](#internal-working)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## What is a DataFrame?

A **DataFrame** is a **2D labeled data structure** — like a spreadsheet, SQL table, or dictionary of Series.

```
       Name     Age    Salary    Dept
  0    Alice     25    50000     IT        ← Row (index 0)
  1    Bob       30    60000     HR        ← Row (index 1)
  2    Charlie   35    70000     IT        ← Row (index 2)
       ↑         ↑      ↑        ↑
     Column   Column  Column   Column
     (str)    (int)   (int)    (str)

Each column = Series (can have different dtypes)
```

---

## Creating DataFrames

### From Dictionary of Lists

```python
import pandas as pd

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

### From List of Dictionaries

```python
# Common when working with JSON/API data
data = [
    {"Name": "Alice", "Age": 25, "Salary": 50000},
    {"Name": "Bob", "Age": 30, "Salary": 60000},
    {"Name": "Charlie", "Age": 35, "Salary": 70000},
]
df = pd.DataFrame(data)
```

### From NumPy Array

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df = pd.DataFrame(arr, columns=["A", "B", "C"], index=["row1", "row2", "row3"])
print(df)
#       A  B  C
# row1  1  2  3
# row2  4  5  6
# row3  7  8  9
```

### From Dictionary of Series

```python
names = pd.Series(["Alice", "Bob"], name="Name")
ages = pd.Series([25, 30], name="Age")
df = pd.DataFrame({"Name": names, "Age": ages})
```

### With Custom Index

```python
df = pd.DataFrame(
    {"Name": ["Alice", "Bob", "Charlie"],
     "Salary": [50000, 60000, 70000]},
    index=["emp1", "emp2", "emp3"]
)
print(df)
#          Name  Salary
# emp1    Alice   50000
# emp2      Bob   60000
# emp3  Charlie   70000
```

---

## DataFrame Properties

```python
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [25, 30, 35, 28],
    "Salary": [50000, 60000, 70000, 55000],
    "Dept": ["IT", "HR", "IT", "HR"]
})

# Shape (rows, columns)
print(df.shape)       # (4, 4)

# Column names
print(df.columns)     # Index(['Name', 'Age', 'Salary', 'Dept'])

# Index (row labels)
print(df.index)       # RangeIndex(start=0, stop=4, step=1)

# Data types
print(df.dtypes)
# Name      object
# Age        int64
# Salary     int64
# Dept      object

# Summary info
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 4 entries, 0 to 3
# Data columns (total 4 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   Name    4 non-null      object
#  1   Age     4 non-null      int64
#  2   Salary  4 non-null      int64
#  3   Dept    4 non-null      object

# Statistical summary (numeric columns only)
print(df.describe())
#              Age        Salary
# count   4.000000      4.000000
# mean   29.500000  58750.000000
# std     4.203173   8539.125639
# min    25.000000  50000.000000
# 25%    27.250000  53750.000000
# 50%    29.000000  57500.000000
# 75%    31.250000  62500.000000
# max    35.000000  70000.000000

# First/Last rows
print(df.head(2))     # First 2 rows
print(df.tail(2))     # Last 2 rows

# Memory usage
print(df.memory_usage(deep=True))
```

---

## Column Operations

### Selecting Columns

```python
# Single column → Series
print(df["Name"])
print(type(df["Name"]))  # <class 'pandas.core.series.Series'>

# Multiple columns → DataFrame
print(df[["Name", "Salary"]])
print(type(df[["Name", "Salary"]]))  # <class 'pandas.core.frame.DataFrame'>

# Dot notation (works for simple column names)
print(df.Name)  # Same as df["Name"], but limited
```

### Adding Columns

```python
# New column from calculation
df["Bonus"] = df["Salary"] * 0.1

# New column from condition
df["Senior"] = df["Age"] > 30

# New column with constant
df["Country"] = "India"

print(df)
#       Name  Age  Salary Dept   Bonus  Senior Country
# 0    Alice   25   50000   IT  5000.0   False   India
# 1      Bob   30   60000   HR  6000.0   False   India
# 2  Charlie   35   70000   IT  7000.0    True   India
# 3    Diana   28   55000   HR  5500.0   False   India
```

### Renaming Columns

```python
# Rename specific columns
df = df.rename(columns={"Name": "Employee", "Dept": "Department"})

# Rename all columns
df.columns = ["emp_name", "emp_age", "emp_salary", "emp_dept"]
```

### Dropping Columns

```python
# Drop single column
df = df.drop("Bonus", axis=1)

# Drop multiple columns
df = df.drop(["Senior", "Country"], axis=1)

# Drop in-place
df.drop("Bonus", axis=1, inplace=True)
```

### Reordering Columns

```python
df = df[["Name", "Dept", "Age", "Salary"]]  # New order
```

---

## Row Operations

### Selecting Rows

```python
# By position
print(df.iloc[0])       # First row (as Series)
print(df.iloc[0:3])     # First 3 rows

# By label
print(df.loc[0])        # Row with index label 0

# Boolean filtering
print(df[df["Age"] > 30])
```

### Adding Rows

```python
# Using loc
df.loc[4] = ["Eve", 32, 65000, "IT"]

# Using concat (preferred for multiple rows)
new_row = pd.DataFrame({"Name": ["Frank"], "Age": [29],
                         "Salary": [58000], "Dept": ["HR"]})
df = pd.concat([df, new_row], ignore_index=True)
```

### Dropping Rows

```python
# By index
df = df.drop(0)            # Drop row with index 0
df = df.drop([0, 2, 4])   # Drop multiple rows

# By condition
df = df[df["Age"] > 25]    # Keep only age > 25
```

### Sorting Rows

```python
# Sort by single column
df = df.sort_values("Age")

# Sort by multiple columns
df = df.sort_values(["Dept", "Salary"], ascending=[True, False])

# Sort by index
df = df.sort_index()
```

---

## Internal Working

### Block Manager Architecture

```
DataFrame internally uses a "Block Manager"
that groups columns by dtype for efficiency:

┌─────────────────────────────────────────┐
│            DataFrame                     │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Index       │  │ Block Manager   │  │
│  │  [0,1,2,3]  │  │                  │  │
│  └─────────────┘  │  ┌────────────┐  │  │
│                    │  │ int64 block│  │  │
│  ┌─────────────┐  │  │ Age|Salary │  │  │
│  │  Columns     │  │  └────────────┘  │  │
│  │  [Name, Age, │  │  ┌────────────┐  │  │
│  │   Salary,    │  │  │object block│  │  │
│  │   Dept]      │  │  │ Name|Dept  │  │  │
│  └─────────────┘  │  └────────────┘  │  │
│                    └──────────────────┘  │
└─────────────────────────────────────────┘
```

```python
# Verify: each column is backed by NumPy
df = pd.DataFrame({"A": [1, 2], "B": [3.0, 4.0], "C": ["x", "y"]})
print(df.dtypes)
# A      int64
# B    float64
# C     object

# Underlying array
print(df["A"].values)        # NumPy array
print(type(df["A"].values))  # <class 'numpy.ndarray'>
```

### Why Column Operations are Fast

```
Column access: O(1) → Direct lookup in Block Manager
Row access:    O(n) → Must traverse all blocks

That's why:
✅ df["column"]        # Fast (column access)
⚠️ df.iloc[0]          # Slower (row access across blocks)
✅ df["column"].mean()  # Fast (vectorized on single array)
```

---

## Common Mistakes

### 1. Single vs Double Brackets

```python
# ❌ Confusing - returns different types!
series = df["Name"]           # Series (1D)
dataframe = df[["Name"]]     # DataFrame (2D)

# This matters for operations:
# series.shape     → (4,)
# dataframe.shape  → (4, 1)
```

### 2. SettingWithCopyWarning

```python
# ❌ WRONG - May not modify original
subset = df[df["Age"] > 30]
subset["Bonus"] = 1000  # ⚠️ Warning!

# ✅ CORRECT - Use .loc
df.loc[df["Age"] > 30, "Bonus"] = 1000
```

### 3. Append is Removed (Pandas 2.0+)

```python
# ❌ WRONG - df.append() removed in Pandas 2.0
# df = df.append(new_row)

# ✅ CORRECT - Use pd.concat()
df = pd.concat([df, new_row], ignore_index=True)
```

---

## Best Practices

### 1. Explore Data First
```python
# ✅ Always run these on new data
df.head()
df.info()
df.describe()
df.shape
df.dtypes
```

### 2. Use Vectorized Operations
```python
# ❌ BAD
for i in range(len(df)):
    df.loc[i, "Bonus"] = df.loc[i, "Salary"] * 0.1

# ✅ GOOD
df["Bonus"] = df["Salary"] * 0.1
```

### 3. Chain Methods
```python
# ✅ GOOD - Clean and readable
result = (df
    .query("Age > 25")
    .sort_values("Salary", ascending=False)
    .head(5)
)
```

---

## Quick Reference

```python
# Creation
pd.DataFrame(dict)                    # From dict
pd.DataFrame(list_of_dicts)          # From records
pd.DataFrame(numpy_array, columns=[]) # From NumPy

# Properties
df.shape, df.dtypes, df.columns, df.index
df.head(), df.tail(), df.info(), df.describe()

# Columns
df["col"]              # Select (Series)
df[["col1", "col2"]]  # Select (DataFrame)
df["new"] = values     # Add column
df.drop("col", axis=1) # Drop column
df.rename(columns={})  # Rename

# Rows
df.iloc[0]             # By position
df.loc[label]          # By label
df[df["col"] > 5]     # Filter
df.sort_values("col")  # Sort
df.drop(index)         # Drop row
pd.concat([df, new])   # Add rows
```

---

[← Previous: Series](2-series.md) | [🏠 Home](README.md) | [Next: Data Loading →](4-data-loading.md)
