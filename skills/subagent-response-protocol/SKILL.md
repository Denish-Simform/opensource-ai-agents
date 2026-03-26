---
name: subagent-response-protocol
description: 'Enforce uniform structured response format for all specialized sub-agents enabling reliable aggregation by orchestrator. Use when: sub-agent reporting, standardizing agent outputs, orchestrator aggregation, structured agent responses, SA sub-agent formatting, consistent reporting protocol, agent communication standards, orchestrator integration, sub-agent output specification, agent response templates.'
argument-hint: 'Optionally specify agent type or specific section requirements'
---

# Sub-Agent Response Protocol

Standardized response format for all specialized sub-agents ensuring consistent, parseable, token-efficient outputs that orchestrators can reliably aggregate.

## When to Use

- **Sub-agent implementation** — All SA sub-agents must follow this protocol
- **Orchestrator design** — Orchestrators rely on this format for aggregation
- **Agent communication** — Standardizing how agents report findings
- **Response parsing** — Enabling reliable extraction of key information
- **Multi-agent workflows** — Ensuring interoperability between agents
- **Quality assurance** — Validating agent output completeness

## The Problem This Solves

**Before (Inconsistent):**
```markdown
Agent A: "I analyzed the security. There are some issues with authentication..."
Agent B: "Requirements Analysis Complete! Here's what I found: [long paragraph]..."  
Agent C: "LOW confidence due to missing artifacts"
```

**After (Standardized):**
```markdown
## Security Governance Assessment
**Confidence: LOW (35%)**
### Summary
Authentication design incomplete. Authorization model undefined. No security testing performed.
### Evidence
- Threat model: Partial (5%)
- Security controls: Missing (0%)
### Gaps
- Authorization model (critical)
- Security testing (10%)
### Recommendation
Complete security design before implementation.

## Requirements Intelligence Assessment
**Confidence: HIGH (85%)**
### Summary
Requirements complete and stakeholder-approved. NFRs quantified. Minor edge cases pending.
### Evidence
- Requirements docs: Complete (20%)
- Stakeholder approval: Obtained (15%)
### Gaps
- Edge case scenarios (3 of 15 stories)
### Recommendation
Requirements sufficient for design. Document edge cases during implementation.
```

## Standard Response Template

### Template Structure

```markdown
## [Agent Name] Assessment

**Confidence: [LEVEL] ([SCORE]%)**

### Summary
[2-3 sentences: What was analyzed, key findings, overall assessment]

### Evidence
- [Artifact/Area 1]: [Status/Finding]
- [Artifact/Area 2]: [Status/Finding]
- [Artifact/Area 3]: [Status/Finding]

### Gaps
- [Critical gap 1]
- [Critical gap 2]

### Recommendation
[1-2 sentences: Clear next step or decision]
```

### Required Sections

All sections are **mandatory**. Use "N/A" or "None" if truly not applicable.

#### 1. Header: `## [Agent Name] Assessment`

**Format:** `## [AgentName] Assessment`

**Purpose:** Clearly identifies which agent produced this response

**Examples:**
- `## Requirements Intelligence Assessment`
- `## Security Governance Assessment`
- `## Cost FinOps Assessment`
- `## Scalability Reliability Assessment`

**Token cost:** ~5-8 tokens

---

#### 2. Confidence: `**Confidence: [LEVEL] ([SCORE]%)**`

**Format:** `**Confidence: [LEVEL] ([SCORE]%)**`

**Purpose:** Quantified assessment using architecture-confidence-scoring

**Levels:** CRITICAL | LOW | MEDIUM | HIGH | VERIFIED

**Examples:**
- `**Confidence: HIGH (78%)**`
- `**Confidence: MEDIUM (62%)**`
- `**Confidence: LOW (35%)**`

**Integration:** Use [architecture-confidence-scoring](../architecture-confidence-scoring/SKILL.md) to compute

**Token cost:** ~8-10 tokens

---

#### 3. Summary: `### Summary`

**Format:** 2-3 concise sentences (max 60 words)

**Content:**
1. **What was analyzed** (scope)
2. **Key finding** (most important insight)
3. **Overall assessment** (ready/needs work)

**Good examples:**
```markdown
### Summary
Analyzed system scalability strategy and performance targets. Load testing shows 
system handles 3x peak capacity. Ready for production with monitoring in place.
```

