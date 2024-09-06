import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import utility.plots_cfg  # noqa: F401

# Load the dataset
script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "../data/clean/cleaned_listings.csv")
df = pd.read_csv(data_path)

# *1. Competition by Neighbourhood (Side-by-side chart)
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
    by="listings_count", ascending=False
)

# Melt the dataframe to prepare for a side-by-side barplot
melted_counts = merged_counts.melt(
    id_vars="neighbourhood",
    value_vars=["listings_count", "hosts_count"],
    var_name="count_type",
    value_name="count",
)
# Plot the data
fig1, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="neighbourhood", y="count", hue="count_type", data=melted_counts, ax=ax)
ax.set_title("Competition by Neighbourhood")
ax.set_xlabel("Neighbourhood")
ax.set_ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# *2. Pricing & Competition Correlation (Scatter plot)
# Calculate the count of "id" and average price per "neighbourhood"
filtered_df2 = (
    filtered_df.groupby("neighbourhood")
    .agg(id_count=("id", "count"), average_price=("price", "mean"))
    .sort_values(by="average_price", ascending=True)
    .reset_index()
)

# Plot the data
fig2, ax = plt.subplots(figsize=(8, 5))
sns.regplot(x="id_count", y="average_price", data=filtered_df2, ci=None, ax=ax)
ax.set_title("Pricing & Competition Correlation")
ax.set_xlabel("Number of Listings")
ax.set_ylabel("Average Price")
ax.set_ylim(0, None)
plt.tight_layout()

plt.show()


# *3. AVG Pricing by Neighbourhood (Bar chart)
fig3, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="average_price",
    y="neighbourhood",
    data=filtered_df2.sort_values(by="average_price", ascending=False),
    palette="coolwarm",
    ax=ax,
    orient="h",
)
ax.set_title("Average Pricing by Neighbourhood")
ax.set_xlabel("Neighbourhood")
ax.set_ylabel("Average Price")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# *4. Popular Property Types by Neighbourhood (Bar chart)
# Calculate the count of room types per neighbourhood
room_counts = (
    filtered_df.groupby(["neighbourhood", "room_type"]).size().reset_index(name="count")
)

# Determine the total count per neighbourhood
neighbourhood_order = (
    room_counts.groupby("neighbourhood")["count"]
    .sum()
    .sort_values(ascending=False)
    .index
)

# Plot the bar chart
fig4, ax = plt.subplots(figsize=(12, 7))
sns.countplot(
    x="neighbourhood",
    hue="room_type",
    data=filtered_df,
    palette="viridis",
    ax=ax,
    order=neighbourhood_order,  # Apply the sorted order
)
ax.set_title("Popular Property Types by Neighbourhood")
ax.set_xlabel("Neighbourhood")
ax.set_ylabel("Count of Property Types")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


# *5. Host Analysis Based on Listing Volume (Histogram)
filtered_df["listings_per_host"] = filtered_df.groupby("host_id")["id"].transform(
    "count"
)
fig5, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_df["listings_per_host"], bins=30, kde=True, color="Blue", ax=ax)
ax.set_title("Host Analysis: Listings per Host")
ax.set_xlabel("Number of Listings per Host")
ax.set_ylabel("Frequency")
plt.tight_layout()

plt.show()


# *6. Correlation Analysis Visualization
numerical_df = filtered_df.select_dtypes(include=[float, int])
correlation_matrix = numerical_df.corr()

# Correlation Heatmap
fig6, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Correlation Heatmap of Numerical Features")

plt.show()


# *7.Correlation with 'price'
price_correlations = correlation_matrix["price"].sort_values(ascending=False)
fig7, ax = plt.subplots(figsize=(10, 6))
price_correlations.drop("price").plot(kind="bar", color="skyblue", ax=ax)
ax.set_title("Correlation of Features with Price")
ax.set_xlabel("Features")
ax.set_ylabel("Correlation Coefficient")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()


from utility.save_plots import export_figs  # noqa: E402 (disable not ot top of file warning)


export_dir = os.path.join(script_dir, "../reports/figures/")
figures = [
    (fig1, "competition_by_neighbourhood.png"),
    (fig2, "pricing_and_competition_correlation.png"),
    (fig3, "average_pricing_by_neighbourhood.png"),
    (fig4, "popular_property_types_by_neighbourhood.png"),
    (fig5, "listings_per_host_histogram.png"),
    (fig6, "correlation_heatmap.png"),
    (fig7, "correlation_with_price.png"),
]

