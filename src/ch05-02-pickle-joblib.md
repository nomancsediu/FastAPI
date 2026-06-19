# Serialization with Pickle and Joblib

## Pickle

Pickle is Python's built-in serialization module. It can serialize almost any Python object, including trained scikit-learn models, to a binary file:

```python
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

# Train the model
X, y = load_iris(return_X_y=True)
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Serialize (save to disk)
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Deserialize (load from disk)
with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

# Make predictions
predictions = loaded_model.predict(X[:3])
print(predictions)
```

## Joblib

Joblib is a library that is part of the scikit-learn ecosystem and is specifically optimized for serializing large NumPy arrays and scikit-learn models. It is generally more efficient than pickle for models that contain large numerical arrays:

```python
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Train the model
X, y = load_iris(return_X_y=True)
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Serialize
joblib.dump(model, "model.joblib")

# Deserialize
loaded_model = joblib.load("model.joblib")

# Make predictions
predictions = loaded_model.predict(X[:3])
print(predictions)
```

## Security Warning

Both pickle and joblib can execute arbitrary code during deserialization. **Never load pickle files from untrusted sources.** Only load models that you or your trusted team have created. For production systems, consider additional security measures like model signing or using safer serialization formats like ONNX or SafeTensors.
