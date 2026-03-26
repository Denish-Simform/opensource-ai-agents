---
name: architecture-confidence-scoring
description: 'Compute, explain, and standardize architecture confidence scoring based on available evidence, missing artifacts, and verification depth. Use when: assessing architecture quality, reporting confidence levels, preventing vague confidence statements, evaluating design completeness, scoring solution proposals, architecture review confidence, evidence-based assessment, SA agent confidence reporting, architecture validation scoring.'
argument-hint: 'Optionally specify architecture domain or artifacts to score'
---

# Architecture Confidence Scoring

Standardized methodology for computing and reporting architecture confidence levels based on evidence, verification depth, and artifact completeness. Prevents vague confidence statements by requiring systematic, evidence-based scoring.

## When to Use

- **Architecture assessments** — Computing confidence in proposed designs
- **Solution reviews** — Evaluating completeness and quality of architecture artifacts
- **Sub-agent reporting** — Standardizing confidence levels across SA agents
- **Risk evaluation** — Identifying gaps that lower confidence
- **Stakeholder communication** — Providing clear, justified confidence statements
- **Decision gates** — Determining if architecture is ready to proceed

## Confidence Scale

Five-level scale with clear criteria for each level:

| Level | Score | Description | Proceed? |
|-------|-------|-------------|----------|
| **CRITICAL** | 0-20% | Fatal flaws, major gaps, unverified assumptions | ❌ Stop |
| **LOW** | 21-40% | Significant gaps, many unverified elements | ⚠️ Risky |
| **MEDIUM** | 41-69% | Some gaps, partial verification, acceptable for early stages | ⚠️ Proceed with caution |
| **HIGH** | 70-89% | Most elements verified, minor gaps, ready for implementation | ✅ Proceed |
| **VERIFIED** | 90-100% | Comprehensive evidence, validated assumptions, production-ready | ✅ Proceed with confidence |

## Evidence Types and Weights

Standard architecture artifacts that contribute to confidence scoring:

### Core Evidence (High Weight: 15-20% each)

| Artifact | Weight | Description | Verification Method |
|----------|--------|-------------|---------------------|
| **Requirements Documentation** | 20% | Functional + non-functional requirements clearly defined | Check for completeness, traceability, stakeholder sign-off |
| **Architecture Diagrams** | 15% | System context, container, component, deployment views | Verify consistency, notation standards, completeness |
| **Technology Decisions** | 15% | Documented decision records with rationale | Check for alternatives considered, trade-offs analyzed |
| **Risk Assessment** | 15% | Identified risks with mitigation strategies | Verify coverage, likelihood/impact analysis |

### Supporting Evidence (Medium Weight: 5-10% each)

| Artifact | Weight | Description | Verification Method |
|----------|--------|-------------|---------------------|
| **Performance Analysis** | 10% | Load testing, capacity planning, bottleneck analysis | Check for realistic scenarios, baseline metrics |
| **Security Analysis** | 10% | Threat modeling, security controls, compliance mapping | Verify threat coverage, control effectiveness |
| **Cost Analysis** | 5% | Budget estimates, TCO, cost optimization | Check for itemization, assumptions documented |
| **Code Analysis** | 5% | Static analysis, quality metrics, technical debt | Verify against standards, check coverage |
| **Test Coverage** | 5% | Unit, integration, E2E test strategy and results | Check for critical path coverage |

### Total Weight: 100%

## Scoring Algorithm

### Step 1: Evidence Inventory

List all available artifacts with completion status:

```markdown
## Evidence Inventory

### Core Evidence (70%)
- [x] Requirements Documentation (20%) — Complete, stakeholder-approved
- [x] Architecture Diagrams (15%) — 4/4 C4 views present
- [~] Technology Decisions (15%) — 3/5 decisions documented
- [ ] Risk Assessment (15%) — Missing

### Supporting Evidence (30%)
- [x] Performance Analysis (10%) — Load testing complete
- [~] Security Analysis (10%) — Threat model draft only
- [ ] Cost Analysis (5%) — Not started
- [ ] Code Analysis (5%) — Not applicable (design phase)
- [ ] Test Coverage (5%) — Not applicable (design phase)
```

**Legend:**
- `[x]` Complete and verified (100% of weight)
- `[~]` Partially complete (50% of weight)
- `[ ]` Missing or not verified (0% of weight)

### Step 2: Calculate Base Score

