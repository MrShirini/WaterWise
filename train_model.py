import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# Load dataset
file_path = "data/Indoor_Plant_Health_and_Growth_Factors.csv"
df = pd.read_csv(file_path)

# Drop columns that are not useful or have too many missing values
df = df.drop(columns=["Health_Notes", "Pest_Presence", "Pest_Severity"])

# Drop rows with missing categorical values (or handle them in pipeline)
df = df.dropna(subset=["Fertilizer_Type"])

# Define features and target
X = df.drop(columns=["Watering_Amount_ml"])
y = df["Watering_Amount_ml"]

# Categorical and numerical features
categorical_features = ["Plant_ID", "Sunlight_Exposure", "Fertilizer_Type", "Soil_Type"]
numerical_features = [col for col in X.columns if col not in categorical_features]

# Preprocessing
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

numerical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean"))
])

preprocessor = ColumnTransformer(transformers=[
    ("cat", categorical_transformer, categorical_features),
    ("num", numerical_transformer, numerical_features)
])

# Full pipeline
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", DecisionTreeRegressor(random_state=42))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model_pipeline.fit(X_train, y_train)

# Save model
joblib.dump(model_pipeline, "models/plant_watering_model.joblib")
