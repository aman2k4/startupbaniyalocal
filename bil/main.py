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
    all_data = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join("statements", pdf_file)
        result = parse_credit_card_statement(pdf_path, model_name="")
        
        if result:
            # Save individual JSON file
            json_filename = f"{os.path.splitext(pdf_file)[0]}.json"
            json_path = os.path.join("json", json_filename)
            with open(json_path, "w") as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=2)
            
            all_data.append(result)
        else:
            print(f"Failed to parse {pdf_file}")

    # Combine all JSON data
    combined_json_path = os.path.join("json", "combined_statements.json")
    with open(combined_json_path, "w") as combined_json_file:
        json.dump(all_data, combined_json_file, ensure_ascii=False, indent=2)

    # Create CSV from combined JSON data
    csv_path = os.path.join("csv", "combined_statements.csv")
    create_csv_from_json(all_data, csv_path)

    print(f"Processing complete. Combined JSON saved to {combined_json_path}")
    print(f"CSV file saved to {csv_path}")

def create_csv_from_json(data, csv_path):
    if not data:
        print("No data to write to CSV")
        return

    # Flatten the nested structure
    flattened_data = []
    for statement in data:
        for transaction in statement.get("transactions", []):
            flattened_data.append({
                "account_number": statement.get("account_number"),
                "statement_date": statement.get("statement_date"),
                "date": transaction.get("date"),
                "description": transaction.get("description"),
                "amount": transaction.get("amount"),
                "category": transaction.get("category")
            })

    # Write to CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = flattened_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in flattened_data:
            writer.writerow(row)

if __name__ == "__main__":
    process_credit_card_statements()

