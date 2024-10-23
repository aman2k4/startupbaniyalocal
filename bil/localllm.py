from openai import OpenAI
import json
from creditcard_models import Response
import PyPDF2


def extract_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
    return text


def parse_credit_card_statement(
    pdf_path: str,
    model_name: str = "model-identifier",
    max_tokens: int = 5000,
    temperature: float = 0,
) -> dict:

    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

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
    
    result = parse_credit_card_statement(pdf_path, model_name="")
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        # save results in json file with same name as pdf file
        with open(f"{pdf_path.split('.')[0]}.json", "w") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
    else:
        print("Failed to parse the credit card statement.")
