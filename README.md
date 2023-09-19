
#### Article Analyzer Project

---

##### Description

This project aims to provide a comprehensive analysis of articles using various NLP models and techniques. It includes modules for the analysis, logging, and storage of articles and analysis feedback.

##### Components

- **Article Class**: Manages article data, including content and metadata.
- **Article Analyzer**: Core component for article analysis.
- **Prompts Library**: Versioned text analysis prompts.
- **Historical Article Database**: Storage for analyzed articles.
- **Logger**: Logs various metrics related to article analysis.
- **Feedback Database**: Manages user feedback for analysis quality.

##### Setup

1. Install Python 3.x.
2. Clone the repository.
3. Install dependencies: `pip install -r requirements.txt`

##### Usage

1. Initialize the historical database: `python initialize_database.py`
2. Run the main analyzer: `python main.py`
3. Provide feedback on analysis quality when prompted.
