# Architecture Confidence Scoring Skill

Standardized methodology for computing and reporting architecture confidence levels based on evidence, verification depth, and artifact completeness. **Eliminates vague confidence statements** by requiring systematic, evidence-based scoring.

## Quick Start

**Invoke this skill when:**
- Assessing architecture quality or readiness
- Reporting confidence in solution proposals
- Making architecture gate decisions
- Aggregating sub-agent assessments
- Comparing architecture alternatives
- Communicating risk to stakeholders

**To use:** Type `/architecture-confidence-scoring` or mention "calculate architecture confidence" in chat.

## The Problem This Solves

**Before:**
```
❌ "I'm fairly confident this will work"
❌ "The design looks pretty solid"
❌ "There's a good chance this meets requirements"
❌ "Security should be fine"
```

**After:**
```
✅ Confidence: HIGH (76%)
   Based on: Complete requirements (20%), verified architecture diagrams (15%), technology decisions documented (15%)
   Missing: Security threat model (5%), detailed cost breakdown (3%)
   Recommendation: Approved for implementation. Complete security review before production.
```

## 5-Level Confidence Scale

| Level | Score | Meaning | Decision |
|-------|-------|---------|----------|
| **CRITICAL** | 0-20% | Fatal flaws, major gaps | ❌ STOP |
| **LOW** | 21-40% | Significant gaps, high risk | ⚠️ Revise |
| **MEDIUM** | 41-69% | Some gaps, proceed with caution | ⚠️ Conditional |
| **HIGH** | 70-89% | Minor gaps, ready to proceed | ✅ Approved |
| **VERIFIED** | 90-100% | Comprehensive, production-ready | ✅ Highly confident |

## Evidence Types (100% Total Weight)

### Core Evidence (70%)
- **Requirements Documentation (20%)** — Functional + non-functional requirements
- **Architecture Diagrams (15%)** — C4 model or equivalent visual design
- **Technology Decisions (15%)** — Documented rationale for tech choices
- **Risk Assessment (15%)** — Identified risks with mitigations

### Supporting Evidence (30%)
- **Performance Analysis (10%)** — Load testing, capacity planning
- **Security Analysis (10%)** — Threat model, security controls
- **Cost Analysis (5%)** — Budget estimates, TCO
- **Code Analysis (5%)** — Quality metrics, technical debt
- **Test Coverage (5%)** — Unit, integration, E2E tests

## How It Works

### 1. Evidence Inventory

List available artifacts with completion status:
- `[x]` Complete (100% of weight)
- `[~]` Partial (50% of weight)  
- `[ ]` Missing (0% of weight)

### 2. Calculate Base Score

```
Base Score = Σ (Artifact Weight × Completion %)

Example:
- Requirements: 20% × 100% = 20
- Diagrams: 15% × 100% = 15
- Decisions: 15% × 50% = 7.5
- Risk: 15% × 0% = 0
Performance: 10% × 100% = 10
- (others omitted for brevity)

Base Score = 52.5%
```

### 3. Apply Quality Modifiers

| Modifier | Adjustment | When |
|----------|-----------|------|
| Critical Gap | -20% | Core evidence missing |
| Unverified Assumptions | -10% | Key assumptions not validated |
| Inconsistent Artifacts | -10% | Documents contradict |
| Outdated Evidence | -5% | >6 months old |
| External Validation | +10% | Third-party review |
| Production Proven | +15% | Similar arch in production |

### 4. Map to Confidence Level

```
0-20%   → CRITICAL
21-40%  → LOW
41-69%  → MEDIUM
70-89%  → HIGH
90-100% → VERIFIED
```

## Quick Examples

### Example 1: Early Stage (MEDIUM)

```
Confidence: MEDIUM (52%)
Based on: Draft requirements (10%), high-level diagrams (12%)
Missing: Component design, risk assessment, cost estimates
Recommendation: Sufficient for concept approval. Develop detailed design.
```

### Example 2: Pre-Implementation (HIGH)

```
Confidence: HIGH (76%)
Based on: Complete requirements (20%), full C4 model (15%), tech decisions documented (15%)
Missing: Cost detail (3%), load testing pending (implementation phase)
Recommendation: Approved for implementation start.
```

### Example 3: Production Ready (VERIFIED)

```
Confidence: VERIFIED (94%)
Based on: All documentation complete (55%), load tested (10%), security audit passed (10%), 85% test coverage (4%)
Missing: Minor cost optimizations identified
Recommendation: Approved for production release.
```

### Example 4: Critical Gaps (CRITICAL)

```
Confidence: CRITICAL (15%)
Based on: High-level requirements only (5%)
Missing: Detailed design, tech decisions, risk assessment, security
Critical: Proposed database can't handle stated scale (10x capacity gap)
Recommendation: STOP. Fundamental rework required.
```

## Files in This Skill

```
architecture-confidence-scoring/
├── SKILL.md                           # Main skill documentation
├── README.md                          # This file
├── scripts/
│   └── calculate_confidence.py        # Automated calculator
└── references/
    ├── evidence-catalog.md            # Detailed evidence criteria
    └── sa-agent-integration.md        # SA agent integration examples
```

## Using the Calculator Script

### Run with Example Scenarios

```bash
# Early stage assessment
python3 scripts/calculate_confidence.py --example early --format brief

# Pre-implementation review
python3 scripts/calculate_confidence.py --example pre-impl --format detailed

# Production readiness check
python3 scripts/calculate_confidence.py --example production --format json

# Critical gaps scenario
python3 scripts/calculate_confidence.py --example critical
```

### Interactive Mode

