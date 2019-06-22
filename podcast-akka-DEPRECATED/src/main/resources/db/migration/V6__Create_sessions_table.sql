CREATE TABLE "sessions" (
  "id" BIGSERIAL PRIMARY KEY,
  "token" TEXT NOT NULL,
  "update_token" TEXT NOT NULL,
  "expires_at" TIMESTAMP DEFAULT NOW(),
  "user_id" BIGINT REFERENCES "users" ("id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);