class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :name
      t.integer :hipster_score, default: 0
      t.string :caption
      t.integer :followers_count, default: 0
      t.integer :location_id
      t.integer :like_count, default: 0
      t.string :fbid
      t.string :username
      t.string :email
      t.integer :followings_count, default: 0

      t.timestamps null: false
    end
    add_index :users, :name
    add_index :users, :location_id
    add_index :users, :followers_count
    add_index :users, :like_count
    add_index :users, :email
    add_index :users, :followings_count
  end
end
