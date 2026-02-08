# Polymorphism in Python

## What is Polymorphism?

**Polymorphism** (Greek: "many forms") is the ability of different objects to respond to the same method call in different ways. The same interface can be used for different underlying forms (data types).

### Simple Definition

"The same method name behaving differently based on the object that calls it."

---

## Types of Polymorphism in Python

### 1. **Duck Typing** (Python's Natural Polymorphism)

Python's philosophy: "If it walks like a duck and quacks like a duck, it's a duck."

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Duck:
    def speak(self):
        return "Quack!"

# Polymorphic function - works with any object that has speak()
def animal_sound(animal):
    print(animal.speak())

# All work without checking types
dog = Dog()
cat = Cat()
duck = Duck()

animal_sound(dog)   # Woof!
animal_sound(cat)   # Meow!
animal_sound(duck)  # Quack!
```

**Key Point**: Python doesn't care about the object's type, only that it has the required method.

### 2. **Method Overriding** (Inheritance-based Polymorphism)

Child classes override parent methods with their own implementation.

```python
class Animal:
    def speak(self):
        return "Some generic sound"
    
    def move(self):
        return "Moving"

class Dog(Animal):
    def speak(self):  # Override
        return "Woof!"
    
    def move(self):  # Override
        return "Running on four legs"

class Bird(Animal):
    def speak(self):  # Override
        return "Chirp!"
    
    def move(self):  # Override
        return "Flying"

# Polymorphic behavior
animals = [Dog(), Bird(), Animal()]

for animal in animals:
    print(f"Sound: {animal.speak()}, Movement: {animal.move()}")
```

**Output:**
```
Sound: Woof!, Movement: Running on four legs
Sound: Chirp!, Movement: Flying
Sound: Some generic sound, Movement: Moving
```

### 3. **Operator Overloading**

Same operator behaves differently with different types.

```python
# Built-in polymorphism
print(5 + 3)        # 8 (integer addition)
print("5" + "3")    # "53" (string concatenation)
print([1, 2] + [3]) # [1, 2, 3] (list concatenation)

# Custom operator overloading
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(4, 5)
v3 = v1 + v2  # Uses __add__
print(v3)  # Vector(6, 8)
```

### 4. **Function Overloading** (Not Direct, but Achievable)

Python doesn't support traditional function overloading, but you can achieve similar behavior:

```python
class Calculator:
    def add(self, a, b=None, c=None):
        if b is None:
            return a
        elif c is None:
            return a + b
        else:
            return a + b + c

calc = Calculator()
print(calc.add(5))        # 5
print(calc.add(5, 3))     # 8
print(calc.add(5, 3, 2))  # 10
```

---

## Practical Examples

### Example 1: Payment Processing System

```python
class PaymentProcessor:
    def process_payment(self, amount):
        raise NotImplementedError("Subclass must implement")

