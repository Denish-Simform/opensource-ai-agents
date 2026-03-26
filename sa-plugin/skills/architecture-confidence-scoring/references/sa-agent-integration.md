# Integration Examples for SA Agents

Practical examples of integrating architecture confidence scoring into solution architect agent workflows.

## Example 1: sa-orchestrator Integration

**Scenario:** Orchestrator aggregates sub-agent assessments and computes overall confidence.

### Workflow

```markdown
## SA Orchestrator Workflow

### Step 1: Invoke Sub-Agents

Call specialized sub-agents for domain analysis:
- requirements-intelligence → Validates requirements
- system-design-domain-modeler → Evaluates architecture design
- security-governance → Assesses security posture
- scalability-reliability → Evaluates scalability/reliability
- cost-finops → Analyzes cost implications

### Step 2: Collect Domain-Specific Confidence

Each sub-agent reports confidence using architecture-confidence-scoring skill:

**requirements-intelligence output:**
```

```markdown
**Domain Confidence: HIGH (85%)**

Evidence: Requirements documentation complete (20%), stakeholder sign-off obtained (15%)
Gaps: Edge case scenarios not fully documented (5%)
```

```markdown
**system-design-domain-modeler output:**
```

```markdown
**Domain Confidence: MEDIUM (68%)**

Evidence: C4 diagrams complete (15%), technology decisions documented (12%)
Gaps: Deployment architecture partial (3%), component-level detail for 2 services missing (2%)
```

```markdown
**security-governance output:**
```

```markdown
**Domain Confidence: LOW (42%)**

Evidence: Threat model draft (5%), authentication design complete (8%)
Gaps: Authorization model incomplete (2%), security testing not performed (10%), compliance not validated (5%)
```

```markdown
### Step 3: Aggregate Using architecture-confidence-scoring

Orchestrator uses skill to compute overall confidence:

[Invoke architecture-confidence-scoring skill]

Evidence inventory from sub-agents:
- Requirements: COMPLETE (from requirements-intelligence)
- Diagrams: PARTIAL (from system-design-domain-modeler)
- Decisions: COMPLETE (from system-design-domain-modeler)
- Risk: PARTIAL (from security-governance, scalability-reliability)
- Performance: PARTIAL (from scalability-reliability)
- Security: PARTIAL (from security-governance)
- Cost: COMPLETE (from cost-finops)

Modifiers:
- Unverified assumptions: Security performance claims not tested

[Calculate confidence]

Base Score: 62%
Modifiers: -10% (unverified assumptions)
Final Score: 52% → MEDIUM

### Step 4: Generate Final Report

**Overall Architecture Confidence: MEDIUM (52%)**

Based on: Complete requirements (20%), technology decisions documented (15%), cost analysis complete (5%)
Missing: Detailed component design (3%), comprehensive security testing (10%), risk mitigation plans (8%)
Recommendation: Proceed with caution. Address security gaps before production deployment. Design detail sufficient for MVP implementation start.

**Sub-Agent Confidence Summary:**
- Requirements Intelligence: HIGH (85%)
- System Design: MEDIUM (68%)
- Security Governance: LOW (42%) ⚠️
- Scalability/Reliability: HIGH (76%)
- Cost/FinOps: MEDIUM (65%)

**Next Steps:**
1. Complete security threat model and testing (critical)
2. Finalize component-level design for remaining services
3. Document risk mitigation strategies
4. Re-assess after addressing gaps
```

---

## Example 2: security-governance Agent Integration

**Scenario:** Security agent uses confidence scoring to report security posture.

### Agent Prompt Integration

