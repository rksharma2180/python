[← Previous: Grouping & Aggregation](8-grouping-aggregation.md) | [🏠 Home](README.md) | [Next: Time Series →](10-time-series.md)

---

# 9. Merging & Joining

## Table of Contents
- [Concatenation](#concatenation)
- [Merge (SQL-style Joins)](#merge-sql-style-joins)
- [Join Types Explained](#join-types-explained)
- [Join Method](#join-method)
- [Internal Working](#internal-working)
- [Traditional vs Pandas Way](#traditional-vs-pandas-way)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Concatenation

### Basic Concat (Stacking)

```python
import pandas as pd

df1 = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
df2 = pd.DataFrame({"Name": ["Charlie", "Diana"], "Age": [35, 28]})

# Stack vertically (default axis=0)
result = pd.concat([df1, df2])
print(result)
#       Name  Age
# 0    Alice   25
# 1      Bob   30
# 0  Charlie   35  ← Notice: index repeats!
# 1    Diana   28

# Fix index
result = pd.concat([df1, df2], ignore_index=True)
print(result)
#       Name  Age
# 0    Alice   25
# 1      Bob   30
# 2  Charlie   35  ← Clean index
# 3    Diana   28
```

### Stack Horizontally

```python
df_names = pd.DataFrame({"Name": ["Alice", "Bob"]})
df_ages = pd.DataFrame({"Age": [25, 30]})

# Stack side by side
result = pd.concat([df_names, df_ages], axis=1)
print(result)
#     Name  Age
# 0  Alice   25
# 1    Bob   30
```

### Handling Unequal Columns

```python
df1 = pd.DataFrame({"Name": ["Alice"], "Age": [25]})
df2 = pd.DataFrame({"Name": ["Bob"], "Salary": [60000]})

# outer join (default) - keeps all columns, fills NaN
result = pd.concat([df1, df2], ignore_index=True)
print(result)
#     Name   Age    Salary
# 0  Alice  25.0       NaN
# 1    Bob   NaN  60000.0

# inner join - keeps only common columns
result = pd.concat([df1, df2], join="inner", ignore_index=True)
print(result)
#     Name
# 0  Alice
# 1    Bob
```

---

## Merge (SQL-style Joins)

### Basic Merge

```python
employees = pd.DataFrame({
    "EmpID": [1, 2, 3, 4],
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "DeptID": [101, 102, 101, 103]
})

departments = pd.DataFrame({
    "DeptID": [101, 102, 104],
    "DeptName": ["IT", "HR", "Finance"]
})

# Inner merge (default)
result = pd.merge(employees, departments, on="DeptID")
print(result)
#    EmpID     Name  DeptID DeptName
# 0      1    Alice     101       IT
# 1      3  Charlie     101       IT
# 2      2      Bob     102       HR
# Note: Diana (DeptID=103) and Finance (DeptID=104) are excluded
```

### Different Column Names

```python
employees = pd.DataFrame({
    "EmpID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"],
    "dept_id": [101, 102, 101]  # Different name!
})

departments = pd.DataFrame({
    "DeptID": [101, 102],
    "DeptName": ["IT", "HR"]
})

# Merge on different column names
result = pd.merge(employees, departments,
                   left_on="dept_id", right_on="DeptID")
```

---

## Join Types Explained

### Visual Guide

```
Left Table (A)          Right Table (B)
┌────┬───────┐          ┌────┬──────────┐
│ ID │ Name  │          │ ID │ Dept     │
├────┼───────┤          ├────┼──────────┤
│  1 │ Alice │          │  1 │ IT       │
│  2 │ Bob   │          │  3 │ Finance  │
│  3 │ Eve   │          │  4 │ HR       │
└────┴───────┘          └────┴──────────┘
```

### Inner Join

```python
# Only matching rows from BOTH tables
result = pd.merge(A, B, on="ID", how="inner")
# ID=1 (Alice, IT) and ID=3 (Eve, Finance)
```
```
Result:  ┌────┬───────┬──────────┐
         │ ID │ Name  │ Dept     │
         ├────┼───────┼──────────┤
         │  1 │ Alice │ IT       │
         │  3 │ Eve   │ Finance  │
         └────┴───────┴──────────┘
```

### Left Join

```python
# ALL rows from LEFT + matching from RIGHT
result = pd.merge(A, B, on="ID", how="left")
# All from A, NaN where no match in B
```
```
Result:  ┌────┬───────┬──────────┐
         │ ID │ Name  │ Dept     │
         ├────┼───────┼──────────┤
         │  1 │ Alice │ IT       │
         │  2 │ Bob   │ NaN      │  ← No match in B
         │  3 │ Eve   │ Finance  │
         └────┴───────┴──────────┘
```

### Right Join

```python
# ALL rows from RIGHT + matching from LEFT
result = pd.merge(A, B, on="ID", how="right")
```
```
Result:  ┌────┬───────┬──────────┐
         │ ID │ Name  │ Dept     │
         ├────┼───────┼──────────┤
         │  1 │ Alice │ IT       │
         │  3 │ Eve   │ Finance  │
         │  4 │ NaN   │ HR       │  ← No match in A
         └────┴───────┴──────────┘
```

### Outer (Full) Join

```python
# ALL rows from BOTH tables
result = pd.merge(A, B, on="ID", how="outer")
```
```
Result:  ┌────┬───────┬──────────┐
         │ ID │ Name  │ Dept     │
         ├────┼───────┼──────────┤
         │  1 │ Alice │ IT       │
         │  2 │ Bob   │ NaN      │  ← Only in A
         │  3 │ Eve   │ Finance  │
         │  4 │ NaN   │ HR       │  ← Only in B
         └────┴───────┴──────────┘
```

### Summary

```
┌───────────┬────────────────────────────────────┐
│ Join Type │ What it keeps                       │
├───────────┼────────────────────────────────────┤
│ inner     │ Only matching rows from both       │
│ left      │ All left + matching right          │
│ right     │ All right + matching left          │
│ outer     │ Everything from both               │
└───────────┴────────────────────────────────────┘
```

---

## Join Method

### Index-based Join

```python
# .join() merges on index (not column)
df1 = pd.DataFrame({"A": [1, 2, 3]}, index=["a", "b", "c"])
df2 = pd.DataFrame({"B": [4, 5, 6]}, index=["a", "b", "d"])

# Left join by default
result = df1.join(df2)
print(result)
#    A    B
# a  1  4.0
# b  2  5.0
# c  3  NaN  ← No "c" in df2

# Different join types
result = df1.join(df2, how="inner")   # Only matching
result = df1.join(df2, how="outer")   # All indices
```

### Merge vs Join

```
┌──────────────┬────────────────────────────────┐
│   merge()    │   join()                       │
├──────────────┼────────────────────────────────┤
│ Column-based │ Index-based                    │
│ pd.merge()   │ df.join()                      │
│ More flexible│ Simpler syntax                 │
│ Explicit key │ Uses index by default          │
└──────────────┴────────────────────────────────┘
```

---

## Multiple Merges

```python
# Chain merges for 3+ tables
employees = pd.DataFrame({
    "EmpID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"],
    "DeptID": [101, 102, 101]
})

departments = pd.DataFrame({
    "DeptID": [101, 102],
    "DeptName": ["IT", "HR"]
})

salaries = pd.DataFrame({
    "EmpID": [1, 2, 3],
    "Salary": [50000, 60000, 70000]
})

# Chain merges
result = (employees
    .merge(departments, on="DeptID")
    .merge(salaries, on="EmpID")
)
print(result)
#    EmpID     Name  DeptID DeptName  Salary
# 0      1    Alice     101       IT   50000
# 1      3  Charlie     101       IT   70000
# 2      2      Bob     102       HR   60000
```

---

## Internal Working

### How Merge Works

```
Step 1: Hash the key column of right DataFrame
        {101: [row0], 102: [row1], 104: [row2]}

Step 2: For each row in left DataFrame:
        Look up key in hash table
        If found → pair rows
        If not found → depends on join type

Step 3: Combine matched rows into result

Time complexity: O(n + m) average case
(n = left rows, m = right rows)
```

---

## Traditional vs Pandas Way

### Joining Two Tables

```python
# ======= Traditional Python =======
employees = [
    {"id": 1, "name": "Alice", "dept_id": 101},
    {"id": 2, "name": "Bob", "dept_id": 102},
]
departments = [
    {"dept_id": 101, "dept_name": "IT"},
    {"dept_id": 102, "dept_name": "HR"},
]

# Manual join
dept_lookup = {d["dept_id"]: d["dept_name"] for d in departments}
for emp in employees:
    emp["dept_name"] = dept_lookup.get(emp["dept_id"], "Unknown")

# ======= Pandas Way =======
result = pd.merge(emp_df, dept_df, on="dept_id")  # One line!
```

---

## Common Mistakes

### 1. Duplicate Rows After Merge

```python
# If merge key is not unique, you get a Cartesian product!
df1 = pd.DataFrame({"key": ["A", "A"], "val1": [1, 2]})
df2 = pd.DataFrame({"key": ["A", "A"], "val2": [3, 4]})

result = pd.merge(df1, df2, on="key")
print(result)  # 4 rows! (2 × 2)
#   key  val1  val2
# 0   A     1     3
# 1   A     1     4
# 2   A     2     3
# 3   A     2     4

# ✅ Check for duplicates BEFORE merging
print(df1["key"].duplicated().any())  # True → problem!
```

### 2. Unnamed Duplicate Columns

```python
# Both DataFrames have a "Name" column
df1 = pd.DataFrame({"ID": [1], "Name": ["Alice"]})
df2 = pd.DataFrame({"ID": [1], "Name": ["IT"]})

result = pd.merge(df1, df2, on="ID")
print(result.columns)  # ['ID', 'Name_x', 'Name_y'] ← Ugly!

# ✅ Use suffixes
result = pd.merge(df1, df2, on="ID", suffixes=("_emp", "_dept"))
```

### 3. Forgetting ignore_index in Concat

```python
# ❌ WRONG - Duplicate indices
result = pd.concat([df1, df2])
# Index: [0, 1, 0, 1]  ← Confusing!

# ✅ CORRECT
result = pd.concat([df1, df2], ignore_index=True)
# Index: [0, 1, 2, 3]  ← Clean
```

---

## Best Practices

### 1. Validate Before Merging
```python
# ✅ Check key uniqueness
print(f"Left duplicates: {df1['key'].duplicated().any()}")
print(f"Right duplicates: {df2['key'].duplicated().any()}")
```

### 2. Use validate Parameter
```python
# ✅ Catch unexpected many-to-many
result = pd.merge(df1, df2, on="key", validate="one_to_one")
# Raises error if not 1:1
```

### 3. Use indicator for Debugging
```python
result = pd.merge(df1, df2, on="key", how="outer", indicator=True)
print(result["_merge"].value_counts())
# both          3
# left_only     1
# right_only    2
```

---

## Quick Reference

```python
# Concatenation
pd.concat([df1, df2])                      # Stack vertically
pd.concat([df1, df2], axis=1)             # Stack horizontally
pd.concat([df1, df2], ignore_index=True)  # Reset index

# Merge (SQL-style)
pd.merge(left, right, on="key")              # Inner join
pd.merge(left, right, on="key", how="left")  # Left join
pd.merge(left, right, on="key", how="right") # Right join
pd.merge(left, right, on="key", how="outer") # Full join
pd.merge(left, right, left_on="a", right_on="b")  # Different names

# Join (index-based)
df1.join(df2)                              # Left join on index
df1.join(df2, how="inner")                 # Inner join on index

# Validation
pd.merge(df1, df2, validate="one_to_one")  # Check 1:1
pd.merge(df1, df2, indicator=True)         # Show merge source
```

---

[← Previous: Grouping & Aggregation](8-grouping-aggregation.md) | [🏠 Home](README.md) | [Next: Time Series →](10-time-series.md)
