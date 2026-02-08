# Magic Methods in Python (Dunder Methods)

## What are Magic Methods?

**Magic methods** (also called **dunder methods** - "double underscore") are special methods in Python that have double underscores before and after their names (e.g., `__init__`, `__str__`). They allow you to define how objects of your class behave with built-in Python operations.

### Why "Magic"?

They're called "magic" because they're automatically invoked by Python in response to certain operations, without you explicitly calling them.

```python
# You write:
obj1 + obj2

# Python automatically calls:
obj1.__add__(obj2)
```

---

## Categories of Magic Methods

### 1. Object Initialization and Representation
### 2. Operator Overloading
### 3. Comparison Operators
### 4. Container/Sequence Methods
### 5. Attribute Access
### 6. Callable Objects
### 7. Context Managers

---

## 1. Object Initialization and Representation

### `__init__(self, ...)` - Constructor/Initializer

Called when creating a new object.

```python
class Person:
    def __init__(self, name, age):
        print("__init__ called")
        self.name = name
        self.age = age

person = Person("Alice", 30)  # __init__ called
```

### `__new__(cls, ...)` - Constructor

Called before `__init__` to create the object.

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating new instance")
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()  # Creating new instance
s2 = Singleton()  # Uses existing instance
print(s1 is s2)   # True
```

### `__str__(self)` - String Representation (User-Friendly)

Called by `str()` and `print()`.

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    def __str__(self):
        return f"'{self.title}' by {self.author}"

book = Book("1984", "George Orwell")
print(book)  # '1984' by George Orwell
print(str(book))  # '1984' by George Orwell
```

### `__repr__(self)` - String Representation (Developer-Friendly)

Called by `repr()` and in interactive shell. Should be unambiguous.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print(str(p))   # (3, 4)
print(repr(p))  # Point(3, 4)
print(p)        # (3, 4) - uses __str__
```

### `__del__(self)` - Destructor

Called when object is about to be destroyed.

```python
class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        print(f"Opening {filename}")
    
    def __del__(self):
        print(f"Closing {self.filename}")

handler = FileHandler("data.txt")  # Opening data.txt
del handler  # Closing data.txt
```

---

## 2. Operator Overloading (Arithmetic)

### `__add__(self, other)` - Addition (+)

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(4, 5)
v3 = v1 + v2  # Calls v1.__add__(v2)
print(v3)  # Vector(6, 8)
```

### `__sub__(self, other)` - Subtraction (-)

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(5, 7)
v2 = Vector(2, 3)
v3 = v1 - v2  # Calls v1.__sub__(v2)
print(v3)  # Vector(3, 4)
```

### `__mul__(self, other)` - Multiplication (*)

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(2, 3)
v2 = v * 3  # Calls v.__mul__(3)
print(v2)  # Vector(6, 9)
```

### Other Arithmetic Operators

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __truediv__(self, other):  # Division (/)
        return Number(self.value / other.value)
    
    def __floordiv__(self, other):  # Floor division (//)
        return Number(self.value // other.value)
    
    def __mod__(self, other):  # Modulo (%)
        return Number(self.value % other.value)
    
    def __pow__(self, other):  # Power (**)
        return Number(self.value ** other.value)
    
    def __repr__(self):
        return f"Number({self.value})"
```

---

## 3. Comparison Operators

### `__eq__(self, other)` - Equal (==)

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

p1 = Person("Alice", 30)
p2 = Person("Alice", 30)
p3 = Person("Bob", 25)

print(p1 == p2)  # True
print(p1 == p3)  # False
```

### `__lt__(self, other)` - Less Than (<)

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __lt__(self, other):
        return self.grade < other.grade
    
    def __repr__(self):
        return f"Student({self.name}, {self.grade})"

s1 = Student("Alice", 85)
s2 = Student("Bob", 90)

print(s1 < s2)  # True
print(sorted([s2, s1]))  # [Student(Alice, 85), Student(Bob, 90)]
```

### Other Comparison Operators

```python
class Number:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):  # ==
        return self.value == other.value
    
    def __ne__(self, other):  # !=
        return self.value != other.value
    
    def __lt__(self, other):  # <
        return self.value < other.value
    
    def __le__(self, other):  # <=
        return self.value <= other.value
    
    def __gt__(self, other):  # >
        return self.value > other.value
    
    def __ge__(self, other):  # >=
        return self.value >= other.value
```

---

## 4. Container/Sequence Methods

### `__len__(self)` - Length

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def add_song(self, song):
        self.songs.append(song)
    
    def __len__(self):
        return len(self.songs)

playlist = Playlist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")
print(len(playlist))  # 2
```

### `__getitem__(self, key)` - Indexing/Slicing

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def add_song(self, song):
        self.songs.append(song)
    
    def __getitem__(self, index):
        return self.songs[index]
    
    def __len__(self):
        return len(self.songs)

playlist = Playlist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")
playlist.add_song("Song 3")

print(playlist[0])    # Song 1
print(playlist[1:3])  # ['Song 2', 'Song 3']

# Enables iteration
for song in playlist:
    print(song)
```

### `__setitem__(self, key, value)` - Assignment

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __getitem__(self, index):
        return self.songs[index]
    
    def __setitem__(self, index, value):
        self.songs[index] = value
    
    def __len__(self):
        return len(self.songs)

playlist = Playlist()
playlist.songs = ["Song 1", "Song 2", "Song 3"]
playlist[1] = "New Song"  # Calls __setitem__
print(playlist[1])  # New Song
```

