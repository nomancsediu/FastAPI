# Common Errors (and How to Fix Them)

| Error | What It Means | Fix |
|-------|--------------|-----|
| **422** | Wrong input data | Open Swagger UI (`/docs`) and check expected format |
| **401** | API key missing or wrong | Add `X-API-Key: <your-key>` header |
| **401** | JWT token missing or expired | Get a new token from `/login` |
| **500** | Model crashed or not loaded | Check the terminal for traceback |
| **500** | Model file not found | Verify `MODEL_PATH` in `.env` points to a valid file |

## Quick Debugging Checklist

1. **422 error** → Open Swagger UI (`/docs`) and compare with the example request
2. **401 error** → Are you sending `X-API-Key` header? Is the key correct?
3. **500 error** → Check the server terminal for the full error traceback
4. **Wrong prediction** → Log the input and output to find the issue
