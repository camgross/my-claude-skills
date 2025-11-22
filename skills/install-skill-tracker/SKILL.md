---
name: install-skill-tracker
description: This skill installs a complete Claude Code skill tracking system using hooks to automatically log skill usage, execution duration, and user prompts for later analysis. Use this skill when setting up activity tracking in a Claude Code project to identify patterns and opportunities for new skills.
---

# Install Skill Tracker

## Overview

This skill automates the installation of a skill tracking system for Claude Code projects. The system uses Claude Code hooks to automatically log all skill invocations, their duration, and the prompts that triggered them. This data enables pattern analysis to identify frequently repeated workflows that could become new skills.

## When to Use This Skill

Use this skill when:
- Setting up skill usage tracking in a new or existing Claude Code project
- Wanting to analyze which skills are used most frequently
- Identifying time-consuming skills that may need optimization
- Discovering patterns in work that could be automated with new skills
- Tracking productivity gains from skill automation

## Installation Workflow

### Step 1: Create Directory Structure

Create the necessary directories for hooks, scripts, and logs:

```bash
mkdir -p .claude/hooks .claude/scripts .claude/activity-logs
```

### Step 2: Install Hook Scripts

Copy the hook scripts from this skill's `scripts/` directory to `.claude/hooks/`:

- **track-prompts.sh** - Logs user prompts with timestamps and session IDs
- **track-skill-start.sh** - Logs when skills begin execution
- **track-skill-end.sh** - Logs skill completion and calculates duration

Make the hook scripts executable:

```bash
chmod +x .claude/hooks/*.sh
```

### Step 3: Install Analysis Script

Copy the analysis script from this skill's `scripts/` directory to `.claude/scripts/`:

- **analyze-skills.py** - Processes logs and generates usage reports

Make the analysis script executable:

```bash
chmod +x .claude/scripts/analyze-skills.py
```

### Step 4: Configure Hooks

Copy the `settings.json` template from this skill's `assets/` directory to `.claude/settings.json`. This configuration registers three hooks:

- **UserPromptSubmit** - Captures all user prompts
- **PreToolUse** (Skill matcher) - Logs skill start times
- **PostToolUse** (Skill matcher) - Logs skill completion times

### Step 5: Add Documentation

Copy the `README.md` from this skill's `assets/` directory to `.claude/README.md`. This provides documentation on:
- What data gets tracked
- How the tracking system works
- How to analyze the logs
- Customization options
- Troubleshooting guide

### Step 6: Update .gitignore

Add the activity logs directory to `.gitignore` to prevent tracking log files:

```bash
echo ".claude/activity-logs/" >> .gitignore
echo ".claude/settings.local.json" >> .gitignore
```

### Step 7: Verify Installation

Confirm all files are in place:

```bash
ls -la .claude/hooks/
ls -la .claude/scripts/
cat .claude/settings.json
```

## Using the Tracking System

### Automatic Logging

After installation, the tracking system operates automatically:
1. Use skills normally through Claude Code
2. Each skill invocation is logged with timestamp, duration, and triggering prompt
3. Logs accumulate in `.claude/activity-logs/` as JSONL files

### Analyzing Usage Data

Run the analysis script to generate insights:

```bash
.claude/scripts/analyze-skills.py
```

The analysis report includes:
- **Skill frequency** - Most commonly used skills
- **Performance metrics** - Average and total duration per skill
- **Prompt patterns** - Common prompts that trigger skills
- **Usage history** - Recent skill invocations with details
- **Insights** - Suggestions for optimization and new skill opportunities

### Example Analysis Output

```
# Skill Usage Analysis Report

**Total skill invocations:** 15

## Most Used Skills

- **microsim-p5**: 7x
- **learning-graph-generator**: 5x
- **glossary-generator**: 3x

## Skill Performance (Average Duration)

- **learning-graph-generator**
  - Average: 2m 34s
  - Total time: 12m 50s
  - Invocations: 5x

## Insights & Suggestions

### Frequently Used Skills
- **microsim-p5** (7x): Could benefit from optimization or templates

### Total Time Automated
Skills have automated **45m 23s** of work
```

## Log Data Format

The system creates two JSONL log files:

### prompts.jsonl
Logs user prompts with session correlation:
```json
{"timestamp": "2025-11-22 14:23:45", "epoch": "1732299825", "session": "abc123", "prompt": "create a learning graph"}
```

### skill-usage.jsonl
Logs skill start/end events with duration:
```json
{"timestamp": "2025-11-22 14:23:46", "epoch": "1732299826", "session": "abc123", "skill": "learning-graph-generator", "event": "start"}
{"timestamp": "2025-11-22 14:26:20", "epoch": "1732299980", "session": "abc123", "skill": "learning-graph-generator", "event": "end", "duration_seconds": "154"}
```

## Customization Options

### Global vs Project-Specific Tracking

**Current setup:** Project-specific tracking (logs in `.claude/activity-logs/`)

**For global tracking across all projects:**
1. Move `settings.json` to `~/.claude/settings.json`
2. Update `LOG_DIR` in hook scripts to `~/.claude/activity-logs`
3. Analysis script will aggregate data from all projects

### Tracking Additional Metrics

Extend the hook scripts to capture:
- All tool usage (not just skills)
- Error rates and failures
- Custom metadata fields
- Project-specific context

Hooks receive full JSON context via stdin with tool names, parameters, and outputs.

## Privacy & Security

All tracking data is stored locally:
- No data transmission to external services
- Logs remain in `.claude/activity-logs/`
- Automatically excluded from git via `.gitignore`

To delete all tracking data:
```bash
rm -rf .claude/activity-logs
```

## Troubleshooting

### Hooks Not Executing

Verify hook configuration:
```bash
cat .claude/settings.json
```

Check script permissions:
```bash
ls -l .claude/hooks/*.sh
```

### No Log Files Created

Ensure directories exist:
```bash
mkdir -p .claude/activity-logs
```

Use a skill to trigger logging, then check:
```bash
ls -la .claude/activity-logs/
```

### Analysis Shows No Data

Logs are created only after skill usage. Run any skill first, then execute the analysis script.

## Resources

This skill includes:

### scripts/
- **track-prompts.sh** - Bash hook to log user prompts
- **track-skill-start.sh** - Bash hook to log skill start times
- **track-skill-end.sh** - Bash hook to log skill completion and duration
- **analyze-skills.py** - Python script to analyze logs and generate reports

### assets/
- **settings.json** - Hook configuration template for `.claude/settings.json`
- **README.md** - Complete documentation for the tracking system
