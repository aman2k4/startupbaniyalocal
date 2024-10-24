from openai import OpenAI
import json
from creditcard_models import Response
import PyPDF2
from pdfminer.high_level import extract_text
import fitz  # PyMuPDF
import pdfplumber
import os
from dotenv import load_dotenv

# Add this at the beginning of your file, after the imports
load_dotenv()





def extract_pdf_text_pypdf2(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
    return text

def extract_pdf_text_pdfminer(pdf_path):
    return extract_text(pdf_path)

def extract_pdf_text_pymupdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n\n"
    return text

def extract_pdf_text_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"
    return text

def extract_pdf_text(pdf_path):
    pypdf2_text = extract_pdf_text_pypdf2(pdf_path)
    pdfminer_text = extract_pdf_text_pdfminer(pdf_path)
    pymupdf_text = extract_pdf_text_pymupdf(pdf_path)
    pdfplumber_text = extract_pdf_text_pdfplumber(pdf_path)
    
    # Save texts to separate files
    with open(f"{pdf_path.split('.')[0]}_pypdf2.txt", "w") as file:
        file.write(pypdf2_text)
    with open(f"{pdf_path.split('.')[0]}_pdfminer.txt", "w") as file:
        file.write(pdfminer_text)
    with open(f"{pdf_path.split('.')[0]}_pymupdf.txt", "w") as file:
        file.write(pymupdf_text)
    with open(f"{pdf_path.split('.')[0]}_pdfplumber.txt", "w") as file:
        file.write(pdfplumber_text)
    
    # Hardcode the method selection here
    # Change this line to switch between methods
    selected_method = "pypdf2"  # or "pypdf2" or "pdfminer" or "pymupdf"
    
    if selected_method == "pdfminer":
        return pdfminer_text
    elif selected_method == "pymupdf":
        return pymupdf_text
    elif selected_method == "pdfplumber":
        return pdfplumber_text
    else:
        return pypdf2_text



def parse_credit_card_statement(
    pdf_path: str,
    model_name: str = "gpt-4o-2024-08-06",
    max_tokens: int = 5000,
    temperature: float = 0,
) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables or .env file.")
        return None

    client = OpenAI(api_key=api_key)

    # Extract text from PDF
    pdf_text = extract_pdf_text(pdf_path)

    # System message
    system_message = """
    You are an AI assistant trained to extract information from credit card statements.
    Your task is to analyze the given credit card statement text and extract key details into a structured format.
    Provide the output as a JSON object that matches the structure of the CardStatement model.
    """

    # User message with PDF text
    user_message = f"""
    Please analyze the following credit card statement text and extract the relevant information.
    Provide the extracted information in a structured JSON format that matches the CardStatement model.
    Include all available details such as account information, card details, transactions, and totals.

    Dates are in the format DD/MM/YYYY. For example, 15/10/2024. The year is always 4 digits either 2024 or 2023.

    Statement text:
    {pdf_text}
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    try:
        completion = client.beta.chat.completions.parse(
            model=model_name,
            messages=messages,
            response_format=Response,
            max_tokens=max_tokens,
            temperature=temperature
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    structured_data = completion.choices[0].message
    if structured_data.refusal:
        print(f"The model refused to respond. Please try again.")
        return {"error": structured_data.refusal}
    else:
        data = json.loads(structured_data.content)
        return data


if __name__ == "__main__":
    pdf_path = "statements/Unknown-5.pdf"
    
    result = parse_credit_card_statement(pdf_path, model_name="gpt-4o-mini")
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        # save results in json file with same name as pdf file
        with open(f"{pdf_path.split('.')[0]}_openai.json", "w") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
    else:
        print("Failed to parse the credit card statement.")
