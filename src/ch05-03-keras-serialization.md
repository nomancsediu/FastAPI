# Serialization with Keras

## Saving Keras/ TensorFlow Models

Deep learning models built with Keras (TensorFlow) have their own serialization formats:

```python
from tensorflow import keras

# Build and train model
model = keras.Sequential([
    keras.layers.Dense(128, activation="relu", input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# model.fit(X_train, y_train, epochs=5)

# Save entire model (architecture + weights + optimizer state)
model.save("my_model.keras")

# Load the model
loaded_model = keras.models.load_model("my_model.keras")

# Make predictions
predictions = loaded_model.predict(X_test[:3])
```

## SaveFormat Options

Keras offers several save formats: the native `.keras` format (recommended for new projects), the HDF5-based SavedModel format (for TensorFlow Serving compatibility), and separate weight-only saves for when you want to reconstruct the architecture in code. For FastAPI serving, the `.keras` format is typically the best choice as it preserves everything needed for inference in a single file.
