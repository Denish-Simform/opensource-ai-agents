---
name: runtime-environment-detection
description: 'Detect execution runtime environment (VS Code Copilot chat, CLI agent runner, API mode, headless automation) and auto-adapt interaction strategy. Use when: determining available user interaction tools, selecting askQuestions vs chat-based prompts, detecting IDE availability, avoiding hard dependencies on IDE-specific tools, runtime context detection, execution environment awareness, interaction strategy selection.'
argument-hint: 'Optionally specify expected environment or interaction needs'
---

# Runtime Environment Detection

Detects the execution runtime environment and automatically selects appropriate user-interaction strategies without hard dependencies on IDE-specific tools.

## When to Use

- **Before asking user questions** — determine if interactive tools are available
- **In multi-environment agents** — CLI, VS Code, API, headless automation
- **When avoiding hard dependencies** — gracefully degrade if IDE tools unavailable
- **For environment-aware workflows** — adapt behavior based on execution context
- **In shared/portable agents** — work across different invocation methods

## Detection Strategy

Use **multiple signals** since environment variables alone can't distinguish VS Code from CLI on the same machine.

### Signal Matrix

| Environment | Tool Availability | Context Indicators | Execution Pattern |
|-------------|------------------|-------------------|------------------|
| **VS Code Copilot Chat** | `vscode_askQuestions` available | `editorContext` present, attachments include UI state | Interactive, UI-rich |
| **CLI Agent Runner** | No VS Code tools | Terminal-only context, stdin/stdout focus | Interactive CLI, text-based |
| **API Mode** | Minimal/custom tools | API request metadata, no user context | Programmatic, structured I/O |
| **Headless Automation** | Script-defined tools | Execution scripts, batch processing signals | Non-interactive, automated |

### Detection Procedure

Run these checks **in order** for progressive certainty:

#### 1. Tool Availability Check
```
Try calling tool_search_tool_regex for 'vscode' or 'ask'
- If vscode_askQuestions found → VS Code environment likely
- If github tools found but no vscode → CLI or API
- If minimal tools → headless/restricted
```

#### 2. Context Inspection
```
Check what's present in context:
- editorContext with file path → IDE active
- Terminal only → CLI session
- API request metadata → API invocation
- Batch/script indicators → headless
```

#### 3. Execution Pattern Analysis
```
Observe interaction history:
- Rich UI references (files, line numbers) → IDE
- Terminal commands dominate → CLI
- Structured requests/responses → API
- No questions asked, direct execution → headless
```

#### 4. Graceful Probing
```
If still uncertain, attempt a low-cost probe:
- Try listing available tools with tool_search_tool_regex
- Check memory for previous environment notes
- Ask user in natural language as fallback
```

## Interaction Strategy Selection

Once environment is detected, **auto-adapt** using this decision tree:

### VS Code Copilot Chat
- ✅ Use `vscode_askQuestions` for multi-choice, forms, complex input
- ✅ Use file links with line numbers: `[file.ts](file.ts#L10)`
- ✅ Leverage editor context for file-aware operations
- ✅ Show rich markdown with tables, collapsible sections

### CLI Agent Runner
- ✅ Use natural language questions in chat response
- ✅ Use bullet lists, simple formatting
- ✅ Provide absolute paths for files
- ✅ Expect text-based responses
- ❌ Avoid IDE-specific tools

### API Mode
- ✅ Use structured JSON request/response
- ✅ Validate inputs upfront, minimize back-and-forth
- ✅ Return machine-parseable output
- ✅ Use defaults for optional parameters
- ❌ Never ask questions — fail fast if input missing

### Headless Automation
- ✅ Use environment variables or config files for inputs
- ✅ Execute with defaults, no interactive prompts
- ✅ Log to files instead of interactive output
- ✅ Return structured exit codes
- ❌ Never wait for user input

## Implementation Pattern

### Detection Function (Pseudocode)

```python
def detect_runtime_environment():
    # Signal 1: Tool availability
    vscode_tools = search_tools_regex('vscode')
    if 'vscode_askQuestions' in vscode_tools:
        return 'vscode-chat'
    
    # Signal 2: Context inspection
    if editor_context_present():
        return 'vscode-integrated'
    
    if terminal_only_context():
        return 'cli-agent-runner'
    
    # Signal 3: Execution pattern
    if api_request_metadata_present():
        return 'api-mode'
    
    # Signal 4: Default assumptions
    if no_interactive_signals():
        return 'headless-automation'
    
    # Fallback: assume CLI with natural language interaction
    return 'cli-with-chat'

def select_interaction_strategy(environment):
    strategies = {
        'vscode-chat': {
            'ask_method': 'use_vscode_askQuestions',
            'format': 'rich_markdown',
            'file_links': 'with_line_numbers',
            'fallback': 'chat_prompts'
        },
        'cli-agent-runner': {
            'ask_method': 'natural_language_in_chat',
            'format': 'simple_text',
            'file_links': 'absolute_paths',
            'fallback': 'continue_with_defaults'
        },
        'api-mode': {
            'ask_method': 'fail_if_input_missing',
            'format': 'structured_json',
            'file_links': 'absolute_paths',
            'fallback': 'error_response'
        },
        'headless-automation': {
            'ask_method': 'read_from_config',
            'format': 'log_files',
            'file_links': 'absolute_paths',
            'fallback': 'use_defaults'
        }
    }
    return strategies.get(environment, strategies['cli-agent-runner'])
```

