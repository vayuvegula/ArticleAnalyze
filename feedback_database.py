import json
import os


class FeedbackDatabase:
    def __init__(self, feedback_file_path='feedback_database.json'):
        self.feedback_file_path = feedback_file_path

    def save_feedback(self, article_id, prompt_version, model_name, quality_rating, additional_feedback, style):
        # Check if the file already exists and is not empty
        if os.path.exists(self.feedback_file_path) and os.path.getsize(self.feedback_file_path) > 0:
            with open(self.feedback_file_path, 'r') as f:
                feedbacks = json.load(f)
        else:
            feedbacks = []

        new_feedback = {
            'article_id': article_id,
            'prompt_version': prompt_version,
            'model_name': model_name,
            'quality_rating': quality_rating,
            'additional_feedback': additional_feedback,
            'style': style
        }

        feedbacks.append(new_feedback)

        with open(self.feedback_file_path, 'w') as f:
            json.dump(feedbacks, f)

    def read_feedback(self):
        if os.path.exists(self.feedback_file_path) and os.path.getsize(self.feedback_file_path) > 0:
            with open(self.feedback_file_path, 'r') as f:
                return json.load(f)
        else:
            return []
