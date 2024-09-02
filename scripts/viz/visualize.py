import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the dataset
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "../../data/clean/cleaned_listings.csv")
df = pd.read_csv(data_path)

# 1. Competition by Neighborhood (Side-by-side chart)
plt.figure(figsize=(10, 6))
sns.barplot(x="neighborhood", y="listings", hue="price_category", data=df)
plt.title("Competition by Neighborhood")
plt.xlabel("Neighborhood")
plt.ylabel("Number of Listings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\competition_by_neighborhood.png"
)

# 2. Pricing & Competition Correlation (Scatter plot)
plt.figure(figsize=(8, 5))
sns.scatterplot(x="listings", y="average_price", data=df)
plt.title("Pricing & Competition Correlation")
plt.xlabel("Number of Listings")
plt.ylabel("Average Price")
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\pricing_competition_correlation.png"
)

# 3. AVG Pricing by Neighborhood (Bar chart)
plt.figure(figsize=(10, 6))
sns.barplot(x="neighborhood", y="average_price", data=df, palette="coolwarm")
plt.title("Average Pricing by Neighborhood")
plt.xlabel("Neighborhood")
plt.ylabel("Average Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\avg_pricing_by_neighborhood.png"
)

# 4. Distribution of Prices (Histogram)
plt.figure(figsize=(10, 6))
sns.histplot(df["price"], bins=30, kde=True, color="skyblue")
plt.title("Distribution of Prices")
plt.xlabel("Price (¥)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\price_distribution.png"
)

# 5. Popular Property Types by Neighborhood (Bar chart)
plt.figure(figsize=(12, 7))
sns.countplot(x="neighborhood", hue="property_type", data=df, palette="viridis")
plt.title("Popular Property Types by Neighborhood")
plt.xlabel("Neighborhood")
plt.ylabel("Count of Property Types")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\popular_property_types.png"
)

# 6. Host Analysis Based on Listing Volume (Bar chart)
plt.figure(figsize=(10, 6))
df["listings_per_host"] = df.groupby("host_id")["id"].transform("count")
sns.histplot(df["listings_per_host"], bins=30, kde=True, color="orange")
plt.title("Host Analysis: Listings per Host")
plt.xlabel("Number of Listings per Host")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\host_analysis.png"
)

# Correlation Analysis Visualization
# Select only the numerical columns for the correlation matrix
numerical_df = df.select_dtypes(include=[float, int])

# Create the correlation matrix
correlation_matrix = numerical_df.corr()

# Plotting the correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Numerical Features")
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\correlation_heatmap.png"
)
plt.show()

# Correlation with 'price'
price_correlations = correlation_matrix["price"].sort_values(ascending=False)

# Plotting correlation with price as a bar chart
plt.figure(figsize=(10, 6))
price_correlations.drop("price").plot(kind="bar", color="skyblue")
plt.title("Correlation of Features with Price")
plt.xlabel("Features")
plt.ylabel("Correlation Coefficient")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    "D:\\Admin Files\\Desktop\\Data Proj\\personal-proj\\tokyo-airbnb-proj\\scripts\\viz\\price_correlation_bar_chart.png"
)
plt.show()
