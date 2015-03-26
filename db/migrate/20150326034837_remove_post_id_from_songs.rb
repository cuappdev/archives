class RemovePostIdFromSongs < ActiveRecord::Migration
  def up
    remove_column :songs, :post_id
  end

  def down
    add_column :songs, :post_id, :integer
  end
end
