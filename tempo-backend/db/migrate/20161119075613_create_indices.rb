class CreateIndices < ActiveRecord::Migration
  def change
    add_index :posts, :user_id if !index_exists?(:posts, :user_id)
    add_index :followings, :follower_id if !index_exists?(:followings, :follower_id)  
    add_index :users, :username if !index_exists?(:users, :username)
    add_index :users, :fbid  if !index_exists?(:users, :fbid) 
  end
end
