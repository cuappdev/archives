CREATE TABLE "episodes" (
  "id" BIGSERIAL PRIMARY KEY,
  "audiosearch_id" BIGINT NOT NULL,
  "title" TEXT NOT NULL,
  "description" TEXT NOT NULL,
  "audio_url" TEXT NOT NULL,
  "image_url" TEXT NOT NULL,
  "series_id" BIGINT REFERENCES "series" ("id"),
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);


