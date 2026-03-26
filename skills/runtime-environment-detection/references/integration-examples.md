# Integration Examples

Practical examples of integrating runtime environment detection into agent workflows.

## Example 1: Multi-Step Configuration Agent

**Scenario:** Agent needs to gather 5 configuration values from user before deploying a service.

### Without Runtime Detection (Fragile)

```markdown
## Agent Logic

Ask user for configuration:
1. deployment_environment
2. region
3. instance_count
4. enable_monitoring
5. notification_email

# ❌ PROBLEM: Hard-coded to VS Code
Use vscode_askQuestions to gather inputs
```

**Failure mode:** Breaks when running in CLI or API, crashes on tool unavailability.

### With Runtime Detection (Robust)

```markdown
## Agent Logic

Step 1: Detect runtime environment
- Run: tool_search_tool_regex pattern: '^vscode_askQuestions$'
- Inspect: editorContext present?
- Store: environment_type in session memory

Step 2: Select interaction strategy
- If vscode-chat: Use vscode_askQuestions with structured form
- If cli-agent-runner: Ask questions one-by-one in natural language
- If api-mode: Validate all required inputs present in request, fail fast if missing
- If headless-automation: Read from config file or environment variables

Step 3: Execute with fallback
Try primary method, catch failure, fall back to chat prompts

Step 4: Continue workflow with gathered inputs
```

**Agent implementation:**

```
[Invoke runtime-environment-detection skill]

Detected: vscode-chat
Strategy: use_vscode_askQuestions, fallback to chat

Attempting primary method...
[Call vscode_askQuestions with structured form]

Success! Gathered:
- deployment_environment: production
- region: us-east-1
- instance_count: 3
- enable_monitoring: true
- notification_email: ops@example.com

Proceeding with deployment...
```

If `vscode_askQuestions` fails:

```
Primary method failed: Tool not available
Falling back to chat prompts...

Which deployment environment? (dev/staging/production)
[Wait for user response]

Great! Using production. Which region?
[Continue asking one-by-one]
```

---

## Example 2: Code Review Agent

**Scenario:** Agent analyzes code and needs to ask clarifying questions about intended behavior.

### Runtime-Aware Implementation

```markdown
## Agent Workflow

1. **Detect environment**
   - Search for vscode tools → Not found
   - Check context → Terminal only
   - Result: cli-agent-runner

2. **Adapt presentation format**
   - Use simple text formatting
   - Avoid rich markdown tables
   - Use absolute file paths (not clickable links)

3. **Ask clarifying questions**
   - Strategy: Natural language in chat (no structured forms)
   - Example: "I see the function handles errors. Should it log to console or throw exceptions?"

4. **Present findings**
   - CLI-friendly format:
```

```
Code Review Findings
====================

src/utils/validator.ts
----------------------
Line 45: Missing null check before property access
Line 67: Unused variable 'tempResult'

src/api/handler.ts
------------------
Line 23: Error handling could be improved

Would you like me to fix these issues?
```

```markdown
   - VS Code format would use:
     - [validator.ts](src/utils/validator.ts#L45) with clickable links
     - Markdown tables
     - Collapsible sections
```

---

## Example 3: Deployment Pipeline Agent (API Mode)

**Scenario:** Webhook triggers agent to deploy service, no user interaction available.

### Runtime-Aware Implementation

```markdown
## Agent Workflow

1. **Detect environment**
   - No vscode tools
   - No interactive terminal
   - API request metadata present
   - Result: api-mode

2. **Change validation strategy**
   - Validate ALL required inputs upfront
   - Do NOT attempt to ask questions
   - Fail fast with clear error if missing

3. **Execute deployment**
   - Use defaults for optional parameters
   - Log to structured format (JSON)
   - Return machine-parseable response

4. **Error handling**
   - Return HTTP-style status codes
   - Include actionable error messages
   - Never wait for user input
```

**Request validation:**

```json
POST /api/agent/deploy
{
  "service": "web-api",
  "environment": "production",
  "version": "v2.3.1"
}
```

**Agent logic:**

```
Detected: api-mode
Strategy: fail_if_input_missing

Validating required inputs...
✓ service: present
✓ environment: present
✓ version: present

Optional inputs (using defaults):
- region: us-east-1 (default)
- replicas: 3 (default)

Proceeding with deployment...
```

**If validation fails:**

