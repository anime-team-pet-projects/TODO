use serde_derive::Serialize;

#[derive(Debug, Serialize)]
pub struct ApiResponse<T> {
	pub(crate) data: Option<T>,
	pub(crate) errors: Vec<String>,
	pub(crate) messages: Vec<String>,
}