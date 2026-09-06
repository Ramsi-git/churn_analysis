"""
Data Processing and Feature Engineering Module
Handles loading, cleaning, and preprocessing of customer churn data.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


class ChurnDataProcessor:
    \"\"\"
    Pipeline for loading and preprocessing telco customer churn data.
    Implements governance rules: excludes protected demographic columns.
    \"\"\"
    
    # Protected demographic columns per Clause 4 (non-discrimination)
    PROTECTED_COLUMNS = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
    
    # Columns to drop (no predictive value)
    DROP_COLUMNS = ['customerID', 'Churn']
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = None
        self.label_encoders = {}
        self.feature_names = None
        
    def load_data(self, filepath_or_url):
        \"\"\"Load data from CSV file or URL.\"\"\"
        if filepath_or_url.startswith('http'):
            import requests
            from io import StringIO
            response = requests.get(filepath_or_url)
            df = pd.read_csv(StringIO(response.text))
        else:
            df = pd.read_csv(filepath_or_url)
        return df
    
    def fix_totalcharges(self, df):
        \"\"\"
        Fix TotalCharges column which often has missing values for new customers.
        Missing values are typically in rows where tenure is very low.
        
        Returns the fixed dataframe and a log of fixes applied.
        \"\"\"
        df = df.copy()
        
        # Convert to numeric, coercing errors to NaN\n        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')\n        \n        # Count missing before fix\n        missing_before = df['TotalCharges'].isnull().sum()\n        \n        # For new customers with missing TotalCharges, calculate based on tenure * MonthlyCharges\n        if missing_before > 0:\n            df.loc[df['TotalCharges'].isnull(), 'TotalCharges'] = (\n                df.loc[df['TotalCharges'].isnull(), 'MonthlyCharges'] * \n                df.loc[df['TotalCharges'].isnull(), 'tenure']\n            )\n        \n        missing_after = df['TotalCharges'].isnull().sum()\n        \n        fix_log = {\n            'missing_before': missing_before,\n            'missing_after': missing_after,\n            'rows_fixed': missing_before - missing_after,\n            'method': 'tenure * MonthlyCharges'\n        }\n        \n        return df, fix_log\n    \n    def preprocess(self, df, drop_demographics=True):\n        \"\"\"
n        Clean and preprocess the data.\n        \n        Args:\n            df: Raw dataframe\n            drop_demographics: If True, exclude protected columns from features\n        \n        Returns:\n            X: Feature matrix (demographics excluded if requested)\n            y: Target vector (Churn binary)\n            X_full: Feature matrix with ALL non-target columns (for reference)\n            df_cleaned: Cleaned dataframe\n        \"\"\"\n        df_cleaned = df.copy()\n        \n        # Fix TotalCharges\n        df_cleaned, fix_log = self.fix_totalcharges(df_cleaned)\n        print(f\"TotalCharges fixed: {fix_log['rows_fixed']} rows\")\n        \n        # Prepare target\n        y = (df_cleaned['Churn'] == 'Yes').astype(int)\n        \n        # Prepare features\n        columns_to_exclude = self.DROP_COLUMNS.copy()\n        if drop_demographics:\n            columns_to_exclude.extend(self.PROTECTED_COLUMNS)\n        \n        X = df_cleaned.drop(columns=columns_to_exclude)\n        X_full = df_cleaned.drop(columns=['customerID', 'Churn'])  # Keep all for reference\n        \n        # Encode categorical variables\n        categorical_cols = X.select_dtypes(include=['object']).columns\n        X_encoded = X.copy()\n        \n        for col in categorical_cols:\n            le = LabelEncoder()\n            X_encoded[col] = le.fit_transform(X[col])\n            self.label_encoders[col] = le\n        \n        self.feature_names = X_encoded.columns.tolist()\n        \n        return X_encoded, y, X_full, df_cleaned\n    \n    def split_and_scale(self, X, y, test_size=0.2):\n        \"\"\"Split and scale features.\"\""\n        X_train, X_test, y_train, y_test = train_test_split(\n            X, y, test_size=test_size, random_state=self.random_state, stratify=y\n        )\n        \n        # Scale\n        self.scaler = StandardScaler()\n        X_train_scaled = self.scaler.fit_transform(X_train)\n        X_test_scaled = self.scaler.transform(X_test)\n        \n        # Back to DataFrame\n        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns, index=X_train.index)\n        X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns, index=X_test.index)\n        \n        return X_train_scaled, X_test_scaled, y_train, y_test\n    \n    def get_feature_names(self):\n        \"\"\"Return list of feature names used in model.\"\"\"
        return self.feature_names