```bash
python3 scripts/calculate_confidence.py

# Prompts for each evidence type:
Requirements (20%): [c/p/m/s]: c
Diagrams (15%): [c/p/m/s]: c
Decisions (15%): [c/p/m/s]: p
...

# Then prompts for modifiers:
Critical Gap (-20%): [y/n]: n
Unverified Assumptions (-10%): [y/n]: y
...

# Outputs confidence score and justification
```

## Integration with SA Agents

### For Sub-Agents (domain-specific)

```markdown
## [Agent] Assessment

[Invoke architecture-confidence-scoring for my domain]

**Domain Confidence: [LEVEL] ([SCORE]%)**

Evidence: [Key artifacts reviewed]
Gaps: [Missing critical items]
Recommendation: [Domain-specific guidance]
```

### For Orchestrator (overall)

```markdown
## Overall Architecture Confidence

[Collect sub-agent confidence scores]
[Invoke architecture-confidence-scoring with aggregated evidence]

**Overall Confidence: [LEVEL] ([SCORE]%)**

Sub-agent scores:
- requirements-intelligence: HIGH (78%)
- system-design-domain-modeler: MEDIUM (65%)
- security-governance: LOW (35%) ⚠️
- scalability-reliability: HIGH (82%)
- cost-finops: MEDIUM (60%)

Based on: [Top evidence contributors]
Missing: [Critical gaps]
Recommendation: [Gate decision with justification]
```

## Decision Gates

Map confidence to architecture governance:

| Gate | Required Confidence | Evidence |
|------|-------------------|----------|
| **Concept Approval** | MEDIUM (41%+) | Requirements, high-level design |
| **Design Approval** | HIGH (70%+) | Complete C4, decisions, risk |
| **Implementation** | HIGH (70%+) | Above + security reviewed |
| **Production** | VERIFIED (90%+) | All evidence + testing complete |

## Best Practices

1. ✅ **Always compute, never estimate** — Use the algorithm, don't guess
2. ✅ **Evidence over intuition** — Base on artifacts, not feelings
3. ✅ **Be explicit about gaps** — List what's missing clearly
4. ✅ **Apply modifiers consistently** — Use same quality factors always
5. ✅ **Update as evidence changes** — Re-score when new artifacts available
6. ✅ **Document assumptions** — State what you assumed complete
7. ✅ **Track over time** — Record confidence progression
8. ✅ **Fail fast on critical gaps** — Core evidence missing = cap confidence
9. ✅ **Separate domain confidence** — Let sub-agents score independently
10. ✅ **Link to governance** — Map confidence to gate decisions

## Anti-Patterns to Avoid

❌ **Vague statements** — "Fairly confident" → Use scored confidence  
❌ **No evidence cited** — "Looks good" → Cite specific artifacts  
❌ **Ignoring gaps** — "Minor issues" → Explicitly list missing evidence  
❌ **Inconsistent scoring** — Different agents using different scales  
❌ **Optimistic bias** — Assuming things are complete without verification  

## Related Resources

- [SKILL.md](./SKILL.md) — Complete methodology and templates
- [Evidence Catalog](./references/evidence-catalog.md) — Detailed artifact criteria and verification methods
- [SA Agent Integration](./references/sa-agent-integration.md) — 6 integration patterns and examples
- [Calculator Script](./scripts/calculate_confidence.py) — Automated confidence computation

## Example Prompts to Try

1. **Basic scoring:**
   > "Calculate the architecture confidence for this project. We have complete requirements, partial diagrams, and no risk assessment."

2. **Sub-agent integration:**
   > "As the security-governance agent, assess my domain confidence using the architecture-confidence-scoring skill."

3. **Gate decision:**
   > "Use architecture confidence scoring to determine if this design is ready for implementation."

4. **Comparison:**
   > "Compare architecture confidence between the microservices and monolith options."

5. **Tracking:**
   > "Update the confidence score now that we've completed load testing and security review."

## Session Memory Tracking

Store confidence history for trend analysis:

```markdown
# /memories/session/architecture-confidence-history.md

## Assessment History

### 2026-03-23 Initial: MEDIUM (52%)
- Missing: Risk assessment, cost detail
- Decision: Approved for design

### 2026-03-25 Design: HIGH (76%)  
- Completed: Risk mitigation plan
- Decision: Approved for implementation

### 2026-04-10 Pre-Prod: VERIFIED (94%)
- Completed: All testing, external audit
- Decision: Approved for production
```

## Common Questions

**Q: What if I don't have all evidence types?**  
A: Score what you have. Missing evidence = 0% for that category. N/A categories (like code analysis during design phase) don't penalize you.

**Q: Can I customize the weights?**  
A: Yes for domain-specific assessments. Security agent might weight security evidence higher. Document any customization.

**Q: How often should I re-score?**  
A: At each major milestone (concept → design → implementation → production) or when significant new evidence becomes available.

**Q: What if confidence is borderline (e.g., 69% = MEDIUM vs 70% = HIGH)?**  
A: Use your judgment on quality factors. A well-documented 69% might justify HIGH. A shaky 71% might warrant MEDIUM. Document rationale.

**Q: Should partial evidence always be 50%?**  
A: 50% is default, but use judgment. "80% complete" could be 80%. "Just started" might be 25%. Be consistent.

## Support

For questions or issues:
1. Review [SKILL.md](./SKILL.md) for complete methodology
2. Check [evidence-catalog.md](./references/evidence-catalog.md) for artifact criteria
3. See [sa-agent-integration.md](./references/sa-agent-integration.md) for examples
4. Run calculator with `--example` flag to see scenarios
5. File issue in awesome-copilot-opensource repository

---

**Version:** 1.0.0  
**Created:** 2026-03-23  
**Status:** ✅ Ready for use

**Key Principle:** *Confidence must be earned through evidence, not assumed through optimism.*
