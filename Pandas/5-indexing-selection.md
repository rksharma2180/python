[← Previous: Data Loading](4-data-loading.md) | [🏠 Home](README.md) | [Next: Data Cleaning →](6-data-cleaning.md)

---

# 5. Indexing & Selection

## Table of Contents
- [loc vs iloc](#loc-vs-iloc)
- [Boolean Filtering](#boolean-filtering)
- [Query Method](#query-method)
- [Multi-Index](#multi-index)
- [Internal Working](#internal-working)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## loc vs iloc

### The Golden Rule

```
.loc  → Label-based   (uses row/column NAMES)
.iloc → Integer-based  (uses row/column POSITIONS)
```

### Setup Data

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Age": [25, 30, 35, 28, 32],
    "Salary": [50000, 60000, 70000, 55000, 62000],
    "Dept": ["IT", "HR", "IT", "HR", "IT"]
}, index=["emp1", "emp2", "emp3", "emp4", "emp5"])

print(df)
#          Name  Age  Salary Dept
# emp1    Alice   25   50000   IT
# emp2      Bob   30   60000   HR
# emp3  Charlie   35   70000   IT
# emp4    Diana   28   55000   HR
# emp5      Eve   32   62000   IT
```

### .loc (Label-based)

```python
# Single row
print(df.loc["emp1"])
# Name      Alice
# Age          25
# Salary    50000
# Dept         IT

# Single value
print(df.loc["emp1", "Name"])  # Alice

# Multiple rows
print(df.loc[["emp1", "emp3"]])

# Slice (inclusive on both ends!)
print(df.loc["emp1":"emp3"])  # emp1, emp2, AND emp3

# Rows + specific columns
print(df.loc["emp1":"emp3", ["Name", "Salary"]])
#          Name  Salary
# emp1    Alice   50000
# emp2      Bob   60000
# emp3  Charlie   70000
```

### .iloc (Position-based)

```python
# Single row (by position)
print(df.iloc[0])  # Same as df.loc["emp1"]

# Single value
print(df.iloc[0, 0])  # Alice

# Multiple rows
print(df.iloc[[0, 2]])

# Slice (exclusive end, like normal Python!)
print(df.iloc[0:3])  # Rows 0, 1, 2 (not 3!)

# Rows + columns by position
print(df.iloc[0:3, [0, 2]])  # First 3 rows, columns 0 and 2
#          Name  Salary
# emp1    Alice   50000
# emp2      Bob   60000
# emp3  Charlie   70000
```

### Key Difference: Slicing

```python
# .loc slicing is INCLUSIVE on both ends
df.loc["emp1":"emp3"]  # Returns emp1, emp2, emp3

# .iloc slicing is EXCLUSIVE on end (normal Python)
df.iloc[0:3]           # Returns rows 0, 1, 2 (not 3)
```

---

## Boolean Filtering

### Single Condition

```python
# Filter rows where Age > 30
print(df[df["Age"] > 30])
#          Name  Age  Salary Dept
# emp3  Charlie   35   70000   IT
# emp5      Eve   32   62000   IT
```

### Multiple Conditions

```python
# AND - use &
print(df[(df["Age"] > 25) & (df["Dept"] == "IT")])
#          Name  Age  Salary Dept
# emp3  Charlie   35   70000   IT
# emp5      Eve   32   62000   IT

# OR - use |
print(df[(df["Dept"] == "IT") | (df["Salary"] > 55000)])

# NOT - use ~
print(df[~(df["Dept"] == "IT")])  # Not IT dept
```

> ⚠️ **Important**: Use `&` `|` `~` (not `and` `or` `not`), and always wrap conditions in `()`.

### Using .isin()

```python
# Check if value is in a list
depts = ["IT", "Finance"]
print(df[df["Dept"].isin(depts)])
```

### Using .between()

```python
# Range filter
print(df[df["Age"].between(25, 32)])  # 25 <= Age <= 32
```

### Using .loc with Boolean

```python
# Filter rows AND select columns
print(df.loc[df["Age"] > 30, ["Name", "Salary"]])
#          Name  Salary
# emp3  Charlie   70000
# emp5      Eve   62000
```

---

## Query Method

A more readable alternative to boolean indexing.

```python
# Boolean indexing
df[df["Age"] > 30]

# Same with query (more readable)
df.query("Age > 30")

# Multiple conditions
df.query("Age > 25 and Dept == 'IT'")

# Using variables
min_age = 30
df.query("Age > @min_age")  # @ references external variable

# String methods in query
df.query("Name.str.startswith('A')", engine='python')
```

### Traditional vs Pandas

```python
# ======= Traditional Python =======
employees = [
    {"Name": "Alice", "Age": 25, "Salary": 50000},
    {"Name": "Bob", "Age": 30, "Salary": 60000},
    {"Name": "Charlie", "Age": 35, "Salary": 70000},
]

# Filter: Age > 30 and Salary > 55000
result = [e for e in employees if e["Age"] > 30 and e["Salary"] > 55000]

# ======= Pandas Way =======
result = df.query("Age > 30 and Salary > 55000")
```

---

## Multi-Index

### Creating Multi-Index

```python
# Multi-level index
df = pd.DataFrame({
    "Value": [100, 200, 300, 400, 500, 600]
}, index=pd.MultiIndex.from_tuples([
    ("IT", "Alice"), ("IT", "Bob"), ("IT", "Charlie"),
    ("HR", "Diana"), ("HR", "Eve"), ("HR", "Frank")
], names=["Dept", "Name"]))

print(df)
#               Value
# Dept Name
# IT   Alice     100
#      Bob       200
#      Charlie   300
# HR   Diana     400
#      Eve       500
#      Frank     600
```

### Accessing Multi-Index

```python
# Access top level
print(df.loc["IT"])
#          Value
# Name
# Alice      100
# Bob        200
# Charlie    300

# Access specific value
print(df.loc[("IT", "Alice")])  # Value    100

# Reset to flat index
df_flat = df.reset_index()
print(df_flat)
#   Dept     Name  Value
# 0   IT    Alice    100
# 1   IT      Bob    200
# ...
```

---

## Setting and Resetting Index

```python
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
})

# Set a column as index
df = df.set_index("Name")
print(df)
#          Age  Salary
# Name
# Alice     25   50000
# Bob       30   60000
# Charlie   35   70000

# Reset index back to default
df = df.reset_index()
print(df)
#       Name  Age  Salary
# 0    Alice   25   50000
# 1      Bob   30   60000
# 2  Charlie   35   70000
```

---

## Internal Working

### How Boolean Indexing Works

```
Step 1: df["Age"] > 30
        → Creates boolean Series: [False, False, True, False, True]

Step 2: df[boolean_series]
        → Selects only True rows

Flow:
┌────────────────┐
│  df["Age"]     │ → Series: [25, 30, 35, 28, 32]
├────────────────┤
│  > 30          │ → Bool:   [F, F, T, F, T]
├────────────────┤
│  df[mask]      │ → Filtered DataFrame (only True rows)
└────────────────┘
```

### .loc vs .iloc Performance

```
.loc["emp1"]  → Hash table lookup → O(1)
.iloc[0]      → Array position     → O(1)

.loc["emp1":"emp3"]  → Find start, find end, slice → O(1)
df[df["x"] > 5]     → Full column scan → O(n)
```

---

## Common Mistakes

### 1. Using `and` Instead of `&`

```python
# ❌ WRONG - Python's 'and' doesn't work on Series
# df[df["Age"] > 25 and df["Dept"] == "IT"]  # ValueError!

# ✅ CORRECT - Use & with parentheses
df[(df["Age"] > 25) & (df["Dept"] == "IT")]
```

### 2. Chained Indexing

```python
# ❌ WRONG - Chained indexing (unpredictable!)
df[df["Age"] > 30]["Name"] = "Modified"  # May not work!

# ✅ CORRECT - Use .loc
df.loc[df["Age"] > 30, "Name"] = "Modified"
```

### 3. Confusing Label vs Position After Filtering

```python
df = pd.DataFrame({"A": [10, 20, 30, 40, 50]})
filtered = df[df["A"] > 20]  # Rows with index 2, 3, 4
# filtered.iloc[0] → 30 (first row of result)
# filtered.loc[0]  → KeyError! (index 0 doesn't exist in filtered)
```

---

## Best Practices

### 1. Always Use .loc or .iloc Explicitly
```python
# ✅ Clear and predictable
df.loc[label]     # By label
df.iloc[position] # By position
```

### 2. Use .query() for Readability
```python
# ✅ More readable than nested boolean expressions
df.query("Age > 25 and Dept == 'IT' and Salary > 50000")
```

### 3. Copy When Modifying Subsets
```python
subset = df[df["Age"] > 30].copy()  # Safe to modify
```

---

## Quick Reference

```python
# Label-based (.loc)
df.loc["row_label"]                    # Single row
df.loc["r1":"r3"]                     # Slice (inclusive!)
df.loc["row", "col"]                  # Single value
df.loc[mask, ["col1", "col2"]]       # Filter + select

# Position-based (.iloc)
df.iloc[0]                            # First row
df.iloc[0:3]                         # Slice (exclusive end)
df.iloc[0, 2]                        # Row 0, col 2

# Boolean filtering
df[df["col"] > 5]                    # Single condition
df[(cond1) & (cond2)]               # AND
df[(cond1) | (cond2)]               # OR
df[~condition]                       # NOT
df[df["col"].isin([1, 2, 3])]       # In list
df[df["col"].between(a, b)]         # Range

# Query (readable alternative)
df.query("col > 5")                  # Simple
df.query("col > @variable")         # With variable

# Index operations
df.set_index("col")                  # Set column as index
df.reset_index()                     # Reset to default
```

---

[← Previous: Data Loading](4-data-loading.md) | [🏠 Home](README.md) | [Next: Data Cleaning →](6-data-cleaning.md)
