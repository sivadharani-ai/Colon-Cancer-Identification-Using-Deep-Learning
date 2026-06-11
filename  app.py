Main Backend
from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load trained model
model = pickle.load(open('model.pkl', 'rb'))
# ============================================================
# COLON CANCER DETECTION USING MACHINE LEARNING AND FLASK
# ============================================================
# Import Required Libraries
# ============================================================

from flask import Flask, request, render_template_string
import numpy as np
import pandas as pd
import pickle

# Machine Learning Libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ============================================================
# STEP 1 : LOAD DATASET
# ============================================================

# Load colon cancer dataset
# Dataset should contain medical features and target column
data = pd.read_csv("colon_cancer.csv")

# Display first few rows (for debugging)
print("Dataset Preview:")
print(data.head())

# ============================================================
# STEP 2 : DATA PREPROCESSING
# ============================================================

# Separate features and target
X = data.drop('target', axis=1)
y = data['target']

# Handle missing values if present
X = X.fillna(X.mean())

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================================
# STEP 3 : TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", X_train.shape)
print("Testing samples:", X_test.shape)

# ============================================================
# STEP 4 : MODEL TRAINING
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("Model Training Completed")

# ============================================================
# STEP 5 : MODEL EVALUATION
# ============================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))

# ============================================================
# STEP 6 : SAVE MODEL
# ============================================================

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))

print("Model Saved Successfully")

# ============================================================
# STEP 7 : CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# Load saved model
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# ============================================================
# STEP 8 : HTML UI DESIGN
# ============================================================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Colon Cancer Detection System</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(to right, #e6e9ff, #f7f4ff);
    text-align: center;
    padding: 40px;
}

.container {
    background: white;
    padding: 30px;
    border-radius: 12px;
    width: 450px;
    margin: auto;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
}

h1 {
    color: #5a3fd6;
}

input {
    width: 90%;
    padding: 12px;
    margin: 8px;
    border-radius: 6px;
    border: 1px solid #ccc;
}

button {
    padding: 12px 25px;
    background: #7b5cff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #5a3fd6;
}

.result {
    margin-top: 20px;
    font-weight: bold;
    font-size: 18px;
}
</style>

</head>

<body>

<div class="container">

<h1>Colon Cancer Detection</h1>

<form action="/predict" method="post">

<input type="text" name="feature1" placeholder="Feature 1" required>
<input type="text" name="feature2" placeholder="Feature 2" required>
<input type="text" name="feature3" placeholder="Feature 3" required>
<input type="text" name="feature4" placeholder="Feature 4" required>
<input type="text" name="feature5" placeholder="Feature 5" required>
<input type="text" name="feature6" placeholder="Feature 6" required>
<input type="text" name="feature7" placeholder="Feature 7" required>
<input type="text" name="feature8" placeholder="Feature 8" required>

<br><br>
<button type="submit">Predict Cancer</button>

</form>

<div class="result">
{{ prediction_text }}
</div>

</div>

</body>
</html>
"""

# ============================================================
# STEP 9 : HOME ROUTE
# ============================================================

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

# ============================================================
# STEP 10 : PREDICTION ROUTE
# ============================================================

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values
        features = [float(x) for x in request.form.values()]

        # Convert to numpy array
        final_features = np.array(features).reshape(1, -1)

        # Scale input
        final_features = scaler.transform(final_features)

        # Predict
        prediction = model.predict(final_features)

        # Result message
        if prediction[0] == 1:
            result = "Cancer Detected"
        else:
            result = "No Cancer Detected"

        return render_template_string(HTML_PAGE, prediction_text=result)

    except Exception as e:
        return render_template_string(HTML_PAGE,
                                     prediction_text="Error in prediction")

# ============================================================
# STEP 11 : RUN APPLICATION
# ======================

if __name__ == "__main__":
    app.run(debug=True)@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        final_features = [np.array(features)]
        prediction = model.predict(final_features)

        if prediction[0] == 1:
            result = "Cancer Detected"
        else:
            result = "No Cancer Detected"

        return render_template('index.html', prediction_text=result)

    except:
        return render_template('index.html', prediction_text="Error in prediction")

if __name__ == "__main__":
    app.run(debug=True) this is complete code