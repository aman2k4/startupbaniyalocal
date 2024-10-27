import pandas as pd
import os
from yam_gemini import analyze_transaction, analyze_transactions_batch

# Function to read the cashbook file
def read_cashbook(filepath):
    """
    Reads the cashbook file into a DataFrame.
    """
    df = pd.read_csv(filepath, sep=';')
    return df

# Function to call LLM for tagging in batches
def call_llm_for_batch_tagging(batch_input, start_index):
    """
    Calls the LLM with relevant columns to identify tags for a batch of payments.
    """
    print(f"\nAnalyzing batch of {len(batch_input)} transactions starting from index {start_index}:")
    for i, data in enumerate(batch_input):
        print(f"\nTransaction {start_index + i + 1}:")
        print(f"Description: {data['Description']}")
        print(f"Amount: {data['Montant en EUR']}")
        print(f"Beneficiary: {data['Nom de la contrepartie']}")
    
    input("Press Enter to continue...")
    
    # Call the LLM and get analysis for the batch
    batch_analysis = analyze_transactions_batch(batch_input)
    
    print("\nBatch analysis complete.")
    input("Press Enter to continue to the next batch...")
    
    return batch_analysis

# Function to augment the DataFrame with tags from LLM in batches
def augment_cashbook_with_tags(df, output_filepath, batch_size=20):
    """
    Adds new columns 'Category', 'AI Description', 'Is Recurring', and 'Transaction Type' to the DataFrame with analysis from the LLM.
    Processes rows in batches, including rows that were previously processed but removed from the augmented file.
    Saves the progress after each batch.
    """
    # Check if the columns already exist, if not, create them
    for col in ['Category', 'AI Description', 'Is Recurring', 'Transaction Type']:
        if col not in df.columns:
            df[col] = ''

    # Create a unique identifier for each transaction
    df['unique_id'] = df.apply(lambda row: f"{row['Date transaction']}_{row['Description']}_{row['Montant en EUR']}", axis=1)

    # Process in batches
    for start_index in range(0, len(df), batch_size):
        end_index = min(start_index + batch_size, len(df))
        batch = df.iloc[start_index:end_index].copy()
        
        # Identify rows that need processing (either empty or previously processed but removed)
        mask_to_process = (
            (batch[['Category', 'AI Description', 'Is Recurring', 'Transaction Type']] == '').any(axis=1) |
            (~batch['unique_id'].isin(df[df['Category'] != '']['unique_id']))
        )
        rows_to_process = batch[mask_to_process]
        
        if not rows_to_process.empty:
            print(f"\nProcessing {len(rows_to_process)} out of {len(batch)} rows in batch starting at index {start_index}")
            batch_input = rows_to_process.apply(lambda row: {
                "Description": row['Description'],
                "Montant en EUR": row['Montant en EUR'],
                "Communication 1": row['Communication 1'],
                "Communication 2": row['Communication 2'],
                "Communication 3": row['Communication 3'],
                "Communication 4": row['Communication 4'],
                "Nom de la contrepartie": row['Nom de la contrepartie']
            }, axis=1).tolist()
            
            batch_analysis = call_llm_for_batch_tagging(batch_input, start_index)
            
            for i, analysis in enumerate(batch_analysis):
                index = rows_to_process.index[i]
                df.at[index, 'Category'] = analysis['category']
                df.at[index, 'AI Description'] = analysis['description']
                df.at[index, 'Is Recurring'] = analysis['is_recurring']
                df.at[index, 'Transaction Type'] = analysis['transaction_type']
            
            # Save progress after each batch
            df.to_csv(output_filepath, index=False, sep=';')
            print(f"\nProgress saved. Augmented file updated at {output_filepath}")
        else:
            print(f"Skipping already processed batch starting at index {start_index}")

    # Remove the temporary unique_id column
    df.drop('unique_id', axis=1, inplace=True)
    return df

# Main function to process the file and add tags
def process_cashbook(filepath, output_filepath):
    """
    Reads the cashbook file or the existing augmented file, adds tags to unprocessed rows, and saves the augmented file after each batch.
    """
    # Always read the original file
    print(f"Reading original file: {filepath}")
    df_original = read_cashbook(filepath)
    
    # Ensure 'Montant en EUR' is treated as a string in the original dataframe
    df_original['Montant en EUR'] = df_original['Montant en EUR'].astype(str)
    
    # Check if the augmented file exists and read it if it does
    if os.path.exists(output_filepath):
        print(f"Reading existing augmented file: {output_filepath}")
        df_augmented = pd.read_csv(output_filepath, sep=';')
        
        # Ensure 'Montant en EUR' is treated as a string in the augmented dataframe
        df_augmented['Montant en EUR'] = df_augmented['Montant en EUR'].astype(str)
        
        # Merge the original and augmented dataframes
        df = pd.merge(df_original, df_augmented[['Date transaction', 'Description', 'Montant en EUR', 'Category', 'AI Description', 'Is Recurring', 'Transaction Type']], 
                      on=['Date transaction', 'Description', 'Montant en EUR'], 
                      how='left')
    else:
        df = df_original
    
    # Ensure new columns exist and are initialized properly
    for col in ['Category', 'AI Description', 'Is Recurring', 'Transaction Type']:
        if col not in df.columns:
            df[col] = ''
    
    print(f"Read {len(df)} transactions")
    input("Press Enter to start processing...")
    
    # Augment with tags and save after each batch
    df_augmented = augment_cashbook_with_tags(df, output_filepath)
    
    print(f"\nProcessing complete. Final augmented file saved to {output_filepath}")

# Example usage:
if __name__ == "__main__":
    process_cashbook("small.csv", "augmented_cashbook.csv")
