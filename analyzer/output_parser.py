# output_analysis/output_parser.py

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class CustomOutput(BaseModel):
    claims: List[str] = Field(description="List of claims made")
    facts: List[str] = Field(description="List of facts presented")
    assumptions: List[str] = Field(description="List of assumptions made")
    sources: List[str] = Field(description="List of sources cited")
    ethical_concerns: Optional[List[str]] = Field(description="List of ethical concerns raised")
    summary: str = Field(description="Assessment of the logic used")


class MungerAnalysisOutput(BaseModel):
    author_credibility: str = Field(description="Credibility of the author")
    main_claim: str = Field(description="Main claim or thesis of the article")
    date_context: str = Field(description="Date and context of the article")
    internal_consistency: str = Field(description="Check for internal consistency")
    inversion: str = Field(description="Inversion analysis")
    availability_bias: str = Field(description="Availability bias check")
    mental_models: Dict[str, str] = Field(
        description="Mental models applied")  # Made it a dictionary to capture multiple models
    evidence_assessment: Dict[str, str] = Field(
        description="Assessment of the evidence")  # Made it a dictionary for multiple types of evidence assessment
    ethical_evaluation: Dict[str, str] = Field(
        description="Ethical and moral evaluation")  # Made it a dictionary for multiple ethical frameworks
    synthesis: str = Field(description="Synthesis and conclusion")
    action_or_file: str = Field(description="Action taken or insights stored")
