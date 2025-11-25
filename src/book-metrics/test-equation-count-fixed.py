#!/usr/bin/env python3
"""
Test script with FIXED equation counting function.
"""

import re
from pathlib import Path

def count_equations_in_file_ORIGINAL(markdown_file: Path) -> int:
    """Original buggy version."""
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

def count_equations_in_file_FIXED(markdown_file: Path) -> int:
    """Fixed version that correctly counts LaTeX equations.

    Fixes:
    1. Removes display math ($$...$$) before counting inline math to avoid double-counting
    2. Improves inline math regex to avoid matching dollar amounts
    """
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Count display math: $$...$$ (must come first)
            display_matches = re.findall(r'\$\$[^$]+?\$\$', content, re.DOTALL)
            display = len(display_matches)

            # Remove all display math blocks to avoid double-counting
            content_no_display = re.sub(r'\$\$[^$]+?\$\$', '', content, flags=re.DOTALL)

            # Count inline math: $...$
            # Pattern requires: $ followed by non-whitespace, then content, then $
            # This avoids matching dollar amounts like "$500" which have digits right after $
            inline_matches = re.findall(r'\$(?!\d)([^\$]+?)\$', content_no_display)
            inline = len(inline_matches)

            return inline + display
    except Exception as e:
        print(f"Warning: Could not read {markdown_file}: {e}")
        return 0

def main():
    """Test both versions."""

    # Path to test file
    test_file = Path(__file__).parent / "equation-count-test.md"

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        import sys
        sys.exit(1)

    # Test original version
    count_original = count_equations_in_file_ORIGINAL(test_file)

    # Test fixed version
    count_fixed = count_equations_in_file_FIXED(test_file)

    # Expected count
    expected = 12

    print(f"Test File: {test_file}")
    print(f"Expected Count: {expected}")
    print(f"\nOriginal Function Count: {count_original} {'❌ FAILED' if count_original != expected else '✅ PASSED'}")
    print(f"Fixed Function Count: {count_fixed} {'❌ FAILED' if count_fixed != expected else '✅ PASSED'}")
    print()

    if count_fixed == expected:
        print("✅ Fixed version PASSED!")
        print("\nTo fix book-metrics.py, replace the count_equations_in_file method with:")
        print("=" * 70)
        print("""
    def count_equations_in_file(self, markdown_file: Path) -> int:
        \"\"\"Count LaTeX equations in a single markdown file.

        Args:
            markdown_file: Path to markdown file

        Returns:
            Number of equations (LaTeX expressions)
        \"\"\"
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Count display math: $$...$$ (must come first)
                display_matches = re.findall(r'\\$\\$[^$]+?\\$\\$', content, re.DOTALL)
                display = len(display_matches)

                # Remove all display math blocks to avoid double-counting
                content_no_display = re.sub(r'\\$\\$[^$]+?\\$\\$', '', content, flags=re.DOTALL)

                # Count inline math: $...$
                # Negative lookahead (?!\\d) ensures we don't match dollar amounts like $500
                inline_matches = re.findall(r'\\$(?!\\d)([^\\$]+?)\\$', content_no_display)
                inline = len(inline_matches)

                return inline + display
        except Exception as e:
            print(f"Warning: Could not read {markdown_file}: {e}")
            return 0
""")
        print("=" * 70)
    else:
        print(f"❌ Fixed version still has issues. Difference: {count_fixed - expected}")

    # Debug info
    print("\n" + "=" * 70)
    print("DETAILED DEBUG INFO")
    print("=" * 70)

    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Show what each regex matches
    print("\n[ORIGINAL] Inline math pattern matches:")
    inline_orig = re.findall(r'\$[^$]+\$', content)
    for i, match in enumerate(inline_orig[:10], 1):
        preview = match[:50] + "..." if len(match) > 50 else match
        print(f"  {i}. {preview}")
    print(f"  ... Total: {len(inline_orig)}")

    print("\n[FIXED] Display math matches:")
    display_fixed = re.findall(r'\$\$[^$]+?\$\$', content, re.DOTALL)
    for i, match in enumerate(display_fixed, 1):
        preview = match[:60] + "..." if len(match) > 60 else match
        print(f"  {i}. {preview}")
    print(f"  Total: {len(display_fixed)}")

    # Remove display math
    content_no_display = re.sub(r'\$\$[^$]+?\$\$', '', content, flags=re.DOTALL)

    print("\n[FIXED] Inline math matches (after removing display math):")
    inline_fixed = re.findall(r'\$(?!\d)([^\$]+?)\$', content_no_display)
    for i, match in enumerate(inline_fixed, 1):
        preview = match[:50] + "..." if len(match) > 50 else match
        print(f"  {i}. ${preview}$")
    print(f"  Total: {len(inline_fixed)}")

if __name__ == "__main__":
    main()