```
Base Score = Σ (Artifact Weight × Completion Percentage)

Example:
- Requirements: 20% × 100% = 20
- Diagrams: 15% × 100% = 15
- Decisions: 15% × 50% = 7.5
- Risk: 15% × 0% = 0
- Performance: 10% × 100% = 10
- Security: 10% × 50% = 5
- Cost: 5% × 0% = 0
- Code: 5% × 0% = 0 (N/A)
- Tests: 5% × 0% = 0 (N/A)

Base Score = 57.5%
```

### Step 3: Apply Modifiers

Adjust base score based on quality factors:

| Modifier | Adjustment | When to Apply |
|----------|-----------|---------------|
| **Critical Gap** | -20% | Core evidence missing (requirements, risk, decisions) |
| **Unverified Assumptions** | -10% | Key assumptions not validated |
| **Inconsistent Artifacts** | -10% | Diagrams contradict documentation |
| **Outdated Evidence** | -5% | Artifacts >6 months old without review |
| **External Validation** | +10% | Third-party review or audit completed |
| **Production Proven** | +15% | Similar architecture in production |

**Example with Modifiers:**
```
Base Score: 57.5%
- Critical Gap (Risk Assessment missing): -20%
- Unverified Assumptions (scalability numbers): -10%

Final Score: 27.5% → LOW CONFIDENCE
```

### Step 4: Map to Confidence Level

```
Final Score → Confidence Level:
0-20%   → CRITICAL
21-40%  → LOW
41-69%  → MEDIUM
70-89%  → HIGH
90-100% → VERIFIED
```

## Standard Output Format

### Brief Justification (Required)

```markdown
**Confidence: [LEVEL] ([SCORE]%)**

Based on: [2-3 key evidence points]
Missing: [1-2 critical gaps]
Recommendation: [Next step or gate decision]
```

### Example Output

```markdown
**Confidence: MEDIUM (57%)**

Based on: Complete requirements (20%), verified architecture diagrams (15%), successful load testing (10%)
Missing: Risk assessment (15%), full security threat model (5%), technology decision rationale for 2/5 choices (7.5%)
Recommendation: Complete risk assessment before proceeding to implementation. Security gaps acceptable for MVP.
```

## Integration with SA Agents

### For Orchestrator (sa-orchestrator)

```markdown
## Final Assessment

After collecting outputs from all sub-agents, compute overall confidence:

1. Inventory evidence from all sub-agent reports
2. Calculate base score using evidence weights
3. Apply modifiers based on quality factors
4. Report confidence with brief justification
5. Recommend gate decision (proceed/revise/stop)
```

### For Sub-Agents

Each sub-agent reports confidence for their domain:

```markdown
## [Agent Name] Assessment

**Domain Confidence: [LEVEL] ([SCORE]%)**

Evidence reviewed:
- [Artifact 1]: Complete
- [Artifact 2]: Partial
- [Artifact 3]: Missing

Key findings: [2-3 sentences]
Gaps: [1-2 critical items]
```

**Example from security-governance agent:**

```markdown
## Security Governance Assessment

**Domain Confidence: LOW (35%)**

Evidence reviewed:
- Threat model: Partial (application layer only, infrastructure threats missing)
- Security controls: Missing (no IAM design, no network segmentation)
- Compliance mapping: Not started

Key findings: Authentication strategy defined but authorization model incomplete. No data classification performed.
Gaps: Infrastructure security design, compliance requirements validation
```

### Aggregating Sub-Agent Confidence

Orchestrator combines domain-specific confidence:

```markdown
## Overall Architecture Confidence

Sub-agent confidence levels:
- requirements-intelligence: HIGH (78%)
- system-design-domain-modeler: MEDIUM (65%)
- security-governance: LOW (35%)
- scalability-reliability: HIGH (82%)
- cost-finops: MEDIUM (60%)

Weighted average: 64% → MEDIUM

**Overall Confidence: MEDIUM (64%)**

Based on: Strong requirements and scalability analysis, well-defined domain model
Missing: Comprehensive security design (critical), detailed cost breakdown
Recommendation: Address security gaps before implementation. Cost analysis sufficient for MVP approval.
```

## Decision Gate Mapping

Use confidence levels to guide architecture governance:

| Gate | Required Confidence | Evidence Required |
|------|-------------------|-------------------|
| **Concept Approval** | MEDIUM (41%+) | Requirements, high-level design |
| **Design Approval** | HIGH (70%+) | Complete C4 diagrams, decisions documented, risk assessed |
| **Implementation Start** | HIGH (70%+) | Above + security reviewed, cost approved |
| **Production Release** | VERIFIED (90%+) | All evidence complete, external validation, test coverage |