```markdown
### Summary
Reviewed security architecture and threat model. Authentication design complete 
but authorization model undefined. Critical security gaps block implementation.
```

**Bad examples:**
```markdown
### Summary
I looked at a lot of things and found various issues that need to be addressed.
Some are critical, others are minor. Overall there's work to do.
```

**Token cost:** ~50-80 tokens

---

#### 4. Evidence: `### Evidence`

**Format:** Bulleted list of key artifacts/areas with status

**Structure:** `- [Artifact/Area]: [Status/Finding]`

**Keep concise:** 3-6 items max, prioritize by importance

**Status patterns:**
- `Complete ([score]%)`
- `Partial ([score]%)`
- `Missing`
- `N/A (not applicable)`
- `Verified`
- `Draft`

**Examples:**
```markdown
### Evidence
- Requirements documentation: Complete (20%)
- Architecture diagrams: Complete (15%)
- Technology decisions: Partial (8%) — 3 of 5 documented
- Risk assessment: Missing (0%)
```

```markdown
### Evidence
- Threat model: Partial (5%) — Application only, infrastructure missing
- Security controls: Missing (0%)
- Authentication design: Complete (8%)
- Compliance validation: Not started
```

**Token cost:** ~40-80 tokens

---

#### 5. Gaps: `### Gaps`

**Format:** Bulleted list of missing/incomplete critical items

**Structure:** `- [Gap description] ([impact if relevant])`

**Prioritize:** List critical gaps first

**Be specific:** Not "security needs work", but "authorization model undefined"

**Examples:**
```markdown
### Gaps
- Authorization model undefined (critical)
- Security testing not performed (10%)
- Compliance requirements not validated (5%)
```

```markdown
### Gaps
- Component-level design for payment service (3%)
- Load testing results pending implementation phase
```

```markdown
### Gaps
None — All required evidence present
```

**Token cost:** ~30-60 tokens

---

#### 6. Recommendation: `### Recommendation`

**Format:** 1-2 clear, actionable sentences

**Content:** Specific next step or gate decision

**Patterns:**
- **Ready:** "Approved for [next phase]. [Optional condition]."
- **Conditional:** "Proceed with caution. Address [gap] before [milestone]."
- **Block:** "Do not proceed. Complete [critical items] first."

**Good examples:**
```markdown
### Recommendation
Approved for implementation. Complete security testing during development phase.
```

```markdown
### Recommendation
Do not proceed to production. Address critical security gaps (authorization model, 
security testing) before deployment.
```

```markdown
### Recommendation
Requirements sufficient for detailed design. Re-assess after security review.
```

**Bad examples:**
```markdown
### Recommendation
You should probably think about addressing these issues at some point.
```

**Token cost:** ~20-40 tokens

---

## Total Token Budget Per Response

**Estimated:** 150-280 tokens per sub-agent response

**Breakdown:**
- Header: 5-8 tokens
- Confidence: 8-10 tokens
- Summary: 50-80 tokens
- Evidence: 40-80 tokens
- Gaps: 30-60 tokens
- Recommendation: 20-40 tokens

**Why this matters:** Orchestrator processing 5 sub-agents = ~750-1,400 tokens for all inputs

## Template Examples by Agent Type

### requirements-intelligence

```markdown
## Requirements Intelligence Assessment

**Confidence: HIGH (85%)**

### Summary
Requirements documentation complete with 15 user stories and quantified NFRs. 
Stakeholder approval obtained from Product Owner and Technical Lead. Minor edge 
cases pending for 3 stories.

### Evidence
- Functional requirements: Complete (15 user stories with acceptance criteria)
- Non-functional requirements: Complete (performance, scalability, availability targets defined)
- Stakeholder approval: 80% complete (security team review pending)
- Constraints: Documented (budget, timeline, technology)

### Gaps
- Edge case scenarios for 3 of 15 user stories
- Third-party API latency assumption not verified

### Recommendation
Requirements sufficient for detailed design phase. Verify API latency assumption 
and obtain security team approval before implementation.
```

---

### security-governance

