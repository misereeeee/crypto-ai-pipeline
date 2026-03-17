import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("1. Loading the Machine Learning dataset...")
# Load the data prepared by transform_data.py
df = pd.read_csv('btc_ml_data.csv', index_col='Timestamp')

# Define "Features" (X)
X = df[['close', 'SMA_3', 'Return']]

# Define our "Target" (y) - The answer key (1 = UP, 0 = DOWN)
y = df['Target']

print("2. Splitting data into Past (Training) and Future (Testing)...")
# CRITICAL ENGINEERING DETAIL: 
# We set shuffle=False. Why? Because this is TIME SERIES data. 
# We cannot let the AI look at data from 2:05 PM to predict the price at 2:01 PM!
# It must learn from the past (first 80% of data) and test on the future (last 20%).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print("3. Training the Random Forest AI...")
# Create the AI model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the AI on the training data (past data) so it can learn patterns and relationships
model.fit(X_train, y_train)

print("4. Testing the AI on unseen future data...")
# Ask the AI to predict the answers for the test data
predictions = model.predict(X_test)

# Grade the AI's test by comparing its predictions to the real answers (y_test)
accuracy = accuracy_score(y_test, predictions)

# Print the final score!
print(f"\n========================================")
print(f"AI Prediction Accuracy: {accuracy * 100:.2f}%")
print(f"========================================")