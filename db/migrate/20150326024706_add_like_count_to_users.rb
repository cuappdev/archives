class AddLikeCountToUsers < ActiveRecord::Migration
  def change
    add_column :users, :like_count, :integer, default: 0
    add_index :users, :like_count
  end
end