```markdown
## Security Governance Assessment

**Confidence: LOW (38%)**

### Summary
Security architecture incomplete with critical gaps. Threat model covers application 
layer only. No security controls designed or tested. Authorization model undefined.

### Evidence
- Threat model: Partial (5%) — Application threats only, infrastructure missing
- Security controls: Missing (0%)
- Authentication design: Complete (8%)
- Data protection: Missing (0%)

### Gaps
- Authorization model undefined (critical)
- Secrets management strategy missing (critical)
- Security testing not performed (10%)
- Infrastructure security not designed (5%)

### Recommendation
Do not proceed to implementation. Complete threat model, design security controls, 
and define authorization model before development start.
```

---

### scalability-reliability

```markdown
## Scalability Reliability Assessment

**Confidence: HIGH (82%)**

### Summary
System capacity verified through load testing at 3x peak capacity. Autoscaling 
configured. Database query performance optimized. Monitoring and alerting in place.

### Evidence
- Load testing: Complete (10%) — Tested at 3x peak (30K concurrent users)
- Capacity planning: Complete (8%) — Infrastructure sized appropriately
- Performance optimization: Complete (7%) — Query optimization done
- Monitoring strategy: Complete (5%)

### Gaps
- Disaster recovery plan partial (3%) — Backup strategy defined, recovery procedures need documentation

### Recommendation
Approved for production. Document disaster recovery procedures during initial deployment.
```

---

### cost-finops

```markdown
## Cost FinOps Assessment

**Confidence: MEDIUM (65%)**

### Summary
Infrastructure costs estimated at $12K/month for target load. Budget within constraints 
($50K limit). Cost optimization opportunities identified but not critical for MVP.

### Evidence
- Infrastructure costs: Itemized ($12K/month projected)
- Service costs: Estimated ($3K/month for managed services)
- Cost optimization: Opportunities identified (reserved instances -20%)
- Budget validation: Within constraints ($15K < $50K limit)

### Gaps
- Data transfer costs estimated but not validated (may increase 10-20%)
- Cost monitoring dashboard not configured

### Recommendation
Approved with monitoring. Configure cost alerts and track actual vs estimated 
costs monthly. Implement reserved instances after 3 months if usage stable.
```

---

### system-design-domain-modeler

```markdown
## System Design Domain Modeler Assessment

**Confidence: MEDIUM (68%)**

### Summary
Architecture design complete with full C4 model (context, container, component views). 
Technology decisions documented for 3 of 5 key choices. Domain boundaries clearly defined.

### Evidence
- C4 diagrams: Complete (15%) — All 4 levels present and consistent
- Technology decisions: Partial (10%) — Database, API gateway, auth documented
- Domain model: Complete (8%) — Bounded contexts identified
- Deployment architecture: Partial (5%) — Kubernetes config 70% complete

### Gaps
- Technology decisions for caching strategy and message queue not documented (5%)
- Deployment configuration incomplete (service mesh, ingress rules pending)

### Recommendation
Approved for implementation start. Complete technology decisions and deployment 
configuration during sprint 1.
```

---

## Orchestrator Aggregation Pattern

### Step 1: Collect Sub-Agent Responses

Orchestrator invokes each sub-agent with this protocol requirement:

```markdown
[To sub-agent]: Analyze [domain] and respond using standard sub-agent protocol. 
Include: Confidence, Summary, Evidence, Gaps, Recommendation. Use architecture-confidence-scoring 
for confidence calculation.
```

### Step 2: Parse Responses

Extract key fields from each response:

```python
# Pseudocode for orchestrator
responses = []
for agent in sub_agents:
    response = agent.assess(input)
    parsed = {
        'agent': extract_header(response),
        'confidence': extract_confidence(response),
        'summary': extract_section(response, 'Summary'),
        'evidence': extract_section(response, 'Evidence'),
        'gaps': extract_section(response, 'Gaps'),
        'recommendation': extract_section(response, 'Recommendation')
    }
    responses.append(parsed)
```

### Step 3: Aggregate Findings

Synthesize into overall assessment:

