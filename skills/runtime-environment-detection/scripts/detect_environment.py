#!/usr/bin/env python3
"""
Runtime Environment Detection Script

This script demonstrates the detection logic that agents can follow
when determining their execution environment.

Usage:
  python detect_environment.py [--verbose]

Outputs:
  JSON with detected environment type, confidence, and recommended strategy
"""

import json
import os
import sys
from typing import Dict, List, Tuple


class EnvironmentDetector:
    """Detects runtime environment using multiple signals"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.signals = []
        
    def log(self, message: str):
        """Log debug message if verbose mode enabled"""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)
    
    def check_vscode_tools(self) -> bool:
        """
        Signal 1: Check if VS Code tools are available
        
        In agent context, this would be:
        tool_search_tool_regex with pattern '^vscode_'
        """
        self.log("Checking for VS Code tools...")
        
        # Simulated tool check - in real agent, use tool_search_tool_regex
        # For demo purposes, check for VS Code environment variables
        vscode_indicators = [
            'VSCODE_PID',
            'VSCODE_IPC_HOOK',
            'TERM_PROGRAM',  # 'vscode' when in VS Code terminal
        ]
        
        vscode_found = any(
            os.getenv(var) and 'vscode' in str(os.getenv(var)).lower()
            for var in vscode_indicators
        )
        
        if vscode_found:
            self.signals.append('vscode_tools_likely')
            self.log("✓ VS Code indicators found")
            return True
        
        self.log("✗ No VS Code indicators found")
        return False
    
    def check_context_structure(self) -> str:
        """
        Signal 2: Inspect context structure
        
        In agent context, check for:
        - editorContext presence
        - API request metadata
        - Terminal-only context
        """
        self.log("Inspecting context structure...")
        
        # Check for CI/CD environment (headless indicator)
        ci_vars = ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'JENKINS_HOME', 'TRAVIS']
        if any(os.getenv(var) for var in ci_vars):
            self.signals.append('ci_environment')
            self.log("✓ CI/CD environment detected")
            return 'ci_environment'
        
        # Check for interactive terminal
        if sys.stdin.isatty() and sys.stdout.isatty():
            self.signals.append('interactive_terminal')
            self.log("✓ Interactive terminal detected")
            return 'interactive_terminal'
        
        # Check for API-like invocation (stdin pipe)
        if not sys.stdin.isatty():
            self.signals.append('piped_input')
            self.log("✓ Piped input detected (possible API mode)")
            return 'piped_input'
        
        self.log("✗ No clear context structure identified")
        return 'unknown'
    
    def check_execution_pattern(self) -> str:
        """
        Signal 3: Analyze execution pattern
        
        In agent context, look at conversation history
        """
        self.log("Analyzing execution pattern...")
        
        # Check if running in batch mode
        batch_indicators = [
            'BATCH_MODE',
            'NO_INTERACTIVE',
            'AUTOMATED_RUN',
        ]
        
        if any(os.getenv(var) for var in batch_indicators):
            self.signals.append('batch_execution')
            self.log("✓ Batch execution pattern detected")
            return 'batch_execution'
        
        # Check for shell environment
        shell = os.getenv('SHELL', '')
        if shell and 'bash' in shell or 'zsh' in shell:
            self.signals.append('shell_environment')
            self.log("✓ Shell environment detected")
            return 'shell_environment'
        
        self.log("✗ No clear execution pattern identified")
        return 'unknown'
    
    def calculate_confidence(self, environment: str) -> Tuple[str, int]:
        """
        Calculate confidence score based on number of matching signals
        
        Returns: (confidence_level, score)
        """
        score = len(self.signals)
        
        if score >= 3:
            return ('HIGH', score)
        elif score == 2:
            return ('MEDIUM', score)
        elif score == 1:
            return ('LOW', score)
        else:
            return ('UNKNOWN', score)
    
    def detect(self) -> Dict:
        """
        Run full detection pipeline
        
        Returns: Detection result with environment, confidence, and strategy
        """
        self.log("Starting runtime environment detection...")
        
        # Signal 1: Tool availability
        vscode_tools = self.check_vscode_tools()
        
        # Signal 2: Context structure
        context_type = self.check_context_structure()
        
        # Signal 3: Execution pattern
        execution_pattern = self.check_execution_pattern()
        
        # Determine environment based on signals
        environment = self._determine_environment(
            vscode_tools, context_type, execution_pattern
        )
        
        # Calculate confidence
        confidence, score = self.calculate_confidence(environment)
        
        # Select interaction strategy
        strategy = self._select_strategy(environment)
        
        result = {
            'environment': environment,
            'confidence': confidence,
            'confidence_score': score,
            'signals': self.signals,
            'interaction_strategy': strategy,
            'timestamp': self._get_timestamp(),
        }
        
        self.log(f"Detection complete: {environment} (confidence: {confidence})")
        
        return result
    
    def _determine_environment(
        self, 
        vscode_tools: bool, 
        context_type: str, 
        execution_pattern: str
    ) -> str:
        """Determine environment from collected signals"""
        
        # VS Code takes priority if tools present
        if vscode_tools:
            return 'vscode-chat'
        
        # CI/CD environment
        if context_type == 'ci_environment' or execution_pattern == 'batch_execution':
            return 'headless-automation'
        
        # API mode (piped input, non-interactive)
        if context_type == 'piped_input' and execution_pattern != 'shell_environment':
            return 'api-mode'
        
        # CLI agent runner (interactive terminal)
        if context_type == 'interactive_terminal':
            return 'cli-agent-runner'
        
        # Default fallback
        return 'cli-with-chat'
    
    def _select_strategy(self, environment: str) -> Dict:
        """Select interaction strategy based on environment"""
        
        strategies = {
            'vscode-chat': {
                'ask_method': 'use_vscode_askQuestions',
                'format': 'rich_markdown',
                'file_links': 'with_line_numbers',
                'fallback': 'chat_prompts'
            },
            'cli-agent-runner': {
                'ask_method': 'natural_language_in_chat',
                'format': 'simple_text',
                'file_links': 'absolute_paths',
                'fallback': 'continue_with_defaults'
            },
            'api-mode': {
                'ask_method': 'fail_if_input_missing',
                'format': 'structured_json',
                'file_links': 'absolute_paths',
                'fallback': 'error_response'
            },
            'headless-automation': {
                'ask_method': 'read_from_config',
                'format': 'log_files',
                'file_links': 'absolute_paths',
                'fallback': 'use_defaults'
            },
            'cli-with-chat': {
                'ask_method': 'natural_language_in_chat',
                'format': 'simple_text',
                'file_links': 'absolute_paths',
                'fallback': 'continue_with_defaults'
            }
        }
        
        return strategies.get(environment, strategies['cli-with-chat'])
    
    def _get_timestamp(self) -> str:
        """Get ISO timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detect runtime environment for agent execution'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose debug output'
    )
    parser.add_argument(
        '--output', '-o',
        choices=['json', 'summary'],
        default='json',
        help='Output format (default: json)'
    )
    
    args = parser.parse_args()
    
    detector = EnvironmentDetector(verbose=args.verbose)
    result = detector.detect()
    
    if args.output == 'json':
        print(json.dumps(result, indent=2))
    else:
        # Summary format
        print(f"Environment: {result['environment']}")
        print(f"Confidence: {result['confidence']} ({result['confidence_score']} signals)")
        print(f"Strategy: {result['interaction_strategy']['ask_method']}")
        print(f"Format: {result['interaction_strategy']['format']}")


if __name__ == '__main__':
    main()