## Common Scenarios

### Scenario 1: Early Stage Assessment

**Context:** Initial architecture proposal, early design phase

**Expected Confidence:** MEDIUM (41-69%)

**Typical Evidence:**
- Requirements: Complete or partial
- High-level diagrams: Present
- Technology decisions: Proposed but not finalized
- Risk: Initial assessment
- Performance/Security/Cost: Estimates only

**Example:**
```
Confidence: MEDIUM (52%)
Based on: Draft requirements (10%), C4 context + container diagrams (12%), initial tech stack selection (8%)
Missing: Component-level design, detailed risk analysis, cost estimates
Recommendation: Sufficient for concept approval. Develop detailed design before implementation.
```

### Scenario 2: Pre-Implementation Review

**Context:** Detailed design complete, ready for development

**Expected Confidence:** HIGH (70-89%)

**Typical Evidence:**
- Requirements: Complete and approved
- All C4 diagrams: Present and consistent
- Technology decisions: Documented with rationale
- Risk: Assessed with mitigations
- Security: Threat model complete
- Performance: Capacity plan ready

**Example:**
```
Confidence: HIGH (76%)
Based on: Complete requirements (20%), full C4 model (15%), 5/5 tech decisions documented (15%), risk register with mitigations (12%)
Missing: Cost breakdown detailed to component level (3%), load testing results (pending implementation)
Recommendation: Approved for implementation start. Re-assess after MVP for production release.
```

### Scenario 3: Production Readiness

**Context:** System built, ready for production deployment

**Expected Confidence:** VERIFIED (90-100%)

**Typical Evidence:**
- All core evidence: Complete and verified
- Performance: Load tested with real workloads
- Security: Penetration tested, compliance validated
- Code: Quality gates passed
- Tests: 80%+ coverage, E2E suite passing

**Example:**
```
Confidence: VERIFIED (94%)
Based on: All documentation complete and current (55%), load testing passed 3x peak capacity (10%), security audit passed (10%), 85% test coverage (4%), production pilot successful (15%)
Missing: Minor cost optimization opportunities identified but not critical
Recommendation: Approved for production release.
```

### Scenario 4: Critical Gaps Identified

**Context:** Architecture proposal with fatal flaws

**Expected Confidence:** CRITICAL (0-20%)

**Typical Evidence:**
- Core evidence: Mostly missing
- Unverified assumptions: Multiple critical
- Inconsistencies: Artifacts contradict
- Risks: Not assessed or major risks unmitigated

**Example:**
```
Confidence: CRITICAL (15%)
Based on: High-level requirements only (5%), single-page architecture sketch (3%)
Missing: Non-functional requirements, detailed design, technology decisions, risk assessment, security analysis, cost estimates
Critical Issues:
- Proposed database cannot handle stated scale (10x capacity gap)
- No authentication/authorization design
- Technology choices conflict with existing enterprise standards
Recommendation: STOP. Fundamental rework required. Re-propose after addressing critical gaps.
```

## Anti-Patterns to Avoid

### ❌ Vague Confidence Statements

**Bad:**
```
"I'm fairly confident this architecture will work."
"The design looks pretty solid."
"There's a good chance this meets requirements."
```

**Good:**
```
Confidence: HIGH (76%)
Based on: Complete requirements (20%), verified architecture diagrams (15%), successful load testing (10%)
Missing: Security threat model (5%), detailed cost breakdown (3%)
```

### ❌ Confidence Without Evidence

**Bad:**
```
Confidence: HIGH
I've seen similar architectures work before.
```

**Good:**
```
Confidence: HIGH (82%)
Based on: Complete requirements (20%), all C4 diagrams present (15%), 5/5 tech decisions documented with rationale (15%), risk assessment complete (15%), similar architecture verified in production (+15% modifier)
Missing: Cost breakdown (4%), formal security audit (pending)
```

### ❌ Ignoring Critical Gaps

**Bad:**
```
Confidence: HIGH (85%)
Most artifacts are present, a few minor things missing.
```

**Good:**
```
Base Score: 85%
Critical Gap: No risk assessment (-20%)
Final Confidence: LOW (65% → adjusted to LOW due to missing core evidence)
```

### ❌ Inconsistent Scoring Across Agents

