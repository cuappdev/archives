class CreateSongPosts < ActiveRecord::Migration
  def change
    create_table :song_posts do |t|
      t.integer :post_id
      t.integer :song_id

      t.timestamps null: false
    end
  end
end
