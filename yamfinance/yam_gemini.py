import os
import google.generativeai as genai
from dotenv import load_dotenv
import typing_extensions as typing
import json

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
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Define the system prompt
system_prompt = """You are a financial transaction analyst specializing in small businesses, specifically in the wellness and yoga studio sector. Your task is to analyze each transaction detail and assign it a category, provide a brief description, and determine if it's a recurring transaction.

The yoga studio has various types of expenses and revenue sources typical to this industry. Use your best judgment to categorize each transaction. Consider the context and patterns based on common yoga studio transactions.

Categories may include (but are not limited to):
- **Revenue**: Membership Fees, Workshop Fees, Merchandise Sales, Donation, Grants. Payments are coming ffrom Stripe, Arcelor Mittal, Payconiq, sometime bank transfers
- **Teacher Payroll**: Teacher Salaries, Staff Payments, Contractor Fees
- **Cooperation Fees**: When we have a special host for a workshop, we pay them a percentage of the revenue. For example, "ALEP" "Workshop" etc
- **Admin Payroll**: Payroll for non-teaching staff
- **Admin Projects**: For example, "Yoga Teacher Training" from "jivamukti global", "systemisches coaching
- **Rent Regular Classes**: Everything sent to "Frank Gutenkauf" 
- **Rent Retreats**: Everything sent to "Beno Bois"
- **Design & Print**: For example, consulting fees for design work, printing costs. MOstly payments are to "Gilles Scaccia" or "Saif Alam Khan" , "Kousca design" etc.
- **Photo Video Shoot**: For example, payments to "Hengen Emile" and "Daniel Oliveiro Carneiro"
- **Marketing**: Social Media Ads, Print Materials, Sponsorships. For example, "Facebook Ads", "Google Ads", "Meta Ads", "LinkedIn Ads"
- **Software & Tools**: Booking Software, Communication Tools, Accounting Software, Website Hosting. For example, "Zoom", "Fitogram", "Mailchimp", "Google Workspace", "EuroDNS","Webflow"
- **Supplies & Materials**: Yoga Mats, Cleaning Supplies, Workshop Materials, Office Supplies. For example, payments to "Amazon" , "Batiself", "Books"
- **Insurance**: Liability Insurance, Health Insurance for Staff. Payments are going to "La Luxembourgeoise Assurances S.A."
- **Event Expenses**: Retreat Costs, Special Event Rentals, Catering for Events
- **Legal Fees**: For example, "Frais de notaire", "LBR", "RCS" etc
- **Professional Services**: Legal Fees, Accounting Services, Consulting Fees
- **Travel & Transportation**: Teacher Travel Reimbursement, Transportation for Events
- **Food & Beverages**: When team lunches, dinners, etc. Payments are mostly done to "Sally Gruneisen" ,comments have keywords like "meeting with", "restaurant", "travail de cuisiniere"
- **Yoga & Brunch**: Payments to "Estratto SARL", "Brunch", "Lacroix Celine"
- **Bank & Transaction Fees**: Payment Processor Fees, Bank Fees. For example, "ARRETE DE COMPTE" , "Fourniture carte"
- **Reimbursements**: When we reimburse someone for cancelled classes. For example transactions with comments like "reimbursment workshop cancelled"
- **Miscellaneous**: Any transaction that doesn’t fit into the categories above
- **Donations**: Having keyword "donation" in the description

For each transaction, provide a structured response with:
- **Category**: The main category the transaction falls under (e.g., 'Revenue', 'Rent & Utilities', etc.)
- **Description**: A brief summary explaining the transaction based on details like invoice numbers, communication notes, and description fields.
- **Is Recurring**: A boolean indicating whether this is likely a recurring transaction (e.g., monthly rent, regular teacher payments).
- **Transaction Type**: Specify if the transaction is an **inflow** (money coming in) or **outflow** (money going out).

### Expected output format
Provide your response as a JSON object:
{
    "category": "XXX",
    "description": "XXX",
    "is_recurring": bool,
    "transaction_type": "inflow" or "outflow"
}

### Example input and output
**Input**: "Description: Monthly payment to GALASSI ZOE, Communication: YaM December, Invoice 2023-013"
**Output**: 
{
    "category": "Teacher Payroll",
    "description": "Monthly payment to a yoga teacher",
    "is_recurring": true,
    "transaction_type": "outflow"
}

Use all available information from the transaction to make accurate categorizations, and feel free to infer the purpose when information is ambiguous based on common patterns in yoga studios.
"""

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
            max_output_tokens=100,
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
