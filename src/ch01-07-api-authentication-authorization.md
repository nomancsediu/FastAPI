# 1.7 API Authentication & Authorization

## Difference

- **Authentication**: Who you are — identity verification
- **Authorization**: What you can do — permission verification

## Common Methods

```
┌──────────────────────────────────────────────┐
│       API Authentication Methods             │
├──────────────┬───────────────────────────────┤
│ API Key      │ Simple, sent in header        │
│ JWT          │ Token-based, stateless         │
│ OAuth 2.0    │ Third-party authorization      │
│ Basic Auth   │ Username/password (Base64)    │
└──────────────┴───────────────────────────────┘
```

## Which One to Use for ML APIs?

- **Internal Service**: API Key (simple and fast)
- **User-Facing API**: JWT (secure, scalable)
- **Third-Party Access**: OAuth 2.0

```
JWT Flow:
[Client] ──username/password──> [/login]
[Client] <──────JWT Token───────── [/login]
[Client] ──Request with Bearer Token──> [/predict]
[Client] <──────Prediction Result─────── [/predict]
```
