# Claude Skills

A collection of reusable skills for Claude Code.

## Repository Structure

```
skills/
 │   ├── learning-graphs/
 │   │   ├── learning-graph-generator/
 │   │   │   ├── SKILL.md
 │   │   │   ├── csv-to-json.py
 │   │   │   └── ...
 │   │   ├── taxonomy-analyzer/
 │   │   └── graph-validator/
 │   ├── documentation/
 │   │   ├── markdown-formatter/
 │   │   └── api-doc-generator/
 │   └── data-science/
 │       ├── csv-analyzer/
 │       └── json-merger/
 ├── shared/
 │   ├── validators/
 │   │   └── schema-validator.py
 │   └── converters/
 │       └── format-converter.py
 └── tools/
     ├── install-skill.sh
     └── update-all.sh
```

## GitHub Best Practices

### Branch Strategy

#### Branch Naming Conventions
- **Feature branches**: `feature/description-of-feature`
- **Bug fixes**: `bugfix/description-of-bug`
- **Hotfixes**: `hotfix/description-of-fix`
- **Documentation**: `docs/description-of-change`
- **Refactoring**: `refactor/description-of-refactor`

Examples:
```
feature/add-csv-validator
bugfix/fix-json-parsing-error
docs/update-installation-guide
```

#### Branch Management
- Keep branches short-lived (ideally < 3 days)
- Delete branches after merging
- Regularly sync with main/master branch
- One branch per feature/fix
- Never commit directly to main/master

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

#### Examples
```
feat(csv-analyzer): add support for custom delimiters

fix(json-merger): handle null values correctly

docs(readme): add installation instructions

refactor(validators): simplify schema validation logic
```

#### Best Practices
- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line should be 50 characters or less
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Explain what and why, not how

### Pull Request (PR) Best Practices

#### PR Creation
- **Clear title**: Use descriptive titles following commit conventions
- **Description**: Include:
  - What changes were made
  - Why changes were necessary
  - How to test the changes
  - Related issues (use "Fixes #123" or "Closes #123")
- **Small PRs**: Keep PRs focused and reviewable (< 400 lines ideally)
- **Draft PRs**: Use draft status for work in progress
- **Self-review**: Review your own PR before requesting reviews

#### PR Template Example
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Closes #123

## Testing
- [ ] Test 1
- [ ] Test 2

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

#### PR Review Process
- **Request specific reviewers**: Tag people with relevant expertise
- **Respond to feedback**: Address all comments or explain why not
- **Resolve conversations**: Only resolve conversations after addressing
- **Keep updated**: Rebase or merge main regularly during review
- **CI/CD checks**: Ensure all checks pass before merging

### Code Review Best Practices

#### For Reviewers
- **Be respectful and constructive**: Focus on the code, not the person
- **Provide context**: Explain why you're suggesting changes
- **Use suggestions**: GitHub's suggestion feature for small fixes
- **Approve or request changes**: Don't leave PRs in limbo
- **Review promptly**: Aim to review within 24-48 hours
- **Look for**:
  - Correctness and logic errors
  - Security vulnerabilities
  - Performance issues
  - Code style and readability
  - Test coverage
  - Documentation

#### For Authors
- **Respond to all comments**: Even if just to acknowledge
- **Don't take it personally**: Reviews improve code quality
- **Ask questions**: If feedback is unclear
- **Update and notify**: Push changes and re-request review
- **Be patient**: Good reviews take time

### Issue Tracking

#### Issue Templates
Create templates for:
- Bug reports
- Feature requests
- Documentation improvements

#### Issue Labels
Use consistent labels:
- **Type**: `bug`, `enhancement`, `documentation`, `question`
- **Priority**: `priority: high`, `priority: medium`, `priority: low`
- **Status**: `status: in-progress`, `status: blocked`, `status: needs-info`
- **Effort**: `effort: small`, `effort: medium`, `effort: large`

#### Writing Good Issues
- **Descriptive title**: Clear and specific
- **Reproduce steps**: For bugs, include steps to reproduce
- **Expected vs actual**: What you expected vs what happened
- **Environment**: OS, version numbers, etc.
- **Screenshots**: Include when helpful
- **Labels**: Apply appropriate labels
- **Assignees**: Assign when appropriate

### Documentation Standards

#### README Requirements
Every project should have:
- Project title and description
- Installation instructions
- Usage examples
- API documentation (if applicable)
- Contributing guidelines
- License information
- Contact information

#### Code Documentation
- **Functions**: Document purpose, parameters, return values
- **Complex logic**: Add inline comments explaining why
- **Public APIs**: Comprehensive documentation
- **Examples**: Include usage examples

#### Keep Updated
- Update docs with code changes
- Version documentation
- Link to external resources
- Include troubleshooting section

### Security Best Practices

#### Sensitive Data
- **Never commit**:
  - Passwords, API keys, tokens
  - Private keys, certificates
  - Environment files (.env)
  - Database credentials
- **Use**:
  - `.gitignore` for sensitive files
  - Environment variables
  - Secret management tools
  - GitHub Secrets for CI/CD

#### Code Security
- Review dependencies regularly
- Enable Dependabot alerts
- Use security scanning tools
- Follow OWASP guidelines
- Validate all inputs
- Use prepared statements for databases

#### Access Control
- Use branch protection rules
- Require reviews before merging
- Enforce status checks
- Restrict who can push to main
- Use two-factor authentication
- Audit access regularly

### Git Workflow

#### Daily Workflow
```bash
# 1. Update your local main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 4. Push to remote
git push -u origin feature/my-feature

# 5. Create PR on GitHub

# 6. After approval, merge and cleanup
git checkout main
git pull origin main
git branch -d feature/my-feature
```

#### Keeping Branch Updated
```bash
# Option 1: Rebase (cleaner history)
git checkout feature/my-feature
git rebase main

# Option 2: Merge (preserves history)
git checkout feature/my-feature
git merge main
```

### Release Management

#### Semantic Versioning
Follow [SemVer](https://semver.org/): `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

#### Release Process
1. Update version numbers
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly
5. Create GitHub release with tag
6. Generate release notes
7. Announce release

#### Tags
```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag
git push origin v1.0.0
```

### Repository Settings

#### Branch Protection
Enable for main/master:
- Require pull request reviews (minimum 1-2)
- Require status checks to pass
- Require branches to be up to date
- Enforce for administrators
- Restrict who can push

#### Automation
- **GitHub Actions**: CI/CD workflows
- **Dependabot**: Dependency updates
- **Code scanning**: Security alerts
- **Auto-merge**: For trusted dependencies
- **Stale bot**: Close inactive issues/PRs

### Collaboration Guidelines

#### Communication
- Use issue comments for discussions
- Tag relevant people with @mentions
- Keep discussions focused and professional
- Use GitHub Discussions for broader topics

#### Contributing
- Fork the repository
- Create feature branch
- Follow coding standards
- Write tests
- Update documentation
- Submit PR with clear description

#### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Report inappropriate behavior
- Follow project guidelines

## Additional Resources

- [GitHub Docs](https://docs.github.com)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## License

[Add your license information here]

## Contact

[Add contact information here]
