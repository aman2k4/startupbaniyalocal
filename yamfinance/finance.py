import pandas as pd
import os
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
    Adds new columns 'Category', 'AI Description', and 'Is Recurring' to the DataFrame with analysis from the LLM.
    Only processes rows that haven't been analyzed yet.
    """
    # Check if the columns already exist, if not, create them
    if 'Category' not in df.columns:
        df['Category'] = ''
    if 'AI Description' not in df.columns:
        df['AI Description'] = ''
    if 'Is Recurring' not in df.columns:
        df['Is Recurring'] = ''

    for index, row in df.iterrows():
        # Check if the row has already been processed
        if row['Category'] == '' or row['AI Description'] == '' or row['Is Recurring'] == '':
            analysis = call_llm_for_tagging(row, index)
            df.at[index, 'Category'] = analysis['category']
            df.at[index, 'AI Description'] = analysis['description']
            df.at[index, 'Is Recurring'] = analysis['is_recurring']
        else:
            print(f"Skipping already processed transaction {index + 1}")

    return df

# Main function to process the file and add tags
def process_cashbook(filepath, output_filepath):
    """
    Reads the cashbook file or the existing augmented file, adds tags to unprocessed rows, and saves the augmented file.
    """
    # Check if the augmented file already exists
    if os.path.exists(output_filepath):
        print(f"Reading existing augmented file: {output_filepath}")
        df = pd.read_csv(output_filepath, sep=';')
    else:
        print(f"Reading original file: {filepath}")
        df = read_cashbook(filepath)
    
    # Ensure new columns exist and are initialized properly
    for col in ['Category', 'AI Description', 'Is Recurring']:
        if col not in df.columns:
            df[col] = ''
    
    print(f"Read {len(df)} transactions")
    input("Press Enter to start processing...")
    
    # Augment with tags
    df_augmented = augment_cashbook_with_tags(df)
    
    # Save the augmented file
    df_augmented.to_csv(output_filepath, index=False, sep=';')
    print(f"\nAugmented file saved to {output_filepath}")

# Example usage:
if __name__ == "__main__":
    process_cashbook("small.csv", "augmented_cashbook.csv")
