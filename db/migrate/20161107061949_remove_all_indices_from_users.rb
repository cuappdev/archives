class RemoveAllIndicesFromUsers < ActiveRecord::Migration
  def change
    remove_index :users, :name if index_exists?(:users, :name)
    remove_index :users, :location_id if index_exists?(:users, :location_id)
    remove_index :users, :followers_count if index_exists?(:users, :followers_count)
    remove_index :users, :like_count if index_exists?(:users, :like_count)
    remove_index :users, :email if index_exists?(:users, :email)
    remove_index :users, :followings_count if index_exists?(:users, :followings_count)
  end
end
