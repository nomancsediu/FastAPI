# Pickle and Joblib

Model serialization means saving a trained model to disk so you can load it later without retraining.

## Pickle

```python
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Save
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Load
with open("model.pkl", "rb") as f:
    loaded = pickle.load(f)

print(loaded.predict(X[:3]))
```

## Joblib (Better for sklearn)

```python
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "model.joblib")

loaded = joblib.load("model.joblib")
print(loaded.predict([[5.1, 3.5, 1.4, 0.2]]))
```

Joblib is faster than pickle for NumPy arrays (which sklearn models use internally).

## Security Warning

Never load pickle/joblib from untrusted sources. They can execute arbitrary code.
