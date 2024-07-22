use chrono::NaiveDateTime;
use serde_derive::{Deserialize, Serialize};
use sqlx::FromRow;
use uuid::Uuid;

#[derive(Serialize, Debug, FromRow)]
pub struct Todo {
  uuid: Uuid,
  title: String,
  status: String,
  description: Option<String>,
  created_at: NaiveDateTime,
  updated_at: NaiveDateTime,
}
#[derive(Deserialize, Debug)]
pub struct CreateTodoDTO {
  pub(crate) title: String,
  pub(crate) description: Option<String>,
}

#[derive(Deserialize, Debug)]
pub struct UpdateTodoDTO {
  pub(crate) title: Option<String>,
  pub(crate) description: Option<String>,
  pub(crate) status: Option<String>,
}