# Orchestrator Aggregation Patterns

How orchestrators collect, parse, and synthesize sub-agent responses following the standard protocol.

## Pattern 1: Sequential Sub-Agent Invocation

**Use when:** Sub-agents don't depend on each other's outputs

### Process

```markdown
1. Orchestrator receives user request
2. Identifies required sub-agents based on request
3. Invokes each sub-agent sequentially
4. Collects responses in standardformat
5. Aggregates findings
6. Produces synthesis report
```

### Example Orchestrator Flow

```markdown
## Orchestrator: Architecture Review Request

**Request:** "Review the proposed e-commerce platform architecture"

### Step 1: Identify Required Sub-Agents

- requirements-intelligence (requirements complete?)
- system-design-domain-modeler (architecture sound?)
- security-governance (security adequate?)
- scalability-reliability (can it scale?)
- cost-finops (within budget?)

### Step 2: Invoke Sub-Agents

**To requirements-intelligence:**
"Assess requirements completeness for e-commerce platform. Use sub-agent response 
protocol. Include confidence from architecture-confidence-scoring."

**Response:**
## Requirements Intelligence Assessment
**Confidence: HIGH (85%)**
### Summary
Requirements complete with 15 user stories and quantified NFRs...
### Evidence
- Functional requirements: Complete (20%)
...

[Repeat for each sub-agent]

### Step 3: Parse Responses

Extracted data:
- requirements-intelligence: HIGH (85%), minor gaps
- system-design-domain-modeler: MEDIUM (68%), 2 tech decisions missing
- security-governance: LOW (38%), critical auth gaps
- scalability-reliability: HIGH (82%), DR docs pending
- cost-finops: MEDIUM (65%), monitoring setup needed

### Step 4: Aggregate Findings

[Use aggregation algorithm to synthesize]

### Step 5: Produce Synthesis

[Final report with overall confidence and recommendations]
```

---

## Pattern 2: Parallel Sub-Agent Invocation

**Use when:** Sub-agents work independently and speed matters

### Benefits

- Faster overall assessment (parallel execution)
- Sub-agents don't wait for each other
- Suitable for large architectures

### Process

```markdown
1. Orchestrator identifies required sub-agents
2. Invokes ALL sub-agents in parallel
3. Waits for all responses
4. Aggregates when all complete
5. Produces synthesis
```

### Implementation Note

LLM agents typically run sequentially, but this pattern is important for future parallel execution or when using multiple agent instances.

---

## Pattern 3: Conditional Sub-Agent Chain

**Use when:** Next sub-agent depends on previous results

### Process

```markdown
1. Invoke requirements-intelligence first
2. IF requirements confidence < MEDIUM:
   - Stop and report "Requirements insufficient"
3. ELSE:
   - Invoke design and security sub-agents
4. IF security confidence < MEDIUM:
   - Skip scalability (security must be addressed first)
5. ELSE:
   - Invoke scalability and cost sub-agents
6. Aggregate all responses
```

### Example Flow

```markdown
Step 1: Requirements check
→ Confidence: HIGH (85%) ✓ Proceed

Step 2: Design + Security (parallel)
→ Design: MEDIUM (68%) ✓
→ Security: LOW (38%) ⚠️ Critical gaps

Step 3: Decision point
→ Security LOW means don't assess scalability yet
→ Skip scalability-reliability
→ Skip cost-finops
→ Recommend: "Fix security first"

Output: "Architecture review blocked by security gaps. Address authorization 
model and security testing before proceeding to scalability assessment."
```

---

## Parsing Logic

### Extract Confidence

```python
def extract_confidence(response: str) -> tuple:
    """Extract confidence level and score from response"""
    
    pattern = r'\*\*Confidence: (CRITICAL|LOW|MEDIUM|HIGH|VERIFIED) \((\d{1,3})%\)\*\*'
    match = re.search(pattern, response)
    
    if match:
        level = match.group(1)
        score = int(match.group(2))
        return (level, score)
    
    return (None, None)

# Example usage
response = "**Confidence: HIGH (82%)**"
level, score = extract_confidence(response)
# Returns: ('HIGH', 82)
```

### Extract Summary

