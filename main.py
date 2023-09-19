# # Main script
# import schedule
# import time
# from controller.main_controller import MainController
#
# def job():
#     main_controller = MainController()
#     main_controller.run()
#
# # Schedule the job to run daily
# schedule.every().day.at("09:00").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)


# main.py
# import json
#
# from langchain.chat_models import ChatOpenAI
# from article.article import Article
# from prompts.prompts_library import Prompts
# from analyzer.article_analyzer import ArticleAnalyzer
# from database.historical_article_database import HistoricalArticleDatabase
# from analyzer.output_parser import CustomOutput,PydanticOutputParser,MungerAnalysisOutput
# from langchain.output_parsers import OutputFixingParser
#
# if __name__ == "__main__":
#     # Initialize the database object with content and database directories
#     db = HistoricalArticleDatabase(
#         content_directory="/Users/ravivayuvegula/Projects/content",
#         database_directory="/Users/ravivayuvegula/Projects/Articles_database"
#     )
#
#     # Load an Article object from a JSON file located in the content directory
#     filepath = "/Users/ravivayuvegula/Projects/content/article_2.json"
#     article_from_json = Article.from_json_file(filepath)
#     print(f"Content of article_2: {article_from_json.content}")  # Check if the content is being correctly loaded
#
#     # Initialize a Prompts object with a version number (e.g., "1" or "2")
#     prompt_version = "1"
#     promptM = Prompts(version=prompt_version)
#
#     # Create an ArticleAnalyzer object and analyze the article
#     analyzer = ArticleAnalyzer()
#
#     # Analyze the article and get the JSON string response
#     # For a Munger-style analysis
#     analysis_response = analyzer.analyze(article_from_json, style="munger", model=MungerAnalysisOutput,version=prompt_version)
#     print(f"Analysis response: {analysis_response}")  # Check what is being returned from the analyze method
#
#     # # Initialize the PydanticOutputParser with the CustomOutput model
#     # parser = PydanticOutputParser(pydantic_object=MungerAnalysisOutput)
#     # # Parse the output
#     # parsed_output = parser.parse(analysis_response)
#     #
#     # new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())
#     #
#     # # Convert parsed_output back to a JSON string (assuming CustomOutput can be easily converted to a dict)
#     # parsed_output_json = json.dumps(parsed_output.dict()) if hasattr(parsed_output, 'dict') else json.dumps(
#     #     parsed_output.__dict__)
#     #
#     # fixed_response = new_parser.parse(parsed_output_json)
#     # final_analysis_response = json.dumps(fixed_response.__dict__)
#
#     # Convert the JSON string response into a dictionary and update the article object's analysis_results attribute
#     if analysis_response:
#         try:
#             article_from_json.analysis_results = json.loads(analysis_response)
#         except json.JSONDecodeError as e:
#             print(f"JSON Decode Error: {e}")
#     else:
#         print("Warning: analysis_response is empty or None.")
#
#     # Store the analyzed article in the database
#     db.store_analyzed_article(article_from_json)
#
#     # Print the analysis results
#     print("Analysis Results:")
#     print(article_from_json.analysis_results)
# promptM = Prompts()
# promptMdetails = promptM.generate_prompt_from_model(article_content=article_from_json, style="munger", model=MungerAnalysisOutput)
# print(promptMdetails)

##########
import json
from article.article import Article
from analyzer.article_analyzer import ArticleAnalyzer
from database.historical_article_database import HistoricalArticleDatabase
from analyzer.output_parser import CustomOutput, PydanticOutputParser, MungerAnalysisOutput
from feedback_database import FeedbackDatabase  # Import FeedbackDatabase

def read_logger_output(log_file_path='analysis_log.json'):
    try:
        with open(log_file_path, 'r') as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        print(f"Log file {log_file_path} not found.")
        return []

if __name__ == "__main__":
    # Initialize the database object with content and database directories
    db = HistoricalArticleDatabase(
        content_directory="/Users/ravivayuvegula/Projects/content",
        database_directory="/Users/ravivayuvegula/Projects/Articles_database"
    )

    # Initialize the FeedbackDatabase
    feedback_db = FeedbackDatabase()

    # Load an Article object from a JSON file located in the content directory
    filepath = "/Users/ravivayuvegula/Projects/content/article_2.json"
    article_from_json = Article.from_json_file(filepath)
    print(f"Content of article to be analyzed:\n{article_from_json.content}")

    # Initialize the ArticleAnalyzer object with the version you want to use
    prompt_version = "1"
    analyzer = ArticleAnalyzer(prompt_version)

    # Analyze the article and get the JSON string response
    analysis_response = analyzer.analyze(article_from_json, style="munger", model=MungerAnalysisOutput)
    print(f"Analysis response: {analysis_response}")

    # Initialize quality_rating to None
    quality_rating = None

    try:
        # Use the QualityEvaluator to rate the analysis
        quality_rating = analyzer.evaluator.evaluate(analysis_response)
    except Exception as e:
        print(f"An error occurred while evaluating the analysis: {e}")

    # Manual override if you wish
    manual_override = input("Would you like to manually rate the quality? (y/n): ")
    if manual_override.lower() == 'y':
        quality_rating = input("Rate the quality of the analysis (1 to 5): ")

    # Collect additional feedback
    additional_feedback = input("Any additional feedback on the analysis?: ")

    # Initialize the FeedbackDatabase object
    feedback_db = FeedbackDatabase()

    # Save the feedback to the database
    feedback_db.save_feedback(article_from_json.id, prompt_version, MungerAnalysisOutput.__name__, quality_rating, additional_feedback, style="munger")

    # Log the analysis details
    analyzer.logger.log(prompt_version, quality_rating, article_from_json.id, MungerAnalysisOutput.__name__)

    # Convert the JSON string response into a dictionary and update the article object's analysis_results attribute
    if analysis_response:
        try:
            article_from_json.analysis_results = json.loads(analysis_response)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        else:
            # Store the analyzed article in the database
            db.store_analyzed_article(article_from_json)
            # Print the analysis results
            print("Analysis Results:")
            print(article_from_json.analysis_results)
    else:
        print("Warning: analysis_response is empty or None.")


    # Read and display the logger's output
    logs = read_logger_output()
    print("Logger Output:")
    print(logs)



    # Read and display feedback
    feedback_logs = feedback_db.read_feedback()
    print("Feedback Logs:")
    print(feedback_logs)