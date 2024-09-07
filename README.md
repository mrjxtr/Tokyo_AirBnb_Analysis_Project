# TOKYO AIRBNB COMPETITION AND PRICING ANALYSIS

## Project Summary <a name="ProjectSummary"></a>

Welcome to my Tokyo AirBnb **Competition and Pricing Analysis**. This project aims to show a potential opportunities to start an AirBnb business in Tokyo, Japan. I will be looking at potential neighbourhoods in Tokyo where, by data driven decision making and insights, a potential real estate entrepreneur or company can start their AirBnb business.

<div align="center">
    <a href="reports/figures/Tokyo_Airbnb_Competition_and_Pricing.png">
        <img src="reports/figures/Tokyo_Airbnb_Competition_and_Pricing.png" alt="Dashboard" width="400">
    </a>
</div>

### Report outline <a name="Reportoutline"></a>

- [Project Summary](#ProjectSummary)
  - [Report outline](#Reportoutline)
  - [Questions to Answer (Business task)](#QuestionstoAnswer)
  - [Tools used](#Toolsused)
  - [Analysis Process](#AnalysisProcess)
- [Step 1 - Gather relevant data](#Gatherrelevantdata)
- [Step 2 - Process data](#Processdata)
- [Step 3 - Explore data](#Exploredata)
- [Step 4 - Visualize data](#Visualizedata)
- [Step 5 - Insights and Recommendations](#Presentinsightsandrecommendations)
  - [Insights](#Insights)
  - [Recommendations](#Recommendations)

### Questions to Answer (Business task) <a name="QuestionstoAnswer"></a>

1. Which neighbourhoods in Tokyo has the highest average rates for their rooms. Give at least the top 10.

2. Which of these top 10 neighbourhoods in Tokyo has the least amount of competitors.

3. Which of these top 10 neighbourhoods has the most amount of competition in terms of listings.

4. Which room types are in demand for this neighbourhoods.

### Tools used (Tech Stack) <a name="Toolsused"></a>

1. **VSCode** - For working with Python files, Jupyter Notebooks, and Markdown files.

    - Python, Jupyter Interactive Window, Jupyter Notebook

2. **Python** - For Data Processing, Exploratory Data Analysis and Data Visualization.

    - Pandas, Numpy, Matplotlib, Seaborn

3. **Tableau** - For creating dynamic Dashboards to better present insights.

Other tools:

- **Git** - for version control,

### Analysis Process <a name="AnalysisProcess"></a>

- **Step 1** - **Gather relevant data** to create this analysis through publicly available open data sources.
- **Step 2** - **Process data** to ensure that it is ready Exploratory Data Analysis or EDA (Exploratory Data Analysis).
- **Step 3** - **Explore data** to to identify patters and trends from the data that answer questions related to the business task.
- **Step 4** - **Visualize data** that is discovered through EDA to gain better visual representation and understanding of the data story.
- **Step 5** - Present **insights and recommendations** by exporting figures and charts created during EDA to create a comprehensive report and documentation and by creating a dynamic Tableau dashboard.

## Step 1 - Gather relevant data <a name="Gatherrelevantdata"></a>

The [raw data](data/raw/listings.csv) was taken from [Inside AirBnb](https://insideairbnb.com/get-the-data/), an official AirBnb open data source that has AirBnb data from dozens of cities and countries around the world.

## Step 2 - Process data <a name="Processdata"></a>

This process created the [clean data](/data/clean/cleaned_listings.csv) used for exploration and analysis is created using the [dataset-v1.0.py](scripts/data/dataset-v1.0.py) script shown below.

<details>

<summary>👀 see code for data cleaning </summary>

```python
# Import necessary libraries
import os
import numpy as np
import pandas as pd

# Read file from root .\data\raw\
script_dir = os.path.dirname(__file__)
listings_file_path = os.path.join(script_dir, "../../data/raw/listings.csv")

# Read the CSV file into a DataFrame
df_listings = pd.read_csv(listings_file_path)
```

Read data from the [raw data folder](data/raw/) and as a Pandas DataFrame.

```python
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
```

Code for data cleaning as seen in the [dataset-v1.0.py](scripts/data/dataset-v1.0.py) script.

```python
# Creating directory path for export of cleaned data.
clean_data_dir = os.path.join("..", "..", "data", "clean")
cleaned_listings_export_path = os.path.abspath(
    os.path.join(script_dir, clean_data_dir, "cleaned_listings.csv")
)

# Exporting cleaned data to directory.
df_listings_cleaned.to_csv(cleaned_listings_export_path, index=False)
print("Data Cleaning Completed!")
```

exporting data to [processed data folder](data/processed/).

</details>

<br />

>I also converted the script above into a Jupyter Notebook. Click this [link](notebooks/jl-data-cleaning-v1.0.ipynb) if you prefer viewing it a jupyter notebook format.

## Step 3 - Explore data <a name="Exploredata"></a>

Data exploration on the [cleaned data](data/clean/cleaned_listings.csv) is done using the [eda-v1.0.py](scripts/data/eda-v1.0.py) script shown below.

<details>

<summary>👀 see code for data cleaning </summary>

```python
# Import necessary libraries
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
```

</details>

<br />

>I also converted the script above into a Jupyter Notebook. Click this [link](notebooks/jl-data-exploration-v1.0.ipynb) if you prefer viewing it a jupyter notebook format.

## Step 4 - Visualize data <a name="Visualizedata"></a>

Using **Tableau** to create a dynamic dashboard to gain better understanding of the data story.

[![Dashboard](reports/figures/Tokyo_Airbnb_Competition_and_Pricing.png)](https://public.tableau.com/views/Book3_17249856024470/Dashboard2?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
[View Dashboard in Tableau Public](https://public.tableau.com/views/Book3_17249856024470/Dashboard2?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Step 5 - Insights and Recommendations <a name="Presentinsightsandrecommendations"></a>

### Insights <a name="Insights"></a>

**Key insights:**

- writing insights and recommendations.
- writing insights and recommendations.
- writing insights and recommendations.

### Recommendations <a name="Recommendations"></a>

- writing insights and recommendations.
- writing insights and recommendations.
- writing insights and recommendations.
