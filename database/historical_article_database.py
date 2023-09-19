import json
import os
import hashlib
from analyzer.output_parser import CustomOutput  # Make sure to import CustomOutput

class HistoricalArticleDatabase:
    def __init__(self, content_directory, database_directory):
        self.content_directory = content_directory
        self.database_directory = database_directory
        self.index_file = os.path.join(self.database_directory, 'index.json')

        # Create directories if they don't exist
        os.makedirs(self.content_directory, exist_ok=True)
        os.makedirs(self.database_directory, exist_ok=True)

        # Load existing index or create a new one
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                self.index = json.load(f)
        else:
            self.index = {}

    def save_index(self):
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f)

    def store_analyzed_article(self, article):
        # Generate a unique ID for this article based on its content
        article_id = hashlib.sha256(article.content.encode()).hexdigest()

        # Construct the path for the new article
        article_path = os.path.join(self.database_directory, f"{article_id}.json")

        # Convert the article object to a dictionary
        article_dict = article.to_dict()

        # Save the article to disk
        try:
            with open(article_path, 'w') as f:
                json.dump(article_dict, f)
        except Exception as e:
            print(f"Error saving article: {e}")
            return

        # Retrieve the old index entry, if it exists
        old_entry = self.index.get(article_id, {})

        # Basic fields that are always present
        index_entry = {
            'title': article.title,
            'author': article.author,
            'date': article.date,
        }

        # Dynamically add fields from the CustomOutput model
        if article.analysis_results:
            for field_name in CustomOutput.__fields__.keys():
                index_entry[field_name] = article.analysis_results.get(
                    field_name, old_entry.get(field_name, [])
                )

        # Update the index
        self.index[article_id] = index_entry

        # Save the updated index
        self.save_index()

