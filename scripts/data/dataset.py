import os
import pandas as pd

# Get the directory of the current script
# Define the relative path to the CSV file
# Construct the full path to the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))

listings_relative_path = os.path.join("..", "..", "data", "raw", "listings.csv")
neighbourhoods_relative_path = os.path.join(
    "..", "..", "data", "raw", "neighbourhoods.csv"
)

listings_file_path = os.path.abspath(os.path.join(script_dir, listings_relative_path))
neighbourhoods_file_path = os.path.abspath(
    os.path.join(script_dir, neighbourhoods_relative_path)
)

# Read the CSV file into a DataFrame
df_listings = pd.read_csv(listings_file_path)
df_neighbourhoods = pd.read_csv(neighbourhoods_file_path)

# Print filepaths and DataFrames
df_listings.head()
df_neighbourhoods.head()
print(df_listings.head())
print(df_neighbourhoods.head())
print(script_dir)
print(listings_relative_path)
print(neighbourhoods_relative_path)
print(listings_file_path)
print(neighbourhoods_file_path)
