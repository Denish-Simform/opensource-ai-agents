# Sub-Agent Response Protocol

Standardized response format for all specialized sub-agents ensuring consistent, parseable, token-efficient outputs that orchestrators can reliably aggregate.

## Quick Start

**Invoke this skill when:**
- Implementing a sub-agent that reports to an orchestrator
- Standardizing agent communication in multi-agent workflows
- Ensuring orchestrator can parse and aggregate responses
- Creating new SA (Solution Architect) sub-agents

**To use:** Type `/subagent-response-protocol` or instruct agents: "Respond using sub-agent protocol"

## The Problem

**Without standard protocol:**
```
Agent A: "I analyzed the security and found some issues..."
Agent B: "Requirements look good overall but..."
Agent C: "Cost estimation: probably around $10K"
```

**Result:** Orchestrator can't reliably parse → manual aggregation → inconsistent reporting

**With standard protocol:**
```
## Security Governance Assessment
**Confidence: LOW (38%)**
### Summary
Authorization model undefined. No security testing performed.
### Evidence
- Threat model: Partial (5%)
### Gaps
- Authorization model (critical)
### Recommendation
Do not proceed. Complete security design.
```

**Result:** Orchestrator automatically parses → systematic aggregation → consistent reporting

## Required Sections (6 Total)

Every sub-agent response **must** include:

1. **Header** — `## [Agent Name] Assessment`
2. **Confidence** — `**Confidence: [LEVEL] ([SCORE]%)**`
3. **Summary** — 2-3 sentences (what analyzed, key finding, assessment)
4. **Evidence** — Bulleted list of artifacts/findings (3-6 items)
5. **Gaps** — Bulleted list of missing/incomplete items
6. **Recommendation** — 1-2 sentences (clear next step)

**Token budget:** 150-280 tokens per response

## Quick Example

```markdown
## Requirements Intelligence Assessment

**Confidence: HIGH (85%)**

### Summary
Requirements complete with 15 user stories and quantified NFRs. Stakeholder 
approval obtained. Minor edge cases pending for 3 stories.

### Evidence
- Functional requirements: Complete (15 stories with acceptance criteria)
- Non-functional requirements: Complete (performance, scalability targets defined)
- Stakeholder approval: 80% complete (security review pending)
- Constraints: Documented (budget, timeline, technology)

### Gaps
- Edge case scenarios for 3 of 15 user stories
- Third-party API latency assumption not verified

### Recommendation
Requirements sufficient for detailed design phase. Verify API latency assumption 
before implementation.
```

## Integration with Other Skills

### architecture-confidence-scoring

**Required:** Use this skill to calculate confidence score

```markdown
[Invoke architecture-confidence-scoring]
Result: MEDIUM (62%)

[Use in response]
**Confidence: MEDIUM (62%)**
```

### sa-orchestrator

**Orchestrator invokes sub-agents:**

```markdown
[To sub-agent]: Assess security using sub-agent response protocol.
[Sub-agent returns]: Standard format response
[Orchestrator]: Parses all responses → Aggregates → Synthesizes
```

## Files in This Skill

```
subagent-response-protocol/
├── SKILL.md                           # Complete protocol specification
├── README.md                          # This file
├── templates/
│   ├── agent-response-template.md     # Blank template
│   ├── requirements-intelligence-template.md
│   ├── security-governance-template.md
│   ├── scalability-reliability-template.md
│   ├── cost-finops-template.md
│   └── system-design-template.md
└── references/
    └── orchestrator-aggregation.md    # How orchestrators parse & aggregate
```

## Copy-Paste Templates

### General Template

```markdown
## [Agent Name] Assessment

**Confidence: [LEVEL] ([SCORE]%)**

### Summary
[2-3 sentences: What analyzed, key finding, assessment]

### Evidence
- [Artifact 1]: [Status]
- [Artifact 2]: [Status]
- [Artifact 3]: [Status]

### Gaps
- [Critical gap 1]
- [Critical gap 2]

### Recommendation
[1-2 sentences: Next step]
```

See [templates/](./templates/) directory for agent-specific templates.

## Token Efficiency

**Design goal:** Minimal tokens, maximum information density

| Section | Tokens | Purpose |
|---------|--------|---------|
| Header | 5-8 | Agent identification |
| Confidence | 8-10 | Quantified assessment |
| Summary | 50-80 | Key findings |
| Evidence | 40-80 | Artifact status |
| Gaps | 30-60 | Missing items |
| Recommendation | 20-40 | Next action |
| **Total** | **150-280** | **Complete response** |

**Why it matters:** Orchestrator processing 5 sub-agents → 750-1,400 tokens input → Efficient aggregation

