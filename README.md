# Python Learning Journey 🐍

A comprehensive Python programming repository covering fundamental to advanced concepts, created as part of Krish Naik's Udemy course.

## 📚 Repository Structure

### 1. Python Basics
Introduction to Python fundamentals and core concepts.

### 2. Control Flow
- Conditional statements (if/else)
- Loops (for, while)
- Control flow patterns

### 3. Data Structures
- Lists
- Tuples
- Dictionaries
- Sets
- String manipulation

### 4. Functions
- Function definition and calling
- Arguments and parameters
- Lambda functions
- Decorators
- Scope and closures

### 5. Modules and Packages
- Importing modules
- Creating custom modules
- Package structure
- `__init__.py` usage
- Module organization

### 6. Standard Libraries
- Built-in Python libraries
- Common standard library usage
- File I/O operations
- Date and time handling

### 7. File Operations
- Reading and writing files
- File modes
- Context managers (`with` statement)
- CSV file handling
- JSON operations
- Binary file operations

### 8. Exception Handling
- Try-except blocks
- Custom exceptions
- Exception hierarchy
- Error handling best practices

### 9. Classes and Objects (OOP)
Comprehensive coverage of Object-Oriented Programming concepts:

#### Core OOP Concepts
- **Classes and Objects** - Basic class structure and instantiation
- **Inheritance** - Single and multiple inheritance
- **Polymorphism** - Method overriding, duck typing, dynamic dispatch
- **Encapsulation** - Access modifiers, private/protected attributes
- **Abstraction** - Abstract base classes, interfaces

#### Advanced Topics
- **Magic Methods** - Dunder methods for operator overloading
- **Operator Overloading** - Custom operator behavior
- **Properties** - `@property` decorator, getters/setters
- **Multiple Inheritance** - MRO, diamond problem, mixins
- **Type System** - Dynamic typing, type hints, type inference

#### Documentation Files
- `abstraction.md` - Abstract base classes and interfaces
- `encapsulation.md` - Data hiding and access control
- `polymorphism.md` - Polymorphism with Java comparison
- `magic_methods.md` - Complete guide to magic methods
- `operator_overloading.md` - All overloadable operators
- `multiple_inheritance.md` - MRO and best practices
- `type_inference.md` - Python's type system
- `functions_vs_methods.md` - Comparison across languages
- `improved_shape.md` - `__new__` vs `__init__`
- `python_scoping.md` - LEGB rule and scope
- `self.md` - Understanding `self` parameter
- `class.md` - Classes as objects, metaclasses
- `type_object_relationship.md` - `type` and `object` relationship

### 10. Iterators
- Iterator protocol (`__iter__`, `__next__`)
- Custom iterators
- Iterable vs Iterator
- Built-in iterators

**Files:** `iterator.ipynb`, `iterators_explained.md`

### 11. Generators
- Generator functions (`yield`)
- Generator expressions
- Lazy evaluation
- Memory-efficient data processing
- Chaining generators

**Files:** `generators.ipynb`, `generators_explained.md`

### 12. Decorators
- Function decorators
- Class decorators
- Closures (prerequisite concept)
- `@wraps`, `@property`, `@staticmethod`, `@classmethod`
- Decorator chaining
- Real-world patterns

**Files:** `decorator.ipynb`, `closures.md`, `decorators.md`

### 13. NumPy
Numerical computing with Python:
- Array creation and manipulation
- Indexing and slicing
- Array operations (element-wise, broadcasting)
- Shape manipulation (reshape, transpose)
- Universal functions (ufuncs)
- Linear algebra
- Statistics
- Random number generation
- Advanced topics

**Files:** `1.ipynb`, plus 10 detailed markdown guides (`1-introduction.md` through `10-advanced-topics.md`)

### 14. Pandas
Data manipulation and analysis:
- Series and DataFrames
- Data loading (CSV, JSON, HTML, Excel)
- Indexing and selection (`loc`, `iloc`)
- Data cleaning (handling missing values, duplicates)
- Data transformation (rename, apply, map)
- Grouping and aggregation
- Merging and joining DataFrames
- Time series analysis
- Advanced topics

**Files:** `1-Series.ipynb`, `2-DataFrames.ipynb`, `3-DataManipulation.ipynb`, `4-ReadData.ipynb`, plus 11 detailed markdown guides

### 15. Logging
Python logging framework:
- Logging levels hierarchy (DEBUG → CRITICAL)
- Formatters and date formats
- Handlers (Console, File, Rotating)
- Multiple loggers
- Comprehensive comparison with Java logging (JUL, Log4j 2, SLF4J + Logback)
- Enterprise logging best practices

**Files:** `logging.ipynb`, `multilogger.ipynb`, `logging-levels.md`, `logs/logger.py`, `logs/test.py`

### 16. HR Programs
Common programming interview questions and solutions.

## 🎯 Learning Objectives

This repository demonstrates proficiency in:

