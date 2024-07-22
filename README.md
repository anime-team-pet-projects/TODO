## Microservice Rust-Todo


**fix postgres with sqlx**
```
cargo add sqlx -F postgres
```

**add new migration**
```
sqlx migrate add -r <name>
```

# Todo API Documentation

## Endpoints

### POST /api/v1/todo
Create a new todo item.

- **Request Body:**
    - `title` (string, required): The title of the todo item.
    - `description` (string, optional): A description of the todo item.

- **Response:**
    - `201 Created`: The todo item was successfully created.
    - `400 Bad Request`: Missing required fields or invalid input.

### GET /api/v1/todo
Retrieve all todo items.

- **Response:**
    - `200 OK`: Returns a list of all todo items.
  ```json
  [
    {
      "uuid": "8a2cd8ed-2e36-4ec9-a4bd-8df4b7727023",
      "title": "Empty",
      "status": "in_progress",
      "description": "Description one",
      "created_at": "2024-07-22T09:52:36.453048",
      "updated_at": "2024-07-22T09:52:36.453048"
    }
  ]
  ```
### GET /api/v1/todo/:id
Retrieve a specific todo item by its UUID.

- **Response:**
  - `200 OK`: Returns the todo item.
  - `404 Not Found`: No todo item found with the given UUID.
```json
{
    "uuid": "8a2cd8ed-2e36-4ec9-a4bd-8df4b7727023",
    "title": "Empty",
    "status": "in_progress",
    "description": "Description one",
    "created_at": "2024-07-22T09:52:36.453048",
    "updated_at": "2024-07-22T09:52:36.453048"
}
```

### PATCH /api/v1/todo/:id
Update an existing todo item.

- **Request Body:**
  - `title` (string, optional): The new title of the todo item.
  - `description` (string, optional): The new description of the todo item.
  - `status` (string, optional): The new status of the todo item. Valid values are todo, in_progress, done.


- **Response:**
  - `200 OK`: The todo item was successfully updated.
  - `400 Bad Request`: Invalid input or status value.
  - `404 Not Found`: No todo item found with the given UUID.

### DELETE /api/v1/todo/:id
Delete a specific todo item by its UUID.

- **Response:**
  - `200 OK`: The todo item was successfully deleted.
  - `404 Not Found`: No todo item found with the given UUID.