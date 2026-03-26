# Runtime Environment Detection Skill

Detect execution runtime environment (VS Code Copilot chat, CLI agent runner, API mode, headless automation) and automatically select appropriate user-interaction strategies.

## Quick Start

**Invoke this skill when:**
- Starting a multi-step workflow that needs user input
- Building agents that work across different environments
- Avoiding hard dependencies on IDE-specific tools like `vscode_askQuestions`
- Implementing graceful degradation for tool availability

**To use:** Type `/runtime-environment-detection` or mention "detect runtime environment" in chat.

## What This Skill Provides

✅ **Multi-signal detection** - Uses tool availability, context inspection, and execution patterns (not just ENV vars)  
✅ **Auto-adapting strategies** - Automatically selects interaction method based on detected environment  
✅ **Graceful fallbacks** - Never crashes when IDE tools unavailable  
✅ **Session caching** - Stores detection result to avoid repeated checks  
✅ **Works everywhere** - VS Code, CLI, API, headless automation  

## Files in This Skill

```
runtime-environment-detection/
├── SKILL.md                           # Main skill documentation
├── README.md                          # This file
├── scripts/
│   └── detect_environment.py          # Reference implementation script
└── references/
    ├── environment-signals.md         # Comprehensive signal reference
    └── integration-examples.md        # Real-world usage examples
```

## Environments Detected

| Environment | Description | Interaction Method |
|-------------|-------------|-------------------|
| **vscode-chat** | VS Code Copilot Chat with IDE tools available | `vscode_askQuestions` with fallback to chat |
| **cli-agent-runner** | Command-line agent with interactive terminal | Natural language questions in chat |
| **api-mode** | HTTP/webhook invocation, no user interaction | Validate inputs upfront, fail fast if missing |
| **headless-automation** | CI/CD, batch processing, no interactivity | Read from config files, use defaults |

## Detection Signals Used

### 1. Tool Availability (Primary)
```
Search for: vscode_askQuestions, vscode_renameSymbol, etc.
Result: Present → VS Code | Absent → Continue detection
```

### 2. Context Structure
```
Check for: editorContext, API metadata, terminal focus
Result: Determines environment type
```

### 3. Execution Patterns
```
Observe: Interactive vs batch, file-centric vs terminal-centric
Result: Confirms environment classification
```

## Usage Examples

### Basic Detection

```markdown
Agent: Starting deployment workflow...
[Invoke /runtime-environment-detection]

Detected: vscode-chat (HIGH confidence)
Using strategy: vscode_askQuestions with fallback

Now gathering deployment configuration...
```

### With Session Caching

```markdown
Turn 1: Detect environment → Store in session memory
Turn 2: Read cached environment → Skip re-detection
Turn 3: Read cached environment → Skip re-detection
```

### Graceful Degradation

```markdown
Agent: Need to ask user questions...
Primary method: vscode_askQuestions
[Tool not available]
Falling back to: Natural language in chat

Which deployment environment would you like? (dev/staging/prod)
```

## Integration Pattern

Add to your agent workflow:

```markdown
## Step 1: Runtime Detection (First Turn Only)

Check session memory for cached detection:
- If present and recent (< 5 minutes) → Use cached
- If absent or stale → Run detection, cache result

## Step 2: Select Interaction Strategy

Based on detected environment:
- vscode-chat → Use vscode_askQuestions
- cli-agent-runner → Ask in natural language
- api-mode → Validate inputs or fail
- headless-automation → Read from config

## Step 3: Execute with Fallback

Try primary method → Catch failure → Fall back to safe default

## Step 4: Continue Workflow

Use gathered inputs (environment-agnostic from here)
```

## Testing

Run the detection script to verify:

```bash
# Test in current terminal
./.github/skills/runtime-environment-detection/scripts/detect_environment.py --verbose

# Example output:
{
  "environment": "cli-agent-runner",
  "confidence": "MEDIUM",
  "confidence_score": 2,
  "signals": ["interactive_terminal", "shell_environment"],
  "interaction_strategy": {
    "ask_method": "natural_language_in_chat",
    "format": "simple_text"
  }
}
```

## Best Practices

1. ✅ **Detect once per conversation** - Cache result in session memory
2. ✅ **Always provide fallbacks** - Never hard-fail on tool unavailability
3. ✅ **Use multiple signals** - Don't rely on ENV vars alone
4. ✅ **Test all environments** - Verify agent works in VS Code, CLI, API, headless
5. ✅ **Log detection results** - Help debug false detections

## Related Documentation

- [SKILL.md](./SKILL.md) - Complete skill documentation
- [Environment Signals Reference](./references/environment-signals.md) - Detailed signal catalog
- [Integration Examples](./references/integration-examples.md) - 7 real-world scenarios
- [Detection Script](./scripts/detect_environment.py) - Reference implementation

## Common Questions

**Q: Why not just check VSCODE_PID environment variable?**  
A: Developer machines can run both VS Code and CLI agents. ENV vars can't distinguish between invocation methods on the same machine. Tool availability is more reliable.

**Q: What if detection is wrong?**  
A: Every strategy includes a fallback. If `vscode_askQuestions` fails, agent falls back to chat prompts. Detection errors degrade gracefully, never crash.

**Q: How often should I re-detect?**  
A: Once per conversation. Cache the result in session memory and reuse.

**Q: Can users override auto-detection?**  
A: Yes! Agents can recognize override tags like `[env:api-mode]` in user messages to force specific strategies during testing.

**Q: Does this work with custom tools?**  
A: Yes! The detection logic is extensible. Add your custom tool patterns to the tool availability checks.

## Support

For issues or questions about this skill:
1. Check [integration-examples.md](./references/integration-examples.md) for your use case
2. Review [environment-signals.md](./references/environment-signals.md) for signal details
3. Run detection script with `--verbose` flag to see detailed analysis
4. File an issue in the awesome-copilot-opensource repository

---

**Version:** 1.0.0  
**Created:** 2026-03-23  
**Status:** Ready for use
