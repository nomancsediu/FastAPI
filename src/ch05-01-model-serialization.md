# Model Serialization

## What is Model Serialization?

When you train a machine learning model, it exists in memory as a Python object. To use it in an API, you need to:

1. **Serialize** it — save the Python object to a file on disk
2. **Deserialize** it — load the file back into a Python object when the API starts

```
  Training Phase                  Serving Phase
  ──────────────                  ─────────────
  ┌──────────────┐    save     ┌──────────────┐
  │ Train Model  │ ──────────► │ model.pkl    │
  │ in Jupyter   │   to disk   │ (file on     │
  │ / Script     │             │  disk)       │
  └──────────────┘             └──────┬───────┘
                                      │ load at
                                      │ API start
                                      ▼
                               ┌──────────────┐
                               │ Loaded Model │
                               │ in memory    │
                               │ (ready to    │
                               │  predict)    │
                               └──────────────┘
```

## Why This Matters

Without serialization, every time your API server restarts, you'd need to retrain the model — which could take hours. Serialization lets you:

- **Train once, serve forever** — save after training, load instantly on restart
- **Version models** — keep `iris_v1.pkl`, `iris_v2.pkl` and switch between them
- **Share models** — send a single file to another team or server
- **A/B test** — load multiple model versions and route traffic

## Common Serialization Formats

| Framework | Format | File Extension | Library |
|-----------|--------|---------------|---------|
| scikit-learn | Pickle / Joblib | `.pkl` / `.joblib` | `pickle`, `joblib` |
| TensorFlow / Keras | Keras / SavedModel | `.keras` | `keras` |
| PyTorch | TorchScript | `.pt` | `torch` |
| Any | ONNX | `.onnx` | `onnx` |
| Any (safe) | SafeTensors | `.safetensors` | `safetensors` |

In the next sections, we'll cover the most common options for ML APIs.
