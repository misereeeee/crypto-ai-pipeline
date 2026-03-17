import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  

print("1. Loading the Machine Learning dataset...")
df = pd.read_csv('btc_ml_data.csv', index_col='Timestamp')

X = df[['close', 'SMA_3', 'Return']]
y = df['Target']

print("2. Splitting data into Past (Training) and Future (Testing)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print("3. Training the Random Forest AI...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("4. Testing the AI on unseen future data...")
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\n========================================")
print(f"AI Prediction Accuracy: {accuracy * 100:.2f}%")
print(f"========================================")

print("\n5. Saving the AI model...")
joblib.dump(model, 'crypto_ai_brain.joblib')
print("Model successfully saved as 'crypto_ai_brain.joblib'!")