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

ActiveRecord::Schema.define(version: 20151117180034) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "followings", force: :cascade do |t|
    t.integer  "follower_id"
    t.integer  "followed_id"
    t.datetime "created_at",  null: false
    t.datetime "updated_at",  null: false
  end

  create_table "likes", force: :cascade do |t|
    t.integer  "post_id"
    t.integer  "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "mutualfriends", force: :cascade do |t|
    t.integer  "user1_id"
    t.integer  "user2_id"
    t.integer  "mutual_friends_count"
    t.datetime "created_at",           null: false
    t.datetime "updated_at",           null: false
  end

  create_table "posts", force: :cascade do |t|
    t.string   "username"
    t.datetime "created_at",             null: false
    t.datetime "updated_at",             null: false
    t.integer  "like_count", default: 0
    t.integer  "user_id"
  end

  add_index "posts", ["like_count"], name: "index_posts_on_like_count", using: :btree

  create_table "sessions", force: :cascade do |t|
    t.integer  "user_id"
    t.string   "code"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "song_posts", force: :cascade do |t|
    t.integer  "post_id"
    t.integer  "song_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "songs", force: :cascade do |t|
    t.string   "spotify_url"
    t.string   "artist"
    t.string   "track"
    t.datetime "created_at",    null: false
    t.datetime "updated_at",    null: false
    t.integer  "hipster_score"
  end

  create_table "users", force: :cascade do |t|
    t.string   "name"
    t.integer  "hipster_score"
    t.string   "caption"
    t.integer  "location_id"
    t.datetime "created_at",                   null: false
    t.datetime "updated_at",                   null: false
    t.integer  "followers_count",  default: 0
    t.integer  "like_count",       default: 0
    t.string   "fbid"
    t.string   "username"
    t.string   "email"
    t.integer  "followings_count", default: 0
  end

  add_index "users", ["email"], name: "index_users_on_email", using: :btree
  add_index "users", ["followers_count"], name: "index_users_on_followers_count", using: :btree
  add_index "users", ["like_count"], name: "index_users_on_like_count", using: :btree
  add_index "users", ["location_id"], name: "index_users_on_location_id", using: :btree
  add_index "users", ["name"], name: "index_users_on_name", using: :btree

end