```python
def extract_summary(response: str) -> str:
    """Extract summary section from response"""
    
    # Find text between ### Summary and next ### section
    pattern = r'### Summary\n(.*?)\n###'
    match = re.search(pattern, response, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return None

# Example usage
summary = extract_summary(response)
# Returns: "Security architecture incomplete..."
```

### Extract Evidence List

```python
def extract_evidence(response: str) -> list:
    """Extract evidence items from response"""
    
    # Find text between ### Evidence and ### Gaps
    pattern = r'### Evidence\n(.*?)\n### Gaps'
    match = re.search(pattern, response, re.DOTALL)
    
    if not match:
        return []
    
    evidence_text = match.group(1).strip()
    
    # Parse bullet points
    items = []
    for line in evidence_text.split('\n'):
        line = line.strip()
        if line.startswith('- '):
            items.append(line[2:])  # Remove "- " prefix
    
    return items

# Example usage
evidence = extract_evidence(response)
# Returns: ['Threat model: Partial (5%)', 'Security controls: Missing (0%)', ...]
```

### Extract Gaps List

```python
def extract_gaps(response: str) -> list:
    """Extract gap items from response"""
    
    # Find text between ### Gaps and ### Recommendation
    pattern = r'### Gaps\n(.*?)\n### Recommendation'
    match = re.search(pattern, response, re.DOTALL)
    
    if not match:
        return []
    
    gaps_text = match.group(1).strip()
    
    # Check for "None" indicator
    if gaps_text.lower().startswith('none'):
        return []
    
    # Parse bullet points
    items = []
    for line in gaps_text.split('\n'):
        line = line.strip()
        if line.startswith('- '):
            items.append(line[2:])
    
    return items
```

### Extract Recommendation

```python
def extract_recommendation(response: str) -> str:
    """Extract recommendation from response"""
    
    # Find text after ### Recommendation to end
    pattern = r'### Recommendation\n(.*?)(?:\n##|$)'
    match = re.search(pattern, response, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return None
```

---

## Aggregation Algorithm

### Step 1: Calculate Overall Confidence

```python
def calculate_overall_confidence(responses: list) -> tuple:
    """
    Calculate overall architecture confidence from sub-agent scores
    
    Strategies:
    1. Weighted average (critical agents weighted higher)
    2. Minimum confidence (conservative)
    3. Custom formula
    """
    
    # Strategy 1: Weighted average
    weights = {
        'requirements-intelligence': 0.25,
        'system-design-domain-modeler': 0.20,
        'security-governance': 0.25,  # High weight for security
        'scalability-reliability': 0.15,
        'cost-finops': 0.15
    }
    
    weighted_sum = 0
    for response in responses:
        agent = response['agent']
        score = response['score']
        weight = weights.get(agent, 0.10)  # Default weight if not in map
        weighted_sum += score * weight
    
    overall_score = weighted_sum
    overall_level = map_score_to_level(overall_score)
    
    return (overall_level, overall_score)

# Strategy 2: Conservative (minimum)
def calculate_conservative_confidence(responses: list) -> tuple:
    """Use lowest confidence among critical agents"""
    
    critical_agents = [
        'requirements-intelligence',
        'security-governance',
        'system-design-domain-modeler'
    ]
    
    min_score = 100
    for response in responses:
        if response['agent'] in critical_agents:
            min_score = min(min_score, response['score'])
    
    return (map_score_to_level(min_score), min_score)
```

### Step 2: Identify Critical Issues

```python
def identify_critical_issues(responses: list) -> list:
    """
    Extract critical gaps across all sub-agents
    
    Critical = confidence LOW or CRITICAL
    """
    
    critical_issues = []
    
    for response in responses:
        if response['level'] in ['CRITICAL', 'LOW']:
            agent = response['agent']
            gaps = response['gaps']
            critical_issues.append({
                'agent': agent,
                'confidence': response['level'],
                'score': response['score'],
                'gaps': gaps
            })
    
    return critical_issues
```

### Step 3: Synthesize Recommendations

