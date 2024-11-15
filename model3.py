# -*- coding: utf-8 -*-
"""Model3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mFVfw-Uw6fyGIpccpdpRjpaTovfXef4f
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

df = pd.read_csv("Model3.csv")

df.head(5)
df.tail(5)
df.columns
df.dtypes
df.info()

columns_to_keep = ['CPI','Store', 'Temperature', 'Fuel_Price', 'Date', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Holiday encoded ', 'log_sales']

df = df.loc[:,columns_to_keep]
df

sns.histplot(df['log_sales'], kde=True)

"""### Machine Learning"""

# Select predictors (X) and target variable (y)
X = df[[ 'CPI', 'Temperature', 'Fuel_Price', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5', 'Holiday encoded ']]

y = df['log_sales']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing pipeline for numerical and categorical features
numeric_features = ['CPI', 'Temperature', 'Fuel_Price','MarkDown1','MarkDown2', 'MarkDown3', 'MarkDown4',  'MarkDown5']
categorical_features = ['Holiday encoded ']

numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Random Forest model pipeline with reduced parameters
model_rf = Pipeline(steps=[('preprocessor', preprocessor),
 ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42))
])

# Fit the model using the training data
model_rf.fit(X_train, y_train)

# Make predictions using the testing set
y_pred_rf = model_rf.predict(X_test)

# Evaluate the model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f'Random Forest - Mean Squared Error: {mse_rf}')
print(f'Random Forest - R-squared: {r2_rf}')

# Make predictions on the test set
y_pred = model_rf.predict(X_test)

# Plot actual vs. predicted sales
plt.figure(figsize=(13, 6))
plt.plot(y_test.values, label='Actual Sales', color='blue')
plt.plot(y_pred, label='Predicted Sales', color='red', linestyle='--')
plt.title('Actual vs Predicted Sales')
plt.xlabel('Observation')
plt.ylabel('Log Sales')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', lw=2)
plt.xlabel('Actual Close Price')
plt.ylabel('Predicted Close Price')
plt.title('Actual vs Predicted Close Price')
plt.show()

"""## Prediction"""

next_year_data = pd.read_csv("Test_Model.csv")

predicted_log_sales_next_year = model_rf.predict(next_year_data)

# Convert log-transformed predictions back to original sales scale if needed
predicted_sales_next_year = np.exp(predicted_log_sales_next_year)

# Display or save the predictions
print("Predicted Sales for Next Year:", predicted_sales_next_year)

# Optional: Add predictions to your DataFrame for easier analysis
next_year_data['Predicted Sales'] = predicted_sales_next_year

# Load your data
next_year_data = pd.read_csv("Test_Model.csv")

# Assuming you already made predictions
predicted_log_sales_next_year = model_rf.predict(next_year_data)
predicted_sales_next_year = np.exp(predicted_log_sales_next_year)

# Add predictions to your DataFrame
next_year_data['Predicted Sales'] = predicted_sales_next_year

# Ensure the 'Date' column is in datetime format
next_year_data['Date'] = pd.to_datetime(next_year_data['Date'])

next_year_data['Date'] = pd.date_range(start='11/2/12', periods=205, freq='D')  # Monthly frequency

# Plotting the predicted sales over time
plt.figure(figsize=(12, 6))
plt.plot(next_year_data['Date'], next_year_data['Predicted Sales'], label='Predicted Sales', color='orange')
plt.xlabel('Date')
plt.ylabel('Predicted Sales')
plt.title('Predicted Sales for Next Year')
plt.xticks(rotation=45)  # Rotate date labels for better visibility
plt.legend()
plt.grid()  # Add a grid for easier reading
plt.tight_layout()  # Adjust layout to fit everything
plt.show()