```markdown
## security-governance Agent Instructions

When assessing security:

1. Inventory security evidence using architecture-confidence-scoring categories:
   - Threat model
   - Security controls
   - Authentication/authorization design
   - Data protection strategy
   - Security testing results
   - Compliance validation

2. Assess completion status:
   - Complete: Artifact present, verified, meets requirements
   - Partial: Artifact present but incomplete or unverified
   - Missing: Artifact not available

3. Apply security-specific modifiers:
   - Critical Gap: No authentication design (-20%)
   - Critical Gap: No data encryption strategy (-20%)
   - Unverified Assumptions: Security claims not tested (-10%)
   - External Validation: Third-party security audit (+10%)

4. Report using standard format:

**Security Confidence: [LEVEL] ([SCORE]%)**

Evidence: [Security artifacts present]
Gaps: [Critical security gaps]
Recommendation: [Proceed/Revise/Stop]
```

### Example Output

```markdown
## Security Governance Assessment

**Security Confidence: LOW (38%)**

### Evidence Inventory

**Security Analysis (10%):**
- Threat Model: PARTIAL (5%) — Application threats modeled, infrastructure threats missing
- Security Controls: MISSING (0%) — No control mapping performed

**Core Evidence (Security-Relevant):**
- Architecture Diagrams: COMPLETE (15%) — Security boundaries marked
- Technology Decisions: PARTIAL (8%) — Auth mechanism chosen, secrets management undefined
- Risk Assessment: MISSING (0%) — Security risks not assessed

### Calculation

Base Score: 28%
Modifiers:
- Critical Gap (no secrets management): -20%
- Unverified Assumptions (API rate limits): -10%

Final Score: -2% → 0% (clamped) → CRITICAL

**Security Confidence: CRITICAL (0%)**

Evidence: Security boundaries in diagrams (15%), authentication mechanism selected (8%)
Gaps: No secrets management strategy (CRITICAL), infrastructure security not designed, no security testing, security risks not assessed
Recommendation: STOP. Security design is insufficient. Complete threat model, design security controls, define secrets management before proceeding.

**Critical Security Issues:**
1. No strategy for managing secrets (API keys, certificates, passwords)
2. Infrastructure security not addressed (network segmentation, firewall rules)
3. Authorization model undefined (who can access what?)
4. No security testing planned or performed
```

---

## Example 3: requirements-intelligence Agent Integration

**Scenario:** Requirements agent validates requirement completeness and quality.

### Integration Pattern

```markdown
## requirements-intelligence Agent Workflow

### Step 1: Analyze Requirements Artifacts

Collect and assess:
- Requirements documentation
- User stories or use cases
- Non-functional requirements
- Constraints and assumptions
- Stakeholder approvals

### Step 2: Score Using architecture-confidence-scoring

Evidence assessment:
- Requirements Documentation (20%):
  - Functional requirements: [COMPLETE/PARTIAL/MISSING]
  - Non-functional requirements: [COMPLETE/PARTIAL/MISSING]
  - Constraints: [COMPLETE/PARTIAL/MISSING]
  - Assumptions: [COMPLETE/PARTIAL/MISSING]
  - Stakeholder sign-off: [YES/NO]

Quality check:
- Requirements are specific (not vague)?
- Requirements are measurable?
- Requirements are testable?
- Requirements trace to business value?

Modifiers:
- Unverified Assumptions: Key assumptions not validated (-10%)
- Inconsistent Artifacts: Requirements contradict each other (-10%)
- External Validation: Business stakeholder approval (+10%)

### Step 3: Report Confidence

**Requirements Confidence: [LEVEL] ([SCORE]%)**

Evidence: [Requirements artifacts present]
Gaps: [Missing or incomplete requirements]
Quality Issues: [Vague, unmeasurable, or contradictory requirements]
Recommendation: [Assessment of requirements readiness]
```

### Example Output

