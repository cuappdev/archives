class AddFollowersCountToUsers < ActiveRecord::Migration
  def change
    add_column :users, :followers_count, :integer, default: 0
    add_index :users, :followers_count
  end
end
