import requests 
from dotenv import load_dotenv
import os
def get_response(user_message: str) -> str:

    load_dotenv()

    URL = os.getenv('URL')

    try:
        payload = {"message": user_message}
        response = requests.post(URL,json = payload) # double check if this a valid API input 
        data = response.json() # check if this is the dictionary that needs to be returned
        answer = data.get('response')
        return answer # return the response from the RAG model
    except Exception as e:
        print(f'{e}there was an error parsing the response')

# make a post request to this url to initiate a conversation with the RAG model with payload of user's query
# intiate a conversation by "!"