```markdown
## Requirements Intelligence Assessment

**Requirements Confidence: HIGH (78%)**

### Evidence Analysis

**Functional Requirements:**
- 15 user stories documented ✓
- Acceptance criteria defined for all stories ✓
- Edge cases covered for 12/15 stories (80%)

**Non-Functional Requirements:**
- Performance: Specific targets defined (95th percentile < 200ms) ✓
- Scalability: Target load specified (10K concurrent users) ✓
- Availability: SLA stated (99.9% uptime) ✓
- Security: High-level requirements present, details TBD

**Constraints:**
- Budget: $50K infrastructure cost limit ✓
- Timeline: MVP in 3 months ✓
- Technology: Must integrate with existing auth system ✓

**Assumptions:**
- Third-party API will provide data in <100ms (NOT VERIFIED)
- Team can learn new framework (PARTIALLY VERIFIED)

**Stakeholder Approval:**
- Product Owner: Approved ✓
- Technical Lead: Approved ✓
- Security Team: Pending review

### Calculation

Base Score: 20% (requirements documentation weight)
- Functional requirements: 100% complete
- NFRs: 85% complete (security details pending)
- Constraints: 100% documented
- Assumptions: 70% verified
- Stakeholder approval: 80% complete (security pending)

Weighted: 20% × 87% = 17.4%

Modifiers:
- Unverified assumption (API latency): -10%
- External validation (stakeholder approval): +10%

Final Contribution to Overall Confidence: 17.4%
Domain-Specific Confidence: HIGH (87%)

**Requirements Confidence: HIGH (78%)**

Evidence: 15 user stories with acceptance criteria (15%), specific NFRs for performance/scalability (3%), documented constraints (2%)
Gaps: Security requirement details (1%), edge cases for 3 stories (0.5%), third-party API latency not verified (assumption)
Quality Issues: One vague security requirement ("must be secure") needs specificity
Recommendation: Requirements sufficient for detailed design. Obtain security team approval and verify API latency assumption before implementation.
```

---

## Example 4: Confidence Tracking Over Time

**Scenario:** Track confidence progression from concept to production.

### Session Memory Integration

Store confidence history in session memory:

```markdown
# /memories/session/architecture-confidence-history.md

## Confidence Progression: Payment Service Modernization

### 2026-03-10: Initial Proposal
- **Overall Confidence:** MEDIUM (45%)
- **Sub-Agent Scores:**
  - Requirements: MEDIUM (60%) — Requirements drafted, NFRs partial
  - Design: LOW (35%) — High-level sketch only
  - Security: CRITICAL (15%) — Not addressed
  - Scalability: MEDIUM (50%) — Estimates provided
  - Cost: LOW (30%) — Rough order of magnitude
- **Decision:** Approved for detailed design phase
- **Action Items:**
  - Complete NFR specifications
  - Develop full C4 model
  - Initiate security threat modeling

### 2026-03-20: Detailed Design Review
- **Overall Confidence:** HIGH (72%)
- **Sub-Agent Scores:**
  - Requirements: HIGH (85%) — NFRs complete, stakeholder approved
  - Design: HIGH (78%) — Full C4 model, tech decisions documented
  - Security: MEDIUM (55%) — Threat model complete, controls designed
  - Scalability: HIGH (80%) — Capacity plan validated
  - Cost: MEDIUM (65%) — Detailed breakdown provided
- **Decision:** Approved for implementation
- **Action Items:**
  - Implement security controls during development
  - Conduct load testing during QA
  - Track actual costs vs estimates

### 2026-04-15: Pre-Production Review
- **Overall Confidence:** VERIFIED (92%)
- **Sub-Agent Scores:**
  - Requirements: VERIFIED (95%) — All requirements met, tested
  - Design: VERIFIED (90%) — Architecture matches implementation
  - Security: HIGH (85%) — Security testing passed, audit scheduled
  - Scalability: VERIFIED (95%) — Load tested at 3x capacity
  - Cost: HIGH (82%) — Costs tracking on budget
- **Modifiers Applied:**
  - Production Proven: Similar architecture in production (+15%)
  - External Validation: Cloud vendor architecture review (+10%)
- **Decision:** Approved for production deployment
- **Next:** Post-deployment review in 30 days

### Confidence Trend

```
100% |                                    ⚫ VERIFIED
 90% |                               ⚫
 80% |
 70% |                      ⚫ HIGH
 60% |
 50% |
 40% |        ⚫ MEDIUM
 30% |
 20% |
 10% |
  0% +----+----------+---------+---------+
     Initial     Design    Implementation Production