```markdown
## Overall Architecture Assessment

### Sub-Agent Confidence Summary

| Agent | Confidence | Critical Gaps |
|-------|-----------|---------------|
| Requirements Intelligence | HIGH (85%) | Minor edge cases |
| System Design | MEDIUM (68%) | Tech decisions (2/5) |
| Security Governance | LOW (38%) | Authorization, testing ⚠️ |
| Scalability Reliability | HIGH (82%) | DR docs |
| Cost FinOps | MEDIUM (65%) | Data transfer validation |

**Overall Confidence: MEDIUM (64%)**

### Synthesis

**Strengths:** Requirements well-defined (85%), scalability validated through load 
testing (82%), system design models complete.

**Critical Issues:** Security architecture incomplete (38%) — authorization model 
undefined, no security testing. This is a blocking issue for production.

**Minor Concerns:** Technology decisions incomplete (2 of 5), cost estimates need 
validation, disaster recovery procedures pending documentation.

### Gate Decision

**Decision: CONDITIONAL APPROVAL for Implementation**

**Conditions:**
1. Complete security architecture (authorization model, security testing) — CRITICAL
2. Document remaining technology decisions during Sprint 1
3. Set up cost monitoring and validate data transfer estimates

**Rationale:** Strong requirements and scalability foundation. Security gaps are 
critical but addressable during development. Design sufficient to start implementation 
with conditions.

**Next Review:** After Sprint 1 (security architecture complete)
```

---

## Protocol Compliance Checklist

Before submitting response, verify:

- [ ] Header uses format `## [AgentName] Assessment`
- [ ] Confidence line present with level and score
- [ ] Confidence score calculated using architecture-confidence-scoring
- [ ] Summary is 2-3 sentences (max 60 words)
- [ ] Evidence lists 3-6 key items with status
- [ ] Gaps explicitly states critical missing items (or "None")
- [ ] Recommendation provides clear next step (1-2 sentences)
- [ ] Total response is ~150-280 tokens
- [ ] No extra sections or verbose explanations
- [ ] All sections use exact header names (Summary, Evidence, Gaps, Recommendation)

## Integration with Existing Skills

### architecture-confidence-scoring

**Relationship:** Sub-agent protocol **requires** confidence scoring

**Usage:**
1. Sub-agent invokes architecture-confidence-scoring to compute confidence
2. Sub-agent includes confidence in protocol response
3. Evidence section aligns with confidence calculation

**Example:**
```markdown
**Confidence: MEDIUM (62%)**  ← From architecture-confidence-scoring

### Evidence
- Requirements: Complete (20%)  ← Matches confidence evidence
- Diagrams: Partial (8%)        ← Matches confidence evidence
```

### runtime-environment-detection

**Relationship:** Protocol can adapt based on runtime environment

**Usage:**
- VS Code: Include file links in evidence `[file.ts](file.ts#L45)`
- CLI: Use absolute paths
- API: Can output as JSON instead of markdown

**Example:**
```markdown
### Evidence
- Architecture diagrams: See [architecture.md](docs/architecture.md#L12-L45)
- Code analysis: [services/auth](src/services/auth) passes quality gates
```

---

## Anti-Patterns

### ❌ Verbose Summaries

**Bad:**
```markdown
### Summary
In this analysis, I have thoroughly examined the security architecture from 
multiple perspectives. After careful consideration of various factors including 
authentication mechanisms, authorization models, data protection strategies, and 
compliance requirements, I have determined that there are several areas that 
require attention before we can proceed...
```

**Good:**
```markdown
### Summary
Security architecture incomplete. Authentication design done but authorization 
model undefined. No security testing performed. Critical gaps block implementation.
```

---

### ❌ Vague Evidence

**Bad:**
```markdown
### Evidence
- Some security stuff is done
- Architecture looks mostly okay
- A few things are missing
```

**Good:**
```markdown
### Evidence
- Threat model: Partial (5%) — Application layer only
- Security controls: Missing (0%)
- Authentication: Complete (8%)
```

---

### ❌ Unclear Gaps

**Bad:**
```markdown
### Gaps
- Various security issues
- Some design not finalized
- Testing needs attention
```

**Good:**
```markdown
### Gaps
- Authorization model undefined (critical)
- Security testing not performed (10%)
- Deployment config incomplete (3%)
```

---

### ❌ Wishy-Washy Recommendations

**Bad:**
```markdown
### Recommendation
You might want to consider looking at these issues. It would probably be good to 
address them at some point, assuming resources are available.
```

**Good:**
```markdown
### Recommendation
Do not proceed to production. Complete authorization model and security testing 
before deployment.
```

---

### ❌ Extra Sections

**Bad:**
```markdown
## Security Assessment

**Confidence: LOW (38%)**

### Executive Summary
[Long executive summary...]

### Detailed Analysis
[Pages of detail...]

### Summary
[Required summary...]

### Methodology
[How I analyzed...]

### Assumptions
[What I assumed...]

### Evidence
[Evidence list...]
```

