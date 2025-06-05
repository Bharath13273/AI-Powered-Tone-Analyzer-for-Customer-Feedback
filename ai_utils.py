from google import genai
import time
from google.genai.errors import ServerError

client = genai.Client(api_key="you api")

def retry_on_server_error(func):
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except ServerError as e:
                if hasattr(e, "code") and e.code == 503 and attempt < retries - 1:
                    time.sleep(delay * (2 ** attempt))
                    continue
                else:
                    raise
    return wrapper

@retry_on_server_error
def analyze_tone(text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"What is the tone of this user comment: '{text}'? Reply with just the tone like 'angry', 'happy', etc."
    )
    return response.text.strip()

@retry_on_server_error
def generate_response(comment, tone, user, product):
    prompt = (
        f"A customer named {user} gave feedback about {product}.\n"
        f"Tone: {tone}\n"
        f"Comment: {comment}\n"
        f"Generate a polite, helpful response as a customer support agent."
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()

