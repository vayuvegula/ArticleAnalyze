import logging

def setup_logger():
    logger = logging.getLogger("ArticleAnalyzer")
    logger.setLevel(logging.INFO)

    # Create a file handler that writes log messages to a file
    file_handler = logging.FileHandler("article_analysis.log")
    file_handler.setLevel(logging.INFO)

    # Create a console handler that writes log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add the formatter to the handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


import json
import os


class AnalysisLogger:
    def __init__(self, log_file='analysis_log.json'):
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log(self, prompt_version, quality, article_id, model_name):
        with open(self.log_file, 'r') as f:
            logs = json.load(f)

        new_log = {
            'prompt_version': prompt_version,
            'quality': quality,
            'article_id': article_id,
            'model_name': model_name
        }

        logs.append(new_log)

        with open(self.log_file, 'w') as f:
            json.dump(logs, f)