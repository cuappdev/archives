CREATE TABLE "users" (
  "id" BIGSERIAL PRIMARY KEY,
  "fb_id" TEXT NOT NULL,
  "created_at" TIMESTAMP DEFAULT NOW(),
  "updated_at" TIMESTAMP DEFAULT NOW()
);

