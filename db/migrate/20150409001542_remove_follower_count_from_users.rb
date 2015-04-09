class RemoveFollowerCountFromUsers < ActiveRecord::Migration
  def up
    remove_column :users, :follower_count
  end

  def down
    add_column :users, :follower_count, :integer
  end
end