## Best Practices

1. ✅ **Use exact section headers** — Summary, Evidence, Gaps, Recommendation (no variations)
2. ✅ **Calculate confidence** — Use architecture-confidence-scoring skill
3. ✅ **Be specific** — "Authorization model undefined" not "some security issues"
4. ✅ **Prioritize gaps** — List critical gaps first
5. ✅ **Action-oriented recommendations** — "Do not proceed" not "you might want to think about"
6. ✅ **Stay within token budget** — 150-280 tokens per response
7. ✅ **Use bullet points** — Easier to parse than paragraphs
8. ✅ **Quantify evidence** — Include percentages, scores, counts
9. ✅ **No extra sections** — Stick to 6 required sections
10. ✅ **Complete all sections** — Use "None" if truly no gaps

## Anti-Patterns

❌ **Verbose summaries** — Keep to 2-3 sentences  
❌ **Vague evidence** — "Some things are done" → Specify what  
❌ **Unclear gaps** — "Various issues" → List specific items  
❌ **Wishy-washy recommendations** — "Maybe consider..." → Be direct  
❌ **Extra sections** — Don't add "Methodology", "Assumptions", etc.  
❌ **Missing sections** — All 6 sections are mandatory  

## Example Prompts

### For Sub-Agents

1. **Basic invocation:**
   > "Assess security architecture using sub-agent response protocol. Include confidence from architecture-confidence-scoring."

2. **With context:**
   > "Review requirements documentation and report using standard sub-agent protocol. Follow 6-section format."

3. **Template-based:**
   > "Use security-governance template from sub-agent-response-protocol to report findings."

### For Orchestrators

1. **Invoke sub-agents:**
   > "Invoke all SA sub-agents (requirements, design, security, scalability, cost) using sub-agent response protocol."

2. **Aggregate responses:**
   > "Aggregate the 5 sub-agent responses and synthesize overall architecture assessment."

3. **Parse and validate:**
   > "Parse sub-agent responses, validate protocol compliance, and produce synthesis report."

## Orchestrator Aggregation

See [orchestrator-aggregation.md](./references/orchestrator-aggregation.md) for:
- Parsing logic (extract confidence, evidence, gaps)
- Aggregation algorithm (calculate overall confidence)
- Synthesis patterns (produce final report)
- Complete examples with 5 sub-agents

## Common Questions

**Q: What if my agent doesn't fit the 6-section format?**  
A: All SA sub-agents must use this format for consistency. If truly not applicable, use "N/A" for sections.

**Q: Can I add extra sections?**  
A: No. Extra sections increase tokens and make parsing harder. Put additional info in Evidence or Gaps.

**Q: What if no gaps found?**  
A: Write `### Gaps\nNone — All required evidence present`

**Q: How do I calculate confidence?**  
A: Use the [architecture-confidence-scoring](../architecture-confidence-scoring/README.md) skill. It provides systematic scoring method.

**Q: Must I use markdown?**  
A: Yes for default. JSON output is possible but markdown is more LLM-friendly and uses fewer tokens.

**Q: What if my response exceeds 280 tokens?**  
A: Revise for conciseness. Remove unnecessary adjectives. Use bullet points. Combine related items.

## Compliance Checklist

Before submitting response:

- [ ] Header uses `## [Agent Name] Assessment` format
- [ ] Confidence line present with level and score
- [ ] Confidence calculated using architecture-confidence-scoring
- [ ] Summary is 2-3 sentences (max 60 words)
- [ ] Evidence lists 3-6 items with status
- [ ] Gaps lists specific missing items (or "None")
- [ ] Recommendation provides clear next step (1-2 sentences)
- [ ] Total response is ~150-280 tokens
- [ ] No extra sections added
- [ ] All section headers use exact naming (Summary, Evidence, Gaps, Recommendation)

## Related Skills

- **architecture-confidence-scoring** — Required for confidence calculation
- **runtime-environment-detection** — Can adapt output format based on environment
- **agent-customization** — Create custom sub-agents following this protocol

## Support

For questions about the protocol:
1. Review [SKILL.md](./SKILL.md) for complete specification
2. Check [templates/](./templates/) for agent-specific examples
3. See [orchestrator-aggregation.md](./references/orchestrator-aggregation.md) for parsing logic
4. File issue in awesome-copilot-opensource repository

---

**Version:** 1.0.0  
**Created:** 2026-03-23  
**Status:** ✅ Ready for use  
**Mandatory for:** All SA sub-agents

**Key Principle:** *Consistency enables automation. Standard format = reliable aggregation.*
