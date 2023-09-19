from analyzer.output_parser import CustomOutput, MungerAnalysisOutput  # Replace with your actual import
from prompts.prompts_library import Prompts
from evals import QualityEvaluator  # Import your QualityEvaluator
from typing import Type, Union
from pydantic import BaseModel
from logger import AnalysisLogger  # Import your AnalysisLogger
import json

class ArticleAnalyzer:
    def __init__(self, prompt_version: str):
        self.prompts = Prompts(prompt_version)  # Initialize Prompts with the desired version
        self.logger = AnalysisLogger()  # Initialize the logger here if not in main.py
        self.evaluator = QualityEvaluator()  # Initialize the QualityEvaluator here

    def analyze(self, article, style: str = "default", model: Type[BaseModel] = CustomOutput):
        try:
            analysis_json = self.prompts.get_article_analysis(article.content, model, style)
            if not analysis_json:
                print("Warning: analysis_json is empty or None.")
                return None
            return analysis_json
        except Exception as e:
            print(f"An error occurred while analyzing the article: {e}")
            return None