```python
def synthesize_recommendation(responses: list, overall_confidence: tuple) -> dict:
    """
    Produce overall recommendation based on aggregated findings
    """
    
    level, score = overall_confidence
    critical_issues = identify_critical_issues(responses)
    
    # Decision logic
    if level == 'CRITICAL' or len(critical_issues) > 0 and any(i['level'] == 'CRITICAL' for i in critical_issues):
        decision = 'STOP'
        rationale = 'Critical flaws in architecture. Fundamental rework required.'
    
    elif level == 'LOW':
        decision = 'REVISE'
        rationale = 'Significant gaps must be addressed before proceeding.'
    
    elif level == 'MEDIUM':
        if len(critical_issues) > 0:
            decision = 'CONDITIONAL APPROVAL'
            rationale = f'Address {len(critical_issues)} critical issues during implementation.'
        else:
            decision = 'CONDITIONAL APPROVAL'
            rationale = 'Proceed with caution. Close gaps before production.'
    
    elif level == 'HIGH':
        if len(critical_issues) > 0:
            decision = 'CONDITIONAL APPROVAL'
            rationale = 'Minor issues to address. Approved for implementation.'
        else:
            decision = 'APPROVED'
            rationale = 'Architecture ready for implementation.'
    
    else:  # VERIFIED
        decision = 'APPROVED'
        rationale = 'Architecture verified and ready for production.'
    
    # Extract next steps from critical issues
    next_steps = []
    for issue in critical_issues:
        for gap in issue['gaps'][:2]:  # Top 2 gaps per critical area
            next_steps.append(f"Address {gap} ({issue['agent']})")
    
    return {
        'decision': decision,
        'rationale': rationale,
        'next_steps': next_steps[:5],  # Max 5 next steps
        're_assessment_trigger': determine_reassessment_trigger(critical_issues)
    }
```

---

## Synthesis Report Template

```markdown
## Overall Architecture Assessment

### Sub-Agent Confidence Summary

| Agent | Confidence | Key Gaps |
|-------|-----------|----------|
| [Agent 1] | [LEVEL] ([XX]%) | [Gap summary] |
| [Agent 2] | [LEVEL] ([XX]%) | [Gap summary] |
| [Agent 3] | [LEVEL] ([XX]%) | [Gap summary] |

**Overall Confidence: [LEVEL] ([XX]%)**

### Synthesis

**Strengths:** [Top 2-3 strengths from HIGH confidence agents]

**Critical Issues:** [Issues from LOW/CRITICAL confidence agents]

**Minor Concerns:** [Issues from MEDIUM confidence agents]

### Gate Decision

**Decision: [APPROVED/CONDITIONAL/REVISE/STOP]**

**Conditions:** [If conditional approval]
1. [Condition 1]
2. [Condition 2]

**Rationale:** [Why this decision was made]

**Next Review:** [When to re-assess]
```

---

## Example Complete Aggregation

### Input: 5 Sub-Agent Responses

```markdown
## Requirements Intelligence Assessment
**Confidence: HIGH (85%)**
### Summary
Requirements complete with 15 user stories...
### Evidence
- Functional requirements: Complete (20%)
### Gaps
- Edge cases for 3 stories
### Recommendation
Sufficient for design.

---

## System Design Domain Modeler Assessment
**Confidence: MEDIUM (68%)**
### Summary
C4 model complete. 2 tech decisions pending...
### Evidence
- C4 diagrams: Complete (15%)
### Gaps
- Tech decisions for cache and queue (5%)
### Recommendation
Approved for implementation. Complete during Sprint 1.

---

## Security Governance Assessment
**Confidence: LOW (38%)**
### Summary
Critical security gaps. Authorization undefined...
### Evidence
- Threat model: Partial (5%)
### Gaps
- Authorization model (critical)
- Security testing (10%)
### Recommendation
Do not proceed. Complete security design first.

---

## Scalability Reliability Assessment
**Confidence: HIGH (82%)**
### Summary
Load tested at 3x capacity. Ready for production...
### Evidence
- Load testing: Complete (10%)
### Gaps
- DR procedures documentation
### Recommendation
Approved. Document DR during deployment.

---

## Cost FinOps Assessment
**Confidence: MEDIUM (65%)**
### Summary
Costs within budget. Monitoring needed...
### Evidence
- Infrastructure costs: $12K/month
### Gaps
- Cost monitoring setup
### Recommendation
Approved with monitoring.
```

### Output: Synthesized Report

