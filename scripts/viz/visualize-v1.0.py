import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the dataset
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "../../data/clean/cleaned_listings.csv")
df = pd.read_csv(data_path)

# Directory to save visualizations
export_path = os.path.join(script_dir, "../../reports/figures/")


def save_plot(fig, filename):
    """Saves the given figure to a file."""
    filepath = os.path.join(export_path, filename)
    fig.savefig(filepath)
    plt.close(fig)


# 1. Competition by Neighbourhood (Side-by-side chart)
# Calculate average price per neighbourhood
avg_price_per_neighbourhood = df.groupby("neighbourhood")["price"].mean().reset_index()
avg_price_per_neighbourhood = avg_price_per_neighbourhood.sort_values(
    by="price", ascending=False
)

# Select the 2nd to 11th average price per neighbourhood
top_neighbourhoods = avg_price_per_neighbourhood.sort_values(
    by="price", ascending=False
).iloc[1:11]

# Filter the original dataframe for these neighbourhoods
filtered_df = df[df["neighbourhood"].isin(top_neighbourhoods["neighbourhood"])]

# Count of "id" (listings) per neighbourhood
listings_count = (
    filtered_df.groupby("neighbourhood")["id"]
    .count()
    .reset_index(name="listings_count")
)

# Count of "host_id" per neighbourhood
hosts_count = (
    filtered_df.groupby("neighbourhood")["host_id"]
    .nunique()
    .reset_index(name="hosts_count")
)

# Merge the counts into one dataframe for plotting
merged_counts = pd.merge(listings_count, hosts_count, on="neighbourhood").sort_values(
    by="listings_count", ascending=True
)

# Melt the dataframe to prepare for a side-by-side barplot
melted_counts = merged_counts.melt(
    id_vars="neighbourhood",
    value_vars=["hosts_count", "listings_count"],
    var_name="count_type",
    value_name="count",
)
# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="neighbourhood", y="count", hue="count_type", data=melted_counts, ax=ax)
ax.set_title("Competition by Neighbourhood")
ax.set_xlabel("Neighbourhood")
ax.set_ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

save_plot(fig, "competition_by_neighbourhood")

# 2. Pricing & Competition Correlation (Scatter plot)
# Calculate the count of "id" and average price per "neighbourhood" in "filtered_df"
filtered_df2 = filtered_df.groupby("neighbourhood")["id"].count().reset_index()
filtered_df2["average_price"] = (
    filtered_df.groupby("neighbourhood")["price"].mean().values
)
# Plot the data
fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(x="id", y="average_price", data=filtered_df2, ci=None, ax=ax)
ax.set_title("Pricing & Competition Correlation")
ax.set_xlabel("Number of Listings")
ax.set_ylabel("Average Price")
ax.set_ylim(0, None)
plt.tight_layout()
plt.show()

save_plot(fig, "pricing_competition_correlation")

# TODO: fix more visualization code.

# 3. AVG Pricing by Neighbourhood (Bar chart)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="neighbourhood", y="average_price", data=df, palette="coolwarm", ax=ax)
ax.set_title("Average Pricing by Neighbourhood")
ax.set_xlabel("Neighbourhood")
ax.set_ylabel("Average Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

save_plot(fig, "avg_pricing_by_neighbourhood")

# 4. Distribution of Prices (Histogram)
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["price"], bins=30, kde=True, color="skyblue", ax=ax)
ax.set_title("Distribution of Prices")
ax.set_xlabel("Price (¥)")
ax.set_ylabel("Frequency")
plt.tight_layout()
plt.show()
save_plot(fig, "price_distribution.png")

# 5. Popular Property Types by Neighbourhood (Bar chart)
fig, ax = plt.subplots(figsize=(12, 7))
sns.countplot(x="neighbourhood", hue="property_type", data=df, palette="viridis", ax=ax)
ax.set_title("Popular Property Types by Neighbourhood")
ax.set_xlabel("Neighbourhood")
ax.set_ylabel("Count of Property Types")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
save_plot(fig, "popular_property_types")

# 6. Host Analysis Based on Listing Volume (Histogram)
df["listings_per_host"] = df.groupby("host_id")["id"].transform("count")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["listings_per_host"], bins=30, kde=True, color="orange", ax=ax)
ax.set_title("Host Analysis: Listings per Host")
ax.set_xlabel("Number of Listings per Host")
ax.set_ylabel("Frequency")
plt.tight_layout()
plt.show()
save_plot(fig, "host_analysis")

# 7. Correlation Analysis Visualization
numerical_df = df.select_dtypes(include=[float, int])
correlation_matrix = numerical_df.corr()

# Correlation Heatmap
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Correlation Heatmap of Numerical Features")
plt.show()
save_plot(fig, "correlation_heatmap")

# Correlation with 'price'
price_correlations = correlation_matrix["price"].sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
price_correlations.drop("price").plot(kind="bar", color="skyblue", ax=ax)
ax.set_title("Correlation of Features with Price")
ax.set_xlabel("Features")
ax.set_ylabel("Correlation Coefficient")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
save_plot(fig, "price_correlation_bar_chart")
