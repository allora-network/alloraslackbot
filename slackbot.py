from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os
import requests
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables from the .env file
load_dotenv()

# Initialize Bolt for Python app with the correct env variables
bolt_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),  # Ensure this variable is set in your .env file
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")  # Ensure this variable is set in your .env file
)

# Define a message listener for "!ask"
@bolt_app.message("!ask")
def handle_mycommand(message, say):
    """
    Triggered when someone posts a message that matches the pattern "!ask".
    """
    user_text = message["text"]
    URL = os.getenv('URL')  # Same URL deployed in Kubernetes (RAG)

    try:
        payload = {"message": user_text}
        response = requests.post(URL, json=payload)
        response.raise_for_status()  # Raise an exception if the request failed

        data = response.json()
        result_text = data.get('response', "No result key found in API response")
        say(result_text)
    except requests.exceptions.RequestException as e:
        print(f"API call error: {e}")
        say("Oops, there was an error calling the external API!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        say("An unexpected error occurred!")

# Flask web server
flask_app = Flask(__name__)
# a SlackRequestHandler for the Bolt app
handler = SlackRequestHandler(bolt_app)

# Endpoint for Slack events
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# Health check endpoint
@flask_app.route("/", methods=["GET"])
def health_check():
    return "ok", 200

if __name__ == "__main__":
    # Run the Flask app on the specified port (default to 3000 if not set)
    flask_app.run(port=int(os.environ.get("PORT", 3000)))
