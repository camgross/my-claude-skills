#!/usr/bin/env python3
"""
MicroSim Quality Report Generator

Generates a comprehensive quality report for all MicroSims in the repository,
identifying quality scores and providing improvement recommendations.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# Base paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
SIMS_DIR = REPO_ROOT / 'docs' / 'sims'
OUTPUT_FILE = REPO_ROOT / 'docs' / 'learning-graph' / 'microsim-quality-report.md'

# Quality score rubric (14 tests, 100 points total)
RUBRIC = {
    'title': {'points': 2, 'desc': 'Level 1 markdown header'},
    'main_html': {'points': 10, 'desc': 'main.html file exists'},
    'yaml_metadata': {'points': 3, 'desc': 'YAML frontmatter with title and description'},
    'image_metadata': {'points': 5, 'desc': 'Image metadata for social preview (image: and og:image)'},
    'metadata_json': {'points': 10, 'desc': 'metadata.json file exists'},
    'metadata_valid': {'points': 20, 'desc': 'metadata.json passes Dublin Core schema validation'},
    'iframe': {'points': 10, 'desc': 'iframe element with src="main.html"'},
    'fullscreen_button': {'points': 5, 'desc': 'Fullscreen link button'},
    'iframe_example': {'points': 5, 'desc': 'Copy-paste iframe example in HTML code block'},
    'image_file': {'points': 5, 'desc': 'PNG screenshot file exists'},
    'overview': {'points': 5, 'desc': 'Overview/Description section'},
    'lesson_plan': {'points': 10, 'desc': 'Comprehensive lesson plan'},
    'references': {'points': 5, 'desc': 'References section with links'},
    'type_specific': {'points': 5, 'desc': 'Library-specific documentation (e.g., p5.js editor link)'}
}

def get_quality_score(index_path):
    """Extract quality score from index.md YAML frontmatter"""
    if not index_path.exists():
        return None

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read(500)
        match = re.search(r'quality_score:\s*(\d+)', content)
        if match:
            return int(match.group(1))
    return None

def check_file_exists(microsim_dir, filename):
    """Check if a file exists in the MicroSim directory"""
    return (microsim_dir / filename).exists()

def check_yaml_metadata(index_path):
    """Check if YAML frontmatter has title and description"""
    if not index_path.exists():
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read(1000)
        if not content.startswith('---'):
            return False

        # Check for title and description
        has_title = 'title:' in content
        has_description = 'description:' in content
        return has_title and has_description

def check_image_metadata(index_path):
    """Check if YAML has image and og:image fields"""
    if not index_path.exists():
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read(1000)
        has_image = 'image:' in content
        has_og_image = 'og:image' in content
        return has_image and has_og_image

def check_content_element(index_path, pattern):
    """Check if index.md contains a specific pattern"""
    if not index_path.exists():
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return pattern in content

def validate_metadata_json(metadata_path):
    """Validate that metadata.json has required Dublin Core fields"""
    if not metadata_path.exists():
        return False

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        required_fields = [
            'title', 'description', 'creator', 'date',
            'subject', 'type', 'format', 'language', 'rights'
        ]

        return all(field in metadata for field in required_fields)
    except (json.JSONDecodeError, Exception):
        return False

def detect_library(main_html_path):
    """Detect which JavaScript library is used"""
    if not main_html_path.exists():
        return "Unknown"

    with open(main_html_path, 'r', encoding='utf-8') as f:
        content = f.read(2000).lower()

    if 'p5.js' in content or 'p5.min.js' in content:
        return 'p5.js'
    elif 'mermaid' in content:
        return 'Mermaid'
    elif 'vis-network' in content:
        return 'vis-network'
    elif 'chart.js' in content or 'chart.min.js' in content:
        return 'Chart.js'
    elif 'plotly' in content:
        return 'Plotly.js'
    elif 'leaflet' in content:
        return 'Leaflet'
    else:
        return 'HTML/CSS/JS'

def analyze_microsim(microsim_dir):
    """Analyze a single MicroSim and return quality details"""
    microsim_name = microsim_dir.name
    index_path = microsim_dir / 'index.md'
    main_html_path = microsim_dir / 'main.html'
    metadata_path = microsim_dir / 'metadata.json'

    # Get current score
    score = get_quality_score(index_path)
    if score is None:
        score = 0

    # Analyze what's present
    checks = {
        'title': check_content_element(index_path, '# '),
        'main_html': check_file_exists(microsim_dir, 'main.html'),
        'yaml_metadata': check_yaml_metadata(index_path),
        'image_metadata': check_image_metadata(index_path),
        'metadata_json': check_file_exists(microsim_dir, 'metadata.json'),
        'metadata_valid': validate_metadata_json(metadata_path),
        'iframe': check_content_element(index_path, '<iframe') and check_content_element(index_path, 'main.html'),
        'fullscreen_button': check_content_element(index_path, '.md-button'),
        'iframe_example': check_content_element(index_path, '```html') and check_content_element(index_path, 'github.io'),
        'image_file': len(list(microsim_dir.glob('*.png'))) > 0,
        'overview': check_content_element(index_path, '## Overview') or check_content_element(index_path, '## Description'),
        'lesson_plan': check_content_element(index_path, '## Lesson Plan'),
        'references': check_content_element(index_path, '## References'),
        'type_specific': False  # Will check based on library
    }

    # Check type-specific based on library
    library = detect_library(main_html_path)
    if library == 'p5.js':
        checks['type_specific'] = check_content_element(index_path, 'editor.p5js.org')
    else:
        # For non-p5.js, consider it met if there's library-specific content
        checks['type_specific'] = True  # Generous for non-p5.js

    # Identify missing items
    missing = []
    for key, present in checks.items():
        if not present:
            missing.append(key)

    return {
        'name': microsim_name,
        'score': score,
        'library': library,
        'checks': checks,
        'missing': missing
    }

def generate_improvement_notes(analysis):
    """Generate specific improvement recommendations"""
    if analysis['score'] == 100:
        return ""

    missing = analysis['missing']
    if not missing:
        return "Score discrepancy - manual review needed"

    notes = []

    # Group by priority
    critical = []
    important = []
    nice_to_have = []

    for item in missing:
        points = RUBRIC[item]['points']
        desc = RUBRIC[item]['desc']

        if points >= 10:
            critical.append(f"**{desc}** (+{points} pts)")
        elif points >= 5:
            important.append(f"{desc} (+{points} pts)")
        else:
            nice_to_have.append(f"{desc} (+{points} pts)")

    if critical:
        notes.append("**Critical**: " + ", ".join(critical))
    if important:
        notes.append("**Important**: " + ", ".join(important))
    if nice_to_have:
        notes.append("Polish: " + ", ".join(nice_to_have))

    return "; ".join(notes)

def generate_report():
    """Generate the complete MicroSim quality report"""
    print("Generating MicroSim Quality Report...")
    print(f"Scanning: {SIMS_DIR}")

    # Collect all MicroSims
    microsims = []
    for item in sorted(SIMS_DIR.iterdir()):
        if item.is_dir() and (item / 'main.html').exists():
            analysis = analyze_microsim(item)
            microsims.append(analysis)

    print(f"Found {len(microsims)} MicroSims")

    # Sort by score (descending)
    microsims.sort(key=lambda x: (-x['score'], x['name']))

    # Calculate statistics
    total = len(microsims)
    perfect = sum(1 for m in microsims if m['score'] == 100)
    excellent = sum(1 for m in microsims if 90 <= m['score'] < 100)
    good = sum(1 for m in microsims if 85 <= m['score'] < 90)
    fair = sum(1 for m in microsims if 70 <= m['score'] < 85)
    needs_work = sum(1 for m in microsims if m['score'] < 70)
    avg_score = sum(m['score'] for m in microsims) / total if total > 0 else 0

    # Generate markdown report
    lines = []
    lines.append("# MicroSim Quality Report")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Summary statistics
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append(f"- **Total MicroSims**: {total}")
    lines.append(f"- **Average Quality Score**: {avg_score:.1f}/100")
    lines.append("")
    lines.append("### Quality Distribution")
    lines.append("")
    lines.append(f"| Category | Count | Percentage |")
    lines.append(f"|----------|-------|------------|")
    lines.append(f"| 🏆 Perfect (100) | {perfect} | {perfect/total*100:.1f}% |")
    lines.append(f"| ✓ Excellent (90-99) | {excellent} | {excellent/total*100:.1f}% |")
    lines.append(f"| ✓ Good (85-89) | {good} | {good/total*100:.1f}% |")
    lines.append(f"| ○ Fair (70-84) | {fair} | {fair/total*100:.1f}% |")
    lines.append(f"| ✗ Needs Work (<70) | {needs_work} | {needs_work/total*100:.1f}% |")
    lines.append("")

    # Detailed table
    lines.append("## Detailed Quality Report")
    lines.append("")
    lines.append("| MicroSim Name | Score | Library | Improvement Notes |")
    lines.append("|---------------|-------|---------|-------------------|")

    for m in microsims:
        name = m['name']
        score = m['score']
        library = m['library']
        notes = generate_improvement_notes(m)

        # Add status emoji
        if score == 100:
            status = "🏆"
        elif score >= 90:
            status = "✓"
        elif score >= 85:
            status = "✓"
        elif score >= 70:
            status = "○"
        else:
            status = "✗"

        lines.append(f"| {status} {name} | {score}/100 | {library} | {notes} |")

    lines.append("")

    # Recommendations section
    lines.append("## Recommendations")
    lines.append("")

    if perfect == total:
        lines.append("🎉 **All MicroSims have achieved perfect quality scores!**")
    else:
        lines.append("### Quick Wins")
        lines.append("")

        # MicroSims close to 100
        close_to_perfect = [m for m in microsims if 90 <= m['score'] < 100]
        if close_to_perfect:
            lines.append(f"**{len(close_to_perfect)} MicroSims** are 90-99/100 and need minor improvements:")
            lines.append("")
            for m in close_to_perfect[:5]:  # Show top 5
                missing_items = [RUBRIC[item]['desc'] for item in m['missing']]
                lines.append(f"- **{m['name']}** ({m['score']}/100): Add {', '.join(missing_items[:2])}")
            if len(close_to_perfect) > 5:
                lines.append(f"- _(and {len(close_to_perfect) - 5} more)_")
            lines.append("")

        # MicroSims needing lesson plans
        need_lesson_plans = [m for m in microsims if 'lesson_plan' in m['missing']]
        if need_lesson_plans:
            lines.append(f"### Lesson Plans Needed ({len(need_lesson_plans)} MicroSims)")
            lines.append("")
            lines.append(f"Adding lesson plans (+10 points each) would significantly improve quality:")
            lines.append("")
            for m in need_lesson_plans[:5]:
                potential = m['score'] + 10
                lines.append(f"- **{m['name']}**: {m['score']} → {potential}/100")
            if len(need_lesson_plans) > 5:
                lines.append(f"- _(and {len(need_lesson_plans) - 5} more)_")
            lines.append("")

        # Critical issues
        critical_issues = [m for m in microsims if m['score'] < 70]
        if critical_issues:
            lines.append(f"### Critical Attention Needed ({len(critical_issues)} MicroSims)")
            lines.append("")
            lines.append("These MicroSims have scores below 70/100 and require immediate attention:")
            lines.append("")
            for m in critical_issues:
                lines.append(f"- **{m['name']}** ({m['score']}/100)")
            lines.append("")

    # Quality rubric reference
    lines.append("## Quality Rubric Reference")
    lines.append("")
    lines.append("| Element | Points | Description |")
    lines.append("|---------|--------|-------------|")

    for key, value in RUBRIC.items():
        lines.append(f"| {key.replace('_', ' ').title()} | {value['points']} | {value['desc']} |")

    lines.append("")
    lines.append("**Total Possible Score**: 100 points")
    lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*This report was automatically generated by the `bk-microsim-quality-report-generator` script.*")
    lines.append("")

    # Write report
    report_content = "\n".join(lines)

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"✓ Report written to: {OUTPUT_FILE}")
    print(f"  Total MicroSims: {total}")
    print(f"  Perfect Scores: {perfect}")
    print(f"  Average Score: {avg_score:.1f}/100")

    return OUTPUT_FILE

if __name__ == '__main__':
    try:
        output_path = generate_report()
        print(f"\nSuccess! View report at:")
        print(f"  {output_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
