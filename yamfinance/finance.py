import pandas as pd
from yam_gemini import analyze_transaction

# Function to read the cashbook file
def read_cashbook(filepath):
    """
    Reads the cashbook file into a DataFrame.
    """
    df = pd.read_csv(filepath, sep=';')
    return df

# Function to call LLM for tagging
def call_llm_for_tagging(row, index):
    """
    Calls the LLM with relevant columns to identify tags for payments.
    """
    # Prepare input data for LLM
    input_data = {
        "Description": row['Description'],
        "Montant en EUR": row['Montant en EUR'],
        "Communication 1": row['Communication 1'],
        "Communication 2": row['Communication 2'],
        "Communication 3": row['Communication 3'],
        "Communication 4": row['Communication 4'],
        "Nom de la contrepartie": row['Nom de la contrepartie']
    }
    
    print(f"\nAnalyzing transaction {index + 1}:")
    print(f"Description: {input_data['Description']}")
    print(f"Amount: {input_data['Montant en EUR']}")
    print(f"Communication 1: {input_data['Communication 1']}")
    print(f"Communication 2: {input_data['Communication 2']}")
    print(f"Communication 3: {input_data['Communication 3']}")
    print(f"Communication 4: {input_data['Communication 4']}")
    print(f"Beneficiary: {input_data['Nom de la contrepartie']}")
    
    input("Press Enter to continue...")
    
    # Call the LLM and get analysis
    analysis = analyze_transaction(input_data)
    
    print("\nAnalysis result:")
    print(f"Category: {analysis['category']}")
    print(f"Description: {analysis['description']}")
    print(f"Is Recurring: {analysis['is_recurring']}")
    print(f"transaction_type: {analysis['transaction_type']}")
    
    input("Press Enter to continue to the next transaction...")
    
    return analysis

# Function to augment the DataFrame with tags from LLM
def augment_cashbook_with_tags(df):
    """
    Adds new columns 'Category', 'Description', and 'Is Recurring' to the DataFrame with analysis from the LLM.
    """
    analyses = []
    for index, row in df.iterrows():
        analysis = call_llm_for_tagging(row, index)
        analyses.append(analysis)
    
    df['Category'] = [a['category'] for a in analyses]
    df['AI Description'] = [a['description'] for a in analyses]
    df['Is Recurring'] = [a['is_recurring'] for a in analyses]
    return df

# Main function to process the file and add tags
def process_cashbook(filepath, output_filepath):
    """
    Reads the cashbook file, adds tags, and saves the augmented file.
    """
    # Step 1: Read the file
    df = read_cashbook(filepath)
    
    print(f"Read {len(df)} transactions from {filepath}")
    input("Press Enter to start processing...")
    
    # Step 2: Augment with tags
    df_augmented = augment_cashbook_with_tags(df)
    
    # Step 3: Save the augmented file
    df_augmented.to_csv(output_filepath, index=False, sep=';')
    print(f"\nAugmented file saved to {output_filepath}")

# Example usage:
if __name__ == "__main__":
    process_cashbook("small.csv", "augmented_cashbook.csv")
