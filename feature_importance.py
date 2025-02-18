import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Load the combined dataset
print("Loading combined dataset...")
data = pd.read_csv("combined_dataset.csv", low_memory=False)

# Define target variable and predictors
target = "yardsGained"  # Response variable
features = [col for col in data.columns if col != target]  # Exclude target from features

# Drop rows with missing target values
data = data.dropna(subset=[target])

# Preprocess data
def preprocess_data(data, features):
    print("Preprocessing data...")
    
    # Identify numeric and categorical features
    numeric_features = data[features].select_dtypes(include=["number"]).columns.tolist()
    categorical_features = data[features].select_dtypes(include=["object"]).columns.tolist()
    
    # Drop irrelevant or high-cardinality features
    high_cardinality_features = [col for col in categorical_features if data[col].nunique() > 500]
    print(f"Dropping high-cardinality features: {high_cardinality_features}")
    data = data.drop(columns=high_cardinality_features)
    
    # Recompute categorical features after dropping
    categorical_features = [col for col in categorical_features if col not in high_cardinality_features]
    
    # Impute missing values for numeric features
    print("Imputing missing values for numeric features...")
    num_imputer = SimpleImputer(strategy="mean")
    data[numeric_features] = num_imputer.fit_transform(data[numeric_features])
    
    # Impute missing values for categorical features
    print("Imputing missing values for categorical features...")
    cat_imputer = SimpleImputer(strategy="most_frequent")
    data[categorical_features] = cat_imputer.fit_transform(data[categorical_features])
    
    # Apply Label Encoding for remaining categorical features
    for col in categorical_features:
        print(f"Label encoding column: {col}")
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
    
    print("Preprocessing complete.")
    return data

# Preprocess the dataset
data = preprocess_data(data, features)

# Split data into training and testing sets
X = data.drop(columns=[target])
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit a Random Forest model for feature importance
print("Fitting Random Forest for feature importance...")
rf_model = RandomForestRegressor(random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Get feature importances
importances = rf_model.feature_importances_
feature_importance_df = pd.DataFrame({"Feature": X.columns, "Importance": importances})
feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)

# Save the top features to a CSV file
top_features = feature_importance_df.head(30)["Feature"].tolist()  # Select top 30 features
print("Top features selected:", top_features)

# Save dataset with only top features
print("Saving dataset with top features...")
X_top_features = X[top_features]
X_top_features[target] = y  # Add back the target column
X_top_features.to_csv("top_features_dataset.csv", index=False)
print("Dataset with top features saved as 'top_features_dataset.csv'.")