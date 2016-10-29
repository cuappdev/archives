CREATE TABLE "series" (
  "id" BIGSERIAL PRIMARY KEY,
  "audiosearch_id" BIGINT NOT NULL,
  "title" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "image_url" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);
