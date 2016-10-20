CREATE TABLE "subscriptions" (
  "user_id" BIGINT REFERENCES "users" ("id"),
  "series_id" BIGINT REFERENCES "series" ("id"),
  PRIMARY KEY ("user_id", "series_id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

/* Trigger to ensure update_at is refreshed on updating tuple */
CREATE TRIGGER subscriptions_updated_at
BEFORE UPDATE ON subscriptions
FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at_column();
