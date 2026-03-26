---
description: "Analyze git changes and create a pull request with comprehensive description including summary, issue links, testing checklist, and breaking changes. Use when: creating PR, generate pull request, make PR from changes, submit PR, open pull request."
name: "Generate PR"
argument-hint: "Target branch (default: main)"
agent: "agent"
tools: [mcp_gitkraken_git_status, mcp_gitkraken_git_log_or_diff, mcp_gitkraken_pull_request_create, mcp_gitkraken_git_branch]
---

# Generate Pull Request

Analyze the current git changes and create a comprehensive pull request.

## Steps

1. **Detect Current Branch and Changes**
   - Use `mcp_gitkraken_git_status` to identify the current branch and changed files
   - Use `mcp_gitkraken_git_log_or_diff` to analyze the actual code changes

2. **Extract Repository Information**
   - Detect repository organization and name from git remote
   - Identify the source branch (current branch)
   - Determine target branch (from argument or default to 'main')

3. **Generate PR Content**
   Create a structured PR description with:
   
   ### Summary
   - Brief overview of what changed and why
   - Key modifications and their purpose
   
   ### Related Issues
   - Search commit messages for issue references (#123, closes #456, fixes #789)
   - Format as: "Closes #123, Related to #456"
   
   ### Changes Made
   - Categorized list of changes:
     - ✨ New Features
     - 🐛 Bug Fixes
     - 📝 Documentation
     - ♻️ Refactoring
     - ⚡ Performance
     - 🔧 Configuration
     - 🧪 Tests
   
   ### Testing Checklist
   ```
   - [ ] Unit tests added/updated
   - [ ] Integration tests pass
   - [ ] Manual testing completed
   - [ ] Edge cases covered
   - [ ] No regressions detected
   ```
   
   ### Breaking Changes
   - List any breaking changes with migration path
   - If none, state: "No breaking changes"
   
   ### Additional Notes
   - Deployment considerations
   - Dependencies updated
   - Configuration changes required

4. **Create PR Title**
   - Format: `{type}: {concise description}`
   - Types: feat, fix, docs, refactor, perf, test, chore
   - Example: `feat: add SA orchestrator agent plugin`

5. **Submit Pull Request**
   - Use `mcp_gitkraken_pull_request_create` with provider='github'
   - Set `is_draft=false` unless changes are incomplete
   - Create the PR and return the URL

## Provider Detection

Default to GitHub. If the repository uses a different provider (GitLab, Azure DevOps, Bitbucket), detect from git remote and adjust accordingly.

## Error Handling

- If no changes detected: inform user and exit
- If not on a feature branch: confirm with user before proceeding
- If repository info cannot be detected: ask user to provide it
- If PR creation fails: show error and suggest manual creation

## Output

Return:
- ✅ PR created successfully
- 🔗 PR URL: {url}
- 📊 Files changed: {count}
- ➕ Additions: {lines}
- ➖ Deletions: {lines}
