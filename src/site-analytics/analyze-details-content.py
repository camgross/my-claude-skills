#!/usr/bin/env python3
"""
analyze-details-content.py
Analyze <details> tags in chapter content to categorize visualization types
and prioritize skill development based on impact and effort.

Supports both old format (<details>) and new format (<details markdown="1">).
"""
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


def extract_details_content(docs_dir: Path) -> List[Dict]:
    """Extract all <details> tag content from chapter markdown files.

    Supports both formats:
    - Old: <details>
    - New: <details markdown="1">
    """
    chapters_dir = docs_dir / 'chapters'
    if not chapters_dir.exists():
        return []

    details_list = []

    for chapter_dir in sorted(chapters_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue

        index_file = chapter_dir / 'index.md'
        if not index_file.exists():
            continue

        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract chapter title
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            chapter_title = title_match.group(1) if title_match else chapter_dir.name

            # Find all <details> blocks (supports both old and new format)
            # Old format: <details>
            # New format: <details markdown="1">
            details_pattern = r'<details(?:\s+markdown="1")?>(.*?)</details>'
            matches = re.finditer(details_pattern, content, re.DOTALL | re.IGNORECASE)

            for match in matches:
                details_content = match.group(1)

                # Extract summary
                summary_match = re.search(r'<summary>(.*?)</summary>', details_content, re.IGNORECASE)
                summary = summary_match.group(1).strip() if summary_match else "No summary"

                # Extract type
                type_match = re.search(r'Type:\s*(.+)$', details_content, re.MULTILINE | re.IGNORECASE)
                viz_type = type_match.group(1).strip() if type_match else "unknown"

                # Extract purpose
                purpose_match = re.search(r'Purpose:\s*(.+)$', details_content, re.MULTILINE | re.IGNORECASE)
                purpose = purpose_match.group(1).strip() if purpose_match else ""

                # Extract learning objective (if present)
                learning_match = re.search(r'Learning objective:\s*(.+)$', details_content, re.MULTILINE | re.IGNORECASE)
                learning_obj = learning_match.group(1).strip() if learning_match else ""

                details_list.append({
                    'chapter': chapter_title,
                    'summary': summary,
                    'type': viz_type,
                    'purpose': purpose,
                    'learning_objective': learning_obj
                })

    return details_list


def categorize_visualization_types(details_list: List[Dict]) -> Dict[str, List[Dict]]:
    """Group visualizations by type."""
    categories = defaultdict(list)

    for item in details_list:
        viz_type = item['type'].lower()
        categories[viz_type].append(item)

    return dict(categories)


def assess_skill_priority(categories: Dict[str, List[Dict]], existing_sims: List[str]) -> List[Dict]:
    """
    Assess priority for each visualization type based on:
    - Impact: How many instances exist (more = higher impact)
    - Effort: Similarity to existing MicroSims (less similar = higher effort)
    """

    # Define similarity to existing MicroSims (0-10 scale, 10 = very similar)
    similarity_scores = {
        'microsim': 10,  # Already have these
        'graph-model': 9,  # Very similar to graph viewer
        'infographic': 8,  # Similar to existing infographic template
        'diagram': 6,  # Medium similarity, structured layouts
        'network-diagram': 6,  # Similar to graph viewer but different focus
        'chart': 5,  # Different from current sims
        'workflow': 4,  # Sequential/timeline visualization
        'interactive': 7,  # General category, similar to existing
        'timeline': 3,  # Time-based, less similar
        'unknown': 5,  # Default middle value
    }

    priorities = []

    for viz_type, items in sorted(categories.items()):
        count = len(items)

        # Calculate impact (0-10 scale based on frequency)
        max_count = max(len(v) for v in categories.values())
        impact = min(10, (count / max_count) * 10)

        # Calculate effort (0-10 scale, inverse of similarity)
        # Higher similarity = lower effort
        similarity = similarity_scores.get(viz_type, 5)
        effort = 10 - similarity

        # Calculate priority score (impact/effort ratio)
        priority_score = impact / effort if effort > 0 else impact

        priorities.append({
            'type': viz_type,
            'count': count,
            'impact': round(impact, 1),
            'effort': round(effort, 1),
            'priority_score': round(priority_score, 2),
            'examples': [item['summary'] for item in items[:3]]  # First 3 examples
        })

    # Sort by priority score (high to low)
    priorities.sort(key=lambda x: x['priority_score'], reverse=True)

    return priorities


def generate_markdown_report(details_list: List[Dict],
                            categories: Dict[str, List[Dict]],
                            priorities: List[Dict],
                            output_file: Path) -> None:
    """Generate a markdown report of the details analysis."""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Details Tag Content Analysis\n\n")
        f.write("This report analyzes all `<details>` tags (both old and new `markdown=\"1\"` format) in the textbook chapters to categorize visualization types and prioritize skill development.\n\n")

        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total `<details>` tags:** {len(details_list)}\n")
        f.write(f"- **Unique visualization types:** {len(categories)}\n\n")

        f.write("## Visualization Type Distribution\n\n")
        f.write("| Type | Count | Percentage |\n")
        f.write("|------|-------|------------|\n")

        total = len(details_list)
        for viz_type, items in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            count = len(items)
            percentage = (count / total) * 100
            f.write(f"| {viz_type} | {count} | {percentage:.1f}% |\n")
        f.write("\n")

        f.write("## Priority Matrix for Skill Development\n\n")
        f.write("Prioritization based on **Impact** (frequency of use) vs. **Effort** (similarity to existing MicroSims).\n\n")

        f.write("### Priority Scores\n\n")
        f.write("| Rank | Type | Count | Impact (0-10) | Effort (0-10) | Priority Score | Status |\n")
        f.write("|------|------|-------|---------------|---------------|----------------|--------|\n")

        for i, item in enumerate(priorities, 1):
            # Determine status based on type
            status = "✅ Exists" if item['type'] in ['microsim'] else "🔨 Build"
            f.write(f"| {i} | **{item['type']}** | {item['count']} | {item['impact']} | {item['effort']} | {item['priority_score']} | {status} |\n")
        f.write("\n")

        f.write("### Interpretation\n\n")
        f.write("- **Impact**: Higher values indicate more instances of this visualization type across chapters\n")
        f.write("- **Effort**: Higher values indicate more development effort required (less similar to existing MicroSims)\n")
        f.write("- **Priority Score**: Impact/Effort ratio - higher scores suggest better ROI for skill development\n\n")

        f.write("## Visual Priority Matrix\n\n")
        f.write("```\n")
        f.write("Impact (Frequency)\n")
        f.write("     ↑\n")
        f.write("  10 │\n")
        f.write("   9 │\n")
        f.write("   8 │\n")
        f.write("   7 │\n")
        f.write("   6 │\n")
        f.write("   5 │\n")
        f.write("   4 │\n")
        f.write("   3 │\n")
        f.write("   2 │\n")
        f.write("   1 │\n")
        f.write("   0 └")
        f.write("─" * 50)
        f.write("→ Effort (Dissimilarity)\n")
        f.write("     0  1  2  3  4  5  6  7  8  9  10\n\n")

        # Place items on the matrix
        for item in priorities:
            effort = int(item['effort'])
            impact = int(item['impact'])
            f.write(f"   [{effort:.0f}, {impact:.0f}]: {item['type']} (n={item['count']})\n")
        f.write("```\n\n")

        f.write("### Quadrant Analysis\n\n")
        f.write("**High Impact, Low Effort (Priority 1):**\n")
        high_impact_low_effort = [p for p in priorities if p['impact'] >= 5 and p['effort'] <= 5]
        if high_impact_low_effort:
            for item in high_impact_low_effort:
                f.write(f"- **{item['type']}** (Impact: {item['impact']}, Effort: {item['effort']}, Count: {item['count']})\n")
        else:
            f.write("- None\n")
        f.write("\n")

        f.write("**High Impact, High Effort (Priority 2):**\n")
        high_impact_high_effort = [p for p in priorities if p['impact'] >= 5 and p['effort'] > 5]
        if high_impact_high_effort:
            for item in high_impact_high_effort:
                f.write(f"- **{item['type']}** (Impact: {item['impact']}, Effort: {item['effort']}, Count: {item['count']})\n")
        else:
            f.write("- None\n")
        f.write("\n")

        f.write("**Low Impact, Low Effort (Priority 3):**\n")
        low_impact_low_effort = [p for p in priorities if p['impact'] < 5 and p['effort'] <= 5]
        if low_impact_low_effort:
            for item in low_impact_low_effort:
                f.write(f"- **{item['type']}** (Impact: {item['impact']}, Effort: {item['effort']}, Count: {item['count']})\n")
        else:
            f.write("- None\n")
        f.write("\n")

        f.write("**Low Impact, High Effort (Priority 4):**\n")
        low_impact_high_effort = [p for p in priorities if p['impact'] < 5 and p['effort'] > 5]
        if low_impact_high_effort:
            for item in low_impact_high_effort:
                f.write(f"- **{item['type']}** (Impact: {item['impact']}, Effort: {item['effort']}, Count: {item['count']})\n")
        else:
            f.write("- None\n")
        f.write("\n")

        f.write("## Detailed Breakdown by Type\n\n")

        for viz_type, items in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"### {viz_type.title()} ({len(items)} instances)\n\n")

            for item in items:
                f.write(f"**Chapter:** {item['chapter']}\n\n")
                f.write(f"**Summary:** {item['summary']}\n\n")
                if item['purpose']:
                    f.write(f"**Purpose:** {item['purpose']}\n\n")
                if item['learning_objective']:
                    f.write(f"**Learning Objective:** {item['learning_objective']}\n\n")
                f.write("---\n\n")

        f.write("## Recommendations\n\n")
        f.write("Based on the priority analysis, focus on developing skills for:\n\n")

        top_priorities = [p for p in priorities if p['priority_score'] > 1.0 and p['type'] != 'microsim'][:5]
        for i, item in enumerate(top_priorities, 1):
            f.write(f"{i}. **{item['type']}** - {item['count']} instances, priority score {item['priority_score']}\n")
            f.write(f"   - Example: {item['examples'][0]}\n")
        f.write("\n")


def main():
    """Main function to analyze details content."""
    repo_root = Path(__file__).parent.parent.parent
    docs_dir = repo_root / 'docs'

    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return 1

    print("Analyzing <details> tag content...")

    # Extract all details content
    details_list = extract_details_content(docs_dir)

    if not details_list:
        print("No <details> tags found in chapters")
        return 1

    # Categorize by type
    categories = categorize_visualization_types(details_list)

    # List existing MicroSims
    sims_dir = docs_dir / 'sims'
    existing_sims = [d.name for d in sims_dir.iterdir() if d.is_dir()] if sims_dir.exists() else []

    # Assess priorities
    priorities = assess_skill_priority(categories, existing_sims)

    # Generate report
    output_file = docs_dir / 'details-analysis.md'
    generate_markdown_report(details_list, categories, priorities, output_file)

    print(f"\n✓ Details analysis report generated: {output_file}")
    print(f"\nFound {len(details_list)} <details> tags across {len(categories)} visualization types")
    print("\nTop 5 priorities for skill development:")
    for i, item in enumerate(priorities[:5], 1):
        print(f"  {i}. {item['type']}: {item['count']} instances (priority score: {item['priority_score']})")

    return 0


if __name__ == "__main__":
    exit(main())
