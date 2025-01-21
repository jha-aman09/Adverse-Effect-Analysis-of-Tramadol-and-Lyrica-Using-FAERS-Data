import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
from typing import Dict, List

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define quarters
quarters = ["1", "2", "3", "4"]

# Define relevant columns
relevant_demo_columns = ["primaryid", "age", "sex", "wt", "reporter_country", "event_dt", "init_fda_dt"]
relevant_drug_columns = ["primaryid", "drugname", "drug_seq"]
relevant_ther_columns = ["primaryid", "dsg_drug_seq", "start_dt", "end_dt", "dur"]
relevant_react_columns = ["primaryid", "pt"]

# Define drug names
drug_names = ["tramal", "lyrica"]

def read_data_from_file(file_path: str) -> pd.DataFrame:
    """Read data from a local file and return a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path, sep="$", low_memory=False, encoding='latin1')
        logging.info(f"Successfully read file: {file_path}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        logging.error(f"Empty file: {file_path}")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
    return pd.DataFrame()

def process_dataframe(df: pd.DataFrame, rename_dict: Dict[str, str] = None) -> pd.DataFrame:
    """Process a DataFrame: rename columns, convert to lowercase."""
    if df.empty:
        return df
    df.columns = df.columns.str.lower()
    if rename_dict:
        df = df.rename(columns=rename_dict)
    return df

def process_quarter_data(quarter: str) -> tuple:
    """Process data for a single quarter."""
    data_dir = "Data"
    demo_path = os.path.join(data_dir, f"DEMO19Q{quarter}.txt")
    drug_path = os.path.join(data_dir, f"DRUG19Q{quarter}.txt")
    ther_path = os.path.join(data_dir, f"THER19Q{quarter}.txt")
    react_path = os.path.join(data_dir, f"REAC19Q{quarter}.txt")

    demo = process_dataframe(read_data_from_file(demo_path), {'gndr_cod': 'sex', 'isr': 'primaryid'})
    drug = process_dataframe(read_data_from_file(drug_path), {'isr': 'primaryid'})
    ther = process_dataframe(read_data_from_file(ther_path), {'isr': 'primaryid', 'drug_seq': 'dsg_drug_seq'})
    react = process_dataframe(read_data_from_file(react_path), {'isr': 'primaryid'})

    if demo.empty or drug.empty or ther.empty or react.empty:
        logging.error(f"One or more required files are empty or couldn't be read for Q{quarter}. Skipping.")
        return None, None, None, None

    demo = demo[relevant_demo_columns]
    drug = drug[relevant_drug_columns]
    ther = ther[relevant_ther_columns]
    react = react[relevant_react_columns]

    drug['drugname'] = drug['drugname'].str.lower()
    drug = drug[drug['drugname'].isin(drug_names)]

    return demo, drug, ther, react

def main():
    all_demo = []
    all_drug = []
    all_ther = []
    all_react = []

    for quarter in quarters:
        logging.info(f"Processing data for Q{quarter} 2019")
        demo, drug, ther, react = process_quarter_data(quarter)
        if demo is not None:
            all_demo.append(demo)
            all_drug.append(drug)
            all_ther.append(ther)
            all_react.append(react)

    if not all_demo:
        logging.error("No data could be processed. Exiting.")
        return

    demo_df = pd.concat(all_demo, ignore_index=True)
    drug_df = pd.concat(all_drug, ignore_index=True)
    ther_df = pd.concat(all_ther, ignore_index=True)
    react_df = pd.concat(all_react, ignore_index=True)

    # Merge and process data
    react_drug = pd.merge(react_df, drug_df, on='primaryid', how='inner')
    react_drug = react_drug.dropna()
    react_drug = react_drug.drop_duplicates(subset=['primaryid', 'pt'])

    react_drug_demo = pd.merge(react_drug, demo_df, on='primaryid', how='left')

    # Create unique drug keys
    ther_df['drugKey'] = ther_df['primaryid'].astype(str) + ther_df['dsg_drug_seq'].astype(str)
    react_drug_demo['drugKey'] = react_drug_demo['primaryid'].astype(str) + react_drug_demo['drug_seq'].astype(str)

    drug_demo_ther_react = pd.merge(react_drug_demo, ther_df, on='drugKey', how='left')

    drug_demo_ther_react['pt'] = drug_demo_ther_react['pt'].str.lower()

    # Save the merged dataset
    merged_file_path = os.path.join("Data", "merged_faers_2019.csv")
    drug_demo_ther_react.to_csv(merged_file_path, index=False)
    logging.info(f"Merged dataset saved to {merged_file_path}")

    # Analyze top adverse effects
    tramal_df = drug_demo_ther_react[drug_demo_ther_react['drugname'] == 'tramal']
    lyrica_df = drug_demo_ther_react[drug_demo_ther_react['drugname'] == 'lyrica']

    top_adverse_effects_tramadol = tramal_df['pt'].value_counts().nlargest(10).reset_index()
    top_adverse_effects_tramadol.columns = ['pt', 'count']

    top_adverse_effects_lyrica = lyrica_df['pt'].value_counts().nlargest(10).reset_index()
    top_adverse_effects_lyrica.columns = ['pt', 'count']

    # Visualize results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    sns.barplot(x='count', y='pt', data=top_adverse_effects_tramadol, ax=ax1)
    ax1.set_title('Top 10 Adverse Effects - Tramadol')
    ax1.set_xlabel('Count')
    ax1.set_ylabel('Adverse Effect')

    sns.barplot(x='count', y='pt', data=top_adverse_effects_lyrica, ax=ax2)
    ax2.set_title('Top 10 Adverse Effects - Lyrica')
    ax2.set_xlabel('Count')
    ax2.set_ylabel('Adverse Effect')

    plt.tight_layout()
    plt.savefig('adverse_effects_comparison.png')
    plt.close()

    logging.info("Top 10 Adverse Effects - Tramadol:")
    logging.info(top_adverse_effects_tramadol)
    logging.info("\nTop 10 Adverse Effects - Lyrica:")
    logging.info(top_adverse_effects_lyrica)

if __name__ == "__main__":
    main()