# for fig, filename in figures:
#     export_figs(fig, filename, export_dir)

for index, (fig, filename) in enumerate(figures, start=1):
    export_figs(fig, filename, export_dir, index)

# * ------------------------------------------------------
# * sub-optimal way to save figures
# * ------------------------------------------------------

# # Directory to save visualizations
# export_path = os.path.join(script_dir, "../../reports/figures/")


# def save_plot(fig, filename):
#     """Saves the given figure to a file."""
#     filepath = os.path.join(export_path, filename)
#     fig.savefig(filepath)
#     plt.close(fig)


# # List of figures and filenames
# figures = [
#     (
#         fig1,
#         "competition_by_neighbourhood.png",
#     ),  # Competition by Neighbourhood (Side-by-side chart)
#     (
#         fig2,
#         "pricing_and_competition_correlation.png",
#     ),  # Pricing & Competition Correlation (Scatter plot)
#     (
#         fig3,
#         "average_pricing_by_neighbourhood.png",
#     ),  # AVG Pricing by Neighbourhood (Bar chart)
#     (
#         fig4,
#         "popular_property_types_by_neighbourhood.png",
#     ),  # Popular Property Types by Neighbourhood (Bar chart)
#     (
#         fig5,
#         "listings_per_host_histogram.png",
#     ),  # Host Analysis Based on Listing Volume (Histogram)
#     (fig6, "correlation_heatmap.png"),  # Correlation (Heatmap)
#     (fig7, "correlation_with_price.png"),  # Correlation Coefficient (Bar Chart)
# ]

# # Save all figures
# for fig, filename in figures:
#     save_plot(fig, filename)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# *Broken code bellow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# save_plot(
#     fig1, "competition_by_neighbourhood"
# )  # Competition by Neighbourhood (Side-by-side chart)
# save_plot(
#     fig2, "pricing_and_competition_correlation"
# )  # Pricing & Competition Correlation (Scatter plot)
# save_plot(
#     fig3, "average_pricing_by_neighbourhood"
# )  # AVG Pricing by Neighbourhood (Bar chart)
# save_plot(
#     fig4, "popular_property_types_by_neighbourhood.png"
# )  # Popular Property Types by Neighbourhood (Bar chart)
# save_plot(
#     fig5, "listings_per_host_histogram.png"
# )  # Host Analysis Based on Listing Volume (Histogram)
# save_plot(fig6, "correlation_heatmap")  # Correlation (Heatmap)
# save_plot(fig7, "correlation_with_price")  # Correlation Coefficient (Bar Chart)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# *Test code bellow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # Load the dataset
# script_dir = os.path.dirname(__file__)
# data_path = os.path.join(script_dir, "../../data/clean/cleaned_listings.csv")
# df = pd.read_csv(data_path)

# # Directory to save visualizations
# export_path = os.path.join(script_dir, "../../reports/figures/")
# if not os.path.exists(export_path):
#     os.makedirs(export_path)


# def save_plot(fig, filename):
#     """Saves the given figure to a file."""
#     filepath = os.path.join(export_path, filename)
#     fig.savefig(filepath, bbox_inches="tight", dpi=300)
#     plt.close(fig)


# # *1. Competition by Neighbourhood (Side-by-side chart)
# avg_price_per_neighbourhood = df.groupby("neighbourhood")["price"].mean().reset_index()
# avg_price_per_neighbourhood = avg_price_per_neighbourhood.sort_values(
#     by="price", ascending=False
# )
# top_neighbourhoods = avg_price_per_neighbourhood.iloc[1:11]
# filtered_df = df[df["neighbourhood"].isin(top_neighbourhoods["neighbourhood"])]

# listings_count = (
#     filtered_df.groupby("neighbourhood")["id"]
#     .count()
#     .reset_index(name="listings_count")
# )
# hosts_count = (
#     filtered_df.groupby("neighbourhood")["host_id"]
#     .nunique()
#     .reset_index(name="hosts_count")
# )
# merged_counts = pd.merge(listings_count, hosts_count, on="neighbourhood").sort_values(
#     by="listings_count", ascending=True
# )
# melted_counts = merged_counts.melt(
#     id_vars="neighbourhood",
#     value_vars=["hosts_count", "listings_count"],
#     var_name="count_type",
#     value_name="count",
# )

