# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20170115013635) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "followings", force: :cascade do |t|
    t.integer  "follower_id"
    t.integer  "followed_id"
    t.datetime "created_at",  null: false
    t.datetime "updated_at",  null: false
  end

  add_index "followings", ["followed_id"], name: "index_followings_on_followed_id", using: :btree
  add_index "followings", ["follower_id"], name: "index_followings_on_follower_id", using: :btree

  create_table "likes", force: :cascade do |t|
    t.integer  "post_id"
    t.integer  "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_index "likes", ["post_id"], name: "index_likes_on_post_id", using: :btree

  create_table "notifications", force: :cascade do |t|
    t.integer "from"
    t.integer "to"
    t.integer "notification_type"
  end

  add_index "notifications", ["from", "to", "notification_type"], name: "index_notifications_on_from_and_to_and_notification_type", using: :btree

  create_table "posts", force: :cascade do |t|
    t.integer  "like_count", default: 0
    t.integer  "user_id"
    t.datetime "created_at",             null: false
    t.datetime "updated_at",             null: false
  end

  add_index "posts", ["like_count"], name: "index_posts_on_like_count", using: :btree
  add_index "posts", ["user_id"], name: "index_posts_on_user_id", using: :btree

  create_table "sessions", force: :cascade do |t|
    t.integer  "user_id"
    t.string   "code"
    t.boolean  "is_active"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_index "sessions", ["user_id"], name: "index_sessions_on_user_id", using: :btree

  create_table "song_posts", force: :cascade do |t|
    t.integer  "post_id"
    t.integer  "song_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_index "song_posts", ["post_id"], name: "index_song_posts_on_post_id", using: :btree
  add_index "song_posts", ["song_id"], name: "index_song_posts_on_song_id", using: :btree

  create_table "songs", force: :cascade do |t|
    t.string   "spotify_url"
    t.string   "artist"
    t.string   "track"
    t.integer  "hipster_score"
    t.datetime "created_at",    null: false
    t.datetime "updated_at",    null: false
  end

  create_table "spotify_creds", force: :cascade do |t|
    t.string   "access_token"
    t.string   "refresh_token"
    t.string   "expires_at"
    t.datetime "created_at",    null: false
    t.datetime "updated_at",    null: false
    t.integer  "user_id"
    t.string   "spotify_id"
    t.string   "playlist_id"
  end

  add_index "spotify_creds", ["user_id"], name: "index_spotify_creds_on_user_id", using: :btree

  create_table "users", force: :cascade do |t|
    t.string   "name"
    t.integer  "hipster_score",                     default: 0
    t.string   "caption"
    t.integer  "followers_count",                   default: 0
    t.integer  "location_id"
    t.integer  "like_count",                        default: 0
    t.string   "fbid"
    t.string   "username"
    t.string   "email"
    t.integer  "followings_count",                  default: 0
    t.datetime "created_at",                                        null: false
    t.datetime "updated_at",                                        null: false
    t.string   "push_id"
    t.boolean  "remote_push_notifications_enabled", default: false
  end

  add_index "users", ["fbid"], name: "index_users_on_fbid", using: :btree

end
