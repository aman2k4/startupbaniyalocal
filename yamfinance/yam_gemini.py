import os
import google.generativeai as genai
from dotenv import load_dotenv
import typing_extensions as typing
import json
from systemprompt import system_prompt
# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the response schema
class TransactionAnalysis(typing.TypedDict):
    category: str
    description: str
    is_recurring: bool
    transaction_type: str

# Create the model
model = genai.GenerativeModel("gemini-1.5-flash-8b")


# Function to analyze a transaction
def analyze_transaction(transaction_data: dict) -> TransactionAnalysis:
    # Prepare input data for the model
    input_data = f"""
    Description: {transaction_data['Description']}
    Amount: {transaction_data['Montant en EUR']}
    Communication 1: {transaction_data['Communication 1']}
    Communication 2: {transaction_data['Communication 2']}
    Communication 3: {transaction_data['Communication 3']}
    Communication 4: {transaction_data['Communication 4']}
    Beneficiary: {transaction_data['Nom de la contrepartie']}
    """

    result = model.generate_content(
        [system_prompt, input_data],
        generation_config=genai.GenerationConfig(
            temperature=0,
            max_output_tokens=5000,
            response_mime_type="application/json",
        ),
    )
    
    # Parse the JSON response
    analysis = json.loads(result.text)
    return analysis

# Function to analyze a batch of transactions
def analyze_transactions_batch(transactions_data: list[dict]) -> list[TransactionAnalysis]:
    # Prepare input data for the model
    input_data = "Analyze the following batch of transactions:\n\n"
    for i, transaction in enumerate(transactions_data, 1):
        input_data += f"""
Transaction {i}:
Description: {transaction['Description']}
Amount: {transaction['Montant en EUR']}
Communication 1: {transaction['Communication 1']}
Communication 2: {transaction['Communication 2']}
Communication 3: {transaction['Communication 3']}
Communication 4: {transaction['Communication 4']}
Beneficiary: {transaction['Nom de la contrepartie']}

"""

    result = model.generate_content(
        [system_prompt, input_data],
        generation_config=genai.GenerationConfig(
            temperature=0,
            max_output_tokens=8192,
            response_mime_type="application/json",
        ),
    )
    
    # Parse the JSON response
    analysis = json.loads(result.text)
    return analysis

if __name__ == "__main__":
    # Example usage
    transaction = {
        "Description": "GALASSI ZOE",
        "Montant en EUR": "-345",
        "Communication 1": "YAM December",
        "Communication 2": "Facture 2023-013",
        "Communication 3": "30.12.2023",
        "Communication 4": "",
        "Nom de la contrepartie": "GALASSI ZOE"
    }

    analysis = analyze_transaction(transaction)
    print(analysis)

    # Example usage for batch processing
    transactions = [
        {
            "Description": "GALASSI ZOE",
            "Montant en EUR": "-345",
            "Communication 1": "YAM December",
            "Communication 2": "Facture 2023-013",
            "Communication 3": "30.12.2023",
            "Communication 4": "",
            "Nom de la contrepartie": "GALASSI ZOE"
        },
        {
            "Description": "STRIPE",
            "Montant en EUR": "1200",
            "Communication 1": "Membership fees",
            "Communication 2": "",
            "Communication 3": "",
            "Communication 4": "",
            "Nom de la contrepartie": "STRIPE PAYMENTS EUROPE LIMITED"
        }
    ]

    batch_analysis = analyze_transactions_batch(transactions)
    print(json.dumps(batch_analysis, indent=2))
