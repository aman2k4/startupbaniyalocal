import os
import google.generativeai as genai
from dotenv import load_dotenv
import typing_extensions as typing

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the response schema
class TransactionAnalysis(typing.TypedDict):
    category: str
    description: str
    is_recurring: bool

# Create the model
model = genai.GenerativeModel("gemini-1.5-flash-8b")

# Define the system prompt
system_prompt = """You are somebody who's good at analyzing credit card statements. I give you each line of the credit card statement and you tell me what type of payment it is, what is the description behind it, and if it is recurring or not.
There are 10 categories: Restaurant, Online Shopping,Travel, Entertainment,SAAS(Software as a Service), Other.
here are some examples:
BONGO.BE - ONLINE SHOPPING
APPLE.COM/BILL ITUNES.COM - SAAS
AMAZON.COM - ONLINE SHOPPING
MCDONALDS - RESTAURANT
NETFLIX.COM - ENTERTAINMENT
SANEF AUTOROUTE SENLIS - Travel
Badibeiz Meilen Meilen - Travel
JET-Tankstelle Loerrach - Travel
Google Payment - SAAS
HTTPSFOURTHWA - Online Shopping
GoDaddy.com, Inc. - SAAS
FLUTTERFLOW - SAAS
Google CLOUD - SAAS
CLOUDFLARE - SAAS
FLUTTERFLOW - SAAS
GODADDY - SAAS
MOBBIN.COM SINGAPORE - SAAS
PERPLEXITY - SAAS

You will give me the answer in this format:
{"type": "XXX", "description": "XXX", "is_recurring": Bool}
"""

# Function to analyze a transaction
def analyze_transaction(transaction_data: str) -> TransactionAnalysis:
    result = model.generate_content(
        [system_prompt, transaction_data],
        generation_config=genai.GenerationConfig(
            temperature=0,
            max_output_tokens=1000,
            response_mime_type="application/json",
            response_schema=TransactionAnalysis
        ),
    )
    return result.text


if __name__ == "__main__":
    # Example usage
    transaction = """
    {
    "transaction_date": "21/06/2024",
    "processing_date": "22/06/2024",
    "description": "CURSOR, AI POWERED IDE HTTPS CURSOR.S",
    "town": "",
    "foreign_amount": 20,
    "foreign_currency": "USD",
    "exchange_rate": 0.956,
    "amount_eur": -19.12,
    "statement_date": "20/07/2024"
    }
    """

    analysis = analyze_transaction(transaction)
    print(analysis)


