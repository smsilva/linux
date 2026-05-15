# API Design

## Conventions

All APIs follow REST conventions with JSON bodies. Endpoints are versioned under `/api/v1/`.

### Base URL

```
https://api.example.com/v1
```

### Authentication

Every request must include a Bearer token in the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

### Response envelope

```json
{
  "data": { ... },
  "meta": {
    "requestId": "abc-123",
    "timestamp": "2026-01-01T00:00:00Z"
  }
}
```

Error responses:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Item with id 42 not found",
    "status": 404
  },
  "meta": {
    "requestId": "abc-123",
    "timestamp": "2026-01-01T00:00:00Z"
  }
}
```

## Endpoints

### Users

| Method | Path              | Description          |
|--------|-------------------|----------------------|
| GET    | `/users/me`       | Get current user     |
| PATCH  | `/users/me`       | Update profile       |
| DELETE | `/users/me`       | Deactivate account   |

### Items

| Method | Path              | Description          |
|--------|-------------------|----------------------|
| GET    | `/items`          | List (paginated)     |
| POST   | `/items`          | Create item          |
| GET    | `/items/:id`      | Get item by id       |
| PATCH  | `/items/:id`      | Update item          |
| DELETE | `/items/:id`      | Delete item          |

#### Pagination query params

```
GET /items?page=1&pageSize=20&sortBy=createdAt&order=desc
```

Response includes:

```json
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 143,
    "totalPages": 8
  }
}
```

## Error Codes

| Code                  | HTTP Status | Description                        |
|-----------------------|-------------|------------------------------------|
| `UNAUTHORIZED`        | 401         | Missing or invalid token           |
| `FORBIDDEN`           | 403         | Insufficient permissions           |
| `RESOURCE_NOT_FOUND`  | 404         | Entity does not exist              |
| `VALIDATION_ERROR`    | 422         | Request body failed validation     |
| `INTERNAL_ERROR`      | 500         | Unexpected server error            |