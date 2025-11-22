# Getting Started Using Intelligent Textbook Skills

This document guides you through the steps to install these intelligent textbook skills on your local computer so they are accessible to Claude Code. At the end of this chapter you should be able to run all the skills and book-building utilities in this project.

## Quick Start Summary

Here's a quick overview of the installation process:

1. **Set environment variables** - Configure `BK_HOME` and add `~/.local/bin` to your `PATH`
2. **Clone the repository** - Download the claude-skills repository
3. **Install book utilities** - Run `bk-install-scripts` to install book-building commands
4. **Install Claude skills** - Run `install-claude-skills.sh` to install skills globally
5. **Install /skills command** (optional) - Enable the `/skills` slash command in Claude Code
6. **Verify installation** - Check that everything is working correctly

Detailed instructions for each step are provided below.

## Installation Options

There are two installation options for Claude skills:

1. **Option 1: Global Skills** - The skills will be usable by all your projects. If you are creating multiple textbooks you should choose this option. (Recommended)
2. **Option 2: Project Skills** - If you are only working on a single textbook you can use this option. If you are using many other skills on other projects that might have conflicting skill names, this is a good choice.

The book-building utilities are always installed globally to `~/.local/bin`.

## Prerequisites

Before installing the skills, you must complete two important setup steps:

### 1. Set the BK_HOME Environment Variable

The `BK_HOME` environment variable must point to the root directory of your cloned claude-skills repository. Add this to your shell startup file:

**For Bash** (add to `~/.bashrc` or `~/.bash_profile`):
```bash
export BK_HOME=/Users/YOUR_USERNAME/Documents/ws/claude-skills
```

**For Zsh** (add to `~/.zshrc`):
```bash
export BK_HOME=/Users/YOUR_USERNAME/Documents/ws/claude-skills
```

**For Fish** (add to `~/.config/fish/config.fish`):
```fish
set -gx BK_HOME /Users/YOUR_USERNAME/Documents/ws/claude-skills
```

Replace `/Users/YOUR_USERNAME/Documents/ws/claude-skills` with the actual path where you cloned the repository.

### 2. Add ~/.local/bin to Your PATH

The book-building scripts will be installed to `~/.local/bin`. Ensure this directory is in your PATH:

