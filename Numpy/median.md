[🏠 Home](README.md)

---

# Mathematical Formula for Median

## Step 1: Sort the array in ascending order

## Step 2: Apply formula based on odd/even count

---

### Case 1: Odd number of elements (n is odd)

```
Median = x[(n+1)/2]
```

Pick the **middle element** directly.

```python
arr = [3, 1, 5, 2, 4]       # n = 5 (odd)
sorted = [1, 2, 3, 4, 5]    # Sort it
#              ↑
#         Middle = (5+1)/2 = 3rd element
# Median = 3
```

---

### Case 2: Even number of elements (n is even)

```
Median = (x[n/2] + x[n/2 + 1]) / 2
```

**Average of the two middle elements.**

```python
arr = [3, 1, 5, 2, 4, 6]     # n = 6 (even)
sorted = [1, 2, 3, 4, 5, 6]  # Sort it
#              ↑  ↑
#           3rd  4th element
# Median = (3 + 4) / 2 = 3.5
```

---

## Visual Flow

```
Input Array: [7, 2, 9, 1, 5]
                ↓
Step 1: Sort → [1, 2, 5, 7, 9]
                ↓
Step 2: n = 5 (odd)
                ↓
Step 3: Position = (5+1)/2 = 3
                ↓
Result: Median = 5 (3rd element)
```

---

## In NumPy

```python
import numpy as np

arr = np.array([7, 2, 9, 1, 5])
print(np.median(arr))  # 5.0

arr = np.array([7, 2, 9, 1, 5, 6])
print(np.median(arr))  # 5.5  →  (5+6)/2
```

---

## Why Median Over Mean?

```python
data = np.array([1, 2, 3, 4, 100])

print(np.mean(data))    # 22.0  ← Skewed by outlier (100)
print(np.median(data))  # 3.0   ← Not affected by outlier
```

Median is **robust against outliers**, which makes it useful in AI/ML data preprocessing!

---

[🏠 Home](README.md)