✅ **Python Fundamentals** - Variables, data types, operators  
✅ **Control Structures** - Conditional logic and loops  
✅ **Data Structures** - Lists, dictionaries, sets, tuples  
✅ **Functions** - Definition, scope, decorators  
✅ **OOP Principles** - Inheritance, polymorphism, encapsulation, abstraction  
✅ **Exception Handling** - Error management and custom exceptions  
✅ **File Operations** - Reading, writing, and processing files  
✅ **Standard Libraries** - Utilizing built-in Python modules  
✅ **Iterators & Generators** - Lazy evaluation, memory-efficient processing  
✅ **Decorators & Closures** - Function wrappers, metaprogramming  
✅ **NumPy** - Numerical computing, arrays, linear algebra, statistics  
✅ **Pandas** - DataFrames, data cleaning, transformation, analysis  
✅ **Logging** - Logging levels, handlers, formatters, enterprise practices  

## 📖 Key Features

### Comprehensive Documentation
Each major topic includes detailed markdown documentation with:
- Concept explanations
- Code examples
- Best practices
- Comparisons with other languages (Java, JavaScript)
- Real-world use cases

### Jupyter Notebooks
Interactive notebooks (`.ipynb`) for hands-on learning and experimentation.

### Practical Examples
Real-world examples demonstrating:
- Payment processing systems
- File handlers
- Database connections
- Plugin architectures
- Banking systems
- Shape calculators

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.x
pip (Python package installer)
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rksharma2180/python.git
cd python
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📝 Usage

### Running Python Files
```bash
python <filename>.py
```

### Running Jupyter Notebooks
```bash
jupyter notebook
```
Then navigate to the desired `.ipynb` file in your browser.

## 🔍 Topics Covered in Detail

### Object-Oriented Programming

#### Inheritance
- Parent-child relationships
- Method overriding
- `super()` usage
- Multiple inheritance and MRO

#### Polymorphism
- Duck typing
- Method overriding
- Operator overloading
- Dynamic method dispatch
- Parent references to child objects

#### Encapsulation
- Public, protected, and private attributes
- `@property` decorator
- Getters and setters
- Data validation

#### Abstraction
- Abstract base classes (ABC)
- `@abstractmethod` decorator
- Interface design
- Hiding implementation details

#### Magic Methods
- `__init__`, `__str__`, `__repr__`
- Arithmetic operators (`__add__`, `__sub__`, etc.)
- Comparison operators (`__eq__`, `__lt__`, etc.)
- Container methods (`__len__`, `__getitem__`, etc.)
- Context managers (`__enter__`, `__exit__`)
- Callable objects (`__call__`)

## 🛠️ Tools and Technologies

- **Python 3.x** - Primary programming language
- **Jupyter Notebook** - Interactive development environment
- **NumPy** - Numerical computing library
- **Pandas** - Data manipulation and analysis library
- **lxml & openpyxl** - HTML/XML and Excel file parsing
- **Git** - Version control
- **Virtual Environment** - Dependency management

## 📚 Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Real Python](https://realpython.com/)
- Krish Naik's Udemy Course

## 🤝 Contributing

This is a personal learning repository. However, suggestions and improvements are welcome!

## 📧 Contact

**Ravikant Sharma**  
GitHub: [@rksharma2180](https://github.com/rksharma2180)

## 📄 License

This project is for educational purposes.

---

**Note**: This repository is actively being updated as I progress through the course. Check back regularly for new content!

## 🗂️ File Organization

```
python/
├── 1-PythonBasics/
├── 2-ControlFlow/
├── 3-DataStructure/
├── 4-Functions/
├── 5-ModuleAndPackages/
├── 6-StandardLibraries/
├── 7-FileOperations/
├── 8-ExceptionHandling/
├── 9-Oops/
│   ├── *.ipynb (Jupyter notebooks)
│   └── *.md (Documentation files)
├── 10-Iterators/
│   ├── iterator.ipynb
│   └── iterators_explained.md
├── 11-Generators/
│   ├── generators.ipynb
│   └── generators_explained.md
├── 12-Decorators/
│   ├── decorator.ipynb
│   ├── closures.md
│   └── decorators.md
├── Numpy/
│   ├── 1.ipynb
│   ├── README.md
│   └── *.md (10 topic guides)
├── Pandas/
│   ├── *.ipynb (4 notebooks)
│   ├── README.md
│   ├── *.md (11 topic guides)
│   └── *.csv / *.xlsx (sample data)
├── Logging/
│   ├── logging.ipynb
│   ├── multilogger.ipynb
│   ├── logging-levels.md
│   └── logs/ (logger scripts)
├── HR-Programs/
├── requirements.txt
└── README.md
```

## 🎓 Learning Path

1. **Start with Basics** - Understand Python syntax and fundamentals
2. **Master Data Structures** - Learn to work with different data types
3. **Functions and Modules** - Code organization and reusability
4. **OOP Concepts** - Object-oriented programming principles
5. **Advanced Python** - Iterators, generators, decorators, closures
6. **Exception Handling & File Operations** - Error management, file I/O
7. **Logging** - Application logging, handlers, formatters
8. **NumPy** - Numerical computing, arrays, linear algebra
9. **Pandas** - Data manipulation, cleaning, analysis
10. **Practice** - Solve HR programming challenges

Happy Learning! 🚀
