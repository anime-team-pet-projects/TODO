use std::sync::Arc;
use axum::http::Method;
use axum::{Extension, Router};
use axum::routing::{delete, get, patch, post};
use tower_http::cors::{Any, CorsLayer};
use crate::todo::handlers::{create_todo, get_todos, get_todo, update_todo, delete_todo};
use crate::AppState;

pub fn create_router(shared_state: Arc<AppState>) -> Router<Arc<AppState>> {
	let cors = CorsLayer::new()
		.allow_origin(Any)
		.allow_methods(vec![
			Method::GET,
			Method::POST,
			Method::PATCH,
			Method::DELETE,
		])
		.allow_headers(Any);

	Router::new()
		.route("/", post(create_todo))
		.route("/", get(get_todos))
		.route("/:id", patch(update_todo))
		.route("/:id", get(get_todo))
		.route("/:id", delete(delete_todo))
		.layer(cors)
		.layer(Extension(shared_state))
}
