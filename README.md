# CSV List Parser

A simple and extensible Python application for parsing CSV files. Extract specific columns and apply transformations to create customized output files.

## Features

- **Column Selection**: Extract only the columns you need from a CSV file
- **Transformations**: Apply built-in transformations (uppercase, lowercase, strip whitespace)
- **Extensible Architecture**: Easy to add custom transformations
- **Command-line Interface**: Simple CLI for quick operations
- **Programmatic API**: Use as a library in your Python code

## Installation

No external dependencies required! This project uses only Python standard library.

```bash
git clone https://github.com/michalwy/colnect-list-parser.git
cd colnect-list-parser
```

## Usage

### Command-line Interface

#### Basic Usage - Extract Specific Columns

```bash
python main.py input.csv output.csv --columns name email city
```

#### Extract All Columns

```bash
python main.py input.csv output.csv
```

#### Apply Transformations

```bash
# Convert city names to uppercase
python main.py input.csv output.csv --columns name city --uppercase city

# Convert email to lowercase and strip whitespace from name
python main.py input.csv output.csv --columns name email --lowercase email --strip name

# Multiple transformations
python main.py input.csv output.csv --columns name email city --uppercase city --strip name
```

#### Command-line Options

```
positional arguments:
  input                 Input CSV file path
  output                Output CSV file path

optional arguments:
  --columns COL1 COL2   Columns to extract (if not specified, all columns will be included)
  --uppercase COL1      Columns to convert to uppercase
  --lowercase COL1      Columns to convert to lowercase
  --strip COL1          Columns to strip whitespace from
  --encoding ENCODING   File encoding (default: utf-8)
```

### Programmatic API

You can also use the CSV parser as a library in your Python code:

```python
from csv_parser import CSVParser, UpperCaseTransformer, LowerCaseTransformer

# Create a parser instance
parser = CSVParser()

# Select columns
parser.set_columns(['name', 'email', 'city'])

# Add transformations
parser.add_transformer('city', UpperCaseTransformer())
parser.add_transformer('email', LowerCaseTransformer())

# Parse the file
parser.parse('input.csv', 'output.csv')
```

## Extending with Custom Transformations

The application is designed to be easily extensible. You can create custom transformations by subclassing `ColumnTransformer`:

```python
from csv_parser import ColumnTransformer, CSVParser

# Create a custom transformer
class PrefixTransformer(ColumnTransformer):
    def __init__(self, prefix):
        self.prefix = prefix
    
    def transform(self, value):
        return f"{self.prefix}{value}"

# Use the custom transformer
parser = CSVParser()
parser.set_columns(['id', 'name'])
parser.add_transformer('id', PrefixTransformer('ID-'))
parser.parse('input.csv', 'output.csv')
```

### More Complex Example

```python
from csv_parser import ColumnTransformer, CSVParser

# Create a custom transformer that formats phone numbers
class PhoneFormatter(ColumnTransformer):
    def transform(self, value):
        # Remove all non-digit characters
        digits = ''.join(c for c in str(value) if c.isdigit())
        # Format as (XXX) XXX-XXXX
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return value

# Use it
parser = CSVParser()
parser.set_columns(['name', 'phone'])
parser.add_transformer('phone', PhoneFormatter())
parser.parse('contacts.csv', 'formatted_contacts.csv')
```

## Running Tests

The project includes comprehensive unit tests:

```bash
python -m unittest test_csv_parser -v
```

## Examples

The `examples/` directory contains sample CSV files for testing:

- `input.csv` - Sample input file with user data
- `output1.csv` - Example output with selected columns
- `output2.csv` - Example output with transformations

## Project Structure

```
colnect-list-parser/
├── csv_parser.py       # Core parser module with transformers
├── main.py             # Command-line interface
├── test_csv_parser.py  # Unit tests
├── examples/           # Example CSV files
│   ├── input.csv
│   ├── output1.csv
│   └── output2.csv
└── README.md           # This file
```

## Built-in Transformers

- **UpperCaseTransformer**: Convert text to uppercase
- **LowerCaseTransformer**: Convert text to lowercase
- **StripTransformer**: Remove leading and trailing whitespace

## License

MIT License - see LICENSE file for details