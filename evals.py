from typing import Union
import json
import openai


class QualityEvaluator:
    def __init__(self):
        pass  # Initialize anything you need here

    def llm_evaluation(self, analysis_json: Union[str, dict]) -> int:
        try:
            prompt_for_quality = "Based on the analysis you have just performed, how would you rate the quality on a scale of 1 to 5?"
            conversation = [
                {"role": "system",
                 "content": "You are a helpful assistant specialized in self-evaluating your performance."},
                {"role": "user", "content": prompt_for_quality}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            return int(response['choices'][0]['message']['content'].strip())
        except Exception as e:
            print(f"An error occurred while getting the LLM's self-evaluation: {e}")
            return 0  # Default value in case of an error

    def evaluate(self, analysis_json: Union[str, dict]) -> int:
        if isinstance(analysis_json, str):
            analysis_dict = json.loads(analysis_json)
        else:
            analysis_dict = analysis_json

        llm_rating = self.llm_evaluation(analysis_json)
        return llm_rating
