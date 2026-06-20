import joblib
import numpy as np
from config import MODEL_PATH


class IrisClassifier:

    def __init__(self, model_path: str = MODEL_PATH):
        self.model = joblib.load(model_path)
        self.species = ["setosa", "versicolor", "virginica"]

    def predict(self, features: list) -> dict:
        x = np.array(features).reshape(1, -1)
        class_id = self.model.predict(x)[0]
        probabilities = self.model.predict_proba(x)[0]
        return {
            "species": self.species[class_id],
            "confidence": float(max(probabilities)),
        }

    def predict_batch(self, samples: list) -> list:
        x = np.array(samples)
        class_ids = self.model.predict(x)
        all_probs = self.model.predict_proba(x)
        results = []
        for i in range(len(class_ids)):
            results.append({
                "species": self.species[class_ids[i]],
                "confidence": float(max(all_probs[i])),
            })
        return results


classifier = IrisClassifier()
