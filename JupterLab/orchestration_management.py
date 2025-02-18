import json
import boto3
from config import CONFIG
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# Define ProcessingStage
class ProcessingStage(Enum):
    PRE_PROCESSING = "pre_processing"
    ORCHESTRATION = "orchestration"
    KB_RESPONSE = "kb_response"

# Define ProcessingStep
@dataclass
class ProcessingStep:
    name: str
    type: str
    input: Dict[str, Any]
    output: Dict[str, str]
    condition: Optional[str] = None
    steps: Optional[List['ProcessingStep']] = None
    model: Optional[str] = None

# Define ProcessingStrategy
@dataclass
class ProcessingStrategy:
    name: str
    description: str
    prompt_template: str
    output_format: Dict[str, Any]
    steps: List[ProcessingStep]

# Define OrchestrationConfig
class OrchestrationConfig:
    def __init__(self):
        self.strategies = {
            ProcessingStage.PRE_PROCESSING: self._init_preprocessing_strategies(),
            ProcessingStage.ORCHESTRATION: self._init_orchestration_strategies(),
            ProcessingStage.KB_RESPONSE: self._init_kb_response_strategies()
        }

    # Init Pre-processing strategy
    def _init_preprocessing_strategies(self):
        return {
            "classify_input": ProcessingStrategy(
                name="classify_input",
                description="Classify user input as question or code",
                prompt_template="""
                You are a system designed to classify user input.
                
                User Input:
                {user_input}
                
                Task:
                - Determine if the input is a natural language question or a smart contract code.
                
                Output Format:
                {
                    "input_type": "question" or "code"
                }
                """,
                output_format={"input_type": str},
                steps=[]
            )
        }

    # Init Orchestration strategy
    def _init_orchestration_strategies(self):
        return {
            "query": ProcessingStrategy(
                name="query_orchestration",
                description="Process user queries and integrate knowledge base results",
                prompt_template="""
                You are an expert Web3 Smart Contract Security Auditor (SCSA).
                
                User Query:
                {{ user_input }}
                
                Context from Knowledge Base:
                {{ knowledge_base_results }}
                
                Task:
                - Provide a detailed answer to the user's question.
                - Include the following sections in your response:
                  1. Core Concepts
                  2. Practical Implementation
                  3. Security Considerations
                  4. Additional Resources.
                """,
                output_format={
                    "core_concepts": List[str],
                    "practical_implementation": List[str],
                    "security_considerations": List[str],
                    "additional_resources": List[str]
                },
                steps=[]
            ),
            "code_analysis": ProcessingStrategy(
                name="code_analysis_orchestration",
                description="Analyze smart contract code and generate a security audit report",
                prompt_template="""
                You are an expert Web3 Smart Contract Security Auditor (SCSA).
                
                User Input (Smart Contract Code):
                {{ user_input }}
                
                Task:
                - Analyze the provided smart contract code for vulnerabilities.
                - Classify vulnerabilities based on severity as Critical, High, Medium, or Low.
                - Provide actionable recommendations for each vulnerability.
                
                Context from Knowledge Base:
                {{ knowledge_base_results }}
                
                Output Format:
                  [Security Audit Report]
                  
                  Executive Summary:
                    - Contract Purpose
                    - Audit Date
                    - Overall Risk Level
                
                  Vulnerability Findings:
                    Critical Findings:
                      ID: [C-01]
                      Title:
                      Description:
                      Impact:
                      Recommendation:
                    High Findings:
                      ID: [H-01]
                      Title:
                      Description:
                      Impact:
                      Recommendation:
                    Medium Findings:
                      ID: [M-01]
                      Title:
                      Description:
                      Impact:
                      Recommendation:
                    Low Findings:
                      ID: [L-01]
                      Title:
                      Description:
                      Impact:
                      Recommendation:

                  Summary Recommendations:
                    - Critical Fixes
                    - Security Improvements
                    - Best Practices.
                """,
                output_format={
                    "executive_summary": Dict[str, Any],
                    "vulnerability_findings": Dict[str, List[Dict[str, Any]]],
                    "summary_recommendations": List[str]
                },
                steps=[]
            )
        }

    # Init KB Response Generation strategy
    def _init_kb_response_strategies(self):
        return {
            "query_kb_response": ProcessingStrategy(
                name="query_kb_response",
                description="Generate response by combining Sonnet analysis and knowledge base results",
                prompt_template="""
                You are an expert Web3 Smart Contract Security Auditor (SCSA).
                
                User Query Context from Knowledge Base Results:

                {{ knowledge_base_results }}

                Task:
                  Provide a concise and accurate answer to the user's query based on the above context.
                  
                  Always write in this language unless explicitly instructed otherwise: mandarin-chinese-simplified.
                  
                  Current date: Monday, February 17, 2025, 12:13 AM CST.
                  
                  Output Format:
                  {
                    "final_response": "The complete answer to the query."
                  }
              """,
                output_format={"final_response": str},
                steps=[]
            ),
            "code_kb_response": ProcessingStrategy(
                name="code_kb_response",
                description="Generate enhanced security report by combining code analysis and knowledge base patterns",
                prompt_template="""
              You are an expert Web3 Smart Contract Security Auditor (SCSA).
              
              Security Analysis Result:

              {{ security_analysis }}

              Knowledge Base Patterns:

              {{ kb_security_patterns }}

              Task:
              - Integrate security analysis results and knowledge base best practices.
              - Generate a complete security report.
              - Provide specific improvement suggestions.

              Output Format:
              {
                  "security_report": {
                      "executive_summary": "Summary of findings.",
                      "vulnerability_analysis": ["Vulnerability 1", "Vulnerability 2"],
                      "risk_assessment": ["Risk 1", "Risk 2"],
                      "mitigation_strategies": ["Strategy 1", "Strategy 2"]
                  },
                  "improvement_plan": {
                      "immediate_actions": ["Immediate action 1", "Immediate action 2"],
                      "long_term_recommendations": ["Long-term recommendation 1", "Long-term recommendation 2"]
                  },
                  "security_guidelines": ["Guideline 1", "Guideline 2"]
              }
              """,
                output_format={
                    "security_report": Dict[str, Any],
                    "improvement_plan": Dict[str, List[str]],
                    "security_guidelines": List[str]
                },
                steps=[]
            )
        }

# Create OrchestrationConfig
orchestration_config = OrchestrationConfig()
print(json.dumps(orchestration_config.strategies, indent=4))