```json
{
  "status": "error",
  "error_code": "MISSING_REQUIRED_INPUT",
  "message": "Missing required field: version",
  "required_fields": ["service", "environment", "version"],
  "provided_fields": ["service", "environment"]
}
```

---

## Example 4: Batch Processing Agent (Headless)

**Scenario:** CI/CD pipeline runs agent to analyze test results and generate report.

### Runtime-Aware Implementation

```markdown
## Agent Workflow

1. **Detect environment**
   - CI environment variables present
   - NO_INTERACTIVE=1 flag
   - Result: headless-automation

2. **Adjust input strategy**
   - Read configuration from: ./config/analysis.yaml
   - Read data from: ./test-results/*.xml
   - Never prompt for user input

3. **Generate report**
   - Output to: ./reports/analysis-YYYYMMDD.md
   - Log progress to: ./logs/agent.log
   - Use exit codes: 0 (success), 1 (failure)

4. **No interactive questions**
   - Use sensible defaults for all optional parameters
   - Fail with clear error if critical data missing
   - Document assumptions in report
```

**Execution:**

```bash
# CI pipeline script
export CI=true
export NO_INTERACTIVE=1

./agent-runner analyze-tests \
  --config=./config/analysis.yaml \
  --output=./reports/ \
  --log-level=info

# Agent detects headless environment
# Reads config: ✓
# Analyzes data: ✓
# Generates report: ✓
# Exit code: 0
```

**Agent internal log:**

```
[2026-03-23 10:30:00] INFO: Starting test analysis
[2026-03-23 10:30:01] INFO: Detected environment: headless-automation
[2026-03-23 10:30:01] INFO: Strategy: read_from_config, no user interaction
[2026-03-23 10:30:02] INFO: Reading config from ./config/analysis.yaml
[2026-03-23 10:30:03] INFO: Found 145 test results
[2026-03-23 10:30:15] INFO: Analysis complete
[2026-03-23 10:30:16] INFO: Report written to ./reports/analysis-20260323.md
[2026-03-23 10:30:16] INFO: Exit code: 0
```

---

## Example 5: Hybrid Agent (Works Everywhere)

**Scenario:** Agent that needs to work seamlessly in VS Code, CLI, API, and headless modes.

### Implementation with Full Fallback Chain

```markdown
## Agent: deployment-orchestrator

### Step 1: Runtime Detection (Always First)

Detect environment and cache in session memory:

```

```python
# Pseudocode
environment = detect_runtime_environment()
session_memory.write('runtime-context.md', f"""
## Detected Environment
Type: {environment['type']}
Confidence: {environment['confidence']}
Strategy: {environment['strategy']}
Detected: {timestamp}
""")
```

```markdown
### Step 2: Gather Inputs (Environment-Aware)

Function: gather_deployment_config()

```

```python
def gather_deployment_config(environment):
    required = ['service_name', 'environment', 'version']
    optional = {'region': 'us-east-1', 'replicas': 3}
    
    if environment == 'vscode-chat':
        try:
            return vscode_askQuestions(required + optional)
        except ToolNotAvailable:
            return ask_in_chat_naturally(required, optional)
    
    elif environment == 'cli-agent-runner':
        return ask_in_chat_naturally(required, optional)
    
    elif environment == 'api-mode':
        config = read_from_request_body()
        validate_required_fields(config, required)
        apply_defaults(config, optional)
        return config
    
    elif environment == 'headless-automation':
        config = read_from_config_file('./deploy.yaml')
        validate_required_fields(config, required)
        apply_defaults(config, optional)
        return config
```

```markdown
### Step 3: Execute Deployment (Same Logic)

Deployment logic is environment-agnostic, just uses the config:

```

```python
def deploy_service(config):
    # Same for all environments
    validate_config(config)
    build_artifacts()
    upload_to_registry()
    deploy_to_cluster(config)
    run_smoke_tests()
    return deployment_result
```

```markdown
### Step 4: Present Results (Environment-Aware)

Function: present_results(deployment_result, environment)

```

```python
def present_results(result, environment):
    if environment == 'vscode-chat':
        # Rich markdown with file links
        return format_rich_markdown(result)
    
    elif environment == 'cli-agent-runner':
        # Simple text with ANSI colors
        return format_simple_text(result)
    
    elif environment == 'api-mode':
        # JSON response
        return format_json_response(result)
    
    elif environment == 'headless-automation':
        # Log file + exit code
        write_log_file(result)
        return exit_code(result)
```

