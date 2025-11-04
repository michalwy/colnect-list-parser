"""
Unit tests for the CSV parser module.
"""

import unittest
import os
import tempfile
import csv
from csv_parser import (
    CSVParser,
    UpperCaseTransformer,
    LowerCaseTransformer,
    StripTransformer,
    create_parser
)


class TestColumnTransformers(unittest.TestCase):
    """Test the column transformer classes."""
    
    def test_uppercase_transformer(self):
        """Test UpperCaseTransformer."""
        transformer = UpperCaseTransformer()
        self.assertEqual(transformer.transform("hello"), "HELLO")
        self.assertEqual(transformer.transform("World"), "WORLD")
        self.assertEqual(transformer.transform(""), "")
    
    def test_lowercase_transformer(self):
        """Test LowerCaseTransformer."""
        transformer = LowerCaseTransformer()
        self.assertEqual(transformer.transform("HELLO"), "hello")
        self.assertEqual(transformer.transform("World"), "world")
        self.assertEqual(transformer.transform(""), "")
    
    def test_strip_transformer(self):
        """Test StripTransformer."""
        transformer = StripTransformer()
        self.assertEqual(transformer.transform("  hello  "), "hello")
        self.assertEqual(transformer.transform("world\n"), "world")
        self.assertEqual(transformer.transform("  "), "")


class TestCSVParser(unittest.TestCase):
    """Test the CSVParser class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, 'input.csv')
        self.output_file = os.path.join(self.test_dir, 'output.csv')
        
        # Create a test input CSV file
        with open(self.input_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'age', 'email'])
            writer.writerow(['John Doe', '30', 'john@example.com'])
            writer.writerow(['Jane Smith', '25', 'jane@example.com'])
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.test_dir)
    
    def test_parse_all_columns(self):
        """Test parsing with all columns."""
        parser = CSVParser()
        parser.parse(self.input_file, self.output_file)
        
        # Read and verify output
        with open(self.output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['name'], 'John Doe')
        self.assertEqual(rows[0]['age'], '30')
        self.assertEqual(rows[0]['email'], 'john@example.com')
    
    def test_parse_subset_columns(self):
        """Test parsing with a subset of columns."""
        parser = CSVParser()
        parser.set_columns(['name', 'email'])
        parser.parse(self.input_file, self.output_file)
        
        # Read and verify output
        with open(self.output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(set(rows[0].keys()), {'name', 'email'})
        self.assertNotIn('age', rows[0])
    
    def test_parse_with_uppercase_transformer(self):
        """Test parsing with uppercase transformation."""
        parser = CSVParser()
        parser.set_columns(['name', 'email'])
        parser.add_transformer('name', UpperCaseTransformer())
        parser.parse(self.input_file, self.output_file)
        
        # Read and verify output
        with open(self.output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(rows[0]['name'], 'JOHN DOE')
        self.assertEqual(rows[1]['name'], 'JANE SMITH')
        # Email should remain unchanged
        self.assertEqual(rows[0]['email'], 'john@example.com')
    
    def test_parse_with_multiple_transformers(self):
        """Test parsing with multiple transformers."""
        parser = CSVParser()
        parser.set_columns(['name', 'email'])
        parser.add_transformer('name', UpperCaseTransformer())
        parser.add_transformer('email', LowerCaseTransformer())
        parser.parse(self.input_file, self.output_file)
        
        # Read and verify output
        with open(self.output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(rows[0]['name'], 'JOHN DOE')
        self.assertEqual(rows[0]['email'], 'john@example.com')  # Already lowercase
    
    def test_parse_missing_column_raises_error(self):
        """Test that requesting a non-existent column raises an error."""
        parser = CSVParser()
        parser.set_columns(['name', 'nonexistent'])
        
        with self.assertRaises(ValueError) as context:
            parser.parse(self.input_file, self.output_file)
        
        self.assertIn('not found', str(context.exception).lower())
    
    def test_parse_empty_csv_raises_error(self):
        """Test that parsing a CSV without headers raises an error."""
        empty_file = os.path.join(self.test_dir, 'empty.csv')
        with open(empty_file, 'w') as f:
            f.write('')
        
        parser = CSVParser()
        
        with self.assertRaises(ValueError) as context:
            parser.parse(empty_file, self.output_file)
        
        self.assertIn('no header', str(context.exception).lower())
        os.remove(empty_file)
    
    def test_method_chaining(self):
        """Test that methods support chaining."""
        parser = CSVParser()
        result = parser.set_columns(['name']).add_transformer('name', UpperCaseTransformer())
        self.assertIs(result, parser)
    
    def test_create_parser_factory(self):
        """Test the create_parser factory function."""
        parser = create_parser()
        self.assertIsInstance(parser, CSVParser)


class TestStripTransformerIntegration(unittest.TestCase):
    """Test the StripTransformer with actual CSV data."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, 'input.csv')
        self.output_file = os.path.join(self.test_dir, 'output.csv')
        
        # Create a test input CSV file with whitespace
        with open(self.input_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'city'])
            writer.writerow(['  John Doe  ', ' New York '])
            writer.writerow([' Jane Smith', 'London  '])
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.test_dir)
    
    def test_strip_transformer(self):
        """Test that StripTransformer removes whitespace."""
        parser = CSVParser()
        parser.add_transformer('name', StripTransformer())
        parser.add_transformer('city', StripTransformer())
        parser.parse(self.input_file, self.output_file)
        
        # Read and verify output
        with open(self.output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(rows[0]['name'], 'John Doe')
        self.assertEqual(rows[0]['city'], 'New York')
        self.assertEqual(rows[1]['name'], 'Jane Smith')
        self.assertEqual(rows[1]['city'], 'London')


if __name__ == '__main__':
    unittest.main()
