# Operator Overloading in Python

## What is Operator Overloading?

**Operator overloading** allows you to define custom behavior for operators (like `+`, `-`, `*`, `==`, etc.) when they are used with objects of your custom classes. It enables your objects to work with Python's built-in operators in a natural and intuitive way.

### Simple Example

```python
# Built-in behavior
print(5 + 3)        # 8 (integer addition)
print("Hello" + " World")  # Hello World (string concatenation)

# Custom behavior
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(2, 3)
v2 = Vector(4, 5)
v3 = v1 + v2  # Custom addition!
```

---

## How It Works

When you use an operator with an object, Python calls a special **magic method** (dunder method) on that object.

```python
# When you write:
a + b

# Python calls:
a.__add__(b)
```

By defining these magic methods in your class, you control what the operator does.

---

## Types of Operators That Can Be Overloaded

### 1. Arithmetic Operators
### 2. Comparison Operators
### 3. Logical Operators
### 4. Bitwise Operators
### 5. Assignment Operators
### 6. Unary Operators
### 7. Type Conversion Operators

---

## 1. Arithmetic Operators

### Addition: `__add__(self, other)` → `+`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # Calls p1.__add__(p2)
print(p3)  # Point(4, 6)
```

### Subtraction: `__sub__(self, other)` → `-`

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(10, 8)
v2 = Vector(3, 2)
v3 = v1 - v2
print(v3)  # Vector(7, 6)
```

