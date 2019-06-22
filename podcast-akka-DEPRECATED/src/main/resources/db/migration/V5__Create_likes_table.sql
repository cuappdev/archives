CREATE TABLE "likes" (
  "id" BIGSERIAL PRIMARY KEY,
  "user_id" BIGINT REFERENCES "users" ("id"),
  "episode_id" BIGINT REFERENCES "episodes" ("id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);
