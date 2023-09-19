import json
import openai
import os
from pydantic import BaseModel
from pydantic.fields import ModelField
from typing import Type


class Prompts:
    def __init__(self,prompt_version:str):
        # Set OpenAI API key
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.prompt_version = prompt_version
        self.prompt_details = {}
        self.load_prompt_details(prompt_version)

    def load_prompt_details(self, prompt_version: str):
        with open(f'prompt_versions/version_{prompt_version}.json', 'r') as f:
            self.prompt_details = json.load(f)

    def generate_prompt_from_model(self, model: Type[BaseModel], article_content: str, style: str = "default") -> str:
        # Use self.prompt_details to generate the prompt
        detailed_instructions = self.prompt_details.get("detailed_instructions", {})
        example_data = self.prompt_details.get("example_data", {})

        if style == "munger":
            prompt = "Charlie Munger is known for his multidisciplinary thinking and structured analysis. Please analyze the following article using a similar approach. Provide your analysis in the following structured format:\n\n"
        else:
            prompt = "Please analyze the following article and provide its key components in the specified format:\n\n"

        for name, field in model.__annotations__.items():
            model_field: ModelField = model.__fields__[name]
            description = model_field.field_info.description
            required = " (Required)" if model_field.required else " (Optional)"
            detailed_instruction = detailed_instructions.get(name, "")
            prompt += f"- {name}: {description}{required}. {detailed_instruction}\n"

        prompt += "\nFor example, your output could look something like this:\n\n"
        prompt += "{\n"
        for name in model.__annotations__:
            example = example_data.get(name, "Example content...")
            prompt += f'  "{name}": "{example}", \n'
        prompt = prompt.rstrip(", \n") + "\n}\n\n"

        prompt += f"Article Content for Analysis:\n{article_content}\n"

        return prompt

    def get_article_analysis(self, content, model: Type[BaseModel], style: str = "default"):
        # Generate the prompt using the loaded prompt_details
        prompt = self.generate_prompt_from_model(model, content, style)

        conversation = [
            {"role": "system",
             "content": "You are a helpful assistant specialized in analyzing articles and outputting structured data."},
            {"role": "user",
             "content": prompt}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            last_message = response['choices'][0]['message']['content']
            return last_message  # Assuming the assistant's response is in a JSON-compatible format
        except Exception as e:
            print(f"Error during API call: {e}")
            return None
