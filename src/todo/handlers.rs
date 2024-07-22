use std::sync::Arc;
use axum::{extract::{Path}};
use crate::AppState;
use crate::core::error::internal_error;
use crate::core::response::ApiResponse;
use crate::todo::model::{CreateTodoDTO, Todo, UpdateTodoDTO};
use uuid::{Uuid};
use axum::{Json, extract::State};

pub async fn create_todo(
	State(state): State<Arc<AppState>>,
	Json(payload): Json<CreateTodoDTO>,
) -> Json<ApiResponse<()>> {
	let description = payload.description.unwrap_or_default();

	// Generate a new UUID
	let new_uuid = Uuid::new_v4();

	let result = sqlx::query(
		"INSERT INTO todo (uuid, title, description) VALUES ($1, $2, $3)"
	)
		.bind(new_uuid)
		.bind(&payload.title)
		.bind(description)
		.execute(&state.pool)
		.await;

	let mut response = ApiResponse {
		data: None,
		errors: Vec::new(),
		messages: Vec::new(),
	};

	match result {
		Ok(_) => {
			response.messages.push("Запись успешно создана".to_string());
			Json(response)
		},
		Err(err) => {
			response.errors.push(internal_error(err).1);
			Json(response)
		}
	}
}

pub async fn get_todos(
	State(state): State<Arc<AppState>>,
) -> Json<ApiResponse<Vec<Todo>>> {
	let todos = sqlx::query_as::<_, Todo>("SELECT * FROM todo")
		.fetch_all(&state.pool)
		.await
		.map_err(|err| {
			let (status_code, error_message) = internal_error(err);
			(status_code, error_message)
		});

	let response = match todos {
		Ok(todos) => ApiResponse {
			data: Some(todos),
			errors: Vec::new(),
			messages: Vec::new(),
		},
		Err((_, error_message)) => ApiResponse {
			data: None,
			errors: vec![error_message],
			messages: Vec::new(),
		},
	};

	Json(response)
}

pub async fn get_todo(
	State(state): State<Arc<AppState>>,
	Path(uuid): Path<Uuid>,
) -> Json<ApiResponse<Todo>> {
	let todo = sqlx::query_as::<_, Todo>("SELECT * FROM todo WHERE uuid = $1")
		.bind(uuid)
		.fetch_one(&state.pool)
		.await
		.map_err(|err| {
			let (status_code, error_message) = internal_error(err);
			(status_code, error_message)
		});

	let response = match todo {
		Ok(todo) => ApiResponse {
			data: Some(todo),
			errors: Vec::new(),
			messages: Vec::new(),
		},
		Err((_, error_message)) => ApiResponse {
			data: None,
			errors: vec![error_message],
			messages: Vec::new(),
		},
	};

	Json(response)
}

pub async fn update_todo(
	State(state): State<Arc<AppState>>,
	Path(uuid): Path<Uuid>,
	Json(payload): Json<UpdateTodoDTO>,
) -> Json<ApiResponse<()>> {
	let mut response = ApiResponse {
		data: None,
		errors: Vec::new(),
		messages: Vec::new(),
	};

	let mut query = String::from("UPDATE todo SET");
	let mut bind_values = Vec::new();
	let mut bind_index = 1;

	// Append status if available
	if let Some(status) = payload.status {
		query.push_str(" status = $");
		query.push_str(&bind_index.to_string());
		bind_values.push(status);
		bind_index += 1;
	}

	// Append title if available
	if let Some(title) = payload.title {
		query.push_str(" title = $");
		query.push_str(&bind_index.to_string());
		bind_values.push(title);
		bind_index += 1;
	}

	// Append description if available
	if let Some(description) = payload.description {
		if bind_index > 2 {
			query.push_str(",");
		}
		query.push_str(" description = $");
		query.push_str(&bind_index.to_string());
		bind_values.push(description);
		bind_index += 1;
	}

	// Ensure there is at least one column to update
	if bind_values.is_empty() {
		response.errors.push("No fields to update".to_string());
		return Json(response);
	}

	// Add WHERE clause
	query.push_str(" WHERE uuid::text = $");
	query.push_str(&bind_index.to_string());
	// Directly bind the UUID value
	bind_values.push(String::from(uuid));

	// Prepare and execute query
	let mut query_builder = sqlx::query(&query);
	for value in &bind_values {
		query_builder = query_builder.bind(value);
	}

	let result = query_builder
		.execute(&state.pool)
		.await
		.map_err(|err| {
			let (status_code, error_message) = internal_error(err);
			(status_code, error_message)
		});

	match result {
		Ok(_) => {
			response.messages.push("Record successfully updated".to_string());
			Json(response)
		},
		Err((_, error_message)) => {
			response.errors.push(error_message);
			Json(response)
		}
	}
}

pub async fn delete_todo(
	Path(uuid): Path<Uuid>,
	State(state): State<Arc<AppState>>,
) -> Json<ApiResponse<()>> {
	let mut response = ApiResponse {
		data: None,
		errors: Vec::new(),
		messages: Vec::new(),
	};

	let result = sqlx::query("DELETE FROM todo WHERE uuid = $1")
		.bind(uuid)
		.execute(&state.pool)
		.await
		.map_err(|err| {
			let (status_code, error_message) = internal_error(err);
			(status_code, error_message)
		});

	match result {
		Ok(_) => {
			response.messages.push("Запись успешно удалена".to_string());
			Json(response)
		},
		Err((_, error_message)) => {
			response.errors.push(error_message);
			Json(response)
		}
	}
}