### Usage in Agent Logic

```markdown
1. Run detection at the start of complex workflows
2. Store result in session memory if multi-turn conversation
3. Select interaction strategy based on detected environment
4. Always provide a fallback path — never hard fail on IDE tool unavailability
```

## Examples

### Example 1: Detecting and Adapting

**Scenario:** Agent needs to ask user 5 configuration questions

```
Step 1: Detect environment
- Search for vscode tools → Found vscode_askQuestions

Step 2: Select strategy
- Environment: vscode-chat
- Strategy: use_vscode_askQuestions with fallback to chat

Step 3: Execute
- Call vscode_askQuestions with structured form
- If fails, fall back to asking questions one-by-one in chat
```

### Example 2: CLI with Chat Fallback

**Scenario:** CLI agent runner needs user input

```
Step 1: Detect environment
- No vscode tools found
- Terminal context present
- Interactive signals detected

Step 2: Select strategy
- Environment: cli-agent-runner
- Strategy: natural_language_in_chat

Step 3: Execute
- Ask: "Which deployment environment? (dev/staging/prod)"
- Parse text response
- Continue with workflow
```

### Example 3: API Mode (No Interaction)

**Scenario:** Webhook-triggered agent run

```
Step 1: Detect environment
- API request metadata found
- No interactive context
- Structured input payload

Step 2: Select strategy
- Environment: api-mode
- Strategy: fail_if_input_missing

Step 3: Execute
- Validate all required inputs present upfront
- If missing, return error: "Missing required field: deployment_target"
- If valid, execute with provided inputs only
```

## Integration with Existing Agents

Add this detection block at the start of multi-step workflows:

```markdown
## Runtime Detection

1. Detect execution environment using runtime-environment-detection skill
2. Store in session memory: `environment_type` and `interaction_strategy`
3. Reference strategy when deciding how to gather user input
4. Always implement fallback path for degraded environments
```

## Anti-patterns

❌ **Hard dependency on IDE tools**
```python
# BAD: Will fail in CLI
questions = vscode_askQuestions([...])
```

✅ **Graceful degradation**
```python
# GOOD: Detects and adapts
env = detect_runtime_environment()
if env == 'vscode-chat':
    questions = vscode_askQuestions([...])
else:
    questions = ask_in_chat_naturally([...])
```

❌ **Assuming environment from ENV vars only**
```python
# BAD: Same machine runs both VS Code and CLI
if os.getenv('VSCODE_PID'):
    return 'vscode'
```

✅ **Multi-signal detection**
```python
# GOOD: Uses tool availability + context + patterns
signals = [
    check_tool_availability(),
    inspect_context(),
    analyze_execution_pattern()
]
return aggregate_signals(signals)
```

❌ **No fallback for failed interaction**
```python
# BAD: Crashes if tool unavailable
response = vscode_askQuestions([...])
```

✅ **Fallback chain**
```python
# GOOD: Try best method, fall back gracefully
try:
    response = vscode_askQuestions([...])
except ToolNotAvailable:
    response = ask_in_chat([...])
```

## Related Skills

- **agent-customization** — Creating environment-specific instruction files
- **multi-environment-deployment** — Deploying agents to different runtimes
- **graceful-degradation** — Building fault-tolerant workflows

## Session Memory Integration

Store detected environment in session memory for reuse:

```markdown
# /memories/session/runtime-context.md

## Detected Environment
- Type: vscode-chat
- Interaction Strategy: use_vscode_askQuestions
- Fallback: natural_language_in_chat
- Detected At: 2026-03-23 10:30:00
- Confidence: high

## Available Tools
- vscode_askQuestions: yes
- vscode_renameSymbol: yes
- terminal access: yes
- file operations: yes
```

Reference this in subsequent turns to avoid re-detection.

## Testing Detection Logic

Create test scenarios for each environment:

### Test Case 1: VS Code
```
Given: vscode_askQuestions available, editorContext present
Expected: Environment = vscode-chat, Strategy = use IDE tools
```

### Test Case 2: CLI
```
Given: No vscode tools, terminal context only
Expected: Environment = cli-agent-runner, Strategy = chat prompts
```

### Test Case 3: API
```
Given: API metadata, no interactive context
Expected: Environment = api-mode, Strategy = validate upfront or fail
```

### Test Case 4: Headless
```
Given: No interactive signals, execution script present
Expected: Environment = headless-automation, Strategy = use defaults
```

## Best Practices

1. **Detect early** — Run detection before asking first question
2. **Cache result** — Store in session memory, don't re-detect every turn
3. **Fail gracefully** — Always have a fallback interaction method
4. **Log decisions** — Record why a strategy was chosen for debugging
5. **Progressive enhancement** — Start with lowest-common-denominator (chat), enhance if IDE available
6. **Explicit over implicit** — Let users override auto-detection if needed
7. **Test all paths** — Verify agent works in all four environment types

## Conclusion

This skill enables agents to work seamlessly across VS Code, CLI, API, and headless environments by detecting runtime context through multiple signals and automatically adapting interaction strategies with graceful fallbacks.