**Bad:**
```
security-governance: "Looks okay" 
scalability-reliability: "Good enough"
cost-finops: "Should work"
```

**Good:**
```
security-governance: LOW (38%) — Threat model incomplete, no IAM design
scalability-reliability: HIGH (78%) — Load tested, capacity plan verified
cost-finops: MEDIUM (62%) — Budget estimated, optimization opportunities identified
```

## Verification Checklist

Before reporting confidence, verify:

- [ ] Evidence inventory complete (all applicable artifacts listed)
- [ ] Completion status accurate (not guessed)
- [ ] Base score calculated correctly (sum = 100%)
- [ ] Modifiers applied and justified
- [ ] Final confidence level matches score range
- [ ] Brief justification includes specific evidence
- [ ] Critical gaps explicitly stated
- [ ] Recommendation provided (proceed/revise/stop)

## Templates

### Quick Confidence Report

```markdown
**Confidence: [LEVEL] ([SCORE]%)**

**Evidence:** [List 2-3 key artifacts present]
**Gaps:** [List 1-2 critical missing items]
**Recommendation:** [Next step]
```

### Detailed Confidence Report

```markdown
## Architecture Confidence Assessment

### Confidence Score: [LEVEL] ([SCORE]%)

### Evidence Inventory

#### Core Evidence (70%)
- [Status] Requirements Documentation (20%) — [Notes]
- [Status] Architecture Diagrams (15%) — [Notes]
- [Status] Technology Decisions (15%) — [Notes]
- [Status] Risk Assessment (15%) — [Notes]

#### Supporting Evidence (30%)
- [Status] Performance Analysis (10%) — [Notes]
- [Status] Security Analysis (10%) — [Notes]
- [Status] Cost Analysis (5%) — [Notes]
- [Status] Code Analysis (5%) — [Notes]
- [Status] Test Coverage (5%) — [Notes]

### Calculation

Base Score: [XX]%
Modifiers:
- [Modifier name]: [±XX]%
Final Score: [XX]%

### Justification

**Based on:** [3-5 key evidence points with weights]

**Missing:** [Critical gaps that lower confidence]

**Quality factors:** [Modifiers applied and why]

### Recommendation

[Proceed/Revise/Stop] — [1-2 sentences explaining gate decision]

**Next steps:**
1. [Address critical gap 1]
2. [Address critical gap 2]
3. [Re-assess after improvements]
```

## Session Memory Integration

Store confidence assessments for tracking over time:

```markdown
# /memories/session/architecture-confidence-history.md

## Assessment History

### 2026-03-23 10:30 - Initial Proposal
- Confidence: MEDIUM (52%)
- Gaps: Component design, risk assessment
- Decision: Approved for detailed design

### 2026-03-25 15:45 - Detailed Design Review
- Confidence: HIGH (76%)
- Gaps: Cost detail, load testing (pending)
- Decision: Approved for implementation

### 2026-04-10 09:20 - Pre-Production Review
- Confidence: VERIFIED (94%)
- Gaps: Minor cost optimizations
- Decision: Approved for production release
```

## Best Practices

1. **Always compute, never estimate** — Use the scoring algorithm, don't guess confidence
2. **Evidence over intuition** — Base confidence on artifacts, not feelings
3. **Be explicit about gaps** — List what's missing, don't hide it
4. **Apply modifiers consistently** — Use the same quality factors across assessments
5. **Update as evidence changes** — Re-score when new artifacts become available
6. **Document assumptions** — If you assume something is complete, note it
7. **Separate domain confidence** — Let sub-agents score their domains independently
8. **Aggregate transparently** — Show how overall confidence was computed from domains
9. **Link to gate decisions** — Map confidence levels to governance gates
10. **Track over time** — Record confidence progression from proposal to production

## Related Skills

- **solution-architect** — Uses confidence scoring for architecture assessments
- **risk-assessment** — Contributes to confidence through risk analysis evidence
- **requirements-intelligence** — Provides requirements evidence for confidence scoring
- **security-governance** — Reports domain-specific security confidence
- **cost-finops** — Reports domain-specific cost confidence

## Conclusion

Architecture confidence scoring provides systematic, evidence-based assessment that replaces vague statements with quantifiable, justified confidence levels. By standardizing scoring across all SA agents and tracking evidence completeness, teams can make informed gate decisions and identify gaps early.

**Key Principle:** Confidence must be earned through evidence, not assumed through optimism.
