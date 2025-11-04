#!/usr/bin/env python3
"""
Command-line interface for the CSV parser.

Usage:
    python main.py input.csv output.csv --columns col1 col2 col3
    python main.py input.csv output.csv --columns col1 col2 --uppercase col1
"""

import argparse
import sys
from csv_parser import CSVParser, UpperCaseTransformer, LowerCaseTransformer, StripTransformer


def main():
    """Main entry point for the CSV parser CLI."""
    parser = argparse.ArgumentParser(
        description='Parse CSV files and output a subset of columns with optional transformations.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract specific columns
  python main.py input.csv output.csv --columns name age email

  # Extract all columns (no --columns flag)
  python main.py input.csv output.csv

  # Extract columns with transformations
  python main.py input.csv output.csv --columns name email --uppercase name
  python main.py input.csv output.csv --columns name email --lowercase email --strip name
        """
    )
    
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('output', help='Output CSV file path')
    parser.add_argument(
        '--columns',
        nargs='+',
        help='Columns to extract (if not specified, all columns will be included)',
        default=[]
    )
    parser.add_argument(
        '--uppercase',
        nargs='+',
        help='Columns to convert to uppercase',
        default=[]
    )
    parser.add_argument(
        '--lowercase',
        nargs='+',
        help='Columns to convert to lowercase',
        default=[]
    )
    parser.add_argument(
        '--strip',
        nargs='+',
        help='Columns to strip whitespace from',
        default=[]
    )
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    args = parser.parse_args()
    
    # Create and configure the parser
    csv_parser = CSVParser()
    
    if args.columns:
        csv_parser.set_columns(args.columns)
    
    # Add transformers
    for column in args.uppercase:
        csv_parser.add_transformer(column, UpperCaseTransformer())
    
    for column in args.lowercase:
        csv_parser.add_transformer(column, LowerCaseTransformer())
    
    for column in args.strip:
        csv_parser.add_transformer(column, StripTransformer())
    
    # Parse the CSV file
    try:
        csv_parser.parse(args.input, args.output, encoding=args.encoding)
        print(f"Successfully parsed {args.input} -> {args.output}")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