### `__delitem__(self, key)` - Deletion

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def __getitem__(self, index):
        return self.songs[index]
    
    def __delitem__(self, index):
        del self.songs[index]

playlist = Playlist()
playlist.songs = ["Song 1", "Song 2", "Song 3"]
del playlist[1]  # Calls __delitem__
print(playlist.songs)  # ['Song 1', 'Song 3']
```

### `__contains__(self, item)` - Membership (in)

```python
class Playlist:
    def __init__(self):
        self.songs = []
    
    def add_song(self, song):
        self.songs.append(song)
    
    def __contains__(self, song):
        return song in self.songs

playlist = Playlist()
playlist.add_song("Song 1")
playlist.add_song("Song 2")

print("Song 1" in playlist)  # True
print("Song 3" in playlist)  # False
```

---

## 5. Attribute Access

### `__getattr__(self, name)` - Get Attribute

Called when attribute is not found.

```python
class DynamicObject:
    def __init__(self):
        self.existing = "I exist"
    
    def __getattr__(self, name):
        return f"Attribute '{name}' not found, returning default"

obj = DynamicObject()
print(obj.existing)  # I exist
print(obj.missing)   # Attribute 'missing' not found, returning default
```

### `__setattr__(self, name, value)` - Set Attribute

Called when setting an attribute.

```python
class ValidatedPerson:
    def __setattr__(self, name, value):
        if name == "age":
            if not isinstance(value, int) or value < 0:
                raise ValueError("Age must be a positive integer")
        super().__setattr__(name, value)

person = ValidatedPerson()
person.name = "Alice"  # OK
person.age = 30        # OK
# person.age = -5      # ValueError
```

### `__delattr__(self, name)` - Delete Attribute

```python
class ProtectedObject:
    def __init__(self):
        self.public = "Can delete"
        self._protected = "Cannot delete"
    
    def __delattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"Cannot delete protected attribute '{name}'")
        super().__delattr__(name)

obj = ProtectedObject()
del obj.public  # OK
# del obj._protected  # AttributeError
```

---

## 6. Callable Objects

### `__call__(self, ...)` - Make Object Callable

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
triple = Multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# Object acts like a function!
print(callable(double))  # True
```

### Practical Example: Counter

```python
class Counter:
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

---

## 7. Context Managers

### `__enter__(self)` and `__exit__(self, ...)` - With Statement

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions

# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello, World!")
# File automatically closed after with block
```

### Database Connection Example

```python
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.db_name}")
        self.connection = f"Connection to {self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Disconnecting from {self.db_name}")
        self.connection = None
        return False

with DatabaseConnection("mydb") as conn:
    print(f"Using {conn}")
```

---

## 8. Iterator Protocol

### `__iter__(self)` and `__next__(self)` - Iteration

```python
class Countdown:
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# Usage
for num in Countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

### Custom Range

```python
class MyRange:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        self.current += 1
        return self.current - 1

for i in MyRange(0, 5):
    print(i)  # 0, 1, 2, 3, 4
```

---

## Complete Example: Custom Class with Multiple Magic Methods

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []
    
    def __str__(self):
        return f"Account({self.owner}: ${self.balance})"
    
    def __repr__(self):
        return f"BankAccount('{self.owner}', {self.balance})"
    
    def __len__(self):
        return len(self.transactions)
    
    def __getitem__(self, index):
        return self.transactions[index]
    
    def __add__(self, amount):
        """Deposit money"""
        self.balance += amount
        self.transactions.append(f"+${amount}")
        return self
    
    def __sub__(self, amount):
        """Withdraw money"""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(f"-${amount}")
        return self
    
    def __eq__(self, other):
        return self.balance == other.balance
    
    def __lt__(self, other):
        return self.balance < other.balance
    
    def __bool__(self):
        return self.balance > 0
    
    def __call__(self):
        return f"{self.owner} has ${self.balance}"

# Usage
account = BankAccount("Alice", 1000)
print(account)  # Account(Alice: $1000)

account + 500  # Deposit
account - 200  # Withdraw

print(len(account))  # 2 transactions
print(account[0])    # +$500

print(account())  # Alice has $1300

account2 = BankAccount("Bob", 1300)
print(account == account2)  # True
print(account < account2)   # False
```

---

## Summary of Common Magic Methods

| Category | Method | Purpose |
|----------|--------|---------|
| **Initialization** | `__init__` | Initialize object |
| | `__new__` | Create object |
| | `__del__` | Destructor |
| **Representation** | `__str__` | User-friendly string |
| | `__repr__` | Developer-friendly string |
| **Arithmetic** | `__add__` | Addition (+) |
| | `__sub__` | Subtraction (-) |
| | `__mul__` | Multiplication (*) |
| | `__truediv__` | Division (/) |
| **Comparison** | `__eq__` | Equal (==) |
| | `__lt__` | Less than (<) |
| | `__gt__` | Greater than (>) |
| **Container** | `__len__` | Length |
| | `__getitem__` | Indexing [] |
| | `__setitem__` | Assignment [] |
| | `__contains__` | Membership (in) |
| **Callable** | `__call__` | Make callable |
| **Context Manager** | `__enter__` | Enter with block |
| | `__exit__` | Exit with block |
| **Iterator** | `__iter__` | Return iterator |
| | `__next__` | Get next item |

Magic methods make your custom classes behave like built-in Python types!