# fig1, ax = plt.subplots(figsize=(10, 6))
# sns.barplot(x="neighbourhood", y="count", hue="count_type", data=melted_counts, ax=ax)
# ax.set_title("Competition by Neighbourhood")
# ax.set_xlabel("Neighbourhood")
# ax.set_ylabel("Count")
# plt.xticks(rotation=45)
# plt.tight_layout()

# # *2. Pricing & Competition Correlation (Scatter plot)
# filtered_df2 = (
#     filtered_df.groupby("neighbourhood")
#     .agg(id_count=("id", "count"), average_price=("price", "mean"))
#     .reset_index()
# )
# fig2, ax = plt.subplots(figsize=(8, 5))
# sns.regplot(x="id_count", y="average_price", data=filtered_df2, ci=None, ax=ax)
# ax.set_title("Pricing & Competition Correlation")
# ax.set_xlabel("Number of Listings")
# ax.set_ylabel("Average Price")
# ax.set_ylim(0, None)
# plt.tight_layout()

# # *3. AVG Pricing by Neighbourhood (Bar chart)
# fig3, ax = plt.subplots(figsize=(10, 6))
# sns.barplot(
#     x="average_price",
#     y="neighbourhood",
#     data=filtered_df2.sort_values(by="average_price", ascending=False),
#     palette="coolwarm",
#     ax=ax,
#     orient="h",
# )
# ax.set_title("Average Pricing by Neighbourhood")
# ax.set_xlabel("Average Price")
# ax.set_ylabel("Neighbourhood")
# plt.xticks(rotation=45)
# plt.tight_layout()

# # *4. Popular Property Types by Neighbourhood (Bar chart)
# room_counts = (
#     filtered_df.groupby(["neighbourhood", "room_type"]).size().reset_index(name="count")
# )
# neighbourhood_order = (
#     room_counts.groupby("neighbourhood")["count"]
#     .sum()
#     .sort_values(ascending=False)
#     .index
# )
# fig4, ax = plt.subplots(figsize=(12, 7))
# sns.countplot(
#     x="neighbourhood",
#     hue="room_type",
#     data=filtered_df,
#     palette="viridis",
#     ax=ax,
#     order=neighbourhood_order,
# )
# ax.set_title("Popular Property Types by Neighbourhood")
# ax.set_xlabel("Neighbourhood")
# ax.set_ylabel("Count of Property Types")
# plt.xticks(rotation=45)
# plt.tight_layout()

# # *5. Host Analysis Based on Listing Volume (Histogram)
# filtered_df["listings_per_host"] = filtered_df.groupby("host_id")["id"].transform(
#     "count"
# )
# fig5, ax = plt.subplots(figsize=(10, 6))
# sns.histplot(filtered_df["listings_per_host"], bins=30, kde=True, color="Blue", ax=ax)
# ax.set_title("Host Analysis: Listings per Host")
# ax.set_xlabel("Number of Listings per Host")
# ax.set_ylabel("Frequency")
# plt.tight_layout()

# # *6. Correlation Analysis Visualization
# numerical_df = filtered_df.select_dtypes(include=[float, int])
# correlation_matrix = numerical_df.corr()

# # Correlation Heatmap
# fig6, ax = plt.subplots(figsize=(12, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
# ax.set_title("Correlation Heatmap of Numerical Features")
# plt.tight_layout()

# # Correlation with 'price'
# price_correlations = correlation_matrix["price"].sort_values(ascending=False)
# fig7, ax = plt.subplots(figsize=(10, 6))
# price_correlations.drop("price").plot(kind="bar", color="skyblue", ax=ax)
# ax.set_title("Correlation of Features with Price")
# ax.set_xlabel("Features")
# ax.set_ylabel("Correlation Coefficient")
# plt.xticks(rotation=45)
# plt.tight_layout()

# # List of figures and filenames
# figures = [
#     (fig1, "competition_by_neighbourhood.png"),
#     (fig2, "pricing_and_competition_correlation.png"),
#     (fig3, "average_pricing_by_neighbourhood.png"),
#     (fig4, "popular_property_types_by_neighbourhood.png"),
#     (fig5, "listings_per_host_histogram.png"),
#     (fig6, "correlation_heatmap.png"),
#     (fig7, "correlation_with_price.png"),
# ]

# # Save all figures
# for fig, filename in figures:
#     save_plot(fig, filename)
