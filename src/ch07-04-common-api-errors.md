# Common Errors (and How to Fix Them)

| Error | What It Means | Fix |
|-------|--------------|-----|
| **422** | You sent wrong data | Check field names, types, and required fields in Swagger UI |
| **404** | Item not found | The ID doesn't exist in the database |
| **401** | Not authenticated | Add `Authorization: Bearer <token>` or `X-API-Key: <key>` header |
| **500** | Server crashed | Look at the terminal running `uvicorn` — the error traceback is there |

## Quick Debugging Checklist

1. **422 error** → Open Swagger UI (`/docs`) and check the expected format
2. **404 error** → Verify the item ID exists
3. **401 error** → Did you log in? Is your token expired?
4. **500 error** → Check the server terminal for the full error message