class CreditCardPayment(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via Credit Card"

class PayPalPayment(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via PayPal"

class CryptoPayment(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via Cryptocurrency"

# Polymorphic function
def checkout(payment_method, amount):
    print(payment_method.process_payment(amount))

# All work with the same interface
checkout(CreditCardPayment(), 100)
checkout(PayPalPayment(), 50)
checkout(CryptoPayment(), 75)
```

**Output:**
```
Processing $100 via Credit Card
Processing $50 via PayPal
Processing $75 via Cryptocurrency
```

### Example 2: File Handler System

```python
class FileHandler:
    def read(self):
        raise NotImplementedError
    
    def write(self, data):
        raise NotImplementedError

class TextFileHandler(FileHandler):
    def read(self):
        return "Reading text file..."
    
    def write(self, data):
        return f"Writing '{data}' to text file"

class JSONFileHandler(FileHandler):
    def read(self):
        return "Reading JSON file..."
    
    def write(self, data):
        return f"Writing '{data}' to JSON file"

class XMLFileHandler(FileHandler):
    def read(self):
        return "Reading XML file..."
    
    def write(self, data):
        return f"Writing '{data}' to XML file"

# Polymorphic processing
def process_file(handler, data):
    print(handler.read())
    print(handler.write(data))

handlers = [TextFileHandler(), JSONFileHandler(), XMLFileHandler()]

for handler in handlers:
    process_file(handler, "Sample data")
    print()
```

### Example 3: Shape Area Calculator

```python
import math

class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

# Polymorphic function
def print_area(shape):
    print(f"{shape.__class__.__name__} area: {shape.area():.2f}")

shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 8)
]

for shape in shapes:
    print_area(shape)
```

**Output:**
```
Circle area: 78.54
Rectangle area: 24.00
Triangle area: 12.00
```

---

## Advantages of Polymorphism

### 1. **Code Reusability**
```python
# One function works with multiple types
def make_sound(animal):
    print(animal.speak())

# Works with any object that has speak()
```

### 2. **Flexibility and Extensibility**
```python
# Easy to add new types without changing existing code
class Cow(Animal):
    def speak(self):
        return "Moo!"

# Existing code still works
make_sound(Cow())
```

### 3. **Simplified Code**
```python
# Instead of:
if isinstance(obj, Dog):
    obj.dog_speak()
elif isinstance(obj, Cat):
    obj.cat_speak()

# Just use:
obj.speak()
```

### 4. **Loose Coupling**
```python
# Code depends on interface, not implementation
def process(handler):
    handler.process()  # Don't care what type handler is
```

---

## Python vs Java Polymorphism

### Key Differences

| Aspect | Java | Python |
|--------|------|--------|
| **Type Checking** | Compile-time (static) | Runtime (dynamic) |
| **Duck Typing** | No | Yes (core feature) |
| **Method Overloading** | Yes (multiple methods same name) | No (use default args) |
| **Operator Overloading** | Limited (only `+` for String) | Full support |
| **Interface/Abstract** | Explicit interfaces required | Duck typing, ABC optional |
| **Polymorphism Style** | Explicit (through inheritance) | Implicit (duck typing) |

### Java Example

```java
// Java - Explicit polymorphism through inheritance
interface Animal {
    void speak();
}

class Dog implements Animal {
    public void speak() {
        System.out.println("Woof!");
    }
}

class Cat implements Animal {
    public void speak() {
        System.out.println("Meow!");
    }
}

// Must use Animal type
public void makeSound(Animal animal) {
    animal.speak();
}

// Usage
makeSound(new Dog());  // Must implement Animal interface
```

### Python Equivalent

```python
# Python - Implicit polymorphism through duck typing
class Dog:
    def speak(self):
        print("Woof!")

class Cat:
    def speak(self):
        print("Meow!")

# No type requirement - just needs speak()
def make_sound(animal):
    animal.speak()

# Usage
make_sound(Dog())  # No interface needed
```

### Python with Explicit Interfaces (Optional)

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        print("Woof!")

# More Java-like, but not required in Python
```

---

## Method Overloading: Java vs Python

### Java (True Overloading)

```java
class Calculator {
    int add(int a, int b) {
        return a + b;
    }
    
    double add(double a, double b) {
        return a + b;
    }
    
    int add(int a, int b, int c) {
        return a + b + c;
    }
}
```

### Python (Simulated with Default Args)

```python
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

calc = Calculator()
print(calc.add(5))        # 5
print(calc.add(5, 3))     # 8
print(calc.add(5, 3, 2))  # 10
```

Or using `*args`:

```python
class Calculator:
    def add(self, *args):
        return sum(args)

calc = Calculator()
print(calc.add(5))           # 5
print(calc.add(5, 3))        # 8
print(calc.add(5, 3, 2, 1))  # 11
```

---

## Common Polymorphic Patterns in Python

### 1. Strategy Pattern

```python
class SortStrategy:
    def sort(self, data):
        raise NotImplementedError

class BubbleSort(SortStrategy):
    def sort(self, data):
        return sorted(data)  # Simplified

class QuickSort(SortStrategy):
    def sort(self, data):
        return sorted(data)  # Simplified

class Sorter:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def sort_data(self, data):
        return self.strategy.sort(data)

# Use different strategies polymorphically
sorter = Sorter(BubbleSort())
print(sorter.sort_data([3, 1, 2]))

sorter = Sorter(QuickSort())
print(sorter.sort_data([3, 1, 2]))
```

### 2. Factory Pattern

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()

# Polymorphic creation
animal = AnimalFactory.create_animal("dog")
print(animal.speak())  # Woof!
```

---

## Dynamic Method Invocation and Parent References

### Can a Parent Class Reference Hold a Child Object?

**Yes!** This is a fundamental aspect of polymorphism in both Python and Java. A parent class reference can hold a child class object, and when methods are called, the **child's implementation** is executed (dynamic method dispatch).

### Python Example: Parent Reference to Child Object

```python
class Animal:
    def speak(self):
        return "Some generic animal sound"
    
    def move(self):
        return "Moving"

class Dog(Animal):
    def speak(self):
        return "Woof!"
    
    def move(self):
        return "Running on four legs"

class Cat(Animal):
    def speak(self):
        return "Meow!"
    
    def move(self):
        return "Sneaking quietly"

# Parent reference holding child objects
animal1: Animal = Dog()  # Animal reference, Dog object
animal2: Animal = Cat()  # Animal reference, Cat object
animal3: Animal = Animal()  # Animal reference, Animal object

# Dynamic method dispatch - calls child's method
print(animal1.speak())  # Woof! (Dog's implementation)
print(animal2.speak())  # Meow! (Cat's implementation)
print(animal3.speak())  # Some generic animal sound (Animal's implementation)

# Check actual types
print(type(animal1))  # <class '__main__.Dog'>
print(type(animal2))  # <class '__main__.Cat'>
print(isinstance(animal1, Animal))  # True
print(isinstance(animal1, Dog))     # True
```

### Detailed Walkthrough

Let's walk through what happens step by step:

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
    
    def start(self):
        return f"{self.brand}: Starting vehicle"
    
    def stop(self):
        return f"{self.brand}: Stopping vehicle"

class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model
    
    def start(self):
        return f"{self.brand} {self.model}: Starting car engine"
    
    def honk(self):
        return "Beep beep!"

class Motorcycle(Vehicle):
    def __init__(self, brand, cc):
        super().__init__(brand)
        self.cc = cc
    
    def start(self):
        return f"{self.brand}: Starting {self.cc}cc motorcycle engine"
    
    def wheelie(self):
        return "Doing a wheelie!"

# Step 1: Create child objects
car = Car("Toyota", "Camry")
bike = Motorcycle("Honda", 600)

# Step 2: Parent references holding child objects
vehicle1: Vehicle = car   # Vehicle reference → Car object
vehicle2: Vehicle = bike  # Vehicle reference → Motorcycle object

print("=" * 60)
print("STEP 1: Calling overridden methods")
print("=" * 60)
print(vehicle1.start())  # Calls Car's start() - dynamic dispatch!
print(vehicle2.start())  # Calls Motorcycle's start() - dynamic dispatch!

print("\n" + "=" * 60)
print("STEP 2: Calling parent methods")
print("=" * 60)
print(vehicle1.stop())  # Calls Vehicle's stop() (not overridden)
print(vehicle2.stop())  # Calls Vehicle's stop() (not overridden)

print("\n" + "=" * 60)
print("STEP 3: Accessing attributes")
print("=" * 60)
print(f"Vehicle 1 brand: {vehicle1.brand}")  # Toyota
print(f"Vehicle 2 brand: {vehicle2.brand}")  # Honda

print("\n" + "=" * 60)
print("STEP 4: Type checking")
print("=" * 60)
print(f"vehicle1 type: {type(vehicle1)}")  # <class '__main__.Car'>
print(f"vehicle2 type: {type(vehicle2)}")  # <class '__main__.Motorcycle'>
print(f"vehicle1 is Vehicle? {isinstance(vehicle1, Vehicle)}")  # True
print(f"vehicle1 is Car? {isinstance(vehicle1, Car)}")          # True

print("\n" + "=" * 60)
print("STEP 5: Child-specific methods")
print("=" * 60)
# These won't work with parent reference (Python doesn't know about them)
# print(vehicle1.honk())    # AttributeError!
# print(vehicle2.wheelie()) # AttributeError!

# Need to cast or use original reference
print(car.honk())   # Beep beep! (using original Car reference)
print(bike.wheelie())  # Doing a wheelie! (using original Motorcycle reference)
```

**Output:**
```
============================================================
STEP 1: Calling overridden methods
============================================================
Toyota Camry: Starting car engine
Honda: Starting 600cc motorcycle engine

============================================================
STEP 2: Calling parent methods
============================================================
Toyota: Stopping vehicle
Honda: Stopping vehicle

============================================================
STEP 3: Accessing attributes
============================================================
Vehicle 1 brand: Toyota
Vehicle 2 brand: Honda

============================================================
STEP 4: Type checking
============================================================
vehicle1 type: <class '__main__.Car'>
vehicle2 type: <class '__main__.Motorcycle'>
vehicle1 is Vehicle? True
vehicle1 is Car? True

============================================================
STEP 5: Child-specific methods
============================================================
Beep beep!
Doing a wheelie!
```

---

### Understanding the Syntax: Type Hints and References

Let's break down this important line of code:

```python
vehicle1: Vehicle = car   # Vehicle reference → Car object
vehicle2: Vehicle = bike  # Vehicle reference → Motorcycle object
```

#### Part 1: Type Annotation

```python
vehicle1: Vehicle
```
- `vehicle1` is the variable name
- `: Vehicle` is a **type hint/annotation** (optional in Python)
- This tells developers (and type checkers like mypy) that `vehicle1` should be of type `Vehicle`
- It's **documentation** - not enforced at runtime

#### Part 2: Assignment

```python
= car
```
- `car` is an object created earlier as `Car("Toyota", "Camry")`
- `Car` is a **child class** that inherits from `Vehicle`
- We're assigning this `Car` object to the variable `vehicle1`

#### The Complete Picture

```python
# Earlier in the code:
car = Car("Toyota", "Camry")      # car is a Car object
bike = Motorcycle("Honda", 600)   # bike is a Motorcycle object

# Now - parent type hint, child object:
vehicle1: Vehicle = car   # Type hint: Vehicle, Actual: Car
vehicle2: Vehicle = bike  # Type hint: Vehicle, Actual: Motorcycle
```

#### Visual Representation

```
┌─────────────────────────────────┐
│  vehicle1 (Variable)            │
│  Type hint: Vehicle             │
│  ↓                               │
│  Points to: Car object          │
│  Actual type: Car               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  vehicle2 (Variable)            │
│  Type hint: Vehicle             │
│  ↓                               │
│  Points to: Motorcycle object   │
│  Actual type: Motorcycle        │
└─────────────────────────────────┘
```

#### Why This Works: The IS-A Relationship

```python
class Vehicle:           # Parent class
    pass

class Car(Vehicle):      # Car IS-A Vehicle (inheritance)
    pass

class Motorcycle(Vehicle):  # Motorcycle IS-A Vehicle (inheritance)
    pass
```

Since `Car` inherits from `Vehicle`, a `Car` **IS-A** `Vehicle`. Therefore, it's valid to assign a `Car` object to a variable with a `Vehicle` type hint.

#### What Happens at Runtime

```python
# Type hint says "Vehicle"
vehicle1: Vehicle = car

# But actual object is "Car"
print(type(vehicle1))  # <class '__main__.Car'>

# When you call a method:
vehicle1.start()  # Calls Car's start() method (dynamic dispatch!)
```

**Key Point**: Even though the type hint says `Vehicle`, Python looks at the **actual object type** (`Car`) and calls the `Car` class's `start()` method. This is **dynamic dispatch**.

#### Type Hints vs Runtime Behavior

```python
# Type hint is just documentation
vehicle1: Vehicle = car

# These all show the actual type (Car), not the hint (Vehicle)
print(type(vehicle1))              # <class '__main__.Car'>
print(isinstance(vehicle1, Car))   # True
print(isinstance(vehicle1, Vehicle))  # True (Car is also a Vehicle)

# Method calls use the actual type
vehicle1.start()  # Calls Car.start(), not Vehicle.start()
```

#### Comparison: Java vs Python

**Java (Strict Type Checking):**
```java
Vehicle vehicle1 = new Car("Toyota", "Camry");
// ↑ Type        ↑ Actual object
// Compile-time  Runtime type

// Type is checked at compile time
// Can't call Car-specific methods without casting
```

**Python (Flexible Type Hints):**
```python
vehicle1: Vehicle = Car("Toyota", "Camry")
# ↑ Type hint   ↑ Actual object
# Optional      Runtime type

# Type hint is optional and not enforced at runtime
# Can call Car-specific methods (but may get AttributeError)
```

#### Practical Example

```python
# Create objects
car = Car("Toyota", "Camry")
bike = Motorcycle("Honda", 600)

# Parent references - enables polymorphism
vehicle1: Vehicle = car
vehicle2: Vehicle = bike

# Both can be treated uniformly as Vehicles
vehicles: list[Vehicle] = [vehicle1, vehicle2]

for vehicle in vehicles:
    print(vehicle.start())  # Calls appropriate child method
    # Output:
    # Toyota Camry: Starting car engine
    # Honda: Starting 600cc motorcycle engine
```

#### Summary of Type Hints and References

| Aspect | Explanation |
|--------|-------------|
| **`vehicle1: Vehicle`** | Type hint (documentation/tooling) |
| **`= car`** | Assignment (actual Car object) |
| **Type hint purpose** | Help developers and type checkers |
| **Runtime behavior** | Uses actual object type (Car) |
| **Benefit** | Polymorphism - uniform interface, specific behavior |

**Remember**: The type hint is just documentation - at runtime, Python always uses the **actual object type**, not the hint!

---

### Dynamic Method Dispatch Explained

```python
class Shape:
    def area(self):
        return 0
    
    def describe(self):
        return f"Shape with area: {self.area()}"  # Calls child's area()!

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

# Parent reference, child objects
shape1: Shape = Circle(5)
shape2: Shape = Rectangle(4, 6)

# Dynamic dispatch in action
print(shape1.describe())  # Calls Circle's area()!
print(shape2.describe())  # Calls Rectangle's area()!

# Even though describe() is in Shape, it calls the child's area()
```

**Output:**
```
Shape with area: 78.53975
Shape with area: 24
```

**Key Point**: When `describe()` calls `self.area()`, Python looks up `area()` in the **actual object's class** (Circle or Rectangle), not the reference type (Shape).

---

## Java vs Python: Dynamic Method Invocation

### Java Example

```java
// Java - Parent reference to child object
class Animal {
    public void speak() {
        System.out.println("Some sound");
    }
}

class Dog extends Animal {
    @Override
    public void speak() {
        System.out.println("Woof!");
    }
    
    public void fetch() {
        System.out.println("Fetching ball");
    }
}

// Usage
Animal animal = new Dog();  // Parent reference, child object
animal.speak();  // Woof! (calls Dog's speak - dynamic dispatch)

// animal.fetch();  // Compile error! Animal doesn't have fetch()

// Need to cast
((Dog) animal).fetch();  // Fetching ball (explicit cast)

// Or use Dog reference
Dog dog = new Dog();
dog.fetch();  // Works fine
```

### Python Equivalent

```python
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def speak(self):
        print("Woof!")
    
    def fetch(self):
        print("Fetching ball")

# Usage
animal: Animal = Dog()  # Parent reference, child object
animal.speak()  # Woof! (calls Dog's speak - dynamic dispatch)

# animal.fetch()  # AttributeError at runtime (not compile time!)

# Can check and call
if hasattr(animal, 'fetch'):
    animal.fetch()  # Fetching ball

# Or use original reference
dog = Dog()
dog.fetch()  # Works fine
```

### Key Differences

| Aspect | Java | Python |
|--------|------|--------|
| **Type checking** | Compile-time | Runtime |
| **Child method access** | Compile error | Runtime AttributeError |
| **Casting** | Explicit cast required | Duck typing, no cast needed |
| **Type hints** | Enforced by compiler | Optional, for documentation |
| **Method lookup** | Based on reference type (compile) + object type (runtime) | Always based on object type (runtime) |

---

## Practical Use Cases

### Use Case 1: Polymorphic Collections

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def calculate_bonus(self):
        return self.salary * 0.1

class Manager(Employee):
    def calculate_bonus(self):
        return self.salary * 0.2

class Developer(Employee):
    def calculate_bonus(self):
        return self.salary * 0.15

class Intern(Employee):
    def calculate_bonus(self):
        return self.salary * 0.05

# Parent reference holding different child objects
employees: list[Employee] = [
    Manager("Alice", 100000),
    Developer("Bob", 80000),
    Developer("Charlie", 85000),
    Intern("David", 30000)
]

# Process all polymorphically
total_bonus = 0
for emp in employees:
    bonus = emp.calculate_bonus()  # Calls appropriate child method
    print(f"{emp.name}: ${bonus:,.2f}")
    total_bonus += bonus

print(f"\nTotal bonuses: ${total_bonus:,.2f}")
```

**Output:**
```
Alice: $20,000.00
Bob: $12,000.00
Charlie: $12,750.00
David: $1,500.00

Total bonuses: $46,250.00
```

### Use Case 2: Plugin System

```python
class Plugin:
    def execute(self):
        raise NotImplementedError

class EmailPlugin(Plugin):
    def execute(self):
        return "Sending email notification"

class SMSPlugin(Plugin):
    def execute(self):
        return "Sending SMS notification"

class SlackPlugin(Plugin):
    def execute(self):
        return "Sending Slack message"

class NotificationSystem:
    def __init__(self):
        self.plugins: list[Plugin] = []
    
    def register_plugin(self, plugin: Plugin):
        """Accept any Plugin subclass"""
        self.plugins.append(plugin)
    
    def notify_all(self):
        """Execute all plugins polymorphically"""
        for plugin in self.plugins:
            print(plugin.execute())

# Usage
system = NotificationSystem()
system.register_plugin(EmailPlugin())
system.register_plugin(SMSPlugin())
system.register_plugin(SlackPlugin())

system.notify_all()
```

**Output:**
```
Sending email notification
Sending SMS notification
Sending Slack message
```

### Use Case 3: Strategy Pattern with Parent References

```python
class PaymentStrategy:
    def pay(self, amount):
        raise NotImplementedError

class CreditCard(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} with Credit Card"

class PayPal(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} with PayPal"

class Bitcoin(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} with Bitcoin"

class ShoppingCart:
    def __init__(self):
        self.payment_method: PaymentStrategy = None
    
    def set_payment_method(self, method: PaymentStrategy):
        """Accept any PaymentStrategy subclass"""
        self.payment_method = method
    
    def checkout(self, amount):
        if self.payment_method:
            return self.payment_method.pay(amount)
        return "No payment method set"

# Usage
cart = ShoppingCart()

# Switch payment methods dynamically
cart.set_payment_method(CreditCard())
print(cart.checkout(100))

cart.set_payment_method(PayPal())
print(cart.checkout(50))

cart.set_payment_method(Bitcoin())
print(cart.checkout(75))
```

**Output:**
```
Paid $100 with Credit Card
Paid $50 with PayPal
Paid $75 with Bitcoin
```

---

## Summary of Dynamic Method Invocation

### Key Concepts

1. **Parent reference can hold child object** ✅
   ```python
   parent: ParentClass = ChildClass()
   ```

2. **Dynamic dispatch** - Child's method is called ✅
   ```python
   parent.method()  # Calls child's implementation
   ```

3. **Type is determined at runtime** ✅
   ```python
   type(parent)  # Returns child class
   ```

4. **Child-specific methods not accessible** ⚠️
   ```python
   parent.child_only_method()  # AttributeError
   ```

### Benefits

✅ **Polymorphic collections**: Store different types in one list  
✅ **Flexible design**: Change behavior at runtime  
✅ **Plugin systems**: Accept any subclass  
✅ **Strategy pattern**: Swap implementations easily  
✅ **Code reusability**: Write once, work with many types

### Python vs Java

- **Python**: Fully dynamic, runtime type checking
- **Java**: Hybrid - compile-time type checking + runtime dispatch
- **Python**: Duck typing allows more flexibility
- **Java**: Stricter type safety, catches errors earlier

---

## Summary

### What is Polymorphism?
- Same interface, different implementations
- "Many forms" of the same operation

### Python's Approach
- **Duck typing** is the primary mechanism
- No need for explicit interfaces (but can use ABC)
- More flexible than Java's compile-time polymorphism

### Key Differences from Java
- Python: Runtime (dynamic) polymorphism
- Java: Compile-time (static) polymorphism
- Python: Duck typing (implicit)
- Java: Interface/inheritance (explicit)

### Advantages
✅ Code reusability  
✅ Flexibility and extensibility  
✅ Simplified code  
✅ Loose coupling  
✅ Easier maintenance

### Implementation Methods
1. Duck typing (natural Python way)
2. Method overriding (inheritance)
3. Operator overloading (magic methods)
4. Abstract base classes (optional, more Java-like)
