pub mod db;
pub mod app;
pub mod error;
pub mod response;

use std::sync::Arc;
pub use db::DatabaseConfig;

use axum::Router;
use crate::AppState;

use crate::todo::{ routing as todo_routing };

pub fn create_routing(shared_state: Arc<AppState>) ->  Router<Arc<AppState>> {
	Router::new()
		.nest("/api/v1/todo", todo_routing::create_router(shared_state.clone()))
}