**Good:**
```markdown
## Security Governance Assessment

**Confidence: LOW (38%)**

### Summary
[2-3 sentences]

### Evidence
[Key findings]

### Gaps
[Missing items]

### Recommendation
[Next step]
```

---

## Special Cases

### No Gaps Found

```markdown
### Gaps
None — All required evidence present and verified
```

### Domain Not Applicable

If an entire assessment doesn't apply:

```markdown
## Code Analysis Assessment

**Confidence: N/A**

### Summary
Code analysis not applicable during design phase. Will assess after implementation.

### Evidence
N/A — No code artifacts available (design phase)

### Gaps
N/A — Assessment scheduled for post-implementation

### Recommendation
Re-invoke code analysis after Sprint 1 implementation completes.
```

### Urgent Blockers

If critical issue demands immediate attention:

```markdown
## Security Governance Assessment

**Confidence: CRITICAL (5%)**

### Summary
URGENT: Proposed architecture exposes admin endpoints publicly with no authentication. 
Fatal security flaw. Immediate redesign required.

### Evidence
- API design review: Admin endpoints on public subnet (0%)
- Authentication: Not implemented for admin routes (0%)

### Gaps  
- Authentication for admin endpoints (CRITICAL)
- Network segmentation missing (CRITICAL)
- Security threat model not performed (10%)

### Recommendation
STOP IMMEDIATELY. Do not implement current design. Complete security architecture 
review and redesign admin endpoint security before any development.
```

---

## Template Files

See `/templates/` directory for copy-paste templates:

- `agent-response-template.md` — Blank template
- `requirements-intelligence-template.md` — Requirements agent template
- `security-governance-template.md` — Security agent template
- `scalability-reliability-template.md` — Scalability agent template
- `cost-finops-template.md` — Cost agent template
- `system-design-template.md` — Design agent template

---

## Best Practices

1. ✅ **Token efficiency** — Keep responses under 280 tokens
2. ✅ **Use exact section headers** — Summary, Evidence, Gaps, Recommendation (no variations)
3. ✅ **Integrate confidence scoring** — Always use architecture-confidence-scoring
4. ✅ **Be specific** — No vague language ("some issues", "looks okay")
5. ✅ **Prioritize gaps** — List critical gaps first
6. ✅ **Action-oriented recommendations** — Clear next steps, not suggestions
7. ✅ **Consistent confidence levels** — Use standard 5-level scale
8. ✅ **Bullet points over paragraphs** — Easier to parse
9. ✅ **Quantify when possible** — Use percentages, scores, numbers
10. ✅ **No extra sections** — Stick to 6 required sections only

---

## Validation by Orchestrator

Optional validation the orchestrator can perform:

```python
def validate_subagent_response(response: str) -> dict:
    """Validate sub-agent response format compliance"""
    
    required_headers = [
        "Assessment",  # Agent name header
        "**Confidence:",  # Confidence line
        "### Summary",
        "### Evidence",
        "### Gaps",
        "### Recommendation"
    ]
    
    issues = []
    for header in required_headers:
        if header not in response:
            issues.append(f"Missing required section: {header}")
    
    # Check token count
    token_count = estimate_tokens(response)
    if token_count > 300:
        issues.append(f"Response too verbose: {token_count} tokens (max 280)")
    
    # Check confidence format
    if "**Confidence:" in response:
        if not re.search(r'\*\*Confidence: (CRITICAL|LOW|MEDIUM|HIGH|VERIFIED) \(\d{1,3}%\)\*\*', response):
            issues.append("Invalid confidence format")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues
    }
```

---

## Related Skills

- **architecture-confidence-scoring** — Computes confidence scores for sub-agents
- **runtime-environment-detection** — Adapts output format based on runtime
- **agent-customization** — Creates custom sub-agents that follow this protocol

---

## Conclusion

The sub-agent response protocol standardizes communication between specialized sub-agents 
and orchestrators. By enforcing a consistent, token-efficient, parseable format, it 
enables reliable aggregation and synthesis of findings across multiple agents.

**Key Principles:**
- **Consistency** — Same format for all sub-agents
- **Conciseness** — ~150-280 tokens per response
- **Completeness** — All 6 required sections present
- **Clarity** — Specific, actionable, quantified
- **Parseable** — Predictable structure for orchestrator parsing
