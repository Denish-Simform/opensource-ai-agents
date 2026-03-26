# Environment Detection Signals

Comprehensive reference for identifying runtime environments through observable signals.

## Signal Categories

### 1. Tool Availability Signals

| Tool Pattern | VS Code | CLI | API | Headless |
|--------------|---------|-----|-----|----------|
| `vscode_askQuestions` | ✅ | ❌ | ❌ | ❌ |
| `vscode_renameSymbol` | ✅ | ❌ | ❌ | ❌ |
| `vscode_searchExtensions` | ✅ | ❌ | ❌ | ❌ |
| `run_vscode_command` | ✅ | ❌ | ❌ | ❌ |
| `github-pull-request_*` | ⚠️ | ⚠️ | ❌ | ❌ |
| `mcp_*` | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| `run_in_terminal` | ✅ | ✅ | ⚠️ | ⚠️ |
| `file_search` | ✅ | ✅ | ✅ | ✅ |

**Legend:**
- ✅ Available
- ❌ Not available
- ⚠️ Depends on configuration

### 2. Context Signals

#### VS Code Copilot Chat Context
```json
{
  "editorContext": {
    "currentFile": "/path/to/file.ts",
    "selection": "line 10-25",
    "cursorPosition": {"line": 15, "column": 8}
  },
  "attachments": [
    {"id": "prompt:customizationsIndex"},
    {"file": "/path/to/SKILL.md"}
  ],
  "terminals": [
    {"name": "bash", "id": "1"}
  ]
}
```

**Indicators:**
- `editorContext` present with file path
- `attachments` array with prompts/skills/instructions
- Rich UI state (selection, cursor)
- Terminal metadata but not primary focus

#### CLI Agent Runner Context
```json
{
  "terminals": [
    {"name": "bash", "id": "main", "active": true}
  ],
  "workspace_info": {
    "folders": ["/path/to/project"]
  }
}
```

**Indicators:**
- Terminal is primary/only context
- No `editorContext` or minimal editor state
- Focus on command execution
- Workspace folders but not file-level context

#### API Mode Context
```json
{
  "request_metadata": {
    "method": "POST",
    "endpoint": "/api/agent/invoke",
    "headers": {"Authorization": "Bearer ..."}
  },
  "workspace_info": null,
  "editorContext": null
}
```

**Indicators:**
- API request metadata present
- No workspace or editor context
- Structured input payload
- Machine-to-machine communication signals

#### Headless Automation Context
```json
{
  "execution_script": "/path/to/batch_runner.sh",
  "environment_variables": {
    "CI": "true",
    "BATCH_MODE": "true",
    "NO_INTERACTIVE": "1"
  },
  "input_source": "config_file"
}
```

**Indicators:**
- CI/CD environment variables
- Batch processing signals
- No user interaction context
- Config-driven execution

### 3. Execution Pattern Signals

#### VS Code Pattern
```
User message: "Refactor this function"
Turn 1: Agent reads file via editorContext
Turn 2: Agent asks clarification via vscode_askQuestions
Turn 3: Agent edits file with replace_string_in_file
Turn 4: User sees inline diff in editor
```

**Characteristics:**
- File-centric workflow
- IDE tool usage
- Rich interactivity
- Visual feedback loop

#### CLI Pattern
```
User message: "Deploy to production"
Turn 1: Agent asks: "Which environment? (staging/prod)"
Turn 2: User replies: "prod"
Turn 3: Agent runs terminal commands
Turn 4: User sees terminal output
```

**Characteristics:**
- Terminal-centric workflow
- Text-based questions
- Command execution focus
- Plain text I/O

#### API Pattern
```
POST /api/agent/invoke
{
  "task": "deploy",
  "environment": "prod",
  "auto_approve": true
}

Response:
{
  "status": "success",
  "deployment_id": "abc123"
}
```

**Characteristics:**
- Single request/response
- No back-and-forth
- Structured data
- Programmatic invocation

#### Headless Pattern
```
$ ./batch_deploy.sh --config=deploy.yaml --no-interactive
Reading config...
Deploying services...
✓ service-1 deployed
✓ service-2 deployed
Deployment complete. Exit code: 0
```

**Characteristics:**
- No user interaction
- Config-driven
- Logging output
- Exit codes for status

### 4. Memory/History Signals

Check session or repository memory for previous environment detection:

```markdown
# /memories/session/runtime-context.md

## Previous Detection
Environment: vscode-chat
Confidence: high
Timestamp: 2026-03-23 10:15:00
```

If present, reuse unless significant time gap or context shift suggests re-detection needed.

## Detection Decision Tree

