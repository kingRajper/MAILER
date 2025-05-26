MAILER Agent – Email Classification Assistant

Overview:
- The MAILER Agent is an intelligent assistant that processes emails by classifying them as spam or legitimate.
- For legitimate emails, it detects the intent (e.g., inquiry, complaint, request) and generates a professional draft reply.
- Emails and their processing results are stored in a local log file for later reference.
- A Streamlit-based GUI is provided to interact with the system.

Features:
- Classifies emails as spam or legitimate using an LLM.
- Identifies intent of legitimate emails (inquiry, complaint, etc.).
- Generates draft replies for legitimate emails.
- Explains the reason for spam classification.
- Stores all email interactions in a local JSON log.
- Streamlit GUI for inputting emails, viewing logs, and uploading test emails.
- Export option to download email logs.

Project Structure:
- app.py: Streamlit application entry point.
- core/
  - email_agent.py: Contains logic for classification and draft generation.
  - state.py: Defines the EmailState dataclass.
- logs/
  - email_log.json: JSON file to store logged email interactions.
- assets/
  - test_emails.json: Sample emails for testing.
- requirements.txt: Python dependencies.

Usage:
1. Clone the repository.
2. Install required packages using `pip install -r requirements.txt`.
3. Add your OpenAI API key in a `.env` file:
   - OPENAI_API_KEY=your-openai-api-key
4. Run the Streamlit app:
   - streamlit run app.py

Log Format (email_log.json):
Each log entry contains:
- uuid: Unique identifier for the email
- timestamp: Time of processing
- sender: Email sender address
- subject: Subject of the email
- body: Body content of the email
- is_spam: Boolean indicating spam classification
- spam_reason: Explanation if marked as spam
- category: Category for legitimate emails (e.g., inquiry)
- response_draft: Suggested reply for legitimate emails

Test Emails:
- Sample emails are available in `assets/test_emails.json`.
- These can be used in the GUI under the "Upload Email" tab.

Requirements:
- Python 3.9+
- Streamlit
- Langchain / LangGraph
- OpenAI
- uuid
- dotenv

Contact:
- Developer: <b> *Iqrar Ali* </b>
- Description: This system was developed to automate intelligent email response handling using LLMs.
