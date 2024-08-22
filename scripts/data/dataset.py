import os
import pandas as pd
import re

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

# Print filepaths and DataFrames for verification

print(df_listings.head())
print(df_neighbourhoods.head())
print(script_dir)
print(listings_relative_path)
print(neighbourhoods_relative_path)
print(listings_file_path)
print(neighbourhoods_file_path)

df_listings.head()
df_neighbourhoods.head()

# Overview of df_listings
df_listings.info()
df_listings.describe()

# Overview of df_neighbourhoods
df_neighbourhoods.info()
df_neighbourhoods.describe()

# Cleaning df_listings
listings_clean = df_listings.copy()
print(listings_clean.columns)
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
    )
    .drop_duplicates()
    .dropna()
)
print(listings_clean)
listings_clean.head()
listings_clean.info()
print(listings_clean.columns)


# Define the function to check for English text
def is_english(text):
    # Regex pattern for English letters, numbers, and common English symbols
    pattern = r"^[A-Za-z0-9\s.,!?\'\"()@#$%^&*;:\[\]{}±_+=/\\|`~]*$"
    return bool(re.match(pattern, text))


# Apply the function to check each relevant column and create a boolean mask
listings_clean["is_english"] = listings_clean.apply(
    lambda row: is_english(str(row.get("name", "")))
    if isinstance(row.get("name", ""), str)
    else False and is_english(str(row.get("host_name", "")))
    if isinstance(row.get("host_name", ""), str)
    else False,
    axis=1,
)

# Delete rows where at least one relevant column contains non-English characters
df_listings_cleaned = listings_clean[listings_clean["is_english"]].drop(
    columns="is_english"
)

print(df_listings_cleaned)
df_listings_cleaned
df_listings_cleaned.info()


# Cleaning df_neighbourhoods
