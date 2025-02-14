from slack_bolt import App
import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize your Bolt for Python app with the correct env variable names
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),          # Ensure this variable is set in your .env file
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")  # Ensure this variable is set in your .env file
)

@app.message("!ask")
def handle_mycommand(message, say):
    """
    Triggered when someone posts a message that matches the pattern "!ask".
    """
    user_text = message["text"]
    URL = os.getenv('URL')  # same url deployed in kubernetes

    try:
        payload = {"message": user_text}
        response = requests.post(
            URL,
            json=payload  
        )
        response.raise_for_status()  # Raise an exception if the request failed

        data = response.json()
        result_text = data.get('response', "No result key found in API response")
        say({result_text})
    except requests.exceptions.RequestException as e:
        print(f"API call error: {e}")
        say("Oops, there was an error calling the external API!")
    except Exception as e:
        print(f"Unexpected error: {e}")
        say("An unexpected error occurred!")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
