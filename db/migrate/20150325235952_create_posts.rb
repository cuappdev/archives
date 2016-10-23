class CreatePosts < ActiveRecord::Migration
  def change
    create_table :posts do |t|
      t.string :username
      t.integer :like_count, default: 0
      t.integer :user_id

      t.timestamps null: false
    end
    add_index :posts, :like_count
  end
end
