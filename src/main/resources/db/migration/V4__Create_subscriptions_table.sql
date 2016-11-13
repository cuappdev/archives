CREATE TABLE "subscriptions" (
  "id" BIGSERIAL PRIMARY KEY,
  "user_id" BIGINT REFERENCES "users" ("id"),
  "series_id" BIGINT REFERENCES "series" ("id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);
