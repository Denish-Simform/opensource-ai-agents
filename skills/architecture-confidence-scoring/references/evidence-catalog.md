# Evidence Catalog and Verification Guide

Comprehensive reference for architecture evidence types, verification methods, and quality criteria.

## Evidence Classification

### Tier 1: Critical Evidence (Cannot proceed without)

These artifacts are mandatory for any architecture assessment beyond initial concept.

#### 1. Requirements Documentation

**Weight:** 20% (highest single contributor)

**Definition:** Documented functional and non-functional requirements with clear acceptance criteria.

**What qualifies as complete:**
- ✅ Functional requirements listed with user stories or use cases
- ✅ Non-functional requirements (performance, security, scalability, availability) quantified
- ✅ Constraints documented (budget, timeline, technology, regulatory)
- ✅ Assumptions explicitly stated
- ✅ Stakeholder sign-off or approval
- ✅ Traceability to business objectives

**Verification checklist:**
```markdown
- [ ] All major use cases documented?
- [ ] Performance targets specified (e.g., "95th percentile < 200ms")?
- [ ] Security requirements defined (authentication, authorization, data protection)?
- [ ] Scalability targets quantified (e.g., "support 10K concurrent users")?
- [ ] Availability SLA stated (e.g., "99.9% uptime")?
- [ ] Budget constraints documented?
- [ ] Compliance requirements identified?
- [ ] Stakeholder approval obtained?
```

**Partial completion (50%):**
- Functional requirements complete, NFRs partially defined
- Requirements documented but not stakeholder-approved
- Major use cases covered, edge cases TBD

**Common gaps:**
- Vague NFRs ("should be fast", "must be secure")
- Missing constraints
- Unstated assumptions
- No traceability to business value

---

#### 2. Architecture Diagrams

**Weight:** 15%

**Definition:** Visual representations of system structure using standard notation (C4, UML, ArchiMate).

**What qualifies as complete:**

**C4 Model (Recommended):**
- ✅ Level 1: System Context diagram (system boundary, external dependencies)
- ✅ Level 2: Container diagram (applications, databases, services)
- ✅ Level 3: Component diagram (internal structure of key containers)
- ✅ Level 4: Code diagram (classes/modules for critical components)

**OR equivalent using other notation:**
- ✅ Logical architecture (components and relationships)
- ✅ Physical architecture (deployment topology)
- ✅ Data flow diagrams (how information moves)
- ✅ Sequence diagrams (key interaction flows)

**Verification checklist:**
```markdown
- [ ] All major components identified?
- [ ] External dependencies shown (APIs, databases, third-party services)?
- [ ] Communication patterns indicated (sync/async, protocols)?
- [ ] Data stores identified with types (relational, NoSQL, cache)?
- [ ] Security boundaries marked (trust zones, DMZ)?
- [ ] Diagram notation consistent and explained?
- [ ] Diagrams match each other (no contradictions)?
- [ ] Deployment architecture shows physical topology?
```

**Partial completion (50%):**
- High-level diagrams only (context + container)
- Component-level detail for some but not all containers
- Diagrams present but using inconsistent notation

**Common gaps:**
- Box-and-arrow diagrams without clear semantics
- Missing deployment view
- No data flow representation
- Diagrams contradict written documentation

---

#### 3. Technology Decisions

**Weight:** 15%

**Definition:** Documented rationale for key technology choices with alternatives considered.

**What qualifies as complete:**

For each major technology decision:
- ✅ Decision stated (e.g., "Use PostgreSQL for primary database")
- ✅ Context explained (requirements driving the decision)
- ✅ Alternatives considered (e.g., "Evaluated MongoDB, DynamoDB, PostgreSQL")
- ✅ Evaluation criteria defined (performance, cost, team skills, ecosystem)
- ✅ Trade-offs analyzed (strengths/weaknesses of each option)
- ✅ Rationale for final choice
- ✅ Consequences documented (implications of the decision)

**Key technology areas:**
1. Programming languages
2. Frameworks (web, mobile, backend)
3. Databases (primary, cache, search)
4. Cloud platform (AWS, Azure, GCP, hybrid)
5. Messaging/integration (REST, GraphQL, message queues)
6. Authentication/authorization
7. Monitoring/observability

**Verification checklist:**
```markdown
- [ ] All major technology choices documented?
- [ ] At least 2 alternatives considered for each decision?
- [ ] Evaluation criteria stated explicitly?
- [ ] Trade-offs analyzed (not just benefits)?
- [ ] Team capability/learning curve considered?
- [ ] Total cost of ownership evaluated?
- [ ] Vendor lock-in risk assessed?
- [ ] Migration path from current state (if applicable)?
```

