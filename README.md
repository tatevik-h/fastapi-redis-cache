# fastapi-redis-cache
FastAPI + Redis: Advanced caching service

## Features
- Payload generation & retrieval
- PostgreSQL persistence
- CLI tool for programmatic testing

## Requirements
- Python
- Docker & Docker Compose
- Redis

 ## API Endpoints

 ### 1. Create Payload
 **POST /payload**

 Generates a new payload (or reuses existing one if already cached).
 - Transforms input strings
 - Caches results in Redis & DB
 - Returns a uinque payload ID

**Request body:**
```json
{
  "list_1": ["first string”, “second string”, “third string”],
  "list_2": ["other string”, “another string”, “last string”]
}
```
**Response:**
```json

{
  "id": "payload_123abc"
}
```

### 2. Get Payload
 **GET /payload/{id}**

 Retrieves a previously generated payload by ID.

 **Response:**
 ```json
{
  "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
}
```


 
