## article module

# Example code for modifying the Article class to accept JSON-formatted content
import json
import uuid


class Article:
    def __init__(self, title, author, date, content):
        self.id = str(uuid.uuid4())  # Generate a unique ID
        self.title = title
        self.author = author
        self.date = date
        self.content = content
        self.analysis_results = {}

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'date': self.date,
            'content': self.content,
            'analysis_results': self.analysis_results
        }
    @classmethod
    def from_json_file(cls, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(data['title'], data['author'], data['date'], data['content'])