**Partial completion (50%):**
- Technologies selected but limited rationale
- Some alternatives mentioned but not thoroughly evaluated
- Missing documentation for 2-3 minor technology choices

**Common gaps:**
- "We chose X because we know it" (no alternatives considered)
- Technology decisions not documented at all
- Evaluation based on hype/trends, not requirements
- No consideration of team skills or learning curve

---

#### 4. Risk Assessment

**Weight:** 15%

**Definition:** Identified risks with likelihood, impact, and mitigation strategies.

**What qualifies as complete:**

**Risk register including:**
- ✅ Technical risks (scalability, performance, integration, technology maturity)
- ✅ Security risks (data breach, unauthorized access, compliance)
- ✅ Operational risks (deployment complexity, monitoring gaps, failure modes)
- ✅ Business risks (timeline, budget, dependency on third parties)
- ✅ Team risks (skill gaps, key person dependencies)

**For each risk:**
- ✅ Description (what could go wrong)
- ✅ Likelihood (Low/Medium/High or percentage)
- ✅ Impact (Low/Medium/High or financial/operational)
- ✅ Risk score (Likelihood × Impact)
- ✅ Mitigation strategy (how to prevent or reduce)
- ✅ Contingency plan (what to do if risk materializes)
- ✅ Owner (who is responsible for monitoring)

**Verification checklist:**
```markdown
- [ ] All major risk categories covered (technical, security, operational, business)?
- [ ] Each risk has likelihood and impact assessment?
- [ ] High-priority risks (likelihood × impact > threshold) have mitigation plans?
- [ ] Mitigation strategies are actionable?
- [ ] Residual risk after mitigation is acceptable?
- [ ] Risk owners assigned?
- [ ] Risks linked to architecture decisions (which decisions carry which risks)?
```

**Partial completion (50%):**
- Risks identified but mitigation strategies incomplete
- Major risk categories covered, some gaps in specific risks
- Likelihood/impact estimated but not rigorously

**Common gaps:**
- "No significant risks identified" (unrealistic)
- Risks listed but no mitigation strategies
- Only technical risks, missing business/operational
- No linkage between architecture decisions and risks

---

### Tier 2: Verification Evidence (Increases confidence through validation)

These artifacts validate that the architecture works as intended.

#### 5. Performance Analysis

**Weight:** 10%

**Definition:** Evidence that system meets performance requirements under expected load.

**What qualifies as complete:**
- ✅ Load testing results (throughput, latency, concurrency)
- ✅ Capacity planning (infrastructure sizing for target load)
- ✅ Bottleneck analysis (identified and addressed)
- ✅ Baseline metrics (current state if migrating)
- ✅ Performance budget (targets per component)

**Verification checklist:**
```markdown
- [ ] Load testing performed with realistic scenarios?
- [ ] Tested at 2-3x expected peak load?
- [ ] Latency measured at different percentiles (p50, p95, p99)?
- [ ] Database query performance analyzed?
- [ ] API response times meet requirements?
- [ ] Resource utilization measured (CPU, memory, network)?
- [ ] Bottlenecks identified and mitigated?
- [ ] Performance regression tests in place?
```

**Partial completion (50%):**
- Capacity planning done but no load testing yet
- Back-of-the-envelope calculations, not measured
- Performance tested but not at scale

**Common gaps:**
- "Should be fast enough" (no testing)
- Load testing with unrealistic data volumes
- No percentile-based latency measurements
- Bottlenecks assumed but not verified

---

#### 6. Security Analysis

**Weight:** 10%

**Definition:** Evidence that security requirements are met and threats are mitigated.

**What qualifies as complete:**
- ✅ Threat model (STRIDE, attack trees, or similar)
- ✅ Security controls mapped to threats
- ✅ Authentication/authorization design
- ✅ Data protection strategy (encryption at rest, in transit)
- ✅ Input validation and output encoding
- ✅ Security testing results (SAST, DAST, penetration testing)
- ✅ Compliance validation (GDPR, HIPAA, PCI-DSS if applicable)

**Verification checklist:**
```markdown
- [ ] Threat model covers all trust boundaries?
- [ ] Authentication mechanism defined (OAuth, SAML, API keys)?
- [ ] Authorization model specified (RBAC, ABAC, custom)?
- [ ] Secrets management strategy documented (key vault, rotation)?
- [ ] Data classification performed (PII, sensitive, public)?
- [ ] Encryption specified for data at rest and in transit?
- [ ] Input validation rules defined?
- [ ] Security controls tested?
- [ ] Compliance requirements validated?
```

**Partial completion (50%):**
- Threat model drafted but not comprehensive
- Security controls designed but not tested
- Authentication defined, authorization partial

