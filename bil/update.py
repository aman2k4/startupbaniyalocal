import json
from gemini_api import analyze_transaction

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def update_transactions(file_path, limit=500):
    data = load_json_file(file_path)
    transactions = data['card_statement']['transactions']
    
    processed_count = 0
    for transaction in transactions:
        # Skip if transaction is already analyzed
        if all(key in transaction for key in ['category', 'analysis_description', 'is_recurring']):
            continue

        transaction_str = json.dumps(transaction, indent=2)
        print("transaction: ", transaction_str)
        analysis = analyze_transaction(transaction_str)
        print("analysis: ", analysis)

        # ask user to press enter to continue
        input("Press Enter to accept")
        
        # Parse the analysis result
        analysis_dict = json.loads(analysis)
        
        # Add the analysis to the transaction
        transaction['category'] = analysis_dict['category']
        transaction['analysis_description'] = analysis_dict['description']
        transaction['is_recurring'] = analysis_dict['is_recurring']
        
        processed_count += 1
        print(f"Processed transaction {processed_count}/{limit}")

        # Save the updated data after each transaction
        save_json_file(data, file_path)
        print(f"Updated data saved to {file_path}")

        

        if processed_count >= limit:
            break

    return data

def main():
    file_path = 'json_old/combined_statements.json'
    
    # Update the transactions (limited to 5 for testing)
    update_transactions(file_path, limit=500)

if __name__ == "__main__":
    main()
