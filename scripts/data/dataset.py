import pandas as pd
import os

# Get the current working directory
pwd = os.getcwd()

# Get the parent directory (one level up)
p_dir = os.path.dirname(pwd)

# Get the grandparent directory (two levels up)
gp_dir = os.path.dirname(p_dir)
print(gp_dir)


listings_path = os.path.join(gp_dir, "data", "raw", "listings.csv")
neighborhoods_path = os.path.join(gp_dir, "data", "raw", "neighbourhoods.csv")

listings = pd.read_csv(listings_path)
neighborhoods = pd.read_csv(neighborhoods_path)

listings.head()
neighborhoods.head()
