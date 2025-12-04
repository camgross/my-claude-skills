#!/usr/bin/env python3
"""Analyze skill usage logs to identify patterns, performance metrics, and token usage."""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import sys
from io import StringIO

def load_jsonl(filepath):
    """Load JSONL file into list of dicts."""
    if not filepath.exists():
        return []
    with open(filepath) as f:
        return [json.loads(line) for line in f if line.strip()]

def format_duration(seconds):
    """Format duration in human-readable format."""
    if seconds == "unknown" or seconds is None:
        return "unknown"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def format_tokens(count):
    """Format token count with K/M suffix."""
    if count is None or count == "null":
        return "N/A"
    count = int(count)
    if count >= 1_000_000:
        return f"{count/1_000_000:.1f}M"
    elif count >= 1_000:
        return f"{count/1_000:.1f}K"
    return str(count)

def correlate_prompts_with_skills(prompts, skill_events):
    """Match user prompts with skill invocations by session ID and timestamp."""
    # Index prompts by session and epoch for better matching
    prompts_by_session = defaultdict(list)
    for prompt in prompts:
        prompts_by_session[prompt['session']].append({
            'epoch': int(prompt['epoch']),
            'prompt': prompt['prompt'],
            'timestamp': prompt['timestamp']
        })

    # Sort prompts by epoch within each session
    for session in prompts_by_session:
        prompts_by_session[session].sort(key=lambda x: x['epoch'])

    # Build a map of start events to calculate duration
    start_events = {}
    for event in skill_events:
        if event['event'] == 'start':
            key = f"{event['session']}-{event['skill']}-{event['epoch']}"
            start_events[key] = int(event['epoch'])

    # Correlate skill events with nearest preceding prompt
    correlated = []
    for event in skill_events:
        if event['event'] != 'end':
            continue

        session = event['session']
        skill_epoch = int(event['epoch'])

        # Find the most recent prompt before this skill event
        best_prompt = "Unknown prompt"
        prompt_epoch = None
        session_prompts = prompts_by_session.get(session, [])
        for p in reversed(session_prompts):
            if p['epoch'] <= skill_epoch:
                best_prompt = p['prompt']
                prompt_epoch = p['epoch']
                break

        # Get duration from the event, or calculate from start event
        duration = event.get('duration_seconds', 'unknown')
        if duration == 'unknown' or duration == '0' or duration == 0:
            # Try to find matching start event
            for key, start_epoch in start_events.items():
                if key.startswith(f"{session}-{event['skill']}-"):
                    if start_epoch <= skill_epoch:
                        duration = skill_epoch - start_epoch
                        break

        # Calculate time from prompt to skill completion
        prompt_to_completion = None
        if prompt_epoch:
            prompt_to_completion = skill_epoch - prompt_epoch

        correlated.append({
            'skill': event['skill'],
            'prompt': best_prompt,
            'duration': duration,
            'prompt_to_completion': prompt_to_completion,
            'timestamp': event['timestamp'],
            'epoch': skill_epoch,
            'session': session,
            'input_tokens': event.get('input_tokens'),
            'output_tokens': event.get('output_tokens'),
            'total_tokens': event.get('total_tokens'),
            'cache_read_tokens': event.get('cache_read_tokens'),
            'cache_creation_tokens': event.get('cache_creation_tokens')
        })

    return correlated


def analyze_prompt_timing(prompts):
    """Analyze timing between prompts to understand session activity."""
    if len(prompts) < 2:
        return []

    # Sort by epoch
    sorted_prompts = sorted(prompts, key=lambda x: int(x['epoch']))

    timing_data = []
    for i in range(1, len(sorted_prompts)):
        prev = sorted_prompts[i-1]
        curr = sorted_prompts[i]

        time_diff = int(curr['epoch']) - int(prev['epoch'])

        timing_data.append({
            'timestamp': curr['timestamp'],
            'prompt': curr['prompt'][:80],
            'seconds_since_prev': time_diff,
            'session': curr['session']
        })

    return timing_data

