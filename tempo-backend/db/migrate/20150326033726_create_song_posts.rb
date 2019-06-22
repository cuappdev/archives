class CreateSongPosts < ActiveRecord::Migration
  def change
    create_table :song_posts do |t|
      t.integer :post_id, references: "post", index: true
      t.integer :song_id, references: "song", index: true

      t.timestamps null: false
    end
  end
end
