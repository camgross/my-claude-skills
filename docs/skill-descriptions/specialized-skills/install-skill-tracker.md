# Install Skill Tracker

The install-skill-tracker skill automates the installation of a skill tracking
system for Claude Code projects. The system uses hooks to automatically log all
skill invocations, duration, token usage, and user prompts for later analysis.

## Key Capabilities

This skill installs tracking for:

- **Skill Usage**: Which skills are invoked and how often
- **Execution Duration**: Time spent in each skill
- **Token Usage**: API costs and efficiency metrics
- **User Prompts**: What triggers skill invocations
- **Session Tracking**: Group activities by session

## When to Use

Use this skill when:

- Setting up skill usage tracking in a new or existing project
- Wanting to analyze which skills are used most frequently
- Monitoring API costs and token usage
- Identifying time-consuming skills needing optimization
- Discovering patterns that could become new skills
- Tracking productivity gains from skill automation
- Understanding prompt cache effectiveness

## What Gets Installed

The skill creates this directory structure:

```
.claude/
├── hooks/
│   ├── track-prompts.sh      # Logs user prompts
│   ├── track-skill-start.sh  # Logs skill start events
│   └── track-skill-end.sh    # Logs skill completion
├── scripts/
│   └── analyze-usage.py      # Analysis script
└── activity-logs/
    └── (log files generated here)
```

## Hook Scripts

- **track-prompts.sh**: Logs user prompts with timestamps and session IDs
- **track-skill-start.sh**: Logs when skills begin execution
- **track-skill-end.sh**: Logs skill completion and calculates duration

## Analysis Capabilities

The analysis script provides:

- Most frequently used skills
- Average execution time per skill
- Token usage breakdown
- Peak usage times
- Common prompt patterns
- Cost estimation

## Workflow

1. Create directory structure (`.claude/hooks`, `.claude/scripts`, `.claude/activity-logs`)
2. Install hook scripts with proper permissions
3. Install analysis script
4. Configure hooks in settings.json
5. Verify installation

## Integration

This skill is typically used at project initialization to enable
ongoing tracking. The analysis data helps identify opportunities
for new skills and optimization of existing workflows.
