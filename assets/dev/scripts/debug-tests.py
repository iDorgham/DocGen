#!/usr/bin/env python3
"""Debug script to test the failing functions."""

import sys
sys.path.insert(0, 'src')

from utils.formatting import format_markdown
from utils.validation import validate_email, validate_yaml

print("Testing format_markdown:")
result = format_markdown('# Test Title\n\nSome content')
print(f"Input: '# Test Title\\n\\nSome content'")
print(f"Output: {repr(result)}")
print(f"Expected: '# Test Title\\n\\nSome content'")
print(f"Match: {result == '# Test Title\\n\\nSome content'}")

print("\nTesting validate_email:")
result = validate_email("test@example.com")
print(f"validate_email('test@example.com'): {result}")

print("\nTesting validate_yaml:")
result = validate_yaml("key: value")
print(f"validate_yaml('key: value'): {result}")
result = validate_yaml("")
print(f"validate_yaml(''): {result}")
result = validate_yaml(None)
print(f"validate_yaml(None): {result}")
