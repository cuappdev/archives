class AddLikeCountToPosts < ActiveRecord::Migration
  def change
    add_column :posts, :like_count, :integer, default: 0
    add_index :posts, :like_count
  end
end
