#!/usr/bin/env python3
"""
Architecture Confidence Score Calculator

Computes standardized confidence scores based on evidence inventory and quality modifiers.

Usage:
  python calculate_confidence.py [--evidence-file evidence.yaml] [--verbose]

Input:
  YAML file with evidence inventory and modifiers, or interactive prompts

Output:
  Confidence level and score with justification
"""

import argparse
import sys
from typing import Dict, List, Tuple
from enum import Enum


class CompletionStatus(Enum):
    """Evidence completion status"""
    COMPLETE = 1.0  # 100% of weight
    PARTIAL = 0.5   # 50% of weight
    MISSING = 0.0   # 0% of weight


class ConfidenceLevel(Enum):
    """Standardized confidence levels"""
    CRITICAL = "CRITICAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERIFIED = "VERIFIED"


# Evidence weights configuration
EVIDENCE_WEIGHTS = {
    # Core Evidence (70%)
    "requirements": 20,
    "diagrams": 15,
    "decisions": 15,
    "risk": 15,
    
    # Supporting Evidence (30%)
    "performance": 10,
    "security": 10,
    "cost": 5,
    "code": 5,
    "tests": 5,
}

# Quality modifiers
MODIFIERS = {
    "critical_gap": -20,
    "unverified_assumptions": -10,
    "inconsistent_artifacts": -10,
    "outdated_evidence": -5,
    "external_validation": 10,
    "production_proven": 15,
}


class ConfidenceCalculator:
    """Calculates architecture confidence scores"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.evidence = {}
        self.modifiers = []
        self.base_score = 0.0
        self.final_score = 0.0
        
    def log(self, message: str):
        """Log debug message if verbose"""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)
    
    def set_evidence(self, evidence_name: str, status: CompletionStatus):
        """Set completion status for an evidence artifact"""
        if evidence_name not in EVIDENCE_WEIGHTS:
            raise ValueError(f"Unknown evidence type: {evidence_name}")
        
        self.evidence[evidence_name] = status
        self.log(f"Evidence set: {evidence_name} = {status.name}")
    
    def add_modifier(self, modifier_name: str):
        """Add a quality modifier"""
        if modifier_name not in MODIFIERS:
            raise ValueError(f"Unknown modifier: {modifier_name}")
        
        self.modifiers.append(modifier_name)
        self.log(f"Modifier added: {modifier_name}")
    
    def calculate_base_score(self) -> float:
        """Calculate base score from evidence inventory"""
        self.log("Calculating base score...")
        
        score = 0.0
        for evidence_name, weight in EVIDENCE_WEIGHTS.items():
            if evidence_name in self.evidence:
                status = self.evidence[evidence_name]
                contribution = weight * status.value
                score += contribution
                self.log(f"  {evidence_name}: {weight}% × {status.value} = {contribution}")
            else:
                self.log(f"  {evidence_name}: Not assessed (0%)")
        
        self.base_score = score
        self.log(f"Base score: {score}%")
        return score
    
    def apply_modifiers(self) -> float:
        """Apply quality modifiers to base score"""
        self.log("Applying modifiers...")
        
        if self.base_score == 0:
            self.calculate_base_score()
        
        score = self.base_score
        
        for modifier_name in self.modifiers:
            adjustment = MODIFIERS[modifier_name]
            score += adjustment
            self.log(f"  {modifier_name}: {adjustment:+d}% → {score}%")
        
        # Clamp to 0-100 range
        score = max(0, min(100, score))
        
        self.final_score = score
        self.log(f"Final score: {score}%")
        return score
    
    def get_confidence_level(self, score: float) -> ConfidenceLevel:
        """Map score to confidence level"""
        if score >= 90:
            return ConfidenceLevel.VERIFIED
        elif score >= 70:
            return ConfidenceLevel.HIGH
        elif score >= 41:
            return ConfidenceLevel.MEDIUM
        elif score >= 21:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.CRITICAL
    
    def generate_justification(self) -> Dict:
        """Generate detailed justification"""
        level = self.get_confidence_level(self.final_score)
        
        # Identify present evidence
        present = [
            f"{name} ({EVIDENCE_WEIGHTS[name]}%)"
            for name, status in self.evidence.items()
            if status == CompletionStatus.COMPLETE
        ]
        
        # Identify partial evidence
        partial = [
            f"{name} (~{EVIDENCE_WEIGHTS[name]//2}%)"
            for name, status in self.evidence.items()
            if status == CompletionStatus.PARTIAL
        ]
        
        # Identify missing evidence
        missing = [
            f"{name} ({EVIDENCE_WEIGHTS[name]}%)"
            for name in EVIDENCE_WEIGHTS.keys()
            if name not in self.evidence or self.evidence[name] == CompletionStatus.MISSING
        ]
        
        # Generate recommendation
        if level in [ConfidenceLevel.VERIFIED, ConfidenceLevel.HIGH]:
            recommendation = "Approved to proceed."
        elif level == ConfidenceLevel.MEDIUM:
            recommendation = "Proceed with caution. Address gaps before production."
        elif level == ConfidenceLevel.LOW:
            recommendation = "Significant gaps. Revise architecture before implementation."
        else:
            recommendation = "STOP. Critical flaws. Fundamental rework required."
        
        return {
            "level": level.value,
            "score": self.final_score,
            "base_score": self.base_score,
            "present_evidence": present,
            "partial_evidence": partial,
            "missing_evidence": missing,
            "modifiers_applied": [
                f"{name} ({MODIFIERS[name]:+d}%)" for name in self.modifiers
            ],
            "recommendation": recommendation,
        }
    
    def calculate(self) -> Dict:
        """Run full calculation and return results"""
        self.calculate_base_score()
        self.apply_modifiers()
        return self.generate_justification()


def format_report(result: Dict, format_type: str = "brief") -> str:
    """Format confidence report"""
    
    if format_type == "brief":
        return f"""**Confidence: {result['level']} ({result['score']:.0f}%)**

