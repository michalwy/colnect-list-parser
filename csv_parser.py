"""
CSV Parser - Read CSV files and output a subset of columns with optional transformations.

This module provides a flexible and extensible CSV parser that can:
- Select specific columns from a CSV file
- Apply transformations to column values
- Output the result to a new CSV file
"""

import csv
from typing import List, Dict, Callable, Optional, Any


class ColumnTransformer:
    """Base class for column transformations."""
    
    def transform(self, value: Any) -> Any:
        """
        Transform a column value.
        
        Args:
            value: The original value to transform
            
        Returns:
            The transformed value
        """
        return value


class UpperCaseTransformer(ColumnTransformer):
    """Transform text to uppercase."""
    
    def transform(self, value: Any) -> Any:
        return str(value).upper() if value else value


class LowerCaseTransformer(ColumnTransformer):
    """Transform text to lowercase."""
    
    def transform(self, value: Any) -> Any:
        return str(value).lower() if value else value


class StripTransformer(ColumnTransformer):
    """Remove leading and trailing whitespace."""
    
    def transform(self, value: Any) -> Any:
        return str(value).strip() if value else value


class CSVParser:
    """
    Parse CSV files and output a subset of columns with optional transformations.
    """
    
    def __init__(self):
        """Initialize the CSV parser."""
        self.columns: List[str] = []
        self.transformers: Dict[str, ColumnTransformer] = {}
    
    def set_columns(self, columns: List[str]) -> 'CSVParser':
        """
        Set the columns to extract from the CSV.
        
        Args:
            columns: List of column names to extract
            
        Returns:
            self for method chaining
        """
        self.columns = columns
        return self
    
    def add_transformer(self, column: str, transformer: ColumnTransformer) -> 'CSVParser':
        """
        Add a transformer for a specific column.
        
        Args:
            column: The column name to apply the transformer to
            transformer: The transformer instance to apply
            
        Returns:
            self for method chaining
        """
        self.transformers[column] = transformer
        return self
    
    def parse(self, input_file: str, output_file: str, encoding: str = 'utf-8') -> None:
        """
        Parse the input CSV file and write the result to the output file.
        
        Args:
            input_file: Path to the input CSV file
            output_file: Path to the output CSV file
            encoding: File encoding (default: utf-8)
        """
        with open(input_file, 'r', encoding=encoding, newline='') as infile:
            reader = csv.DictReader(infile)
            
            # Get available columns from the file
            if reader.fieldnames is None:
                raise ValueError("Input CSV file has no header row")
            
            # Determine which columns to output
            output_columns = self.columns if self.columns else list(reader.fieldnames)
            
            # Validate that requested columns exist in the input file
            missing_columns = set(output_columns) - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"Columns not found in input file: {missing_columns}")
            
            with open(output_file, 'w', encoding=encoding, newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=output_columns)
                writer.writeheader()
                
                for row in reader:
                    # Extract only the desired columns
                    output_row = {}
                    for column in output_columns:
                        value = row[column]
                        
                        # Apply transformer if one is defined for this column
                        if column in self.transformers:
                            value = self.transformers[column].transform(value)
                        
                        output_row[column] = value
                    
                    writer.writerow(output_row)


def create_parser() -> CSVParser:
    """
    Factory function to create a new CSV parser instance.
    
    Returns:
        A new CSVParser instance
    """
    return CSVParser()
