CREATE TABLE "likes" (
  "user_id" BIGINT REFERENCES "users" ("id"),
  "episode_id" BIGINT REFERENCES "episodes" ("id"),
  PRIMARY KEY ("user_id", "episode_id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

/* Trigger to ensure update_at is refreshed on updating tuple */
CREATE TRIGGER likes_updated_at
BEFORE UPDATE ON likes
FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at_column();

