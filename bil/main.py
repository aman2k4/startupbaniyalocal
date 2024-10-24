import os
import json
import csv
from localllm import parse_credit_card_statement

def process_credit_card_statements():
    # Create directories if they don't exist
    os.makedirs("json", exist_ok=True)
    os.makedirs("csv", exist_ok=True)

    # Process all PDF files in the statements folder
    pdf_files = [f for f in os.listdir("statements") if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join("statements", pdf_file)
        json_filename = f"{os.path.splitext(pdf_file)[0]}.json"
        json_path = os.path.join("json", json_filename)
        
        # Check if JSON file already exists
        if os.path.exists(json_path):
            print(f"JSON file already exists for {pdf_file}. Skipping processing.")
        else:
            result = parse_credit_card_statement(pdf_path, model_name="")
            
            if result:
                # Save individual JSON file
                with open(json_path, "w") as json_file:
                    json.dump(result, json_file, ensure_ascii=False, indent=2)
            else:
                print(f"Failed to parse {pdf_file}")

    print("Processing of individual statements complete.")

def combine_json_files():
    json_folder = "json"
    all_transactions = []
    combined_card_statement = {}

    for json_file in os.listdir(json_folder):
        if json_file.endswith(".json") and json_file != "combined_statements.json":
            json_path = os.path.join(json_folder, json_file)
            with open(json_path, "r") as file:
                data = json.load(file)
                
                card_statement = data.get("card_statement", {})
                
                # Update combined_card_statement with non-transaction data
                for key, value in card_statement.items():
                    if key != "transactions":
                        combined_card_statement[key] = value
                
                # Add transactions to all_transactions list
                for transaction in card_statement.get("transactions", []):
                    transaction["statement_date"] = card_statement.get("statement_date")
                    all_transactions.append(transaction)

    # Add all transactions to the combined card statement
    combined_card_statement["transactions"] = all_transactions
    
    # Calculate total amount
    combined_card_statement["total_amount"] = sum(t["amount_eur"] for t in all_transactions)

    # Wrap the combined card statement in the expected structure
    combined_data = {"card_statement": combined_card_statement}

    # Save combined JSON data
    combined_json_path = os.path.join(json_folder, "combined_statements.json")
    with open(combined_json_path, "w") as combined_json_file:
        json.dump(combined_data, combined_json_file, ensure_ascii=False, indent=2)

    print(f"Combined JSON saved to {combined_json_path}")
    return combined_data

def create_csv_from_json(data, csv_path):
    if not data or not data.get("transactions"):
        print("No data to write to CSV")
        return

    # Flatten the nested structure
    flattened_data = data["transactions"]

    # Write to CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = flattened_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in flattened_data:
            writer.writerow(row)

if __name__ == "__main__":
    process_credit_card_statements()
    combined_data = combine_json_files()
    csv_path = os.path.join("csv", "combined_statements.csv")
    create_csv_from_json(combined_data, csv_path)
    print(f"CSV file saved to {csv_path}")
