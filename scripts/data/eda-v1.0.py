import os

import numpy as np
import pandas as pd

# Load the dataset
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "../../data/clean/cleaned_listings.csv")
df = pd.read_csv(data_path)

df.head()  # Inspect the first few rows
df.info()  # Get basic info about the dataset
df.isnull().sum()  # Check for missing values
df.describe()  # Summary statistics for numerical columns
df.median(numeric_only=True)  # Calculate Median for numerical columns
df.mode(numeric_only=True).iloc[0]  # Calculate Mode for numerical columns
df.nunique()  # Unique values count for categorical columns

# Distribution of Listings Across Neighborhoods
df["neighbourhood"].value_counts()

# Correlation Analysis
# Select only the numerical columns for the correlation matrix
numerical_df = df.select_dtypes(include=[np.number])
correlation_matrix = numerical_df.corr()  # Create the correlation matrix
price_correlations = correlation_matrix["price"].sort_values(
    ascending=False
)  # Focus on correlation with 'price'
print("Price Correlations:\n", price_correlations)

# Distribution and Analysis of Key Metrics
# Listings count by Host
listings_per_host = (
    df.groupby("host_id")
    .size()
    .sort_values(ascending=False)
    .reset_index(name="listings_count")
)
print("Listings per Host:\n", listings_per_host)

# Summary statistics for neighborhoods
neighbourhood_stats = (
    df.groupby("neighbourhood")["price"]
    .agg(["count", "mean", "median", "std"])
    .sort_values("count", ascending=False)
    .reset_index()
)
print("Neighbourhood Stats:\n", neighbourhood_stats)
print("\nEND OF EXPLORATORY DATA ANALYSIS!")
