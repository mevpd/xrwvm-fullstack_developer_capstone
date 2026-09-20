import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    try:
        response = requests.get(request_url, **kwargs)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        logger.error(f"GET {request_url} failed: {e}")
    return None


def analyze_review_sentiments(text):
    request_url = (
        sentiment_analyzer_url + "analyze/" + text.replace(" ", "%20"))
    try:
        response = requests.get(request_url)
        if response.status_code == 200:
            # return response.json().get('sentiment', 'neutral')
            return response.json()
    except requests.RequestException as e:
        logger.error(f"Sentiment analysis failed: {e}")
    return "neutral"


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.RequestException:
        print("Network exception occurred")
