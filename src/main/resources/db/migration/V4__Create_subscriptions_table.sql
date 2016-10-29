CREATE TABLE "subscriptions" (
  "user_id" BIGINT REFERENCES "users" ("id"),
  "series_id" BIGINT REFERENCES "series" ("id"),
  PRIMARY KEY ("user_id", "series_id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