### Multiplication: `__mul__(self, other)` → `*`

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, scalar):
        """Multiply vector by scalar"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(2, 3)
v2 = v * 5
print(v2)  # Vector(10, 15)
```

### Division: `__truediv__(self, other)` → `/`

```python
class Fraction:
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator
    
    def __truediv__(self, other):
        return Fraction(
            self.num * other.den,
            self.den * other.num
        )
    
    def __repr__(self):
        return f"{self.num}/{self.den}"

f1 = Fraction(1, 2)
f2 = Fraction(3, 4)
f3 = f1 / f2
print(f3)  # 4/6
```

### Floor Division: `__floordiv__(self, other)` → `//`

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __floordiv__(self, other):
        return Number(self.value // other.value)
    
    def __repr__(self):
        return f"Number({self.value})"

n1 = Number(10)
n2 = Number(3)
n3 = n1 // n2
print(n3)  # Number(3)
```

### Modulo: `__mod__(self, other)` → `%`

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __mod__(self, other):
        return Number(self.value % other.value)
    
    def __repr__(self):
        return f"Number({self.value})"

n1 = Number(10)
n2 = Number(3)
n3 = n1 % n2
print(n3)  # Number(1)
```

### Power: `__pow__(self, other)` → `**`

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __pow__(self, other):
        return Number(self.value ** other.value)
    
    def __repr__(self):
        return f"Number({self.value})"

n1 = Number(2)
n2 = Number(3)
n3 = n1 ** n2
print(n3)  # Number(8)
```

### Complete Arithmetic Example

```python
class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
    
    def __add__(self, other):
        return ComplexNumber(
            self.real + other.real,
            self.imag + other.imag
        )
    
    def __sub__(self, other):
        return ComplexNumber(
            self.real - other.real,
            self.imag - other.imag
        )
    
    def __mul__(self, other):
        # (a + bi) * (c + di) = (ac - bd) + (ad + bc)i
        return ComplexNumber(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )
    
    def __repr__(self):
        return f"{self.real} + {self.imag}i"

c1 = ComplexNumber(3, 2)
c2 = ComplexNumber(1, 7)

print(c1 + c2)  # 4 + 9i
print(c1 - c2)  # 2 + -5i
print(c1 * c2)  # -11 + 23i
```

---

## 2. Comparison Operators

### Equal: `__eq__(self, other)` → `==`

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age
    
    def __repr__(self):
        return f"Person('{self.name}', {self.age})"

p1 = Person("Alice", 30)
p2 = Person("Alice", 30)
p3 = Person("Bob", 25)

print(p1 == p2)  # True
print(p1 == p3)  # False
```

### Not Equal: `__ne__(self, other)` → `!=`

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def __ne__(self, other):
        return self.price != other.price

p1 = Product("Laptop", 1000)
p2 = Product("Phone", 500)

print(p1 != p2)  # True
```

### Less Than: `__lt__(self, other)` → `<`

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __lt__(self, other):
        return self.grade < other.grade
    
    def __repr__(self):
        return f"Student('{self.name}', {self.grade})"

s1 = Student("Alice", 85)
s2 = Student("Bob", 90)

print(s1 < s2)  # True
print(sorted([s2, s1]))  # [Student('Alice', 85), Student('Bob', 90)]
```

### Less Than or Equal: `__le__(self, other)` → `<=`

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __le__(self, other):
        return self.celsius <= other.celsius

t1 = Temperature(20)
t2 = Temperature(25)

print(t1 <= t2)  # True
```

### Greater Than: `__gt__(self, other)` → `>`

```python
class Score:
    def __init__(self, value):
        self.value = value
    
    def __gt__(self, other):
        return self.value > other.value

s1 = Score(100)
s2 = Score(85)

print(s1 > s2)  # True
```

### Greater Than or Equal: `__ge__(self, other)` → `>=`

```python
class Age:
    def __init__(self, years):
        self.years = years
    
    def __ge__(self, other):
        return self.years >= other.years

a1 = Age(30)
a2 = Age(25)

print(a1 >= a2)  # True
```

### Complete Comparison Example

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @property
    def area(self):
        return self.width * self.height
    
    def __eq__(self, other):
        return self.area == other.area
    
    def __lt__(self, other):
        return self.area < other.area
    
    def __le__(self, other):
        return self.area <= other.area
    
    def __gt__(self, other):
        return self.area > other.area
    
    def __ge__(self, other):
        return self.area >= other.area
    
    def __repr__(self):
        return f"Rectangle({self.width}x{self.height}, area={self.area})"

r1 = Rectangle(5, 4)   # area = 20
r2 = Rectangle(10, 2)  # area = 20
r3 = Rectangle(3, 5)   # area = 15

print(r1 == r2)  # True (same area)
print(r1 > r3)   # True (20 > 15)
print(r3 < r1)   # True (15 < 20)
```

---

## 3. Augmented Assignment Operators

### In-Place Addition: `__iadd__(self, other)` → `+=`

```python
class Counter:
    def __init__(self, value=0):
        self.value = value
    
    def __iadd__(self, other):
        self.value += other
        return self
    
    def __repr__(self):
        return f"Counter({self.value})"

counter = Counter(10)
counter += 5  # Calls counter.__iadd__(5)
print(counter)  # Counter(15)
```

### Other Augmented Operators

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __iadd__(self, other):      # +=
        self.value += other
        return self
    
    def __isub__(self, other):      # -=
        self.value -= other
        return self
    
    def __imul__(self, other):      # *=
        self.value *= other
        return self
    
    def __itruediv__(self, other):  # /=
        self.value /= other
        return self
    
    def __repr__(self):
        return f"Number({self.value})"

n = Number(10)
n += 5   # 15
n -= 3   # 12
n *= 2   # 24
n /= 4   # 6.0
print(n)  # Number(6.0)
```

---

## 4. Unary Operators

### Negation: `__neg__(self)` → `-obj`

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(3, 4)
v_neg = -v
print(v_neg)  # Vector(-3, -4)
```

### Positive: `__pos__(self)` → `+obj`

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __pos__(self):
        return Number(abs(self.value))
    
    def __repr__(self):
        return f"Number({self.value})"

n = Number(-5)
n_pos = +n
print(n_pos)  # Number(5)
```

### Absolute Value: `__abs__(self)` → `abs(obj)`

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(3, 4)
print(abs(v))  # 5.0 (magnitude)
```

### Inversion: `__invert__(self)` → `~obj`

```python
class BinaryNumber:
    def __init__(self, value):
        self.value = value
    
    def __invert__(self):
        return BinaryNumber(~self.value)
    
    def __repr__(self):
        return f"BinaryNumber({self.value})"

b = BinaryNumber(5)  # 0101 in binary
print(~b)  # BinaryNumber(-6) - bitwise NOT
```

---

## 5. Bitwise Operators

### AND: `__and__(self, other)` → `&`

```python
class BitSet:
    def __init__(self, value):
        self.value = value
    
    def __and__(self, other):
        return BitSet(self.value & other.value)
    
    def __repr__(self):
        return f"BitSet({self.value})"

b1 = BitSet(12)  # 1100
b2 = BitSet(10)  # 1010
b3 = b1 & b2     # 1000 = 8
print(b3)  # BitSet(8)
```

### OR: `__or__(self, other)` → `|`

```python
class BitSet:
    def __init__(self, value):
        self.value = value
    
    def __or__(self, other):
        return BitSet(self.value | other.value)
    
    def __repr__(self):
        return f"BitSet({self.value})"

b1 = BitSet(12)  # 1100
b2 = BitSet(10)  # 1010
b3 = b1 | b2     # 1110 = 14
print(b3)  # BitSet(14)
```

### XOR: `__xor__(self, other)` → `^`

```python
class BitSet:
    def __init__(self, value):
        self.value = value
    
    def __xor__(self, other):
        return BitSet(self.value ^ other.value)
    
    def __repr__(self):
        return f"BitSet({self.value})"

b1 = BitSet(12)  # 1100
b2 = BitSet(10)  # 1010
b3 = b1 ^ b2     # 0110 = 6
print(b3)  # BitSet(6)
```

### Left Shift: `__lshift__(self, other)` → `<<`

```python
class BitNumber:
    def __init__(self, value):
        self.value = value
    
    def __lshift__(self, other):
        return BitNumber(self.value << other)
    
    def __repr__(self):
        return f"BitNumber({self.value})"

b = BitNumber(5)  # 0101
b2 = b << 2       # 10100 = 20
print(b2)  # BitNumber(20)
```

### Right Shift: `__rshift__(self, other)` → `>>`

```python
class BitNumber:
    def __init__(self, value):
        self.value = value
    
    def __rshift__(self, other):
        return BitNumber(self.value >> other)
    
    def __repr__(self):
        return f"BitNumber({self.value})"

b = BitNumber(20)  # 10100
b2 = b >> 2        # 00101 = 5
print(b2)  # BitNumber(5)
```

---

## 6. Reverse/Reflected Operators

When the left operand doesn't support the operation, Python tries the reverse operation on the right operand.

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, scalar):
        """Vector * scalar"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        """scalar * Vector (reverse)"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(2, 3)
