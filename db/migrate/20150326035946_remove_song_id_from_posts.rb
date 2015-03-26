class RemoveSongIdFromPosts < ActiveRecord::Migration
  def up
    remove_column :posts, :song_id
  end

  def down
    add_column :posts, :song_id, :integer
  end
end
