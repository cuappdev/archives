CREATE TABLE "likes" (
  "user_id" BIGINT REFERENCES "users" ("id"),
  "episode_id" BIGINT REFERENCES "episodes" ("id"),
  PRIMARY KEY ("user_id", "episode_id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

