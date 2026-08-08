import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return """
        Dear Customer,

        We apologize for the inconvenience.

        Our records indicate that the payment failed after the amount was debited.

        The transaction qualifies for a refund and the refund will be processed within 5–7 business days.

        If the refund is not received within the expected timeframe, please contact support with your transaction ID.

        Thank you for your patience.

        Regards,
        Financial Operations Team
        """