**Common gaps:**
- "We'll use HTTPS" (insufficient)
- No threat modeling
- Security as afterthought, not designed in
- Compliance requirements not validated

---

#### 7. Cost Analysis

**Weight:** 5%

**Definition:** Estimated costs with breakdown and optimization opportunities.

**What qualifies as complete:**
- ✅ Infrastructure costs itemized (compute, storage, network, data transfer)
- ✅ Service costs estimated (managed services, SaaS, licenses)
- ✅ Operational costs included (monitoring, support, maintenance)
- ✅ Development costs estimated (if relevant)
- ✅ Total Cost of Ownership (TCO) calculated
- ✅ Cost optimization opportunities identified
- ✅ Cost monitoring strategy defined

**Verification checklist:**
```markdown
- [ ] All infrastructure components priced?
- [ ] Data transfer costs estimated (often forgotten)?
- [ ] Managed service pricing validated (not outdated)?
- [ ] Reserved instances / savings plans considered?
- [ ] Cost scaling analyzed (cost at 1x, 10x, 100x scale)?
- [ ] Budget alerts defined?
- [ ] Cost allocation tags/strategy specified?
```

**Partial completion (50%):**
- High-level cost estimate, not itemized
- Infrastructure costs estimated, operational costs missing
- Cost optimization opportunities not explored

**Common gaps:**
- "Should fit in budget" (no estimates)
- Data transfer and egress costs forgotten
- No analysis of cost scaling
- Missing operational/maintenance costs

---

#### 8. Code Analysis

**Weight:** 5%

**Definition:** Evidence of code quality, maintainability, and technical health.

**What qualifies as complete:**
- ✅ Static analysis results (linting, complexity, code smells)
- ✅ Technical debt assessment (SonarQube, CodeClimate)
- ✅ Code review metrics (coverage, turnaround time)
- ✅ Dependency analysis (vulnerabilities, licenses, outdated packages)
- ✅ Architecture conformance (code matches design)

**Verification checklist:**
```markdown
- [ ] Static analysis passing quality gates?
- [ ] Cyclomatic complexity within acceptable range?
- [ ] Code duplication below threshold (e.g., <5%)?
- [ ] Critical security vulnerabilities in dependencies addressed?
- [ ] Code follows team standards (style guide, naming conventions)?
- [ ] Architectural boundaries enforced (no layer violations)?
```

**Partial completion (50%):**
- Static analysis setup but quality gates not enforced
- Some code reviewed, not comprehensive
- Technical debt identified but not quantified

**Common gaps:**
- No automated code analysis
- Code review ad-hoc, not systematic
- Dependencies not scanned for vulnerabilities
- Architecture drift (code diverges from design)

---

#### 9. Test Coverage

**Weight:** 5%

**Definition:** Evidence that system behavior is verified through testing.

**What qualifies as complete:**
- ✅ Unit test coverage >70% (critical paths 100%)
- ✅ Integration tests for key workflows
- ✅ End-to-end tests for critical business scenarios
- ✅ Performance/load tests
- ✅ Security tests (SAST, DAST)
- ✅ Test execution passing in CI/CD
- ✅ Test maintenance strategy (keeping tests current)

**Verification checklist:**
```markdown
- [ ] Unit tests cover business logic?
- [ ] Integration tests verify component interactions?
- [ ] E2E tests cover critical user journeys?
- [ ] Tests run automatically in CI/CD?
- [ ] Test failures block deployment?
- [ ] Tests are maintainable (not brittle)?
- [ ] Test data strategy defined (fixtures, factories)?
```

**Partial completion (50%):**
- Unit tests exist, coverage <70%
- Integration tests for some but not all workflows
- E2E tests planned but not implemented

**Common gaps:**
- "We'll test manually" (no automated tests)
- High unit test coverage but no integration/E2E tests
- Tests that pass but don't verify requirements
- Brittle tests that break frequently

---

## Verification Methods by Artifact Type

### Documentation Review

**Applies to:** Requirements, Decisions, Risk Assessment

**Method:**
1. Read the artifact
2. Check completeness against checklists above
3. Verify internal consistency
4. Validate against other artifacts (no contradictions)
5. Confirm stakeholder review/approval

**Red flags:**
- Vague language ("should be fast", "reasonably secure")
- Missing sections or TBD placeholders
- Last updated >6 months ago
- No author or owner identified

---

### Diagram Validation

**Applies to:** Architecture Diagrams

**Method:**
1. Check notation consistency (legend provided?)
2. Verify all components have labels and purpose
3. Trace key scenarios through diagrams
4. Cross-reference with requirements (all requirements addressable?)
5. Check for contradictions with other diagrams or documentation

**Red flags:**
- Box-and-arrow with no clear semantics
- Missing deployment architecture
- Diagrams contradict written docs
- No data flows shown

