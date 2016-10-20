CREATE TABLE "users" (
  "id" BIGSERIAL PRIMARY KEY,
  "fb_id" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

/* Trigger to ensure update_at is refreshed on updating tuple */
CREATE TRIGGER users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at_column();