**For Bash** (add to `~/.bashrc` or `~/.bash_profile`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**For Zsh** (add to `~/.zshrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**For Fish** (add to `~/.config/fish/config.fish`):
```fish
set -gx PATH $HOME/.local/bin $PATH
```

After adding these lines, restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc, depending on your shell
```

## Downloading the Skills

The best way to download the skills is to use the git clone command:

```sh
cd ~/Documents/ws  # or your preferred workspace directory
git clone https://github.com/dmccreary/claude-skills.git
```

This assumes that `ws` (workspace) is the directory where you check out your GitHub repositories. You can use any directory you prefer, just remember to update your `BK_HOME` environment variable accordingly.

## Installing Book-Building Scripts

Before installing the Claude skills, you should install the book-building utility scripts. These are scripts prefixed with `bk-` that help you manage and build intelligent textbooks.

Run the installation script:

```sh
cd $BK_HOME/scripts
./bk-install-scripts
```

This script will:
- Create symbolic links for all `bk-*` scripts in `$BK_HOME/scripts/`
- Place the links in `$HOME/.local/bin` for easy command-line access
- Verify that `$HOME/.local/bin` is in your PATH
- Display a list of all installed book utilities

After installation, you can use commands like `bk-book-status`, `bk-build`, and other book utilities from anywhere in your terminal.

## Installing Claude Skills

After you have downloaded the repository and installed the book-building scripts, you have two options for installing the Claude skills:

1. **Personal Level:** Install these skills for ALL your projects. (Recommended)
2. **Project Level:** Install these skills for a specific project

The first option will allow you to work on many different intelligent textbook projects without duplicating the skills on your local computer. It is highly recommended.

The only reason that you might want to use the second option for specific projects is if you are doing complex development such as creating different versions of these skills.

## Skill Installation for ALL Projects

We will do this by creating symbolic links from your home Claude directory (`~/.claude/skills/`) to the skills in the cloned repository.

Run the installation script:

```sh
cd $BK_HOME/scripts
./install-claude-skills.sh
```

You will see a log of all the skills that were correctly installed:

```
Created symlink: ~/.claude/skills/faq-generator -> /Users/dan/Documents/ws/claude-skills/skills/faq-generator
Created symlink: ~/.claude/skills/glossary-generator -> /Users/dan/Documents/ws/claude-skills/skills/glossary-generator
Created symlink: ~/.claude/skills/intelligent-textbook -> /Users/dan/Documents/ws/claude-skills/skills/intelligent-textbook
Created symlink: ~/.claude/skills/intelligent-textbook-creator -> /Users/dan/Documents/ws/claude-skills/skills/intelligent-textbook-creator
Created symlink: ~/.claude/skills/learning-graph-generator -> /Users/dan/Documents/ws/claude-skills/skills/learning-graph-generator
Created symlink: ~/.claude/skills/microsim-p5 -> /Users/dan/Documents/ws/claude-skills/skills/microsim-p5
Created symlink: ~/.claude/skills/moving-rainbow -> /Users/dan/Documents/ws/claude-skills/skills/moving-rainbow
Created symlink: ~/.claude/skills/quiz-generator -> /Users/dan/Documents/ws/claude-skills/skills/quiz-generator
```

## Getting Updates

These skills will be updated frequently. To install the latest release, just run git pull:

```sh
cd $BK_HOME
git pull
```

After pulling updates, you may need to re-run the installation scripts if new scripts or skills were added:

```sh
cd $BK_HOME/scripts
./bk-install-scripts      # For book-building utilities
./install-claude-skills.sh # For Claude skills
```

## Details of the Installation script

The script will create a set of symbolic link commands, one for each skill file in this repo.

```sh
#!/bin/bash

   # Create the target directory if it doesn't exist
   # CHANGE $HOME to be the project you are working on
   # $HOME = ~
   # $HOME = /User/NAME/projects/PROJECT_NAME/.claude/skills
   mkdir -p $HOME/.claude/skills

   # Get the absolute path of the skills directory
   SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills" && pwd)"

   # Create symbolic links for each skill folder
   for skill_dir in "$SKILLS_DIR"/*; do
       if [ -d "$skill_dir" ]; then
           skill_name=$(basename "$skill_dir")
           target_link="$HOME/.claude/skills/$skill_name"

           # Remove existing symlink if it exists
           if [ -L "$target_link" ]; then
               rm "$target_link"
           fi

           # Create the symbolic link
           ln -s "$skill_dir" "$target_link"
           echo "Created symlink: $HOME/.claude/skills/$skill_name -> $skill_dir"
       fi
   done

   echo "Done! All skill symlinks created in $HOME/.claude/skills"
```

If you want to change the links to work in your specific project, just change the
path where the links are created.

Change:

```sh
$HOME = ~
```

to be:

```sh
$HOME = /User/NAME/projects/PROJECT_NAME/.claude/skills
```

## Testing Your Skill List

```
What skills do you know about.  Check the ~/.claude/skills/ area.
```

Response:

```
You have 8 skills installed in ~/.claude/skills/:

  1. faq-generator - Generates FAQ content
  2. glossary-generator - Creates glossary entries
  3. intelligent-textbook - Works with intelligent textbook content
  4. intelligent-textbook-creator - Creates intelligent textbooks
  5. learning-graph-generator - Generates learning graphs
  6. microsim-p5 - Creates p5.js micro-simulations
  7. moving-rainbow - Creates moving rainbow animations
  8. quiz-generator - Generates quiz content
```

## Add the /skills Command

Claude Code allows you to add custom slash commands that execute scripts. You can add a `/skills` command that lists all available skills.

The custom slash command system works by:
1. Creating a command definition file in `~/.claude/commands/` (or `.claude/commands/` in your project)
2. Having an executable script in your `$PATH` that the command calls

The `list-skills.sh` script provides this functionality and is automatically installed to `~/.local/bin` when you run `bk-install-scripts`.

To enable the `/skills` slash command:

**Option 1: Install globally (recommended):**
```sh
cd $BK_HOME/scripts
./install-skills-command.sh
```

This will:
- Copy `list-skills.sh` to `~/.local/bin/` (if not already installed by bk-install-scripts)
- Copy `commands/skills.md` to `~/.claude/commands/skills.md`

**Option 2: Install for a specific project:**
```sh
mkdir -p .claude/commands
cp $BK_HOME/commands/skills.md .claude/commands/skills.md
```

Note: The `list-skills.sh` script must be in your `$PATH` (which it will be if you followed the prerequisites and ran `bk-install-scripts`).

## Sample Skill Slash Command Execution

I just type '/sk` into Claude Code and you should see the code listed

![](img/claude-code-skill-command.png)

**Result:**

```
Available Claude Skills (8 total)

  Educational Content Creation:
  - faq-generator (user) - Generates FAQs from course content
  - glossary-generator (user) - Creates ISO 11179-compliant glossaries
  - quiz-generator (user) - Creates Bloom's Taxonomy-aligned quizzes

  Intelligent Textbook Development:
  - intelligent-textbook (user) - Complete workflow for AI-generated textbooks
  - intelligent-textbook-creator (user) - Creates MkDocs Material textbooks (Level 2-5)
  - learning-graph-generator (user) - Generates 200-concept learning graphs

  Interactive Simulations:
  - microsim-p5 (user) - Creates p5.js educational MicroSims

  Hardware Projects:
  - moving-rainbow (user) - MicroPython for Raspberry Pi Pico NeoPixels

  All 8 skills are from your user directory (~/.claude/skills/). No project-specific skills found in .claude/skills/.

```

## Verifying Your Installation

After completing all installation steps, verify everything is working:

**1. Check environment variables:**
```sh
echo $BK_HOME
# Should output: /Users/YOUR_USERNAME/Documents/ws/claude-skills (or your path)

echo $PATH | grep -o "$HOME/.local/bin"
# Should output: /Users/YOUR_USERNAME/.local/bin
```

**2. Check book-building utilities:**
```sh
which bk-book-status
# Should output: /Users/YOUR_USERNAME/.local/bin/bk-book-status

bk-book-status --help  # Test a book utility
```

**3. Check Claude skills:**
```sh
ls ~/.claude/skills/
# Should list all installed skills (learning-graph-generator, glossary-generator, etc.)
```

**4. Test the /skills command in Claude Code:**
Type `/skills` in Claude Code and it should list all available skills.

## Configuring Permissions

The default Claude Code permission behavior is very strict and will prompt you for many operations. For efficient workflow when working on textbook projects, you can configure permissions to be more permissive.

**IMPORTANT**: Only use permissive settings when working in a safe, version-controlled directory (like a Git repository). This way, you can always revert unwanted changes.

Create or edit `.claude/settings.json` in your project directory:

```json
{
  "permissions": {
    "allow": [
      "Skill(*)",
      "Bash(*:*)",
      "FileSystem(read:./**/*.*,write:./**/*.*)"
    ],
    "deny": [],
    "ask": []
  }
}
```

This configuration:
- Allows all skills to run without prompting
- Allows all bash commands
- Allows reading and writing all files in the current project directory (`./**/*.*`)

Since your work is in a Git repository, you can always review changes with `git diff` and revert if needed.

## Troubleshooting

### BK_HOME not set error

If you get an error saying `BK_HOME environment variable is not set`:

1. Add the export to your shell startup file (see Prerequisites section)
2. Restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc`)
3. Verify with: `echo $BK_HOME`

### Scripts not found in PATH

If you get `command not found` when trying to run `bk-*` commands:

1. Check that `~/.local/bin` is in your PATH: `echo $PATH | grep .local/bin`
2. Add the export to your shell startup file (see Prerequisites section)
3. Restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc`)
4. Re-run the installation: `cd $BK_HOME/scripts && ./bk-install-scripts`

### Skills not showing up in Claude Code

If skills don't appear when you try to use them:

1. Check that symlinks were created: `ls -la ~/.claude/skills/`
2. Re-run the installation: `cd $BK_HOME/scripts && ./install-claude-skills.sh`
3. Restart Claude Code
4. Try listing skills with `/skills` command or ask Claude: "What skills do you have access to?"

### /skills command not working

If the `/skills` slash command doesn't work:

1. Check that `list-skills.sh` is in your PATH: `which list-skills.sh`
2. Check that the command file exists: `ls ~/.claude/commands/skills.md`
3. Re-run: `cd $BK_HOME/scripts && ./install-skills-command.sh`
4. Restart Claude Code

### Permission denied when running scripts

If you get permission denied errors:

1. Make scripts executable: `chmod +x $BK_HOME/scripts/*.sh`
2. For specific scripts: `chmod +x $BK_HOME/scripts/bk-install-scripts`

## Next Steps

Once you have successfully installed the skills and utilities, you can:

1. **Create a new intelligent textbook project** - Use the `intelligent-textbook-creator` skill
2. **Generate a learning graph** - Use the `learning-graph-generator` skill
3. **Create interactive simulations** - Use the `microsim-p5` skill
4. **Generate course content** - Use the `glossary-generator`, `quiz-generator`, and `faq-generator` skills

For detailed documentation on each skill, visit the [skills documentation](https://dmccreary.github.io/claude-skills/) or use the `/skills` command in Claude Code.



