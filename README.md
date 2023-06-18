# Flask Python Chatbot

This repository contains a simple Flask chatbot that uses AIML and Neo4j for natural language processing and database operations respectively. The chatbot is designed to provide responses to user queries, perform database operations like user authentication and social network creation, and also has web scraping capabilities.

## Installation

To run the chatbot, follow these steps:

1. Clone the repository:

```bash
git clone <repository_url>
```

2. Install the required dependencies:

```bash
pip install flask neo4j nltk pyaiml21 pyswip openai google
```

3. Download the NLTK packages:

```python
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
```

4. Set up a Neo4j database:

   - Install Neo4j locally.
   - Start the Neo4j server.
   - Create a database with the name "chatbot" and set the username and password as "neo4j".

5. Set up the OpenAI API:

   - Create an account on OpenAI (https://openai.com).
   - Obtain an API key.
   - Replace `openai.api_key` with your API key in the `get_completion` function.

6. Run the Flask application:

python bot.py

7. Access the chatbot at `http://localhost:8888` in your web browser.

## Files

The repository contains the following files:

- `bot.py`: The main Flask application file that handles the chatbot functionality.
- `relationships.pl`: Prolog file used for storing relationships between users.
- `AIML_FILES/*.aiml`: AIML files used for defining chatbot responses and actions.
- `templates/`: Directory containing HTML templates for the web interface.

## Functionality

The Flask chatbot provides the following features:

- User authentication: Users can sign up and log in to the chatbot.
- User session management: The chatbot tracks user sessions using Flask's `session` object.
- Natural language processing: The chatbot uses NLTK for natural language processing, including named entity recognition and part-of-speech tagging.
- AIML-based responses: The chatbot uses AIML (Artificial Intelligence Markup Language) for generating responses to user queries.
- Neo4j database operations: The chatbot performs database operations using the Neo4j Python driver, including user authentication and social network creation.
- Web scraping: The chatbot can perform web searches using the Google Search API and open web pages using the `webbrowser` module.

## Usage

- To interact with the chatbot, open your web browser and access `http://localhost:8888`.
- Sign up for an account or log in if you already have one.
- Enter your queries in the chatbot interface and see the responses.
- The chatbot can provide information, perform calculations, search the web, and more.

## Notes

- The chatbot uses the Neo4j database to store user information and relationships. Make sure you have Neo4j installed and running locally before using the chatbot.
- The AIML files in the `AIML_FILES` directory define the chatbot's responses. You can modify these files to customize the chatbot's behavior.
- The OpenAI API key is required to use the `get_completion` function. Replace `openai.api_key` with your API key to enable the completion functionality.
- The NLTK packages are used for natural language processing tasks. Make sure to download the required packages using `nltk.download` as mentioned in the installation steps.

Feel free to explore and modify the code to meet your requirements!
