#!/usr/bin/env python3
"""
Example: Custom Transformers

This example demonstrates how to create and use custom transformers
to extend the functionality of the CSV parser.
"""

from csv_parser import ColumnTransformer, CSVParser


# Example 1: Simple prefix transformer
class PrefixTransformer(ColumnTransformer):
    """Add a prefix to column values."""
    
    def __init__(self, prefix):
        self.prefix = prefix
    
    def transform(self, value):
        return f"{self.prefix}{value}"


# Example 2: Phone number formatter
class PhoneFormatter(ColumnTransformer):
    """Format phone numbers as (XXX) XXX-XXXX."""
    
    def transform(self, value):
        # Remove all non-digit characters
        digits = ''.join(c for c in str(value) if c.isdigit())
        # Format as (XXX) XXX-XXXX for 10-digit numbers
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return value


# Example 3: Title case transformer
class TitleCaseTransformer(ColumnTransformer):
    """Convert text to title case."""
    
    def transform(self, value):
        return str(value).title() if value else value


# Example 4: Truncate transformer
class TruncateTransformer(ColumnTransformer):
    """Truncate text to a maximum length."""
    
    def __init__(self, max_length, suffix='...'):
        self.max_length = max_length
        self.suffix = suffix
    
    def transform(self, value):
        text = str(value)
        if len(text) > self.max_length:
            return text[:self.max_length - len(self.suffix)] + self.suffix
        return text


# Example 5: Default value transformer
class DefaultValueTransformer(ColumnTransformer):
    """Replace empty values with a default."""
    
    def __init__(self, default_value='N/A'):
        self.default_value = default_value
    
    def transform(self, value):
        return self.default_value if not value or str(value).strip() == '' else value


def example_1_prefix():
    """Example: Add prefix to ID column."""
    print("Example 1: Adding prefix to ID column")
    parser = CSVParser()
    parser.set_columns(['id', 'name', 'email'])
    parser.add_transformer('id', PrefixTransformer('USER-'))
    parser.parse('examples/input.csv', 'examples/example1_output.csv')
    print("  Created: examples/example1_output.csv\n")


def example_2_phone():
    """Example: Format phone numbers."""
    print("Example 2: Formatting phone numbers")
    parser = CSVParser()
    parser.set_columns(['name', 'phone'])
    parser.add_transformer('phone', PhoneFormatter())
    parser.parse('examples/input.csv', 'examples/example2_output.csv')
    print("  Created: examples/example2_output.csv\n")


def example_3_title_case():
    """Example: Convert names to title case."""
    print("Example 3: Converting to title case")
    parser = CSVParser()
    parser.set_columns(['name', 'city', 'country'])
    parser.add_transformer('city', TitleCaseTransformer())
    parser.add_transformer('country', TitleCaseTransformer())
    parser.parse('examples/input.csv', 'examples/example3_output.csv')
    print("  Created: examples/example3_output.csv\n")


def example_4_multiple_transformers():
    """Example: Combine multiple transformers."""
    print("Example 4: Combining multiple transformers")
    parser = CSVParser()
    parser.set_columns(['id', 'name', 'email', 'city'])
    parser.add_transformer('id', PrefixTransformer('ID-'))
    parser.add_transformer('name', TitleCaseTransformer())
    parser.add_transformer('city', TitleCaseTransformer())
    parser.add_transformer('email', TruncateTransformer(20))
    parser.parse('examples/input.csv', 'examples/example4_output.csv')
    print("  Created: examples/example4_output.csv\n")


def main():
    """Run all examples."""
    print("=" * 60)
    print("CSV Parser - Custom Transformer Examples")
    print("=" * 60)
    print()
    
    example_1_prefix()
    example_2_phone()
    example_3_title_case()
    example_4_multiple_transformers()
    
    print("=" * 60)
    print("All examples completed!")
    print("Check the examples/ directory for output files.")
    print("=" * 60)


if __name__ == '__main__':
    main()