v1 = v * 5    # Calls v.__mul__(5)
v2 = 5 * v    # Calls v.__rmul__(5)

print(v1)  # Vector(10, 15)
print(v2)  # Vector(10, 15)
```

### Common Reverse Operators

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __radd__(self, other):      # other + self
        return Number(other + self.value)
    
    def __rsub__(self, other):      # other - self
        return Number(other - self.value)
    
    def __rmul__(self, other):      # other * self
        return Number(other * self.value)
    
    def __repr__(self):
        return f"Number({self.value})"

n = Number(10)
print(5 + n)  # Number(15) - calls n.__radd__(5)
print(20 - n)  # Number(10) - calls n.__rsub__(20)
print(3 * n)  # Number(30) - calls n.__rmul__(3)
```

---

## 7. Type Conversion Operators

### Integer: `__int__(self)` → `int(obj)`

```python
class Fraction:
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator
    
    def __int__(self):
        return self.num // self.den
    
    def __repr__(self):
        return f"{self.num}/{self.den}"

f = Fraction(7, 2)
print(int(f))  # 3
```

### Float: `__float__(self)` → `float(obj)`

```python
class Fraction:
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator
    
    def __float__(self):
        return self.num / self.den
    
    def __repr__(self):
        return f"{self.num}/{self.den}"

f = Fraction(3, 4)
print(float(f))  # 0.75
```