Based on: {', '.join(result['present_evidence'][:3]) if result['present_evidence'] else 'No complete evidence'}
Missing: {', '.join(result['missing_evidence'][:2]) if result['missing_evidence'] else 'None'}
Recommendation: {result['recommendation']}"""
    
    elif format_type == "detailed":
        report = f"""## Architecture Confidence Assessment

**Confidence Score: {result['level']} ({result['score']:.0f}%)**

### Evidence Inventory

#### Complete Evidence
{chr(10).join(['- ' + e for e in result['present_evidence']]) if result['present_evidence'] else '- None'}

#### Partial Evidence
{chr(10).join(['- ' + e for e in result['partial_evidence']]) if result['partial_evidence'] else '- None'}

#### Missing Evidence
{chr(10).join(['- ' + e for e in result['missing_evidence']]) if result['missing_evidence'] else '- None'}

### Calculation

Base Score: {result['base_score']:.0f}%
Modifiers:
{chr(10).join(['- ' + m for m in result['modifiers_applied']]) if result['modifiers_applied'] else '- None applied'}
Final Score: {result['score']:.0f}%

### Recommendation

{result['recommendation']}
"""
        return report
    
    else:  # json
        import json
        return json.dumps(result, indent=2)


def interactive_mode() -> ConfidenceCalculator:
    """Interactive evidence collection"""
    calc = ConfidenceCalculator(verbose=True)
    
    print("Architecture Confidence Calculator")
    print("=" * 50)
    print("\nEvidence Inventory:")
    print("  [c] Complete  [p] Partial  [m] Missing  [s] Skip\n")
    
    for evidence_name, weight in EVIDENCE_WEIGHTS.items():
        while True:
            response = input(f"{evidence_name.capitalize()} ({weight}%): [c/p/m/s]: ").lower().strip()
            
            if response == 'c':
                calc.set_evidence(evidence_name, CompletionStatus.COMPLETE)
                break
            elif response == 'p':
                calc.set_evidence(evidence_name, CompletionStatus.PARTIAL)
                break
            elif response == 'm':
                calc.set_evidence(evidence_name, CompletionStatus.MISSING)
                break
            elif response == 's':
                break
            else:
                print("  Invalid input. Use c/p/m/s")
    
    print("\n" + "=" * 50)
    print("\nQuality Modifiers:")
    print("  [y] Yes  [n] No\n")
    
    for modifier_name, adjustment in MODIFIERS.items():
        display_name = modifier_name.replace('_', ' ').title()
        response = input(f"{display_name} ({adjustment:+d}%): [y/n]: ").lower().strip()
        
        if response == 'y':
            calc.add_modifier(modifier_name)
    
    return calc


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Calculate architecture confidence score'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['brief', 'detailed', 'json'],
        default='brief',
        help='Output format (default: brief)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose debug output'
    )
    
    # Example mode for testing
    parser.add_argument(
        '--example',
        choices=['early', 'pre-impl', 'production', 'critical'],
        help='Run with example scenario'
    )
    
    args = parser.parse_args()
    
    if args.example:
        calc = ConfidenceCalculator(verbose=args.verbose)
        
        if args.example == 'early':
            # Early stage assessment
            calc.set_evidence('requirements', CompletionStatus.PARTIAL)
            calc.set_evidence('diagrams', CompletionStatus.PARTIAL)
            calc.set_evidence('decisions', CompletionStatus.PARTIAL)
            calc.set_evidence('risk', CompletionStatus.MISSING)
            
        elif args.example == 'pre-impl':
            # Pre-implementation review
            calc.set_evidence('requirements', CompletionStatus.COMPLETE)
            calc.set_evidence('diagrams', CompletionStatus.COMPLETE)
            calc.set_evidence('decisions', CompletionStatus.COMPLETE)
            calc.set_evidence('risk', CompletionStatus.COMPLETE)
            calc.set_evidence('performance', CompletionStatus.PARTIAL)
            calc.set_evidence('security', CompletionStatus.COMPLETE)
            
        elif args.example == 'production':
            # Production readiness
            calc.set_evidence('requirements', CompletionStatus.COMPLETE)
            calc.set_evidence('diagrams', CompletionStatus.COMPLETE)
            calc.set_evidence('decisions', CompletionStatus.COMPLETE)
            calc.set_evidence('risk', CompletionStatus.COMPLETE)
            calc.set_evidence('performance', CompletionStatus.COMPLETE)
            calc.set_evidence('security', CompletionStatus.COMPLETE)
            calc.set_evidence('cost', CompletionStatus.COMPLETE)
            calc.set_evidence('code', CompletionStatus.COMPLETE)
            calc.set_evidence('tests', CompletionStatus.COMPLETE)
            calc.add_modifier('external_validation')
            
        elif args.example == 'critical':
            # Critical gaps
            calc.set_evidence('requirements', CompletionStatus.PARTIAL)
            calc.set_evidence('diagrams', CompletionStatus.PARTIAL)
            calc.add_modifier('critical_gap')
            calc.add_modifier('unverified_assumptions')
    else:
        # Interactive mode
        calc = interactive_mode()
    
    # Calculate and display
    result = calc.calculate()
    report = format_report(result, args.format)
    print("\n" + "=" * 50)
    print(report)


if __name__ == '__main__':
    main()