```

**Key Learnings:**
- Confidence increased 47 points (45% → 92%) over 5 weeks
- Security was initial blocker (15% → 85% improvement)
- Load testing provided significant validation (+25% confidence boost)
- External validation from vendor review added credibility
```

---

## Example 5: Gate Decision Automation

**Scenario:** Use confidence scores to automate architecture governance gates.

### Gate Configuration

```yaml
# architecture-gates.yaml

gates:
  concept_approval:
    required_confidence: 41  # MEDIUM minimum
    required_evidence:
      - requirements: partial_minimum
      - diagrams: high_level_minimum
    decision_logic: |
      IF overall_confidence >= 41 AND requirements >= 50 THEN
        APPROVE for detailed design
      ELSE
        REJECT - insufficient requirements or design

  design_approval:
    required_confidence: 70  # HIGH minimum
    required_evidence:
      - requirements: complete
      - diagrams: complete
      - decisions: complete
      - risk: complete
    critical_gaps_blocking:
      - requirements: false  # Cannot be missing
      - risk: false          # Cannot be missing
    decision_logic: |
      IF overall_confidence >= 70 AND no_critical_gaps THEN
        APPROVE for implementation
      ELSE IF overall_confidence >= 60 AND security_confidence >= 70 THEN
        CONDITIONAL APPROVE with security review
      ELSE
        REJECT - complete detailed design

  implementation_approval:
    required_confidence: 70  # HIGH minimum
    required_evidence:
      - requirements: complete
      - diagrams: complete
      - decisions: complete
      - risk: complete
      - security: partial_minimum
    decision_logic: |
      Same as design_approval
      Security must be designed (partial OK, will be completed during dev)

  production_release:
    required_confidence: 90  # VERIFIED minimum
    required_evidence:
      - requirements: complete
      - diagrams: complete
      - decisions: complete
      - risk: complete
      - performance: complete
      - security: complete
      - tests: complete
    required_validation:
      - load_testing: true
      - security_testing: true
    decision_logic: |
      IF overall_confidence >= 90 AND 
         all_core_evidence_complete AND
         performance_tested AND
         security_tested THEN
        APPROVE for production
      ELSE
        REJECT - not production ready
```

### Automated Gate Check

```markdown
## Architecture Gate Check: Design Approval

[Invoke architecture-confidence-scoring]

**Overall Confidence: HIGH (76%)**

### Gate Requirements Check

✅ Required Confidence: 70% minimum → **PASS** (76% achieved)

✅ Required Evidence:
- [x] Requirements: COMPLETE
- [x] Diagrams: COMPLETE
- [x] Decisions: COMPLETE
- [x] Risk: COMPLETE

✅ Critical Gaps Check: No core evidence missing → **PASS**

### Gate Decision: **APPROVED FOR IMPLEMENTATION**

**Justification:** Architecture meets design approval criteria. All core evidence complete with confidence score of 76% (exceeds 70% threshold). No critical gaps identified.

**Conditions:**
- Complete security testing during development (currently 55%, needs 85%+ for production)
- Re-assess after load testing results available
- Track actual costs vs estimates

**Next Gate:** Production Release (requires 90%+ confidence)
```

---

## Example 6: Multi-Architecture Comparison

**Scenario:** Compare confidence scores across multiple architecture options.

### Comparison Framework