```
Start
  ↓
Search for 'vscode' tools
  ↓
[vscode_askQuestions found?]
  ├─ YES → VS Code Chat (HIGH confidence)
  └─ NO → Continue
      ↓
Check editorContext present?
  ├─ YES → VS Code Integrated (MEDIUM confidence)
  └─ NO → Continue
      ↓
Check API request metadata?
  ├─ YES → API Mode (HIGH confidence)
  └─ NO → Continue
      ↓
Check CI/batch environment variables?
  ├─ YES → Headless Automation (MEDIUM confidence)
  └─ NO → Continue
      ↓
Check terminal-only context?
  ├─ YES → CLI Agent Runner (MEDIUM confidence)
  └─ NO → CLI with Chat (LOW confidence, fallback)
```

## Confidence Scoring

Combine multiple signals to increase confidence:

| Score | Confidence | Decision |
|-------|------------|----------|
| 3+ signals match | HIGH | Proceed with detected environment |
| 2 signals match | MEDIUM | Proceed with caution, prepare fallback |
| 1 signal match | LOW | Use safe default (CLI with chat) |
| 0 signals match | UNKNOWN | Assume CLI with chat, log warning |

## Edge Cases

### Same Machine, Different Invocations

**Problem:** Developer machine has both VS Code and CLI agent runner installed.

**Solution:** Don't rely on machine-level ENV vars. Use invocation-specific signals:
- VS Code invocation → `vscode_askQuestions` tool available
- CLI invocation → No vscode tools in tool list

### VS Code Remote Development

**Problem:** VS Code running on local machine, agent on remote server.

**Signals:**
- `vscode_askQuestions` still available (forwarded)
- Workspace paths may be remote-mounted
- Terminal is remote shell

**Detection:** Treat as VS Code Chat (tools are the source of truth)

### Jupyter Notebook in VS Code

**Signals:**
- `editorContext` shows `.ipynb` file
- Notebook-specific tools available (`run_notebook_cell`)
- VS Code tools also available

**Detection:** VS Code Chat with notebook specialization

### GitHub Copilot Chat vs VS Code Copilot Chat

Both run in VS Code UI but may have different tool sets.

**GitHub Copilot Extension:**
- `github-pull-request_*` tools available
- May have limited file tools

**VS Code Copilot:**
- Full VS Code tool set
- `vscode_askQuestions` available

**Detection:** Check for `vscode_askQuestions` as primary signal

## Testing Checklist

Verify detection works correctly in each environment:

- [ ] VS Code: Open chat, run `/runtime-environment-detection` → Should detect VS Code
- [ ] CLI: Run from terminal agent runner → Should detect CLI
- [ ] API: Invoke via webhook/API → Should detect API mode
- [ ] Headless: Run in CI/batch script → Should detect headless
- [ ] Fallback: Simulate tool unavailability → Should gracefully default to CLI with chat

## Signal Collection Template

Use this template to systematically collect signals:

```markdown
## Signal Collection for Detection

### Tools Available
- [ ] vscode_askQuestions
- [ ] vscode_renameSymbol
- [ ] run_in_terminal
- [ ] github-pull-request_*
- [ ] file_search, grep_search, semantic_search

### Context Present
- [ ] editorContext with file path
- [ ] terminals array
- [ ] attachments (prompts/skills)
- [ ] API request metadata
- [ ] CI environment variables

### Execution Patterns
- [ ] File-centric workflow
- [ ] Terminal command focus
- [ ] Structured request/response
- [ ] No user interaction

### Confidence Score
[Tool signals] + [Context signals] + [Pattern signals] = Total

- Total ≥ 3 → HIGH confidence
- Total = 2 → MEDIUM confidence
- Total = 1 → LOW confidence
- Total = 0 → UNKNOWN (use safe default)
```

## Implementation Notes

### Signal Priority Order

1. **Tool availability** (most reliable) - Tools can't be faked
2. **Context structure** (very reliable) - Hard to confuse editorContext with API metadata
3. **Execution patterns** (reliable) - Require multiple turns to observe
4. **Environment variables** (unreliable) - Can be inconsistent across same machine

### Performance Considerations

- **Tool search** - Use regex patterns efficiently (`^vscode_`, not `vscode`)
- **Context inspection** - Check simple fields first (presence of keys)
- **Pattern analysis** - Only if first two signals inconclusive
- **Cache result** - Store in session memory after first detection

### Logging for Debugging

When environment detection runs, log:

```
[Runtime Detection] Starting...
[Signal 1/4] Tool search for 'vscode': Found 3 tools
[Signal 2/4] Context inspection: editorContext present
[Signal 3/4] Pattern analysis: Skipped (high confidence already)
[Signal 4/4] Historical context: No previous detection
[Result] Environment: vscode-chat | Confidence: HIGH | Strategy: use_vscode_askQuestions
```

This helps debug false detections and improve signal weights.