def generate_report(log_dir, project_dir=None):
    """Generate skill usage report and return as string."""
    log_dir = Path(log_dir)
    output = StringIO()

    def write(text=""):
        output.write(text + "\n")

    # Load logs
    prompts = load_jsonl(log_dir / "prompts.jsonl")
    skill_events = load_jsonl(log_dir / "skill-usage.jsonl")

    if not skill_events:
        write("No skill usage data found yet.")
        write(f"Logs will be created in: {log_dir}")
        write("\nUse skills in Claude Code and they'll be tracked automatically.")
        return output.getvalue(), False

    # Correlate prompts with skills
    correlated = correlate_prompts_with_skills(prompts, skill_events)

    write("# Skill Usage Report")
    write()
    write(f"**Project:** {project_dir.name if project_dir else 'Unknown'}<br/>")
    write(f"**Log directory:** `{log_dir}`<br/>")
    write(f"**Total skill invocations:** {len(correlated)}<br/>")
    write(f"**Report generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    write()

    # Skill frequency analysis
    skill_counts = Counter(entry['skill'] for entry in correlated)
    write("## Skill Usage Summary")
    write()
    for skill, count in skill_counts.most_common():
        write(f"- **{skill}**: {count}x")

    # Token usage analysis
    write()
    write("## Token Usage by Skill")
    write()
    skill_tokens = defaultdict(lambda: {
        'input': 0, 'output': 0, 'total': 0,
        'cache_read': 0, 'cache_creation': 0, 'count': 0,
        'total_time': 0, 'time_count': 0
    })

    total_tokens_all = 0
    total_cache_read = 0
    total_cache_creation = 0

    for entry in correlated:
        skill = entry['skill']
        skill_tokens[skill]['count'] += 1

        if entry.get('total_tokens') and entry['total_tokens'] != 'null':
            tokens = int(entry['total_tokens'])
            skill_tokens[skill]['total'] += tokens
            total_tokens_all += tokens

        if entry.get('input_tokens') and entry['input_tokens'] != 'null':
            skill_tokens[skill]['input'] += int(entry['input_tokens'])

        if entry.get('output_tokens') and entry['output_tokens'] != 'null':
            skill_tokens[skill]['output'] += int(entry['output_tokens'])

        if entry.get('cache_read_tokens') and entry['cache_read_tokens'] != 'null':
            cache_read = int(entry['cache_read_tokens'])
            skill_tokens[skill]['cache_read'] += cache_read
            total_cache_read += cache_read

        if entry.get('cache_creation_tokens') and entry['cache_creation_tokens'] != 'null':
            cache_create = int(entry['cache_creation_tokens'])
            skill_tokens[skill]['cache_creation'] += cache_create
            total_cache_creation += cache_create

        # Track timing from prompt to completion
        if entry.get('prompt_to_completion') and entry['prompt_to_completion'] > 0:
            skill_tokens[skill]['total_time'] += entry['prompt_to_completion']
            skill_tokens[skill]['time_count'] += 1

    write("| Skill | Invocations | Total Tokens | Avg Time | Cache Read | Cache Creation |")
    write("|-------|-------------|--------------|----------|------------|----------------|")

    # Sort by total tokens descending
    sorted_skills = sorted(skill_tokens.items(), key=lambda x: x[1]['total'], reverse=True)
    for skill, data in sorted_skills:
        avg_time = format_duration(data['total_time'] // data['time_count']) if data['time_count'] > 0 else 'N/A'
        write(f"| {skill} | {data['count']}x | {format_tokens(data['total'])} | {avg_time} | {format_tokens(data['cache_read'])} | {format_tokens(data['cache_creation'])} |")

    # Cache efficiency summary
    cache_hit_ratio = 0
    if total_tokens_all > 0:
        cache_hit_ratio = (total_cache_read / total_tokens_all) * 100
        write()
        write("## Token Summary")
        write()
        write(f"| Metric | Value |")
        write(f"|--------|-------|")
        write(f"| Total tokens processed | {format_tokens(total_tokens_all)} |")
        write(f"| Cache reads | {format_tokens(total_cache_read)} ({cache_hit_ratio:.1f}%) |")
        write(f"| Cache creations | {format_tokens(total_cache_creation)} |")
        write(f"| Estimated API cost | ${total_tokens_all * 0.000003:.2f} |")

    # Timing summary
    total_time = sum(e.get('prompt_to_completion', 0) or 0 for e in correlated)
    timed_skills = [e for e in correlated if e.get('prompt_to_completion') and e['prompt_to_completion'] > 0]
    if timed_skills:
        avg_time = total_time // len(timed_skills)
        write()
        write("## Timing Summary")
        write()
        write(f"| Metric | Value |")
        write(f"|--------|-------|")
        write(f"| Total time in skills | {format_duration(total_time)} |")
        write(f"| Average time per skill | {format_duration(avg_time)} |")
        write(f"| Skills with timing data | {len(timed_skills)} of {len(correlated)} |")

    # Common prompts that trigger skills
    write()
    write("## Common Prompts")
    write()
    prompt_counts = Counter(entry['prompt'][:100] for entry in correlated if entry['prompt'] != "Unknown prompt")
    shown = 0
    for prompt, count in prompt_counts.most_common(10):
        if count > 1 or shown < 5:
            truncated = prompt[:80] + "..." if len(prompt) > 80 else prompt
            write(f"- {count}x: \"{truncated}\"")
            shown += 1
        if shown >= 10:
            break

    # Recent skill usage table with timing
    write()
    write("## Recent Skill Usage")
    write()
    write("| Timestamp | Skill | Tokens | Time from Prompt | Prompt (truncated) |")
    write("|-----------|-------|--------|------------------|---------------------|")
    for entry in sorted(correlated, key=lambda x: x['timestamp'], reverse=True)[:20]:
        tokens = format_tokens(entry.get('total_tokens'))
        prompt_short = entry['prompt'][:50].replace('|', '\\|').replace('\n', ' ')
        time_from_prompt = format_duration(entry.get('prompt_to_completion')) if entry.get('prompt_to_completion') else 'N/A'
        write(f"| {entry['timestamp']} | {entry['skill']} | {tokens} | {time_from_prompt} | {prompt_short}... |")

    # Session activity timing
    prompt_timing = analyze_prompt_timing(prompts)
    if prompt_timing:
        write()
        write("## Session Activity Timeline")
        write()
        write("| Timestamp | Time Since Previous | Prompt (truncated) |")
        write("|-----------|---------------------|---------------------|")
        for entry in prompt_timing[-15:]:  # Last 15 entries
            time_since = format_duration(entry['seconds_since_prev'])
            prompt_short = entry['prompt'][:60].replace('|', '\\|').replace('\n', ' ')
            write(f"| {entry['timestamp']} | {time_since} | {prompt_short}... |")

    # Insights
    write()
    write("## Insights")
    write()

    # Find frequently used skills
    frequent_skills = [s for s, c in skill_counts.items() if c >= 3]
    if frequent_skills:
        write("### Frequently Used Skills")
        write()
        for skill in frequent_skills[:5]:
            count = skill_counts[skill]
            tokens = skill_tokens[skill]['total']
            write(f"- **{skill}** ({count}x, {format_tokens(tokens)} tokens)")
        write()

    # Token-heavy skills
    if sorted_skills:
        write("### Most Token-Intensive Skills")
        write()
        for skill, data in sorted_skills[:3]:
            avg_tokens = data['total'] / data['count'] if data['count'] > 0 else 0
            write(f"- **{skill}**: {format_tokens(data['total'])} total ({format_tokens(avg_tokens)} avg)")
        write()

    # Cache efficiency
    if total_tokens_all > 0:
        write("### Cache Efficiency")
        write()
        if cache_hit_ratio > 70:
            write(f"✅ Good cache utilization ({cache_hit_ratio:.1f}% cache hits)")
        elif cache_hit_ratio > 40:
            write(f"⚠️ Moderate cache utilization ({cache_hit_ratio:.1f}% cache hits)")
        else:
            write(f"❌ Low cache utilization ({cache_hit_ratio:.1f}% cache hits)")

    return output.getvalue(), True

def generate_html_report(markdown_content, project_name="Skill Usage"):
    """Convert markdown report to styled HTML."""
    import re

    # Basic markdown to HTML conversion
    html_content = markdown_content

    # Convert headers
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

    # Convert bold
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

    # Convert inline code
    html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)

    # Convert line breaks
    html_content = html_content.replace('<br/>', '<br>')

    # Convert tables
    lines = html_content.split('\n')
    in_table = False
    new_lines = []
    for line in lines:
        if line.startswith('|') and line.endswith('|'):
            if not in_table:
                new_lines.append('<table>')
                in_table = True
            # Skip separator lines
            if '---|' in line:
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not any('<th>' in l for l in new_lines[-5:] if '<t' in l):
                # First row is header
                new_lines.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                new_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_table:
                new_lines.append('</table>')
                in_table = False
            new_lines.append(line)
    if in_table:
        new_lines.append('</table>')
    html_content = '\n'.join(new_lines)

    # Convert list items
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)

    # Wrap consecutive <li> elements in <ul>
    html_content = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html_content)

    # Convert paragraphs (lines that aren't already HTML)
    lines = html_content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<') and not stripped.endswith('>'):
            new_lines.append(f'<p>{line}</p>')
        else:
            new_lines.append(line)
    html_content = '\n'.join(new_lines)

    # Full HTML document with styling
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Skill Usage Report</title>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        h1 {{
            font-size: 2rem;
            color: var(--primary-dark);
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--primary);
        }}

        h2 {{
            font-size: 1.5rem;
            color: var(--text);
            margin: 2rem 0 1rem;
            padding-bottom: 0.25rem;
            border-bottom: 2px solid var(--border);
        }}

        h3 {{
            font-size: 1.2rem;
            color: var(--text-muted);
            margin: 1.5rem 0 0.75rem;
        }}

        p {{
            margin: 0.5rem 0;
        }}

        code {{
            background: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 0.9em;
            color: var(--primary-dark);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            background: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        th {{
            background: var(--primary);
            color: white;
            font-weight: 600;
            text-align: left;
            padding: 0.75rem 1rem;
        }}

        td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: #f8fafc;
        }}

        ul {{
            list-style: none;
            margin: 1rem 0;
        }}

        li {{
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }}

        li::before {{
            content: "•";
            color: var(--primary);
            font-weight: bold;
            position: absolute;
            left: 0;
        }}

        strong {{
            color: var(--primary-dark);
        }}

        .metric-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}

        .metric-card {{
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        .footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 0.875rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
        <div class="footer">
            Generated by Claude Skills Analyzer
        </div>
    </div>
</body>
</html>'''

    return html


def analyze_skill_usage(log_dir, output_file=None, project_dir=None, output_format='markdown'):
    """Analyze skill usage patterns and generate report."""
    report, success = generate_report(log_dir, project_dir)

    # Generate HTML if requested
    if output_format == 'html':
        project_name = project_dir.name if project_dir else 'Unknown'
        html_report = generate_html_report(report, project_name)

        # Write HTML to file
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(html_report)
            print(f"📄 HTML report saved to: {output_path}")

        return success

    # Default: print markdown to stdout
    print(report)

    # Write markdown to file if specified
    if output_file and success:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {output_path}")

    return success

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze skill usage logs')
    parser.add_argument('log_dir', nargs='?', help='Log directory path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-p', '--project', help='Project directory (for context)')
    parser.add_argument('--html', action='store_true', help='Generate HTML report instead of markdown')

    args = parser.parse_args()

    # Determine log directory
    if args.log_dir:
        log_dir = Path(args.log_dir)
    else:
        log_dir = Path.cwd() / ".claude" / "activity-logs"

    # Determine project directory
    if args.project:
        project_dir = Path(args.project)
    elif args.log_dir:
        # Assume log_dir is inside project/.claude/activity-logs
        project_dir = Path(args.log_dir).parent.parent.parent
    else:
        project_dir = Path.cwd()

    # Determine output file
    output_file = None
    if args.output:
        output_file = args.output
    elif not args.html:
        # Default: write to project's docs/learning-graph/skill-usage.md (only for markdown)
        default_output = project_dir / "docs" / "learning-graph" / "skill-usage.md"
        if default_output.parent.exists():
            output_file = default_output

    if not log_dir.exists():
        print(f"Log directory not found: {log_dir}")
        print("\nHooks will create this directory on first skill usage.")
        print("\nTip: You can specify a log directory as an argument:")
        print(f"  {sys.argv[0]} /path/to/.claude/activity-logs")
        return

    output_format = 'html' if args.html else 'markdown'
    analyze_skill_usage(log_dir, output_file, project_dir, output_format)

if __name__ == "__main__":
    main()