```markdown
## Architecture Options Comparison

Using architecture-confidence-scoring to evaluate three proposed architectures:

### Option A: Microservices with Event-Driven Architecture

[Invoke architecture-confidence-scoring for Option A]

**Confidence: MEDIUM (58%)**

Evidence: Complete requirements (20%), partial diagrams (8%), partial decisions (8%)
Gaps: Event schema design incomplete (7%), operational complexity not assessed (15%)
Risks: Team inexperienced with event-driven patterns (-10% modifier)

---

### Option B: Modular Monolith with API Gateway

[Invoke architecture-confidence-scoring for Option B]

**Confidence: HIGH (74%)**

Evidence: Complete requirements (20%), complete diagrams (15%), complete decisions (15%)
Gaps: Scaling plan partial (5%), monitoring strategy TBD (5%)
Strengths: Production-proven pattern (+15% modifier), team experienced with approach

---

### Option C: Serverless Function-Based

[Invoke architecture-confidence-scoring for Option C]

**Confidence: LOW (39%)**

Evidence: Complete requirements (20%), partial diagrams (8%)
Gaps: Cold start latency not assessed (10%), cost model uncertain (5%), vendor lock-in risk not evaluated (15%)
Risks: Unverified performance assumptions (-10% modifier)

---

### Recommendation Matrix

| Option | Confidence | Strengths | Weaknesses | Risk Level |
|--------|-----------|-----------|------------|------------|
| **A: Microservices** | MEDIUM (58%) | Scalable, modern | Complex, team learning curve | MEDIUM-HIGH |
| **B: Modular Monolith** | HIGH (74%) | Proven, team expertise | Scaling limits | LOW-MEDIUM |
| **C: Serverless** | LOW (39%) | Low ops overhead | Performance unknowns, lock-in | HIGH |

**Selected Option: B (Modular Monolith)**

Rationale: Highest confidence score (74%), leverages team expertise, production-proven pattern. Option A has potential but requires addressing event-driven complexity. Option C too many unknowns for current timeline.

Plan: Implement Option B, design for future migration to Option A when team gains experience and business justifies complexity.
```

---

## Best Practices for Integration

### 1. Standard Reporting Format

All sub-agents use consistent format:

```markdown
**[Domain] Confidence: [LEVEL] ([SCORE]%)**

Evidence: [Key artifacts]
Gaps: [Missing items]
Recommendation: [Action]
```

### 2. Domain-Specific Weights

Agents can customize evidence weights for their domain:

```python
# security-governance: Emphasize security evidence
SECURITY_WEIGHTS = {
    "security": 30,  # Increase from 10%
    "risk": 20,      # Increase from 15%
    "requirements": 15,  # Decrease from 20%
    # ... adjust others
}
```

### 3. Progressive Assessment

Track confidence progression:
- Concept: MEDIUM target (41%+)
- Design: HIGH target (70%+)
- Implementation: HIGH maintained (70%+)
- Production: VERIFIED target (90%+)

### 4. Fail Fast on Critical Gaps

If critical evidence missing (requirements, risk, security), cap confidence at MEDIUM even if other evidence is strong.

### 5. Document Assumptions

When scoring, explicitly state assumptions made:

```markdown
**Assumptions in Confidence Scoring:**
- Database performance estimates based on vendor benchmarks (not tested)
- Security controls assumed effective (not validated)
- Cost estimates based on current pricing (subject to change)
```

---

## Conclusion

Integrating architecture-confidence-scoring into SA agent workflows provides:
- **Consistency:** All agents use same methodology
- **Transparency:** Confidence scores are evidence-based and auditable
- **Governance:** Automated gate decisions based on objective criteria
- **Communication:** Stakeholders understand confidence levels clearly
- **Risk Management:** Gaps identified early and systematically

**Key Integration Points:**
1. Sub-agents report domain confidence using skill
2. Orchestrator aggregates overall confidence
3. Gate decisions reference confidence thresholds
4. Confidence tracked over architectural lifecycle
5. Comparisons between options use same scoring