```markdown
**Result:** Single agent codebase that works in all four environments!

---

## Example 6: Session Memory Integration

Store detection result for reuse across conversation turns.

### First Turn

```

Agent: Running runtime environment detection...
[Invoke runtime-environment-detection skill]

Detected: vscode-chat (HIGH confidence)
Storing in session memory...

```

**Session memory file created:**

```markdown
# /memories/session/runtime-context.md

## Detected Environment
Type: vscode-chat
Confidence: HIGH
Confidence Score: 3
Signals:
  - vscode_tools_available
  - editorContext_present
  - interactive_terminal

## Interaction Strategy
Ask Method: use_vscode_askQuestions
Format: rich_markdown
File Links: with_line_numbers
Fallback: chat_prompts

## Detection Details
Timestamp: 2026-03-23T10:30:00Z
Tool Search Result: Found vscode_askQuestions, vscode_renameSymbol
Context: editorContext = /path/to/file.ts

## Notes
- VS Code extension active
- User working on file.ts
- Rich UI available
```

### Subsequent Turns

```
Agent: Need to ask user a question...
[Check session memory for runtime-context.md]

Found cached detection: vscode-chat
Using strategy: use_vscode_askQuestions
Skipping re-detection (recent, high confidence)

[Call vscode_askQuestions directly]
```

**Benefits:**
- No re-detection overhead
- Consistent behavior across turns
- Faster response time
- Debugging trail

---

## Example 7: Detection Override

Allow users to explicitly override auto-detection when needed.

### User Override Syntax

```
User: "Deploy to production [env:api-mode]"

Agent: Detected override: env=api-mode
Ignoring auto-detection, using API mode strategy
Validating all inputs present... OK
Executing deployment...
```

### Implementation

```python
def detect_with_override(user_message):
    # Check for explicit override
    override = extract_override_tag(user_message)
    
    if override:
        log(f"User override detected: {override}")
        return override
    
    # Normal auto-detection
    return detect_runtime_environment()
```

**Use cases:**
- Testing agent in different modes
- Forcing non-interactive behavior in VS Code
- Simulating API mode during development

---

## Best Practices Summary

1. **Always detect first** - Run detection before asking questions
2. **Cache results** - Store in session memory for subsequent turns
3. **Provide fallbacks** - Every interaction method needs a Plan B
4. **Test all paths** - Verify agent works in all four environments
5. **Log decisions** - Record why a strategy was chosen
6. **Allow overrides** - Let users force specific strategies when debugging
7. **Fail gracefully** - Clear error messages, not crashes

---

## Anti-patterns to Avoid

❌ **Assuming VS Code is always available**
```python
# Never do this
questions = vscode_askQuestions([...])  # Will crash in CLI
```

❌ **Using environment variables alone**
```python
# Unreliable - same machine runs multiple environments
if os.getenv('VSCODE_PID'):
    return 'vscode'
```

❌ **No fallback for failed tools**
```python
# Will break agent if tool unavailable
try:
    result = vscode_askQuestions([...])
except:
    raise  # Now what?
```

❌ **Repeating detection every turn**
```python
# Wasteful - detect once, cache result
def every_turn():
    env = detect_runtime_environment()  # Don't do this repeatedly
```

✅ **Correct pattern:**
```python
def once_per_conversation():
    if not session_memory.exists('runtime-context.md'):
        env = detect_runtime_environment()
        session_memory.write('runtime-context.md', env)
    return session_memory.read('runtime-context.md')
```

---

## Testing Your Integration

Create test scenarios for each environment:

### Test Script Template

```bash
#!/bin/bash
# test-runtime-detection.sh

echo "Test 1: VS Code mode"
# Simulate VS Code environment
export VSCODE_PID=12345
export TERM_PROGRAM=vscode
./test-agent.sh --expect-environment=vscode-chat

echo "Test 2: CLI mode"
# Simulate CLI environment
unset VSCODE_PID
unset TERM_PROGRAM
./test-agent.sh --expect-environment=cli-agent-runner

echo "Test 3: API mode"
# Simulate API call
cat request.json | ./test-agent.sh --expect-environment=api-mode

echo "Test 4: Headless mode"
# Simulate CI/CD
export CI=true
export NO_INTERACTIVE=1
./test-agent.sh --expect-environment=headless-automation
```

Run this test suite before deploying agent updates to catch environment detection regressions.
