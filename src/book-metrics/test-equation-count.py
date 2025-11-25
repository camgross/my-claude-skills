#!/usr/bin/env python3
"""
Test script for equation counting function.
Tests the count_equations_in_file method against a known test file.
"""

import re
from pathlib import Path

def count_equations_in_file(markdown_file: Path) -> int:
    """Count LaTeX equations in a single markdown file.

    This is a copy of the function from book-metrics.py for testing.
    """
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count inline math: $...$
            inline = len(re.findall(r'\$[^$]+\$', content))
            # Count display math: $$...$$
            display = len(re.findall(r'\$\$[^$]+\$\$', content))
            return inline + display
    except Exception as e:
        print(f"Warning: Could not read {markdown_file}: {e}")
        return 0

def main():
    """Test the equation counting function."""

    # Path to test file
    test_file = Path(__file__).parent / "equation-count-test.md"

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        import sys
        sys.exit(1)

    # Count equations
    count = count_equations_in_file(test_file)

    # Expected count
    expected = 10

    print(f"Test File: {test_file}")
    print(f"Expected Count: {expected}")
    print(f"Actual Count: {count}")
    print()

    if count == expected:
        print("✅ Test PASSED!")
    else:
        print(f"❌ Test FAILED! Difference: {count - expected}")
        print()
        print("Issues detected:")
        if count > expected:
            print("  - Function is over-counting (likely counting dollar amounts as equations)")
        else:
            print("  - Function is under-counting (missing some equations)")

    # Additional debug info
    print("\nDebug: Let's check what the regex is matching...")
    import re

    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Test inline pattern
    inline_matches = re.findall(r'\$[^$]+\$', content)
    print(f"\nInline math matches ($...$): {len(inline_matches)}")
    for i, match in enumerate(inline_matches[:15], 1):  # Show first 15
        print(f"  {i}. {match}")
    if len(inline_matches) > 15:
        print(f"  ... and {len(inline_matches) - 15} more")

    # Test display pattern
    display_matches = re.findall(r'\$\$[^$]+\$\$', content)
    print(f"\nDisplay math matches ($$...$$): {len(display_matches)}")
    for i, match in enumerate(display_matches, 1):
        print(f"  {i}. {match[:60]}..." if len(match) > 60 else f"  {i}. {match}")

if __name__ == "__main__":
    main()
