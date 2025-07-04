import kagglehub
import pandas as pd

import kagglehub

# Download latest version
path = kagglehub.dataset_download("souvikrana17/indoor-plant-health-and-growth-dataset")

print("Path to dataset files:", path)
#
# Assuming the dataset downloaded as a CSV inside the path folder
df = pd.read_csv(path + "/Indoor_Plant_Health_and_Growth_Factors.csv")
# df = pd.read_csv(path)
# Display the first few rows
print(df.head())

# Check for general info
print(df.info())

# Count missing values
print(df.isnull().sum())

# Show unique values per column
for col in df.columns:
    print(f"{col}: {df[col].unique()}")
