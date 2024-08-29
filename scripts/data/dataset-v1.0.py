# Import necessary libraries
import os
import numpy as np
import pandas as pd

# Read file from root .\data\raw\
script_dir = os.path.dirname(__file__)
listings_file_path = os.path.join(script_dir, "../../data/raw/listings.csv")

# Read the CSV file into a DataFrame
df_listings = pd.read_csv(listings_file_path)

# Preview Dataframes
df_listings.head()

# Overview of df_listings
df_listings.info()
df_listings.describe()
df_listings.columns

# Cleaning df_listings
listings_clean = (
    df_listings.copy()
)  # Creating copy of the df_listings before making changes

# Cleaning column names since they contain white spaces
listings_clean.columns = listings_clean.columns.str.strip().str.lower()
listings_clean = (
    listings_clean.drop(
        columns=[
            "neighbourhood_group",
            "minimum_nights",
            "number_of_reviews",
            "last_review",
            "reviews_per_month",
            "calculated_host_listings_count",
            "availability_365",
            "number_of_reviews_ltm",
            "license",
        ]
    ).drop_duplicates()  # Dropping duplicate data
)

# Quick check to see if changes were made
listings_clean.head()
listings_clean.info()

# Replacing non-ASCII characters with blank spaces.
listings_clean["name"] = listings_clean["name"].apply(
    lambda x: "" if any(ord(char) > 127 for char in x) else x
)
listings_clean["host_name"] = listings_clean["host_name"].apply(
    lambda x: "" if any(ord(char) > 127 for char in x) else x
)

# Replace empty strings in the 'price' column with NaN.
listings_clean["price"] = pd.to_numeric(
    listings_clean["price"].replace("", np.nan), errors="coerce"
)

# Drop rows with NaN values in 'price'
listings_clean = listings_clean.dropna(subset=["price"])

# Convert to int64 (this removes decimal places)
listings_clean["price"] = listings_clean["price"].astype(int)

# Create a copy of the cleaned listings DataFrame
df_listings_cleaned = listings_clean.copy()

print(df_listings_cleaned.head)

# Creating directory path for export of cleaned data.
clean_data_dir = os.path.join("..", "..", "data", "clean")
cleaned_listings_export_path = os.path.abspath(
    os.path.join(script_dir, clean_data_dir, "cleaned_listings.csv")
)

# Exporting cleaned data to directory.
df_listings_cleaned.to_csv(cleaned_listings_export_path, index=False)
print("Data Cleaning Completed!")
