# 🐼 Pandas Learning Guide

## Complete Guide: Beginner to Advanced

> **Prerequisites**: Python basics, NumPy fundamentals
> **Built on**: NumPy arrays (see [NumPy Guide](../Numpy/README.md))

---

## 📚 Table of Contents

### 🟢 Beginner
| # | Topic | Description |
|---|-------|-------------|
| 1 | [Introduction to Pandas](1-introduction.md) | What is Pandas, installation, why Pandas over Excel/Python |
| 2 | [Series](2-series.md) | 1D labeled array - creation, indexing, operations |
| 3 | [DataFrames](3-dataframes.md) | 2D labeled data structure - creation, properties, basic ops |

### 🟡 Intermediate
| # | Topic | Description |
|---|-------|-------------|
| 4 | [Data Loading & Export](4-data-loading.md) | Reading/writing CSV, Excel, JSON, SQL |
| 5 | [Indexing & Selection](5-indexing-selection.md) | loc, iloc, boolean filtering, query |
| 6 | [Data Cleaning](6-data-cleaning.md) | Missing values, duplicates, type conversion |
| 7 | [Data Transformation](7-data-transformation.md) | apply, map, lambda, string operations |

### 🔴 Advanced
| # | Topic | Description |
|---|-------|-------------|
| 8 | [Grouping & Aggregation](8-grouping-aggregation.md) | groupby, pivot tables, crosstab |
| 9 | [Merging & Joining](9-merging-joining.md) | merge, join, concat, compare |
| 10 | [Time Series](10-time-series.md) | DateTime, resampling, rolling windows |
| 11 | [Advanced Topics & Best Practices](11-advanced-topics.md) | Performance, memory, vectorization, AI/ML prep |

---

## 🔗 How Pandas Relates to Your AI/ML Journey

```
Python Basics → NumPy (arrays) → Pandas (data) → Scikit-learn (ML)
                                       ↓
                              LangChain / LangGraph
```

---

## 🧠 Key Concept

```
NumPy  = Numerical computation on arrays
Pandas = Data manipulation on labeled, tabular data
         (built ON TOP of NumPy)
```

---

## Quick Start

```python
import pandas as pd
import numpy as np

# Create a DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Salary': [50000, 60000, 70000]
})

print(df)
#       Name  Age  Salary
# 0    Alice   25   50000
# 1      Bob   30   60000
# 2  Charlie   35   70000
```

---

Happy Learning! 🚀