```markdown
## Overall Architecture Assessment

### Sub-Agent Confidence Summary

| Agent | Confidence | Key Gaps |
|-------|-----------|----------|
| Requirements Intelligence | HIGH (85%) | Minor edge cases |
| System Design | MEDIUM (68%) | 2 tech decisions |
| Security Governance | LOW (38%) | Authorization, testing ⚠️ |
| Scalability Reliability | HIGH (82%) | DR docs |
| Cost FinOps | MEDIUM (65%) | Monitoring setup |

**Overall Confidence: MEDIUM (64%)**

*Calculation: (85×0.25 + 68×0.20 + 38×0.25 + 82×0.15 + 65×0.15) = 64%*

### Synthesis

**Strengths:** Requirements well-defined and stakeholder-approved (85%). Scalability 
validated through comprehensive load testing at 3x capacity (82%). C4 architecture 
model complete and consistent.

**Critical Issues:** Security architecture incomplete (38%) — authorization model 
undefined and security testing not performed. This is a BLOCKING issue for production 
deployment.

**Minor Concerns:** Technology decisions pending for caching and message queue 
strategies (can be completed during Sprint 1). Cost monitoring dashboard needs 
configuration. Disaster recovery procedures need documentation.

### Gate Decision

**Decision: CONDITIONAL APPROVAL for Implementation**

**Conditions:**
1. Complete security architecture (authorization model, security testing) — REQUIRED before production
2. Document remaining 2 technology decisions during Sprint 1
3. Set up cost monitoring dashboard
4. Document disaster recovery procedures

**Rationale:** Strong requirements foundation and validated scalability provide confidence 
for implementation start. Security gaps are critical but addressable during development 
phase. Design completeness sufficient for Sprint 1. Cost within budget constraints.

**Next Review:** After Sprint 1 completion and security architecture review (estimated 4 weeks)

**Recommended Actions (Priority Order):**
1. Schedule security architecture review — address authorization model (CRITICAL)
2. Plan security testing (penetration testing, SAST/DAST) for Sprint 2
3. Document cache and message queue technology decisions by Sprint 1 end
4. Configure cost monitoring and alerting (via Azure Portal / AWS CloudWatch)
5. Create disaster recovery runbook template
```

---

## Token Efficiency

### Per Response Parsing

- Extract confidence: ~5 tokens (regex operations)
- Extract summary: ~50-80 tokens (content dependent)
- Extract evidence: ~40-80 tokens
- Extract gaps: ~30-60 tokens
- Store for aggregation: ~150-280 tokens per agent

### Orchestrator Synthesis

- Parse 5 sub-agents: ~750-1,400 tokens input
- Generate synthesis: ~400-600 tokens output
- **Total orchestrator operation: ~1,150-2,000 tokens**

### Optimization Tips

1. **Parallel parsing:** Parse all responses before synthesis
2. **Summarize evidence:** Don't repeat full evidence in synthesis
3. **Top N critical gaps:** Show max 3-5 critical gaps total
4. **Confidence table:** Compact overview reduces tokens
5. **Token budget per synthesis:** Target <600 tokens for orchestrator output

---

## Best Practices

1. ✅ **Parse before aggregate** — Extract all data first, then synthesize
2. ✅ **Weight confidence appropriately** — Critical agents (security, requirements) should have higher weight
3. ✅ **Fail fast on CRITICAL** — If any agent returns CRITICAL confidence, overall should not exceed MEDIUM
4. ✅ **Highlight blocking issues** — Make critical gaps visually distinct
5. ✅ **Provide clear decision** — APPROVED/CONDITIONAL/REVISE/STOP (no ambiguity)
6. ✅ **Limit next steps** — Max 5 actionable items
7. ✅ **Set re-assessment trigger** — When should architecture be reviewed again?
8. ✅ **Show calculation** — Briefly explain how overall confidence was derived
9. ✅ **Balance detail and conciseness** — Synthesis should be ~400-600 tokens
10. ✅ **Link related gaps** — Group related gaps from multiple agents

---

## Validation Checklist

Before finalizing synthesis:

- [ ] Overall confidence calculated correctly
- [ ] All sub-agent responses parsed successfully
- [ ] Critical issues identified and highlighted
- [ ] Gate decision aligned with confidence level
- [ ] Next steps are specific and actionable
- [ ] Re-assessment trigger defined
- [ ] Synthesis is 400-600 tokens
- [ ] Confidence table included
- [ ] Rationale explains decision clearly
- [ ] No contradictions between sub-agent findings