### Boolean: `__bool__(self)` → `bool(obj)`

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def __bool__(self):
        return self.balance > 0

account1 = BankAccount(100)
account2 = BankAccount(0)

print(bool(account1))  # True
print(bool(account2))  # False

if account1:
    print("Account has money")  # This prints
```

### String: `__str__(self)` → `str(obj)`

Already covered in magic methods, but included for completeness.

---

## Complete Real-World Example: Money Class

```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency
    
    # Arithmetic operators
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, scalar):
        return Money(self.amount * scalar, self.currency)
    
    def __truediv__(self, scalar):
        return Money(self.amount / scalar, self.currency)
    
    # Comparison operators
    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency
    
    def __lt__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.amount < other.amount
    
    def __le__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.amount <= other.amount
    
    # Unary operators
    def __neg__(self):
        return Money(-self.amount, self.currency)
    
    def __abs__(self):
        return Money(abs(self.amount), self.currency)
    
    # Type conversion
    def __float__(self):
        return float(self.amount)
    
    def __int__(self):
        return int(self.amount)
    
    def __bool__(self):
        return self.amount != 0
    
    # Representation
    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"
    
    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"

# Usage
m1 = Money(100, "USD")
m2 = Money(50, "USD")

print(m1 + m2)  # USD 150.00
print(m1 - m2)  # USD 50.00
print(m1 * 2)   # USD 200.00
print(m1 / 4)   # USD 25.00

print(m1 > m2)  # True
print(m1 == Money(100, "USD"))  # True

print(-m1)      # USD -100.00
print(abs(Money(-50, "USD")))  # USD 50.00

print(float(m1))  # 100.0
print(int(m1))    # 100
```

---

## Summary: All Overloadable Operators

| Category | Operator | Method | Example |
|----------|----------|--------|---------|
| **Arithmetic** | `+` | `__add__` | `a + b` |
| | `-` | `__sub__` | `a - b` |
| | `*` | `__mul__` | `a * b` |
| | `/` | `__truediv__` | `a / b` |
| | `//` | `__floordiv__` | `a // b` |
| | `%` | `__mod__` | `a % b` |
| | `**` | `__pow__` | `a ** b` |
| **Comparison** | `==` | `__eq__` | `a == b` |
| | `!=` | `__ne__` | `a != b` |
| | `<` | `__lt__` | `a < b` |
| | `<=` | `__le__` | `a <= b` |
| | `>` | `__gt__` | `a > b` |
| | `>=` | `__ge__` | `a >= b` |
| **Augmented** | `+=` | `__iadd__` | `a += b` |
| | `-=` | `__isub__` | `a -= b` |
| | `*=` | `__imul__` | `a *= b` |
| | `/=` | `__itruediv__` | `a /= b` |
| **Unary** | `-` | `__neg__` | `-a` |
| | `+` | `__pos__` | `+a` |
| | `~` | `__invert__` | `~a` |
| | `abs()` | `__abs__` | `abs(a)` |
| **Bitwise** | `&` | `__and__` | `a & b` |
| | `\|` | `__or__` | `a \| b` |
| | `^` | `__xor__` | `a ^ b` |
| | `<<` | `__lshift__` | `a << b` |
| | `>>` | `__rshift__` | `a >> b` |
| **Type Conversion** | `int()` | `__int__` | `int(a)` |
| | `float()` | `__float__` | `float(a)` |
| | `bool()` | `__bool__` | `bool(a)` |
| | `str()` | `__str__` | `str(a)` |

Operator overloading makes your custom classes behave like built-in Python types!