---

### Testing and Measurement

**Applies to:** Performance, Security, Code, Tests

**Method:**
1. Review test results or analysis reports
2. Verify tests are relevant to requirements
3. Check test environment realism (production-like?)
4. Validate test coverage (all critical paths tested?)
5. Confirm results meet acceptance criteria

**Red flags:**
- Tests in unrealistic environment
- Low coverage of critical paths
- Tests passing but requirements not met
- Outdated test results

---

### Financial Validation

**Applies to:** Cost Analysis

**Method:**
1. Review cost breakdown line by line
2. Spot-check pricing against cloud provider calculator
3. Verify all cost categories covered (no missing items)
4. Check cost scaling (linear, sublinear, superlinear?)
5. Validate against budget constraints

**Red flags:**
- Round numbers ("about $10K/month")
- Missing data transfer costs
- No cost scaling analysis
- Estimates much older than 6 months (pricing changes)

---

## Quality Modifiers in Detail

### Critical Gap (-20%)

**Applies when:** Any Tier 1 (core) evidence is completely missing.

**Rationale:** Core evidence is mandatory for confidence. Missing requirements, design, decisions, or risk assessment is a fatal flaw.

**Examples:**
- No requirements documentation
- Architecture diagrams missing or stub only
- Technology decisions not documented
- No risk assessment performed

**Impact:** Automatically caps confidence at MEDIUM (69%) even if all other evidence is perfect.

---

### Unverified Assumptions (-10%)

**Applies when:** Key assumptions are stated but not validated.

**Examples:**
- "Assume database can handle 10K TPS" (not tested)
- "Third-party API will respond in <100ms" (not verified)
- "Team can learn new framework in 2 weeks" (not validated)
- "Cost will stay under budget" (not estimated)

**Rationale:** Unverified assumptions are risks in disguise. Each assumption should be validated or explicitly managed as a risk.

---

### Inconsistent Artifacts (-10%)

**Applies when:** Evidence contradicts other evidence.

**Examples:**
- Diagram shows microservices, documentation describes monolith
- Requirements specify 99.9% availability, design has single points of failure
- Cost analysis assumes 1K users, requirements specify 100K users
- Security requirements mandate encryption, design omits it

**Rationale:** Contradictions indicate incomplete analysis or lack of rigor. Cannot have confidence when evidence conflicts.

---

### Outdated Evidence (-5%)

**Applies when:** Artifacts are >6 months old without recent review.

**Rationale:** Technology, pricing, and best practices evolve. Outdated evidence may not reflect current reality.

**Examples:**
- Architecture diagrams from 2024, current date is 2026
- Cost estimates from before major cloud pricing changes
- Security threat model predating new attack vectors

**Note:** If evidence was recently reviewed and confirmed current, do not apply modifier.

---

### External Validation (+10%)

**Applies when:** Third-party expert has reviewed and validated architecture.

**Examples:**
- Cloud vendor architecture review completed
- Independent security audit passed
- Peer review by another architecture team
- Consulting firm assessment

**Rationale:** External eyes catch blind spots and provide objective validation.

---

### Production Proven (+15%)

**Applies when:** Similar architecture is already running successfully in production.

**Examples:**
- Existing production system with similar characteristics
- Pilot/MVP deployed and operating successfully
- Reference architecture from vendor/community used successfully by others

**Rationale:** Production experience dramatically reduces uncertainty. Proven designs carry higher confidence.

**Note:** Must be truly similar (scale, requirements, constraints). "We've built web apps before" doesn't qualify if new architecture is vastly different.

---

## Evidence Deprecation Schedule

Evidence loses value over time. Re-assessment triggers:

| Artifact | Deprecation Period | Re-assessment Trigger |
|----------|-------------------|----------------------|
| Requirements | 3 months | Business priorities change, new stakeholders |
| Diagrams | 6 months | Major code changes, architecture drift |
| Decisions | 12 months | New technology versions, paradigm shifts |
| Risk | 3 months | New threats, environment changes |
| Performance | 1 month | Code changes, traffic pattern shifts |
| Security | 6 months | New vulnerabilities, attack techniques |
| Cost | 3 months | Pricing changes, usage pattern changes |
| Code | Continuous | Every commit ideally |
| Tests | Continuous | Code changes, new features |

**Re-assessment:** Update or re-verify evidence, don't just reuse old artifacts.

---

## Conclusion

This evidence catalog provides detailed criteria for evaluating architecture artifacts. Use these checklists to systematically assess evidence quality and determine appropriate confidence scores.

**Key principle:** Evidence quality matters as much as evidence presence. Partially complete or low-quality evidence receives 50% weight or less.
