CREATE TABLE "series" (
  "id" BIGSERIAL PRIMARY KEY,
  "audiosearch_id" BIGINT NOT NULL,
  "title" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "image_url" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

/* Trigger to ensure update_at is refreshed on updating tuple */
CREATE TRIGGER series_updated_at
BEFORE UPDATE ON series
FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at_column();